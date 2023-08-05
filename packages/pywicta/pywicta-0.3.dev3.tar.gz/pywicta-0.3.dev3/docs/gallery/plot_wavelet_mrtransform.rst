.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_gallery_plot_wavelet_mrtransform.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_gallery_plot_wavelet_mrtransform.py:


===================
Wavelet MRTransform
===================

This example show how to clean images (remove NSB) using Wavelet transform
filtering.



.. code-block:: python


    import numpy as np

    import matplotlib
    import matplotlib.pyplot as plt

    import pywicta
    from pywicta.io import geometry_converter
    from pywicta.io.images import image_generator
    from pywicta.io.images import plot_ctapipe_image
    from pywicta.denoising import wavelets_mrtransform
    from pywicta.denoising.wavelets_mrtransform import WaveletTransform
    from pywicta.denoising import inverse_transform_sampling
    from pywicta.denoising.inverse_transform_sampling import EmpiricalDistribution

    import ctapipe
    from ctapipe.utils.datasets import get_dataset




.. code-block:: pytb

    Traceback (most recent call last):
      File "/home/jeremie/git/pub/jdhp/pywi-cta/examples/plot_wavelet_mrtransform.py", line 19, in <module>
        from pywicta.io import geometry_converter
      File "/home/jeremie/git/pub/jdhp/pywi-cta/pywicta/io/__init__.py", line 6, in <module>
        from . import geometry_converter
      File "/home/jeremie/git/pub/jdhp/pywi-cta/pywicta/io/geometry_converter.py", line 27, in <module>
        import ctapipe.image.geometry_converter as geomconv
      File "/home/jeremie/git/pub/jdhp/ctapipe/ctapipe/image/__init__.py", line 4, in <module>
        from .charge_extractors import *
      File "/home/jeremie/git/pub/jdhp/ctapipe/ctapipe/image/charge_extractors.py", line 14, in <module>
        from ctapipe.utils.neighbour_sum import get_sum_array
      File "/home/jeremie/git/pub/jdhp/ctapipe/ctapipe/utils/neighbour_sum.py", line 14, in <module>
        lib = np.ctypeslib.load_library("neighbour_sum_c", os.path.dirname(__file__))
      File "/home/jeremie/anaconda3/envs/pywi-cta-dev/lib/python3.6/site-packages/numpy/ctypeslib.py", line 129, in load_library
        from numpy.distutils.misc_util import get_shared_lib_extension
      File "/home/jeremie/anaconda3/envs/pywi-cta-dev/lib/python3.6/site-packages/numpy/distutils/__init__.py", line 8, in <module>
        from . import ccompiler
      File "/home/jeremie/anaconda3/envs/pywi-cta-dev/lib/python3.6/site-packages/numpy/distutils/ccompiler.py", line 17, in <module>
        from numpy.distutils import log
      File "/home/jeremie/anaconda3/envs/pywi-cta-dev/lib/python3.6/site-packages/numpy/distutils/log.py", line 13, in <module>
        from numpy.distutils.misc_util import (red_text, default_text, cyan_text,
      File "/home/jeremie/anaconda3/envs/pywi-cta-dev/lib/python3.6/site-packages/numpy/distutils/misc_util.py", line 16, in <module>
        from distutils.msvccompiler import get_build_architecture
      File "/home/jeremie/anaconda3/envs/pywi-cta-dev/lib/python3.6/distutils/msvccompiler.py", line 43, in <module>
        log.info("Warning: Can't read registry to find the "
      File "/home/jeremie/anaconda3/envs/pywi-cta-dev/lib/python3.6/distutils/log.py", line 44, in info
        self._log(INFO, msg, args)
      File "/home/jeremie/anaconda3/envs/pywi-cta-dev/lib/python3.6/distutils/log.py", line 30, in _log
        if stream.errors == 'strict':
    AttributeError: 'LoggingTee' object has no attribute 'errors'




Ignore warnings.



.. code-block:: python


    import warnings
    warnings.filterwarnings('ignore')


Get images from ctapipe embedded datasets.



.. code-block:: python


    SIMTEL_FILE = get_dataset('gamma_test_large.simtel.gz')


Choose the instrument to use.



.. code-block:: python


    #cam_id = None
    #cam_id = "ASTRICam"
    #cam_id = "CHEC"
    #cam_id = "DigiCam"
    #cam_id = "FlashCam"
    #cam_id = "NectarCam"
    cam_id = "LSTCam"


Configure the trace integration as in the CTA Mars analysis.



.. code-block:: python


    integrator = 'LocalPeakIntegrator'
    integration_correction = False

    if cam_id == "ASTRICam":
        integrator_window_width = 1
        integrator_window_shift = 1
    elif cam_id == "CHEC":
        integrator_window_width = 10
        integrator_window_shift = 5
    elif cam_id == "DigiCam":
        integrator_window_width = 5
        integrator_window_shift = 2
    elif cam_id == "FlashCam":
        integrator_window_width = 6
        integrator_window_shift = 3
    elif cam_id == "NectarCam":
        integrator_window_width = 5
        integrator_window_shift = 2
    elif cam_id == "LSTCam":
        integrator_window_width = 5
        integrator_window_shift = 2
    else:
        raise ValueError('Unknown cam_id "{}"'.format(cam_id))

    integrator_t0 = None
    integrator_sig_amp_cut_hg = None
    integrator_sig_amp_cut_lg = None
    integrator_lwt = None


Get the 4th image of the dataset using pywicta image generator.



.. code-block:: python


    PATHS = [SIMTEL_FILE]
    NUM_IMAGES = 5

    #rejection_criteria = lambda image: not 50 < np.nansum(image.reference_image) < 200
    rejection_criteria = None

    it = image_generator(PATHS,
                         max_num_images=NUM_IMAGES,
                         cam_filter_list=[cam_id],
                         ctapipe_format=True,
                         time_samples=False,
                         mc_rejection_criteria=rejection_criteria,
                         integrator=integrator,
                         integrator_window_width=integrator_window_width,
                         integrator_window_shift=integrator_window_shift,
                         integrator_t0=integrator_t0,
                         integrator_sig_amp_cut_hg=integrator_sig_amp_cut_hg,
                         integrator_sig_amp_cut_lg=integrator_sig_amp_cut_lg,
                         integrator_lwt=integrator_lwt,
                         integration_correction=integration_correction)

    image = next(it)  # This image is useless...
    image = next(it)  # This image is useless...
    image = next(it)  # This image is useless...
    image = next(it)


Plot the selected image with NSB.



.. code-block:: python


    geom1d = geometry_converter.get_geom1d(image.meta['cam_id'])

    title_str = "{} (run {}, event {}, tel {}, {:0.2f} {})".format(image.meta['cam_id'],
                                                                   image.meta['run_id'],
                                                                   image.meta['event_id'],
                                                                   image.meta['tel_id'],
                                                                   image.meta['mc_energy'][0],
                                                                   image.meta['mc_energy'][1])

    plot_ctapipe_image(image.input_image, geom=geom1d, plot_axis=False, title=title_str)
    plt.show()


Plot the selected image with NSB after the geometric transformation.



.. code-block:: python


    image_2d = geometry_converter.image_1d_to_2d(image.input_image, image.meta['cam_id'])

    plt.imshow(image_2d)
    plt.show()


Fill blank pixels with noise.



.. code-block:: python


    noise_cdf_file = inverse_transform_sampling.get_cdf_file_path(cam_id)  # pywicta.denoising.cdf.LSTCAM_CDF_FILE
    print(noise_cdf_file)
    noise_distribution = EmpiricalDistribution(noise_cdf_file)


Cleaning the image with Wavelets transform filtering.



.. code-block:: python


    #TMP_DIR = "/Volumes/ramdisk"
    TMP_DIR = "."

    wavelet = WaveletTransform()
    cleaned_image = wavelet.clean_image(image_2d,
                                        type_of_filtering = 'hard_filtering',
                                        filter_thresholds = [8, 2],            # <- TODO
                                        last_scale_treatment = "mask",
                                        detect_only_positive_structures = False,
                                        kill_isolated_pixels = False,
                                        noise_distribution = noise_distribution,
                                        tmp_files_directory = TMP_DIR)


Plot the cleaned image.



.. code-block:: python


    plt.imshow(cleaned_image)
    plt.show()

    cleaned_image_1d = geometry_converter.image_2d_to_1d(cleaned_image, image.meta['cam_id'])

    plot_ctapipe_image(cleaned_image_1d, geom=geom1d, plot_axis=False, title=title_str)
    plt.show()

**Total running time of the script:** ( 0 minutes  0.000 seconds)


.. _sphx_glr_download_gallery_plot_wavelet_mrtransform.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_wavelet_mrtransform.py <plot_wavelet_mrtransform.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_wavelet_mrtransform.ipynb <plot_wavelet_mrtransform.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
