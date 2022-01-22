# Quantum-Cryptography-protocols

This repository is dedicated to provide code and results concerning the experimental implementation of Quantum Cryptography protocols. In particular, data and software are based on the course "Quantum Cryptography and security" held in the AY 2021/2022 at the University of Padova.

The repository is divided in folders, each of which regards a specific experience, here we describe the main guidelines and describe how to reuse the code. 

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
5. Security parameter from the leftover hashing lemma: given the results of the previous steps we compute how the security parameter changes as a function of the block length for fixed values of min-entropy. Run `security.py` to generate results.

See [the report](https://github.com/nicolezattarin/Quantum-Cryptography-protocols/blob/main/QRNG/report.pdf) for a complete discussion of both theoretical background and results.

***References:***

[1] M. Fiorentino, C. Santori, S. M. Spillane, R. G. Beausoleil, and W. J. Munro. Secure self-calibrating quantum random-bit generator. Phys. Rev. A, 75:032334, Mar 2007. doi: 10.1103/PhysRevA.75.032334. URL https://link.aps.org/doi/10.1103/PhysRevA.75.032334.

[2] Marco Tomamichel and Renato Renner. Uncertainty relation for smooth entropies. Physical Review Letters, 106(11), Mar 2011. ISSN 1079-7114. doi: 10.1103/physrevlett.106.110506. URL http://dx. doi.org/10.1103/PhysRevLett.106.110506.

[3] Giuseppe Vallone, Davide G. Marangon, Marco Tomasin, and Paolo Villoresi. Quantum randomness certified by the uncertainty principle. Phys. Rev. A, 90:052327, Nov 2014. doi: 10.1103/PhysRevA.90. 052327. URL https://link.aps.org/doi/10.1103/PhysRevA.90.052327.

[4] Marco Tomamichel, Christian Schaffner, Adam Smith, and Renato Renner. Leftover hashing against quantum side information. IEEE Transactions on Information Theory, 57(8):5524–5535, Aug 2011. ISSN 1557-9654. doi: 10.1109/tit.2011.2158473. URL http://dx.doi.org/10.1109/TIT.2011. 2158473.

## Quantum Key Distribution (QKD)
Quantum Key Distribution (QKD) is an approach for sharing symmetrical keys between distant users, usually referred as Alice and Bob, in an information-theoretically secure way. The implementation is based on establishing an optical link between Alice and Bob: the first prepares a state that is then sent to the receiver, who performs a measurement.

QKD folder contains code to analyse data from a laboratory session in which we discussed the implementation the 3-state 1decoy QKD protocol proposed in [3]. Indeed the well known BB84 [1] was originally meant to work with true single-photons. Nevertheless, from a practical point of view, deterministic single-photon sources are still not available. Therefore, nowadays applications employ weak coherent laser pulses.

Our analysis provides a way to compute a bound on the security key rate, security key length and quantum bit error rate (QBER), as proposed in [3].

In particular:

1. `decoding.py` is meant to read the data from a file and decode the keys encoded. Files contain key blocks of different length, each file begins with 8 bytes that code for a uint64 big-endian, which is the length N of the block (in bytes).  After these first 8 bytes, N bytes (=8N bits) of raw keys follow. After the N bytes, another block begins.

    Each QKD state is represented by two bits.
    
    Encoding of input-keys.alice: (00,H), (01,V), (10,D), (11,A) A not used in the three state protocol.
    
    Encoding of input-keys.decoy: (00,Strong Intensity), (01,Low Intensity), (10,unused), (11,unused).
    
    Encoding of input-keys.bob: (00,H), (01,V), (10,D), (11,A).
    
    This code saves the decoded keys in a .csv file with the corresponding block length.
  	Thus, such code should work with this specific kind of files, anyway it can be adapted to different situations;
  	
2. `basis_reconciliation.py`: reads files generated by `decoding.py` and generates a csv file with the occurrences of errors and observations of both the decoys in both the basis and the corresponding time necessary to build the key;
3. `security_bounds.py`: Computes QBER and SKR with the respective error propagation as it is proposed in [3] and [4]; 

Finally `parameters.py` contains all the parameters that it is necessary to fix for the apparatus.


***References***

[1] C. H. Bennett and G. Brassard. Proceedings of the IEEE International Conference on Computers, Systems and Signal Processing, Bangalore, page 175–179, 1984.

[2] B. Huttner, N. Imoto, N. Gisin, and T. Mor. Quantum cryptography with coherent states. Phys. Rev. A, 51:1863–1869, Mar 1995. doi: 10.1103/PhysRevA.51.1863. URL https://link.aps.org/ doi/10.1103/PhysRevA.51.1863.

[3] Davide Rusca, Alberto Boaron, Fadri Gru ̈nenfelder, Anthony Martin, and Hugo Zbinden. Finite- key analysis for the 1-decoy state qkd protocol. Applied Physics Letters, 112(17):171104, 2018. doi: 10.1063/1.5023340. URL https://doi.org/10.1063/1.5023340.

[4] Charles Ci Wen Lim, Marcos Curty, Nino Walenta, Feihu Xu, and Hugo Zbinden. Concise security bounds for practical decoy-state quantum key distribution. Phys. Rev. A, 89:022307, Feb 2014. doi: 10.1103/PhysRevA.89.022307. URL https://link.aps.org/doi/10.1103/PhysRevA.89.022307.

[5] Wassily Hoeffding. Probability inequalities for sums of bounded random variables. Journal of the American Statistical Association, 58(301):13–30, 1963. doi: 10.1080/01621459.1963.10500830. URL https://www.tandfonline.com/doi/abs/10.1080/01621459.1963.10500830.

[6] Costantino Agnesi, Marco Avesani, Andrea Stanco, Paolo Villoresi, and Giuseppe Vallone. All-fiber self-compensating polarization encoder for quantum key distribution. Optics Letters, 44(10):2398, May 2019. ISSN 1539-4794. doi: 10.1364/ol.44.002398. URL http://dx.doi.org/10.1364/OL.44. 002398.


