hrf_opt
=======

Optimize hemodynamic response function parameters.

A free & open source package for finding best-fitting hemodynamic
response function (HRF) parameters for fMRI data. Optimization takes
place within the framework of population receptive field (pRF)
parameters.

The fitting process requires, for every voxel of fMRI data, optimized
pRF parameters. These can be obtained using
`pyprf_feature <https://github.com/MSchnei/pyprf_feature>`__.

Installation
------------

For installation, follow these steps:

0. (Optional) Create conda environment

.. code:: bash

    conda create -n env_hrf_opt python=2.7
    source activate env_hrf_opt
    conda install pip

1. Clone repository

.. code:: bash

    git clone https://github.com/MSchnei/hrf_opt.git

2. Install hrf_opt with pip

.. code:: bash

    pip install /path/to/cloned/hrf_opt

How to use
----------

1. Run pyprf_feature to obtain an initial guess of the pRF parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `here <https://github.com/MSchnei/pyprf_feature>`__ for more
information on how to use pyprf_feature. In brief, open a terminal and
run:

::

    pyprf_feature -config path/to/custom_pRF_config.csv

2. Obtain model responses for every voxel for best-fitting pRF model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When pyprf_feature is done, run it again with -save_tc and -mdl_rsp
flag. This will save the fitted pRF model time courses and corresponding
neural responses to disk:

::

    pyprf_feature -config path/to/custom_pRF_config.csv -save_tc -mdl_rsp

3. Adjust the csv file for hrf_opt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adjust the information in the config_default.csv file in the hrf_opt
folder, such that the provided information is correct. It is recommended
to make a specific copy of the csv file for every subject.

4. Run hrf_opt
~~~~~~~~~~~~~~

Open a terminal and run:

::

    hrf_opt -config path/to/custom_hrf_opt_config.csv

References
----------

This application is based on the following work:

-  Dumoulin, S. O., & Wandell, B. A. (2008). Population receptive field
   estimates in human visual cortex. NeuroImage, 39(2), 647–660.
   https://doi.org/10.1016/j.neuroimage.2007.09.034

-  Harvey, B. M., & Dumoulin, S. O. (2011). The Relationship between
   Cortical Magnification Factor and Population Receptive Field Size in
   Human Visual Cortex: Constancies in Cortical Architecture. Journal of
   Neuroscience, 31(38), 13604–13612.
   https://doi.org/10.1523/JNEUROSCI.2572-11.2011

License
-------

The project is licensed under `GNU General Public License Version
3 <http://www.gnu.org/licenses/gpl.html>`__.
