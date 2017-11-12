Installation Guide
==================

To execute the application, there are a minimum set of steps you should execute, basically we need to have an adequate working environment. First we will create a virtual environment, if you have not installed ``virtualenv`` do it now:


::

    pip install virtualenv

The project has been tested with both python 2.X and 3.X, no issues have been found, so use the one you prefer. To keep things standard it is advised that all your virtual environments lay in the same directory so, lets create create one and place our virtual environment in it:

::

    cd
    mkdir pyenvs
    cd pyenvs
    virtualenv vip

Now activate it by sourcing the ``activate`` script in the ``bin`` folder of your virtual enviroment.

::

    cd vip/bin
    source activate

With this we have a working environment, so lets install the dependencies of our application. The application dependencies are listed below and the installation commands using ``pip`` are provided, it is up to you if you wish to use another method:

- PyGames ``pip install pygame``
- PyLSL ``pip install pylsl``
- SciPy ``pip install scipy``
- SciKit Learn ``pip install scikit-learn``
- Sphinx ``pip install sphinx`` (Optional, if you want to build the documentation)

Finally clone the latest version of our code in a directory of your preference:

::

    cd <path-to-container-directory>
    git clone https://github.com/JorgeluissilvaC/VIPproject.git

Normally this is all you need to do. The application provides different interaction modes such as demos and two games for training and testing, this information is explained in detail in the *Tutorials* section. However, if you simply want to test the correct execution of the program, try starting the **car game**. Assuming you are in the directory you cloned from github:

::

    cd game/cars_game
    python test.py

If you want to build the documentation, for any reason you may have, you should switch to the documentation branch, as it has the latest documentation version:

::

    git checkout docs

If you face trouble saying the branch does not exist try fetching from Github via ``git fetch`` command. Then simply run the following command in the ``docs`` directory:

::

    make html