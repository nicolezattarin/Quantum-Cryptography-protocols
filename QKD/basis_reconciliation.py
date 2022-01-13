import numpy as np
import pandas as pd
import argparse
from parameters import parameters

parser = argparse.ArgumentParser()
parser.add_argument("--block_length", default=int(15000), help="number of total observations in the key basis",type=float)



def main(block_length):

    a = pd.read_csv('QKD_keys/decoded_keys_alice.csv')
    b = pd.read_csv('QKD_keys/decoded_keys_bob.csv')
    d = pd.read_csv('QKD_keys/decoded_keys_decoy.csv')
    a['key'] = a['key'].apply(lambda x: np.array(list(x), dtype=int)) #true if it is the basis X (not key)
    a['basis'] = a['basis'].apply(lambda x: np.array(list(x), dtype=int))
    b['key'] = b['key'].apply(lambda x: np.array(list(x), dtype=int))
    b['basis'] = b['basis'].apply(lambda x: np.array(list(x), dtype=int))
    d = d.drop(columns=['block_size'])
    b = b.drop(columns=['block_size'])

    df = pd.concat([a,b,d], axis=1)
    df.columns = ['alice_state','total_bits', 'alice_key', 'alice_basis', 
                'bob_state', 'bob_key', 'bob_basis', 'decoy_state']
    df['total_bits'] = df.apply(lambda x: len(x['alice_key']), axis=1)
    df['same_basis'] = df.apply(lambda x: x['alice_basis'] == x['bob_basis'], axis=1)
    df['same_bits'] = df.apply(lambda x: x['alice_key'] == x['bob_key'], axis=1)
    df['correctness'] = df.apply(lambda x: x['same_basis'] & x['same_bits'], axis=1)

    df['decoy'] = df.apply(lambda x: list(x['decoy_state']) == np.full(len(x['decoy_state']), 'S'), axis=1) #true if the decoy is the  strong one
    df.to_csv('QKD_keys/basis_reconciliation.csv', index=False)

    def counting(df, block_length=int(15000), N_data=None):
        if N_data is None:
            N_data = len(df)
        df = df[:N_data]

        total_pulses = []
        m_key_mumax, m_key_mumin, m_check_mumax, m_check_mumin = [], [] ,[], []
        n_key_mumax, n_key_mumin, n_check_mumax, n_check_mumin = [], [] ,[], []

        from tqdm import tqdm
        for i in tqdm(range(len(df)), desc='computing errors and observations'):
            tot_pulses=0
            nkmin, nkmax, ncmin, ncmax = 0, 0, 0, 0
            mkmin, mkmax, mcmin, mcmax = 0, 0, 0, 0
            for j in tqdm(range(df['total_bits'][i]), desc='cheeking the {}-th key'.format(i)):
                tot_pulses+=1
                if not df['same_basis'][i][j]: continue
                if (not df['bob_key'][i][j]) and df['decoy'][i][j] and df['correctness'][i][j]: nkmax += 1 #decoy strong, basis 0 (key), correct
                elif (not df['bob_key'][i][j]) and (not df['decoy'][i][j]) and (df['correctness'][i][j]): nkmin += 1 #decoy weak, basis 0 (key), correct
                elif (df['bob_key'][i][j]) and df['decoy'][i][j] and (df['correctness'][i][j]): ncmax += 1 #decoy strong, basis 1 (check), correct
                elif (df['bob_key'][i][j]) and (not df['decoy'][i][j]) and (df['correctness'][i][j]): ncmin += 1 #decoy weak, basis 1 (check), correct
                elif (not df['bob_key'][i][j]) and df['decoy'][i][j] and (not df['correctness'][i][j]): mkmax += 1 #decoy strong, basis 0 (key), incorrect
                elif (not df['bob_key'][i][j]) and (not df['decoy'][i][j]) and (not df['correctness'][i][j]): mkmin += 1 #decoy weak, basis 0 (key), incorrect
                elif (df['bob_key'][i][j]) and df['decoy'][i][j] and (not df['correctness'][i][j]): mcmax += 1 #decoy strong, basis 1 (check), incorrect
                elif (df['bob_key'][i][j]) and (not df['decoy'][i][j]) and (not df['correctness'][i][j]): mcmin += 1 #decoy weak, basis 1 (check), incorrect

                #check the block length: fix the total observations in the Z basis (n_Z)
                if (nkmax+nkmin) >= block_length: break
                
            total_pulses.append(tot_pulses)
            m_key_mumax.append(mkmax)
            m_key_mumin.append(mkmin)
            m_check_mumax.append(mcmax)
            m_check_mumin.append(mcmin)
            n_key_mumax.append(nkmax)
            n_key_mumin.append(nkmin)
            n_check_mumax.append(ncmax)
            n_check_mumin.append(ncmin)
            
        return m_key_mumax, m_key_mumin, m_check_mumax, m_check_mumin, \
                n_key_mumax, n_key_mumin, n_check_mumax, n_check_mumin, total_pulses

    # Basis reconciliation. Alice and Bob announce their basis and 
    # intensity choices over an authenticated public channel and identify the following sets:
    # X_k := {i: ai=bi=X and ki=k} and Z_k := {i: ai=bi=Z and ki=k}

    m_key_mumax, m_key_mumin, m_check_mumax, m_check_mumin,\
    n_key_mumax, n_key_mumin, n_check_mumax, n_check_mumin, total_pulses = counting(df, block_length=block_length)

    results = pd.DataFrame({'m_key_mumax': m_key_mumax, 'm_key_mumin': m_key_mumin, \
                        'm_check_mumax': m_check_mumax, 'm_check_mumin': m_check_mumin,\
                        'n_key_mumax': n_key_mumax, 'n_key_mumin': n_key_mumin, \
                        'n_check_mumax': n_check_mumax, 'n_check_mumin': n_check_mumin, \
                        'total_pulses':total_pulses})
    import os
    if not os.path.exists('results'): os.mkdir('results')
    results.to_csv('results/countings.csv', index=False)


if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)