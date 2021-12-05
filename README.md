# Quantum-Cryptography-protocols

This repository is dedicated to provide code and results concerning the experimental implementation of Quantum Cryptography protocols. In particular, data and software are based on the course "Quantum Cryptography and security" held in the AY 2021/2022 at the University of Padova.

The repository is divided in three folders, each of which regards a specific experience, here we describe the main guidelines and describe how to reuse the code. 

## Quantum Random Number Generators (QRNG)
QRNG folder is dedicated to the analysis of data from a laboratory session in which we discussed the implementation of two types of QRNG, characterized by different degrees of trust on their elements. We will focus both on a trusted and a Semi-Device Independent QRNG.

The objective of the analysis is to compute the min-entropy and the guessing probability for each setup. Eventually we evaluate the dependency of the security parameter of the Leftover Hashing Lemma by the block length.

Both raw and cleaned data are available [here](https://drive.google.com/drive/folders/1Z872z6Zmbru9QIgAJOHpkMe-Vgy6MLc5?usp=sharing).
In particular, the drive contains raw data in .mat format concerning the measurement of:
* a mixed state on H/V and D/A basis;
* a D state on H/V and D/A basis;
* a L state on H/V, D/A and L/R basis.

Here we present the workflow to get the results and process data:
1. Preprocessing:  we keep only the events which have a coincidence between the heralded photon (channel 2) and the observed photon (either channel 3 or 4)
* Run `coincidences.py` multiple times, passing as argument the path to the .mat file. This code generates the folder `coincidences`, where we store the time differences between the detection of a photon in channel 2 and either in 3 or 4;
* Run `cleandata.py` multiple times, passing as argument the path to file in the `/coincidences` folder. This code generates the folder `cleaned_data`, where we store events that are coincident within a given window, the default value is 3ns;
2. Trusted QRNG: we use the measurements of a mixed and a pure D state on H/V basis to estimate the classical min-entropy.
Run `trusted.py`. This code generates the files in the `results` folder with the computed probabilities, min-entropy and guessing probability. All quantities are presented with their propagated error
3. Source-DI QRNG with uncertainty principle: we use the measurements of a mixed and a pure D state on D/A basis and measurements of a L state on D/A, L/R basis to estimate a bound for the classical min-entropy. Run `uncertainty.py` to generate results;
4. Source-DI QRNG with full tomography: we use the measurements L state on all the basis, to estimate a bound for the classical min-entropy. Run `uncertainty.py` to generate results and reconstruct the density matrix of the state;
5. Security parameter from the leftover hashing lemma: given the results of the previous steps we compute how the security parameter changes as a function of the block length for fixed values of min-entropy.







