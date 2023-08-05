# Core imports
import os.path
import sys
from math import floor, ceil

# Forward compatibility
# Would be great, but importing `future` breaks the line_profiler :(
# from future.builtins import range  # a generator

# Numpy is your best friend when you have to handle numerical arrays of data
import numpy as np

# Scipy has useful sparse matrices.
# They only are 2D, so we're cheating and flattening our WCS pixels along one
# axis, and use the healpixels on the other axis, for the geometry information.
from scipy.sparse import dok_matrix, csr_matrix

# Healpy reads / writes to [HEALPix](http://healpix.sourceforge.net/) files
# Documentation for query_disc and query_polygon can be found in the source :
# https://github.com/healpy/healpy/blob/master/healpy/src/_query_disc.pyx
import healpy as hp

# Astropy offers some really nice FITS and conversion utils
# This package requires astropy version >= 1.0
from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import wcs_to_celestial_frame

# From our C extension `src/optimized.c`, which help us compute the area of
# intersection between WCS pixels and HEALPixels.
# Most of our inner loop is written there.
from optimized import intersection_area, get_weights_for_hpixs

# Our private utils
from .utils import _project_hpix_polys_to_wcs, _log, _human_file_size


# CONSTANTS ###################################################################

# Patterns of the cache filenames. Will be provided the WCS filename and nside.
PATTERN_CACHE_WEIGHTS = '%s_%d_weights.mtx'
PATTERN_CACHE_HPOLYS = '%s_%d_hpix_polys.npy'
PATTERN_CACHE_HTALLY = '%s_%d_hpix_tally.npy'


# PUBLIC FUNCTIONS ############################################################

# @profile  # this annotation is for the line_profiler, see the footer comments
def wcs2healpix(wcs_files, nside=32, write_to=None, clobber=False,
                cache_dir=None, use_cache=True, ignore_blank=True,
                show=False):
    """
    For each WCS image, project the healpixel grid in its plane, using the
    projection defined in the WCS, and for each healpixel, compute the weight
    of the contribution of each WCS pixel.
    Store the weights as geometry information in a file.
    For each healpixel, compute the weighed mean.
    Ouput the HEALPix file.

    wcs_files: str[]
        List of filepaths of input WCS FITS files to read from.
    nside: int
        Desired `nside` of the output HEALPix file.
    write_to: str
        Desired file path of the output HEALPix file.
    clobber: bool
        Should we overwrite the output file if it already exists ?
    show: bool
        Show a mollview of produced healpix.
    cache_dir: str
        The directory path where the cache files may reside and be created.
    use_cache: bool
        Whether or not to use cache files. (True by default)
        Deprecated. Use `cache_dir=` instead.
    """

    def _use_cache():
        return cache_dir is not None and use_cache

    # Debug
    _log("Using Python %s" % sys.version)

    # Make sure we can write to the output -file, and ensure it ends with fits
    if not write_to.endswith(".fits"):
        write_to += ".fits"
    if os.path.isfile(write_to) and not clobber:
        _log("The output file already exists! Set clobber=True to overwrite.")
        return None

    # Make sure the provided nside is OK
    if not hp.isnsideok(nside):
        _log("Provided nside (%d) is invalid. Provide a power of 2." % nside)
        return None

    # Prepare HEALPix data
    hpix_cnt = npix = hp.nside2npix(nside)
    _log("Number of pixels in the output HEALPix file : %d" % npix)
    hpix_ids = range(npix)
    hpixs_values = np.ndarray((npix, 1))  # Collected from all WCS files,
    hpixs_weights = np.ndarray((npix, 1))  # to make the weighed mean.

    # Be gentle with the user
    if not _use_cache():
        _log("No file cache will be used. Enable cache file saving "
             "and loading with the `cache_dir=` parameter.")

    ## LOOP ON WCS FILES ######################################################

    # Let's handle the input WCS files one at a time, filling the values and
    # their weights, so that we can make a weighed mean of all WCS files.
    for wcs_filepath in wcs_files:

        wcs_basename = os.path.basename(wcs_filepath)
        wcs_filename = wcs_basename.rsplit('.', 1)[0]  # remove extension

        _log("Handling WCS file '%s':" % wcs_filepath)

        # Read the settings from the WCS FITS file
        wcs_header = fits.getheader(wcs_filepath)
        # print wcs_header
        wcs = WCS(header=wcs_header, naxis=2)
        wcs.printwcs()

        # Extract the dimensions of the WCS image from the header
        x_dim = int(wcs_header['NAXIS1'])  # todo: is it always X/Y order ?
        y_dim = int(wcs_header['NAXIS2'])
        wpix_cnt = x_dim * y_dim
        _log("  (x * y) : %d * %d = %d WCS pixels" % (x_dim, y_dim, wpix_cnt))

        # Guess the coordinates frame from the WCS header cards.
        # We highly rely on astropy, so this may choke on illegal headers.
        frame = wcs_to_celestial_frame(wcs)
        _log("  Coordinates frame : '%s'." % frame)

        # CAR (plate carree) projections are special cases :
        # their pixel indices can be negative, from -dim/2 to +dim/2
        # We need to adjust our WCS pixels coordinates accordingly
        is_origin_center = True if 'CAR' in wcs_header['CTYPE1'] else False

        # We ignore BLANK values only if they are defined in the header
        blank = wcs_header['BLANK']  # or -32768
        if blank is None:
            ignore_blank = False
        if ignore_blank:
            _log("  Ignoring BLANK HEALPixels of value %.0f." % blank)

        # Grab the WCS data from the file
        wcs_data = fits.getdata(wcs_filepath)
        # Sometimes the shape of the data is (Z, Y, X), we only want (0, Y, X)
        if len(np.shape(wcs_data)) == 3:
            _log("  WCS data has shape %s." % str(np.shape(wcs_data)))
            _log("  We'll only use the first slice.")
            wcs_data = wcs_data[0]
            _log("  WCS data used has shape %s." % str(np.shape(wcs_data)))

        ## HEALPIX POLYGONS ###################################################

        # Pre-compute the HEALPix polygons,
        # the cartesian vertices of all healpixs on the WCS projection plane.
        # It is a list of lists of 4 to 8 (x, y) tuples, in pixel space.
        # When there are 8, it's because we have a horizontally seamless WCS
        # projection such as CAR and a WCS image as big as the sky, and some
        # healpixels must be projected both on the left and the right.
        # It is therefore a ndarray of shape (wpix_cnt, 8, 2).
        # We load it up from file cache if there is a file-cached version.

        hpix_polys = hpix_tally = None
        if _use_cache():
            hpix_polys_path = os.path.join(
                cache_dir, PATTERN_CACHE_HPOLYS % (wcs_filename, nside)
            )
            hpix_tally_path = os.path.join(
                cache_dir, PATTERN_CACHE_HTALLY % (wcs_filename, nside)
            )
            if os.path.isfile(hpix_polys_path):
                _log("  Loading %d HEALPix polygons from cache file '%s'..."
                     % (npix, hpix_polys_path))
                try:
                    hpix_polys = np.load(hpix_polys_path)
                    hpix_tally = np.load(hpix_tally_path)
                except Exception as e:
                    _log("  FAILURE: %s" % e)
                    hpix_polys = None
            else:
                _log("  No cache found for HEALPix polygons at '%s', "
                     "will compute them." % hpix_polys_path)
        if hpix_polys is None:
            _log("  Computing %d HEALPix polygons..." % npix)
            hpix_polys, hpix_tally = _project_hpix_polys_to_wcs(
                nside, wcs, is_origin_center=is_origin_center,
                x_dim=x_dim, y_dim=y_dim
            )
            if cache_dir is not None:
                hpix_polys_path = os.path.join(
                    cache_dir, PATTERN_CACHE_HPOLYS % (wcs_filename, nside)
                )
                hpix_tally_path = os.path.join(
                    cache_dir, PATTERN_CACHE_HTALLY % (wcs_filename, nside)
                )
                np.save(hpix_polys_path, hpix_polys)
                np.save(hpix_tally_path, hpix_tally)
                _log("  Wrote %s of HEALPix polygons to file '%s'."
                     % (_human_file_size(hpix_polys_path), hpix_polys_path))
                _log("  Wrote %s of tally of HEALPix polygons to file '%s'."
                     % (_human_file_size(hpix_tally_path), hpix_tally_path))

            # from utils import dbg_plot_poly
            # x_off = 0
            # y_off = 0
            # if is_origin_center:
            #     x_off = x_dim / 2.
            #     y_off = y_dim / 2.
            # img = [[-x_off, -y_off],[-x_off, -y_off+y_dim],[-x_off+x_dim, -y_off+y_dim],[-x_off+x_dim, -y_off]]
            # tmp = [593920, 595968, 598016]
            # dbg_plot_poly(np.concatenate((hpix_polys[:, 0:4, :], hpix_polys[:, 4:8, :]), axis=0), [img])
            # dbg_plot_poly(hpix_polys[tmp, 0:4, :], [img])
            # dbg_plot_poly(hpix_polys[tmp, 4:8, :], [img])
            # dbg_plot_poly(hpix_polys[hpix_tally > 1][:1000], [img])

        ## WEIGHTS ############################################################

        # Weights (aka geometry info) for this WCS file.
        # file_weights is one of scipy's sparse matrices.
        # It holds the area of intersection (used as weight in our mean)
        # between healpixels and wcspixels.
        # Its shape is (npix, y_dim * x_dim).
        # The healpixels indices are on the first axis.
        # The WCS image was flattened along the second axis as scipy's
        # sparse matrices are only 2D.
        file_weights = None

        # Load them up from cache if there is a cached version.
        if _use_cache():
            weights_filepath = os.path.join(
                cache_dir, PATTERN_CACHE_WEIGHTS % (wcs_filename, nside)
            )
            if os.path.isfile(weights_filepath):
                _log("  Loading weights from cache file '%s'..."
                     % weights_filepath)
                try:
                    from scipy.io import mmread
                    file_weights = mmread(weights_filepath)
                except Exception as e:
                    _log("  FAILURE to load the weights cache: %s" % e)
                    _log("  Will compute the weights.")
            else:
                _log("  No cache found for weights at '%s', "
                     "will compute them." % weights_filepath)

        # No ? Compute them, then !
        if file_weights is None:

            # For each healpixel
            _log("  Computing weights of %d HEALPixels..." % npix)

            # Useful profiler of C extensions for Python.
            # import yep
            # yep.start('get_weights_for_hpixs_37.prof')  # .stop() is below

            # Returns three same-sized lists, to fill a 2D array.
            # ws: (values) weights
            # hs: (1st key) healpixel identifier
            # ks: (2nd key) wcspixel  identifier (y*x_dim+x)
            ws, hs, ks = get_weights_for_hpixs(  # see optimized.c
                hpix_polys=hpix_polys,
                hpix_tally=hpix_tally,
                hpix_cnt=hpix_cnt,  # aka. npix
                wcs_x_dim=x_dim,
                wcs_y_dim=y_dim,
                wcs_data=wcs_data,
                ignored_value=blank if blank else 0,
                should_ignore=1 if ignore_blank else 0,
                is_origin_center=1 if is_origin_center else 0,
            )

            # yep.stop()

            _log("  Computed %d weights." % len(ws))

            # The shape is too big for dense matrices
            # http://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.sparse.csr_matrix.html
            file_weights = csr_matrix(
                (ws, (hs, ks)), shape=(npix, y_dim * x_dim)
            )

            # Store the geometry information to file
            # Note that we don't use numpy.save here, as it cannot save/load
            # properly sparse matrices from scipy.
            if cache_dir is not None:
                weights_filepath = os.path.join(
                    cache_dir, PATTERN_CACHE_WEIGHTS % (wcs_filename, nside)
                )
                _log("  Writing weights to file '%s'..." % weights_filepath)
                from scipy.io import mmwrite
                mmwrite(weights_filepath, file_weights)
                _log("  Weights written to file (%s)."
                     % _human_file_size(weights_filepath))

        ## LOCAL WEIGHTED MEAN CONTRIBUTION ###################################

        # Debug plot snippet
        # import matplotlib.pyplot as plt
        # plt.imshow(wcs_data)

        _log("  Computing the weighted mean...")
        # We have a (# of healpixels, # of wcs pixels) sparse matrix, as
        # sparse matrices are only supported in 2D.
        # Therefore we need to reshape the WCS image data as a vector to fit as
        # a row.
        spm_wcs_data = csr_matrix(np.reshape(wcs_data, (1, x_dim * y_dim)))
        hpixs_weights += file_weights.sum(axis=1)
        # Sparse matrices multiply method is element-wise.
        hpixs_values += file_weights.multiply(spm_wcs_data).sum(axis=1)

        # Note that hpixs_weights and hpixs_values become scipy matrices, and
        # not simple unadulterated numpy ndarrays as their were defined.
        # Their shape is still (npix, 1), as are the results of sum(axis=1).

        _log("  Freeing some memory...")
        del wcs_data
        del hpix_polys
        del file_weights

    ## FINAL WEIGHTED MEAN ####################################################

    _log("Computing the final weighted mean...")
    hpixs = hpixs_values / hpixs_weights
    # Our sparse matrices send back a (dense) matrix shaped like this :
    # [ [1.], [2.], [3.], ... ]  (npix, 1)
    # We make it a simple [ 1., 2., 3., ... ] (npix)
    # There probably is a much better way to do that.
    hpixs = np.array(hpixs).transpose()[0]

    # And finally write to ouput file
    # May want to propagate the `coord=` parameter, as now we assume Galactic !
    if write_to is not None:
        _log("Writing HEALPix to '%s'..." % write_to)
        hp.write_map(write_to, hpixs, coord='G')
        # fixme: we also probably need to write some headers in here too
        _log("HEALPix written to file (%s)." % _human_file_size(write_to))

    # Cleanup
    del hpixs_values
    del hpixs_weights

    if show:
        # This will stop the process until the window is closed
        hp.mollview(map=hpixs)

    _log("Done.")

    return hpixs


### FOR THE PROFILER ##########################################################

# $ pip install line_profiler
# add @profile before the function you want to profile, and then run :
# $ kernprof -v -l lib/wcs2healpix.py
# Warning: if you have `future` package installed, kernprof will fail.
# if __name__ == "__main__":
#     try:
#         # wcs2healpix(
#         #     [
#         #         'tests/wcs2healpix/set1/wcs/CHIPASS_Equ.fits',
#         #         'tests/wcs2healpix/set1/wcs/CHIPASS_Gal_new.fits',
#         #     ],
#         #     nside=1024,
#         #     write_to='tests/wcs2healpix/set1/result.fits',
#         #     clobber=True
#         # )
#         wcs2healpix(
#             [
#                 'tests/wcs2healpix/set2/wcs/reich_lb21_CAR.fits',
#             ],
#             nside=256,
#             write_to='tests/wcs2healpix/set2/result_profile.fits',
#             cache_dir='tests/wcs2healpix/set2/3.4',
#             clobber=True
#         )
#     except KeyboardInterrupt:
#         pass
