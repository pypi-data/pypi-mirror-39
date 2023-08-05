.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_gallery_plot_ctapipe_dataset.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_gallery_plot_ctapipe_dataset.py:


===================
Get ctapipe dataset
===================

This example show how to get images from ctapipe embedded datasets using
pywicta image generator and how to print them with pywicta plot functions.



.. code-block:: python


    import pywicta
    from pywicta.io import geometry_converter
    from pywicta.io.images import image_generator
    from pywicta.io.images import plot_ctapipe_image

    import ctapipe
    from ctapipe.utils.datasets import get_dataset

    import matplotlib.pyplot as plt




.. code-block:: pytb

    Traceback (most recent call last):
      File "/home/jeremie/git/pub/jdhp/pywi-cta/examples/plot_ctapipe_dataset.py", line 14, in <module>
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


Print the list of available ctapipe extra resources.



.. code-block:: python


    print(ctapipe.utils.datasets.find_all_matching_datasets(''))


Get images from ctapipe embedded datasets.



.. code-block:: python


    #SIMTEL_FILE = get_dataset('gamma_test.simtel.gz')
    SIMTEL_FILE = get_dataset('gamma_test_large.simtel.gz')


Get dataset images using pywicta image generator.



.. code-block:: python


    PATHS = [SIMTEL_FILE]
    NUM_IMAGES = 3

    CAM_FILTER_LIST = None
    #CAM_FILTER_LIST = ["LSTCam"]

    it = image_generator(PATHS,
                         max_num_images=NUM_IMAGES,
                         ctapipe_format=True,
                         time_samples=False,
                         cam_filter_list=CAM_FILTER_LIST)


Plot some images in the gamma test dataset using pywicta plot functions.



.. code-block:: python


    for image in it:
        title_str = "{} (run {}, event {}, tel {}, {:0.2f} {})".format(image.meta['cam_id'],
                                                                       image.meta['run_id'],
                                                                       image.meta['event_id'],
                                                                       image.meta['tel_id'],
                                                                       image.meta['mc_energy'][0],
                                                                       image.meta['mc_energy'][1])
        geom1d = geometry_converter.get_geom1d(image.meta['cam_id'])
    
        # Plot the image with NSB
        plot_ctapipe_image(image.input_image, geom=geom1d, plot_axis=False, title=title_str)
        plt.show()
    
        # Plot the image without NSB
        plot_ctapipe_image(image.reference_image, geom=geom1d, plot_axis=False, title=title_str)
        plt.show()

**Total running time of the script:** ( 0 minutes  0.000 seconds)


.. _sphx_glr_download_gallery_plot_ctapipe_dataset.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_ctapipe_dataset.py <plot_ctapipe_dataset.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_ctapipe_dataset.ipynb <plot_ctapipe_dataset.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
