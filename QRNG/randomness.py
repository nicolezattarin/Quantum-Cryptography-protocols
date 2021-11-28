import numpy as np
import pandas as pd
from scipy.io import loadmat 

class probability():
    def __init__(self, h, v, d, a, r, l):
        self.h = h
        self.v = v
        self.d = d
        self.a = a
        self.r = r
        self.l = l

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
        df = dfHV
        pH = len(df[df['channel']==3])/len(df)
        pV = len(df[df['channel']==4])/len(df)
        p = probability(pH, pV, 0, 0, 0, 0)
        return p
    elif basis.lower() == 'hvda':
        N = len(dfHV)+len(dfDA)
        pH = len(dfHV[dfHV['channel']==3])/len(dfHV)
        pV = len(dfHV[dfHV['channel']==4])/len(dfHV)
        pD = len(dfDA[dfDA['channel']==3])/len(dfDA)
        pA = len(dfDA[dfDA['channel']==4])/len(dfDA)
        p = probability(pH, pV, pD, pA, 0, 0)
        return p
    elif basis == 'all':
        N = len(dfHV)+len(dfDA)+len(dfRL)
        pH = len(dfHV[dfHV['channel']==3])/len(dfHV)
        pV = len(dfHV[dfHV['channel']==4])/len(dfHV)
        pD = len(dfDA[dfDA['channel']==3])/len(dfDA)
        pA = len(dfDA[dfDA['channel']==4])/len(dfDA)
        pR = len(dfRL[dfRL['channel']==3])/len(dfRL)
        pL = len(dfRL[dfRL['channel']==4])/len(dfRL)
        p = probability(pH, pV, pD, pA, pR, pL)   
        return p
    else: raise ValueError('basis must be hv or hvda')

def trusted_randomness (pch3, pch4):
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
    hmin = -np.log2(pguess)
    return pguess, hmin

def uncertainty_randomness (pch3, pch4):
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
    pguess=2**(-hmin)
    return pguess, hmin

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
