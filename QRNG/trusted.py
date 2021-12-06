import numpy as np
import pandas as pd
from coincidences import*
from randomness import*

def main():

    # For the trusted QRNG setup, use the first set of data to 
    # estimate the classical min-entropy for the mixed state and 
    # for the pure D state

    mixedfile='cleaned_data/mixed_state_measured_on_hv_basis_coincidences_clean.txt'
    dfile='cleaned_data/d_state_measured_on_hv_basis_coincidences_clean.txt' 
    files=[mixedfile, dfile]

    import os
    if os.path.isdir('results')==False:
        os.mkdir('results')

    for f in files:
        filename = 'results/'+f[13:-23]+'_results.txt'
        out = open(filename, 'w')
        df = pd.read_csv(f, usecols=['time','channel'],dtype={'time':np.float128,'channel':np.int64})
        p = probabilities(df)
        pch3=p.h
        sigma3 = p.sigmah
        pch4=p.v
        sigma4 = p.sigmav

        pguess, perror, hmin, herror= trusted_randomness(pch3, sigma3, pch4, sigma4)
        print(f[13:-23])
        print('pch3:', pch3, 'pch4:', pch4)
        print('pguess:', pguess, 'hmin:', hmin, '\n\n')

        out.write('pH\tsigmaH\tpV\tsigmaV\tpguess\tsigmapguess\thmin\tsigmahmin\n')
        out.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.\
                format(pch3, sigma3, pch4, sigma4, pguess, perror, hmin, herror))
        out.close()

if __name__ == "__main__":
    main()


