import numpy as np
import pandas as pd
from coincidences import*
from randomness import*

def main():
    # For the Source-Device-Independent QRNG, use the first and the second 
    # set of data to calculate the quantum conditional min-entropy using 
    # the tomographic method, for both the mixed state and the pure D state. 
    # ( since you don’t have full tomographic measurements you can assume S2=0 )
    
    # For the Source-Device-Independent QRNG, use the third set of data to calculate 
    # the quantum conditional min-entropy using the entropic uncertainty principle, 
    # for the L state, using both the Entropic Uncertainty Principle and the 
    # tomographic method.

    mixed_hv='cleaned_data/mixed_state_measured_on_hv_basis_coincidences_clean.txt'
    mixed_da='cleaned_data/mixed_state_measured_on_da_basis_coincidences_clean.txt'
    d_hv ='cleaned_data/d_state_measured_on_hv_basis_coincidences_clean.txt'
    d_da ='cleaned_data/d_state_measured_on_da_basis_coincidences_clean.txt' 
    l_da ='cleaned_data/l_state_measured_on_da_basis_coincidences_clean.txt'
    l_hv ='cleaned_data/l_state_measured_on_hv_basis_coincidences_clean.txt'
    l_lr = 'cleaned_data/l_state_measured_on_lr_basis_coincidences_clean.txt'

    mixed = [mixed_hv, mixed_da]
    d =[d_hv, d_da]
    l = [l_hv, l_da, l_lr]
    sim = [mixed, d, l]
    name = ['mixed', 'd', 'l']

    import os
    if os.path.isdir('results')==False:
        os.mkdir('results')
        
    for s, n in zip(sim, name):
        dfs=[]
        for f in s:
            print(f[13:-23])
            dfs.append(pd.read_csv(f, usecols=['time', 'channel'], \
                dtype={'time': np.float128, 'channel': np.int64}))
        if s != l:
            p=probabilities(*dfs, basis='hvda')
        else:
            p=probabilities(*dfs, basis='all')
        print('pH: ', p.h, '\tpV: ', p.v, \
            '\npA: ', p.a, '\tpD: ', p.d, \
            '\npR: ', p.r, '\tpL: ', p.l)
        rho, s, sigmas = density_matrix(p.h, p.v, p.a, p.d, p.r, p.l, 
                                        p.sigmah, p.sigmav, p.sigmaa, p.sigmad, p.sigmar, p.sigmal)
        pguess, perror, hmin, herror= tomographic_randomness(s, sigmas)
        print('pguess:', pguess, 'hmin:', hmin, '\n\n')

        filename = 'results/'+f[13:18]+'_results_tomography.txt'
        out = open(filename, 'w')

        out.write('pH\tpV\tpA\tpD\tpR\tpL\tpguess\tsigmapguess\thmin\tsigmahmin\n')
        out.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'\
            .format(p.h, p.v, p.a, p.d, p.r, p.l, pguess, perror, hmin, herror))
        out.close()

        filename = 'results/'+n+'_densitymatrix.txt'
        np.savetxt(filename, rho.reshape(4,1))
            
    
if __name__ == "__main__":
    main()

    