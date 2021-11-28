import numpy as np


def main():
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
