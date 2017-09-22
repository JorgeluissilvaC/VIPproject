.. FlightStone documentation master file, created by
   sphinx-quickstart on Tue Jul 25 20:39:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to VIP-BCI documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   Introduction <introduction>
   Installation <installation>
   Theory <theory>
   Component Description <cmp_description>
   Tutorials <tutorials>
   Statistics and Performance <stats>
   Code Explorer <explorer>

Hello, navigating this documentation is fairly straight foward, you can see the component tree in the navigation bar at the left. Each description unit serves a specific porpuse, perhaps you will find particularly interesting the *Installation* and *Tutorials* sections, as the information there is enough to give you working knowledge of the platform (installing, training, testing and extending it for your personal use cases). This is, however, surface knowledge; to delve into the advanced tutorials you will need to look into the *Component Description* section, to have a notion of the organization of the application. Further more, if you want to modify, remove or add functionality, exploring the source code is mandatory. *Theory* section and *Statistics and Performance* section is not required, but are valuable assets if you ever want to replicate some of the things we do here.

General Objective
-----------------
Our principal purpose is to build brain interfaces that can be used by general people in two applications: gaming and robotic hand control. The brain-computer interface has to establish a communication with the application without the employment muscles. To use the software knowledge about the usage of electroencephalographic (EEG) sensors, signal processing, machine learning and programming skills is required.

Limitations
-----------
This project is subject to several limitations, the first one comes from the motivation itself, and it is that the system must be non-invasive and should rely only brain signals that reach the cerebral cortex. Also, due to the limited amount of sensors for data acquisition only 8 sections of said cortex can be explored at the same time. The type of signal that can be extracted with this limitations enables us to differentiate between two states: whether the region is consideration is under stress or it is relaxed. See the *Theory* section for further information.

Objectives
----------
So, what can you expect from our work, well here are the objectives we set our minds in:

- Use the data acquired with each sensor, determine the stress state of each region of the brain in a given time (by measuring power in frequency ranges)
- Train a classifier that takes the said data and determines the action the user is thinking about (only two actions are possible)
- Build different gaming platforms to test the classifying algorithm

Specific Capabilities
---------------------
With this application you can do basically the following things:

- Train the system to recognize LEFT and RIGHT brain signals of a specific individual
- Train the system to recognize whether the user is under mental concentration or is relaxed
- Play to different games: a box moving game and a car race game with your brain (using the data acquired in the training stages)
