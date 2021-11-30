import numpy as np
import pandas as pd

def security_parameter(H, errorH, length):
    epsilon = 2**(length/2.-1-H/2.)
    errepsilon = 2**(length/2.-2-H/2.)*errorH*np.log(2)
    return epsilon, errepsilon

def security(Hmin, Herr, length):
    """
    Using the min-entropies estimated in 
    the previous steps, study how the security parameter from 
    the leftover hashing lemma changes as a function of the block length.  

    given a \delta-universal hashing family
    if there is not quantum side information as in the case of trusted QRNGs the 
    trace distance is upper bounded by:
    1/2 \sqrt{|Z|(\delta+P_g(x)-1)}

    if there is quantum side information as in the case of SDI QRNGs the 
    trace distance is upper bounded by:
    1/2 \sqrt{|Z|P_{coll}(x|E)}
    """
    #untrusted
    import os
    if os.path.isdir('security')==False:
        os.mkdir('security')

    columns = [str(h) for h in Hmin]
    security = pd.DataFrame(columns=columns)
    errsecurity = pd.DataFrame(columns=columns)
    for h, err in zip (Hmin, Herr):
        eps = []
        err_eps = []
        for l in length:
            epsilon, errepsilon = security_parameter(h, err, l)
            print('h: {}, l: {}, epsilon: {}, errepsilon: {}'.format(h, l, epsilon, errepsilon))
            eps.append(epsilon)
            err_eps.append(errepsilon)
        security[str(h)] = eps
        errsecurity[str(h)] = err_eps
    security['length'] = length
    errsecurity['length'] = length
    security.to_csv('security/security_untrusted.csv')
    errsecurity.to_csv('security/errsecurity_untrusted.csv')

def main():
    Hmin = [8e-6, 0.580, 0.79]
    Herr = [6e-6, 0.007, 0.01]
    length = [2,4,6,8,10,12,14,16]
    security(Hmin, Herr, length)

if __name__ == '__main__':
    main()