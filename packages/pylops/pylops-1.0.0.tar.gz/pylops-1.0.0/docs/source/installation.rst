.. _installation:

Installation
============

You need **Python 3.6.4 or greater**.

We advise using the `Anaconda Python distribution <https://www.anaconda.com/download>`__
to ensure that all the dependencies are installed via the ``Conda`` package manager.

Step-by-step installation for users
-----------------------------------

Clone the repository by executing the following in your terminal:

.. code-block:: bash

   >> git clone git@github.com:Statoil/pylops.git

Alternatively, you can download the zip file of the repository at the top of the main page.

The first time you clone the repository run the following command:

.. code-block:: bash

   >> make install

to install the dependencies of PyLops and the PyLops library in your own active environemnt.

If you prefer to build a new Conda enviroment just for PyLops, run the following command:

.. code-block:: bash

   >> make install_conda

Remember to always activate the conda environment every time you open a new *bash* shell by typing:

.. code-block:: bash

   >> source activate lops


Step-by-step installation for developers
----------------------------------------
The first time you clone the repository run the following command:

.. code-block:: bash

   >> make dev-install

If you prefer to build a new Conda enviroment just for PyLops, run the following command:

.. code-block:: bash

   >> make dev-install_conda

To ensure that everything has been setup correctly, run tests:

.. code-block:: bash

    >> make tests

Make sure no tests fail, this guarantees that the installation has been successfull.

Again, if using Conda environment, remember to always activate the conda environment every time you open
a new *bash* shell by typing:

.. code-block:: bash

   >> source activate lops