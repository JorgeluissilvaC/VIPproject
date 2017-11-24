[![Documentation Status](https://readthedocs.org/projects/vipproject/badge/?version=docs)](http://vipproject.readthedocs.io/en/docs/?badge=docs)

### VIP: BCI
Platform for developing a Brain Computer Interface (BCI) Application. The idea is to collect neuronal data via Starstim device, in particular the [NIC system](http://www.neuroelectrics.com/products/software/nic/).

## Motivation
Our principal purpose is to build brain interfaces that can be used by general people in two applications: gaming and robotic hand control. The brain-computer interface has to establish a communication with the application without the employment muscles. To use the software knowledge about the usage of electroencephalographic (EEG) sensors, signal processing, machine learning and programming skills is required.

## Limitations
This project is subject to several limitations, the first one comes from the motivation itself, and it is that the system must be non-invasive and should rely only brain signals that reach the cerebral cortex. Also, due to the limited amount of sensors for data acquisition only 8 sections of said cortex can be explored at the same time. The type of signal that can be extracted with this limitations enables us to differentiate between two states: whether the region is consideration is under stress or it is relaxed.

## Objectives
So, what can you expect from our work, well here are the objectives we set our minds in:

* Use the data acquired with each sensor, determine the stress state of each region of the brain in a given time (by measuring power in frequency ranges)
* Train a classifier that takes the said data and determines the action the user is thinking about (only two actions are possible)
* Build different gaming platforms to test the classifying algorithm

## Documentation
For detailed information about the usage and extensibility of the platform, head to the latest version of the documentation [**here**](http://vipproject.readthedocs.io/en/docs).
