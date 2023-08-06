

.. _sphx_glr_source_auto_examples_plot_fun_with_constraints.py:


Example on geographic plotting and constraint variation
-------------------------------------------------------

In this example we show how to plot wind fields on a map and change
the default constraint coefficients using PyDDA.

This shows how important it is to have the proper intitial state and
constraints when you derive your wind fields. In the first figure,
the sounding was used as the initial state, but for the latter
two examples we use a zero initial state which provides for more 
questionable winds at the edges of the Dual Doppler Lobes.





.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /source/auto_examples/images/sphx_glr_plot_fun_with_constraints_001.png
            :scale: 47

    *

      .. image:: /source/auto_examples/images/sphx_glr_plot_fun_with_constraints_002.png
            :scale: 47

    *

      .. image:: /source/auto_examples/images/sphx_glr_plot_fun_with_constraints_003.png
            :scale: 47


.. rst-class:: sphx-glr-script-out

 Out::

    Calculating weights for radars 0 and 1
    Calculating weights for models...
    Starting solver 
    rmsVR = 45.92438215135045
    Total points:92092.0
    | Jvel    | Jmass   | Jsmooth |   Jbg   | Jvort   | Jmodel | Max w  
    |   7.2677|   9.6635|   0.0000|   0.0000|   0.0000|   0.0000|  21.4218
    Norm of gradient: 0.0019325121319328296
    Iterations before filter: 10
    | Jvel    | Jmass   | Jsmooth |   Jbg   | Jvort   | Jmodel | Max w  
    |   3.4229|   5.6720|   0.0000|   0.0000|   0.0000|   0.0000|  19.1172
    Norm of gradient: 0.000927609111435287
    Iterations before filter: 20
    | Jvel    | Jmass   | Jsmooth |   Jbg   | Jvort   | Jmodel | Max w  
    |   3.4229|   5.6720|   0.0000|   0.0000|   0.0000|   0.0000|  19.1172
    Norm of gradient: 0.000927609111435287
    Iterations before filter: 30
    Applying low pass filter to wind field...
    Iterations after filter: 1
    Iterations after filter: 2
    Done! Time = 36.8
    Calculating weights for radars 0 and 1
    Calculating weights for models...
    Starting solver 
    rmsVR = 45.92438215135045
    Total points:92092.0
    | Jvel    | Jmass   | Jsmooth |   Jbg   | Jvort   | Jmodel | Max w  
    |  10.3019|  27.3722|   0.0000|   0.0000|   0.0000|   0.0000|  19.7168
    Norm of gradient: 0.03852252520788402
    Iterations before filter: 10
    | Jvel    | Jmass   | Jsmooth |   Jbg   | Jvort   | Jmodel | Max w  
    |   1.7766|   8.6518|   0.0000|   0.0000|   0.0000|   0.0000|  28.8783
    Norm of gradient: 0.004759001517216492
    Iterations before filter: 20
    | Jvel    | Jmass   | Jsmooth |   Jbg   | Jvort   | Jmodel | Max w  
    |   0.9924|   5.3533|   0.0000|   0.0000|   0.0000|   0.0000|  31.8040
    Norm of gradient: 0.0031699283228517473
    Iterations before filter: 30
    | Jvel    | Jmass   | Jsmooth |   Jbg   | Jvort   | Jmodel | Max w  
    |   0.4994|   4.2252|   0.0000|   0.0000|   0.0000|   0.0000|  31.7813
    Norm of gradient: 0.002385027566474536
    Iterations before filter: 40
    | Jvel    | Jmass   | Jsmooth |   Jbg   | Jvort   | Jmodel | Max w  
    |   0.4109|   3.7416|   0.0000|   0.0000|   0.0000|   0.0000|  31.9045
    Norm of gradient: 0.0006029510309811339
    Iterations before filter: 50
    | Jvel    | Jmass   | Jsmooth |   Jbg   | Jvort   | Jmodel | Max w  
    |   0.4109|   3.7416|   0.0000|   0.0000|   0.0000|   0.0000|  31.9045
    Norm of gradient: 0.0006029510309811339
    Iterations before filter: 60
    Applying low pass filter to wind field...
    Iterations after filter: 1
    Iterations after filter: 2
    Done! Time = 81.1




|


.. code-block:: python


    import pydda
    import pyart
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt


    berr_grid = pyart.io.read_grid(pydda.tests.BERR_GRID)
    cpol_grid = pyart.io.read_grid(pydda.tests.CPOL_GRID)

    # Load our radar data
    sounding = pyart.io.read_arm_sonde(
        pydda.tests.SOUNDING_PATH)
    u_init, v_init, w_init = pydda.initialization.make_constant_wind_field(
        berr_grid, (0.0, 0.0, 0.0))

    # Let's make a plot on a map
    fig = plt.figure(figsize=(7, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())

    pydda.vis.plot_horiz_xsection_streamlines_map(
        [berr_grid, cpol_grid], ax=ax, bg_grid_no=-1, level=7, w_vel_contours=[3, 5, 8])
    plt.show()

    # Let's see what happens when we use a zero initialization
    new_grids = pydda.retrieval.get_dd_wind_field([berr_grid, cpol_grid],
                                        u_init, v_init, w_init,
                                        Co=1.0, Cm=1500.0, frz=5000.0)

    fig = plt.figure(figsize=(7, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())

    pydda.vis.plot_horiz_xsection_streamlines_map(
        new_grids, ax=ax, bg_grid_no=-1, level=7, w_vel_contours=[3, 5, 8])
    plt.show()

    # Or, let's make the radar data more important!
    new_grids = pydda.retrieval.get_dd_wind_field([berr_grid, cpol_grid],
                                        u_init, v_init, w_init,
                                        Co=10.0, Cm=1500.0, frz=5000.0)
    fig = plt.figure(figsize=(7, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())

    pydda.vis.plot_horiz_xsection_streamlines_map(
        new_grids, ax=ax, bg_grid_no=-1, level=7, w_vel_contours=[3, 5, 8])
    plt.show()

**Total running time of the script:** ( 2 minutes  2.791 seconds)



.. only :: html

 .. container:: sphx-glr-footer


  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_fun_with_constraints.py <plot_fun_with_constraints.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_fun_with_constraints.ipynb <plot_fun_with_constraints.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
