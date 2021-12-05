# Quantum-Cryptography-protocols

This repository is dedicated to provide code and results concerning the experimental implementation of Quantum Cryptography protocols. In particular, data and software are based on the course "Quantum Cryptography and security" held in the AY 2021/2022 at the University of Padova.

The repository is divided in three folders, each of which regards a specific experience, here we describe the main guidelines and describe how to reuse the code. 

## Quantum Random Number Generators (QRNG)
QRNG folder is dedicated to the analysis of data from a laboratory session in which we discussed the implementation of two types of QRNG, characterized by different degrees of trust on their elements. We will focus both on a trusted and a Semi-Device Independent QRNG.

The objective of the analysis is to compute the min-entropy and the guessing probability for each setup. Eventually we evaluate the dependency of the security parameter of the Leftover Hashing Lemma by the block length.

Both raw and cleaned data are available [here](https://drive.google.com/drive/folders/1Z872z6Zmbru9QIgAJOHpkMe-Vgy6MLc5?usp=sharing).
In particular, the drive contains raw data in .mat format concerning the measurement of:
	- a mixed state on H/V and D/A basis;
	- a D state on H/V and D/A basis;
	- a L state on H/V, D/A and L/R basis.

To get the results one should follow the workflow that follows
1. Preprocessing:  we keep only the events which have a coincidence between the heralded photon (channel 2) and the observed photon (either channel 3 or 4)
	- 
2. 



