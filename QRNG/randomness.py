import numpy as np
import pandas as pd
from scipy.io import loadmat 
from math import e

class probability():
    def __init__(self, h, v, d, a, r, l, sigmah, sigmav, sigmad, sigmaa, sigmar, sigmal):
        self.h = h
        self.v = v
        self.d = d
        self.a = a
        self.r = r
        self.l = l
        self.sigmah = sigmah
        self.sigmav = sigmav
        self.sigmad = sigmad
        self.sigmaa = sigmaa
        self.sigmar = sigmar
        self.sigmal = sigmal

def get_probabilities (df):
    """
    From the number of coincidence events estimate the probabilities 
    for each projector of the measurement basis. 
    This function considers only two basis

    parameters:
        df: dataframe with the number of coincidence events
    return:
        pch3, pch4: probabilities of the measurement basis
    """
    pch3 = len(df[df['channel']==3])/len(df)
    pch4 = len(df[df['channel']==4])/len(df)
    return pch3, pch4


def probabilities (dfHV, dfDA=None, dfRL=None, basis='hv' ):
    """
    From the number of coincidence events estimate the probabilities 
    for each projector of the measurement basis. 
    """
    if basis.lower() == 'hv':
        N = len(dfHV)
        df = dfHV
        nH = len(df[df['channel']==3])
        nV = len(df[df['channel']==4])
        pH = nH/N
        pV = nV/N

        sigmaH = np.sqrt(nH/(N**2)+(nH**2)/N**3)
        sigmaV = np.sqrt(nV/(N**2)+(nV**2)/N**3)
        p = probability(pH, pV, 0, 0, 0, 0, sigmaH, sigmaV, 0, 0, 0, 0)
        return p
    elif basis.lower() == 'hvda':
        Nhv = len(dfHV)
        Nda = len(dfDA)
        nH = len(dfHV[dfHV['channel']==3])
        nV = len(dfHV[dfHV['channel']==4])
        nD = len(dfDA[dfDA['channel']==3])
        nA = len(dfDA[dfDA['channel']==4])
        pH = nH/Nhv
        pV = nV/Nhv
        pD = nD/Nda
        pA = nA/Nda
        sigmaH = np.sqrt(nH/(Nhv**2)+(nH**2)/Nhv**3)
        sigmaV = np. sqrt(nV/(Nhv**2)+(nV**2)/Nhv**3)
        sigmaD = np.sqrt(nD/(Nda**2)+(nD**2)/Nda**3)
        sigmaA = np.sqrt(nA/(Nda**2)+(nA**2)/Nda**3)
        p = probability(pH, pV, pD, pA, 0, 0, sigmaH, sigmaV, sigmaD, sigmaA, 0, 0)
        return p
    elif basis == 'all':
        Nhv = len(dfHV)
        Nda = len(dfDA)
        Nlr = len(dfRL)
        nH = len(dfHV[dfHV['channel']==3])
        nV = len(dfHV[dfHV['channel']==4])
        nD = len(dfDA[dfDA['channel']==3])
        nA = len(dfDA[dfDA['channel']==4])
        nR = len(dfRL[dfRL['channel']==3])
        nL = len(dfRL[dfRL['channel']==4])
        pH = nH/Nhv
        pV = nV/Nhv
        pD = nD/Nda
        pA = nA/Nda
        pR = nR/Nlr
        pL = nL/Nlr
        sigmaH = np.sqrt(nH/(Nhv**2)+(nH**2)/Nhv**3)
        sigmaV = np. sqrt(nV/(Nhv**2)+(nV**2)/Nhv**3)
        sigmaD = np.sqrt(nD/(Nda**2)+(nD**2)/Nda**3)
        sigmaA = np.sqrt(nA/(Nda**2)+(nA**2)/Nda**3)
        sigmaR = np.sqrt(nR/(Nlr**2)+(nR**2)/Nlr**3)
        sigmaL = np.sqrt(nL/(Nlr**2)+(nL**2)/Nlr**3)
        p = probability(pH, pV, pD, pA, pR, pL, sigmaH, sigmaV, sigmaD, sigmaA, sigmaR, sigmaL)
        return p
    else: raise ValueError('basis must be hv or hvda')

def trusted_randomness (pch3, sigma_pch3, pch4, sigma_pch4):
    """
    From the probabilities of the measurement basis, estimate the guessing 
    Probability of the randomness of the measurement and the min entropy

    parameters:
        pch3, pch4: probabilities of the measurement basis
    return:
        pguess: guessing probability 
        hmin: min entropy
    """
    pguess = max(pch4, pch3)
    if pguess == pch3: perror = sigma_pch3
    else: perror = sigma_pch4

    hmin = -np.log2(pguess)
    herror = np.log2(e)*perror/pguess
    return pguess, perror, hmin, herror

def uncertainty_randomness (pch3, sigma_pch3, pch4, sigma_pch4):
    """
    From the probabilities of the measurement basis, estimates bounds for 
    the guessing probability and the min entropy applying the uncertainty priciple

    pch3 and pch4 are probability of measurements on the ausiliary basis, 
    the results of projective measurements in POVM Z. The bound obtained 
    is on the variable corresponding to the POVM X. 

    parameters:
        pch3, pch4: probabilities of the measurement basis
    return:
        pguess: guessing probability (upper bound)
        hmin: min entropy  (lower bound)
    """
    dim=2
    hmin=np.log2(dim)-2*np.log2(sum([np.sqrt(pch3), np.sqrt(pch4)]))
    herror =(np.log2(e)/(np.sqrt(pch3)+np.sqrt(pch4)))*np.sqrt(pch3**(-3)*sigma_pch3**2+pch4**(-3)*sigma_pch4**2)
    pguess=2**(-hmin)
    perror = hmin*herror*2**(-hmin-1)
    return pguess, perror, hmin, herror

def density_matrix (pH, pV, pD=0, pA=0, pR=0, pL=0):
    """
    Computes the density matrix from the probabilities of the measurement basis.
    parameters:
        pH, pV, pD, pA, pR, pL: probabilities of the measurement basis
    return:
        rho: density matrix
        S: stoke's coefficients as in D. F. V. James et al., Phys. Rev. A 64, 052312 (2001).
    """
    S0 = pH+pV
    S1 = pD-pA
    S2 = pR-pL
    S3 = pH-pV
    S = np.array([S0, S1, S2, S3])/S0
    print('stokes: ', S)
    print('check normalization: ', np.linalg.norm(S[1:]))
    sigma0 = np.identity(2)
    sigma1 = np.array([[0,1],[1,0]])
    sigma2 = np.array([[0,-1j],[1j,0]])
    sigma3 = np.array([[1,0],[0,-1]])
    sigma = [sigma0, sigma1, sigma2, sigma3]

    rho = sigma[0]*S[0]+sigma[1]*S[1]+sigma[2]*S[2]+sigma[3]*S[3]
    return rho*0.5, S

def tomographic_randomness (S):
    """
    From the probabilities of the measurement basis, estimates bounds for 
    the guessing probability and the min entropy applying Fiorentino's method 

    parameters:
        S: stoke's coefficients as in D. F. V. James et al., Phys. Rev. A 64, 052312 (2001).
    return:
        pguess: guessing probability (upper bound)
        hmin: min entropy   (lower bound)
    """
    pguess = (1+np.sqrt(1-S[1]**2-S[2]**2))/2
    hmin = -np.log2(pguess)
    return pguess, hmin
