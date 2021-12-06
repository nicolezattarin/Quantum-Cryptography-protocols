import numpy as np
import pandas as pd
from coincidences import*
from randomness import*

def main():
    # For the Source-Device-Independent QRNG, use the first and the second set of 
    # data to calculate the quantum conditional min-entropy using the entropic 
    # uncertainty principle, for both the mixed state and the pure D state.

    # For the Source-Device-Independent QRNG, use the third set 
    # of data to calculate the quantum conditional min-entropy
    # using the entropic uncertainty principle, for the L state, 
    # using both the Entropic Uncertainty Principle and the tomographic method.

    mixed_da='cleaned_data/mixed_state_measured_on_da_basis_coincidences_clean.txt'
    d_da ='cleaned_data/d_state_measured_on_da_basis_coincidences_clean.txt' 
    l_da ='cleaned_data/l_state_measured_on_da_basis_coincidences_clean.txt'
    l_hv ='cleaned_data/l_state_measured_on_hv_basis_coincidences_clean.txt'
    l_lr = 'cleaned_data/l_state_measured_on_lr_basis_coincidences_clean.txt'

    files=[mixed_da, d_da, l_da, l_hv, l_lr]

    import os
    if os.path.isdir('results')==False:
        os.mkdir('results')

    for f in files:
        print(f[13:-23])
        filename = 'results/'+f[13:-23]+'_results_uncertainty.txt'
        out = open(filename, 'w')
        df = pd.read_csv(f, usecols=['time', 'channel'], dtype={'time': np.float128, 'channel': np.int64})
        p=probabilities(df)
        pch3=p.h
        sigma3 = p.sigmah
        pch4=p.v
        sigma4 = p.sigmav
        pguess, perror, hmin, herror = uncertainty_randomness(pch3, sigma3, pch4, sigma4)

        print('pch3:', pch3, 'pch4:', pch4)
        print('pguess:', pguess, 'hmin:', hmin, '\n\n')

        out.write('pH\tsigmaH\tpV\tsigmaV\tpguess\tsigmapguess\thmin\tsigmahmin\n')
        out.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.\
                    format(pch3, sigma3, pch4, sigma4, pguess, perror, hmin, herror))
        out.close()

    
if __name__ == "__main__":
    main()

    