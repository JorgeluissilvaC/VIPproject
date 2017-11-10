Theoretical Background
======================

Overall system considerations
-----------------------------

The BCI system is focused in identifying two types of mental states that modulate the alpha rhythms present in the human brain. The alpha rhythms are brain rhythms that range in the 8-13 Hz frequency band, they are produced mainly by activities in the thalamus (Figure 1). Alpha rhythms are predominant (in regards to other rhythms, such as the beta rhythm) when the person has the eyes closed and is in a relaxed state, they are also important in network coordination and communication. Alpha rhythms (or waves) can be detected either by  electroencephalography (EEG) or magnetoencephalography (MEG); due to acquisition easiness, a commercial electroencephalography (EEG) device is used.


Given the particularity of alpha waves for detecting relaxed-to-stressed states, our system we have established this two activities as the ones the user must perform. The overall aim is, thus, design a system capable of determining in each state the user is by analysing the alpha waves of the subject, in real time. A second objective is desired: the user is asked, during the stressed state, to think in one of two actions, if possible opposite actions (like moving left, then right); the action the user want to perform will then modify the spectral disposition of the wave, allowing us to characterize the alpha waves for the two actions, and, with that information let the user control an object on-screen.

To keep matter short, the aim is:
Acquire alpha waves with a EEG system
Classify waves between relaxed and stressed states using a training software (that we will develop)
Classify stressed states between two different actions using a training software (that we will develop)
Construct a classifier with the classified data to predict future instances
Construct a game-like environment where the two previously classified actions can be tested

Alpha waves acquisition
-----------------------

Alpha waves will be acquired via Starstim EEG device with 14 acquisition probes. The users are subjected to a training interface that iterates between relaxation and stress stages in a periodic manner, in each stage the user is requested the effect the respective action. In Figure 2 you can see the overall process for data acquisition. Each stage is repeated a large number of times, so that their contribution is statistically significant to the classifier.

(Figure 2)

Each probe samples the voltage at a rate of 500Hz (good enough, given the frequency of the alpha waves). Thus we have 14 channels of voltage-time information, however, to characterize the alpha waves per channel the spectral information is more useful (this spectrum show the relation of relative amplitude against frequency value). Non desired frequency may be present so, a low-pass filter is applied. Some transforms to acquire the spectrum information are available: most popular one is the Fourier transform, and the other is the Hilbert transform (the main difference is that the Hilbert transform relays less data, as it only takes into account the envelope of the wave). Thus we have, power-vs-frequency data in a time interval (for each probe); we then generate a vector per probe where the power per frequency is averaged throughout the interval of acquisition (5 seconds), which results, as a whole, in a two dimensional data array. Adding all the repetitions together results in a tridimensional data array, as shown in Figure 3

(Figure 3)
