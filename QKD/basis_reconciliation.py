import numpy as np
import pandas as pd
import argparse
from parameters import parameters

parser = argparse.ArgumentParser()
parser.add_argument("--block_length", default=int(1e9), help="number of total observations in the key basis",type=float)
parser.add_argument("--fracdata", default=1, help="fraction of data to analyze",type=float)


def main(block_length,fracdata):

    a = pd.read_csv('QKD_keys/decoded_keys_alice.csv')
    b = pd.read_csv('QKD_keys/decoded_keys_bob.csv')
    d = pd.read_csv('QKD_keys/decoded_keys_decoy.csv')
    ndata=int(len(a)*fracdata)
    a = a[:ndata]
    b = b[:ndata]
    d = d[:ndata]

    print('processing data...')
    a['key'] = a['key'].apply(lambda x: np.array(list(x), dtype=int)) #true if it is the basis X (not key)
    a['basis'] = a['basis'].apply(lambda x: np.array(list(x), dtype=int))
    b['key'] = b['key'].apply(lambda x: np.array(list(x), dtype=int))
    b['basis'] = b['basis'].apply(lambda x: np.array(list(x), dtype=int))
    d = d.drop(columns=['block_size'])
    b = b.drop(columns=['block_size'])

    df = pd.concat([a,b,d], axis=1)
    df.columns = ['alice_state','total_bits', 'alice_key', 'alice_basis', 
                'bob_state', 'bob_key', 'bob_basis', 'decoy_state']

    print('checking basis and correctness...')
    df['total_bits'] = df.apply(lambda x: len(x['alice_key']), axis=1)
    df['same_basis'] = df.apply(lambda x: x['alice_basis'] == x['bob_basis'], axis=1)
    df['same_bits'] = df.apply(lambda x: x['alice_key'] == x['bob_key'], axis=1)
    df['correctness'] = df.apply(lambda x: x['same_basis'] & x['same_bits'], axis=1)
    #true if the decoy is the strong one
    df['decoy'] = df.apply(lambda x: list(x['decoy_state']) == np.full(len(x['decoy_state']), 'S'), axis=1) 
    df['time'] = np.arange(len(df))
    df.to_csv('QKD_keys/basis_reconciliation.csv', index=False)

    #------------------------------------------------------------------------------------------------

    def counting(df, block_length, N_data=None):
        if N_data is None:
            N_data = len(df)
        raw_keys = pd.DataFrame({'time': [], 'total_pulses': [], 'm_key_mumax': [], 'm_key_mumin': [], 
                                'n_key_mumax': [], 'n_key_mumin': [], 'm_check_mumax': [], 
                                'm_check_mumin': [], 'n_check_mumax': [], 'n_check_mumin': []})
                                
        from tqdm import tqdm
        # for i in tqdm(range(len(df)), desc='computing errors and observations'):

        i = 0
        jbit = 0
        pbar = tqdm(total=100, desc='computing errors and observations for each key')
        while i < len(df):
            old_i = i
            tot_pulses = 0
            nkmin, nkmax, ncmin, ncmax = 0, 0, 0, 0
            mkmin, mkmax, mcmin, mcmax = 0, 0, 0, 0
            key_time = 0
            while nkmax+ncmax<block_length:
                key_time+=1 #everytime we read a new line a second has passed 
                for j in range(jbit, df['total_bits'][i]):
                    tot_pulses+=1
                    if not df['same_basis'][i][j]: continue
                    if (not df['bob_key'][i][j]) and df['decoy'][i][j] and df['correctness'][i][j]:
                        nkmax += 1 #decoy strong, basis 0 (key), correct
                    elif (not df['bob_key'][i][j]) and (not df['decoy'][i][j]) and (df['correctness'][i][j]): 
                        nkmin += 1 #decoy weak, basis 0 (key), correct
                    elif (df['bob_key'][i][j]) and df['decoy'][i][j] and (df['correctness'][i][j]): 
                        ncmax += 1 #decoy strong, basis 1 (check), correct
                    elif (df['bob_key'][i][j]) and (not df['decoy'][i][j]) and (df['correctness'][i][j]): 
                        ncmin += 1 #decoy weak, basis 1 (check), correct
                    elif (not df['bob_key'][i][j]) and df['decoy'][i][j] and (not df['correctness'][i][j]): 
                        mkmax += 1 #decoy strong, basis 0 (key), incorrect
                    elif (not df['bob_key'][i][j]) and (not df['decoy'][i][j]) and (not df['correctness'][i][j]): 
                        mkmin += 1 #decoy weak, basis 0 (key), incorrect
                    elif (df['bob_key'][i][j]) and df['decoy'][i][j] and (not df['correctness'][i][j]): 
                        mcmax += 1 #decoy strong, basis 1 (check), incorrect
                    elif (df['bob_key'][i][j]) and (not df['decoy'][i][j]) and (not df['correctness'][i][j]): 
                        mcmin += 1 #decoy weak, basis 1 (check), incorrect
                    if nkmax+ncmax >= block_length: 
                        # if the block is full in the middle of the reading 
                        # of a key we have to restart from that point  
                        jbit = j
                        break
                if nkmax+ncmax >= block_length: break
                i+=1
                jbit=0
            pbar.update((i-old_i)*100/len(df))
            raw_keys = raw_keys.append({'time': key_time, 'total_pulses': tot_pulses, 
                                        'm_key_mumax': mkmax, 'm_key_mumin': mkmin,
                                        'n_key_mumax': nkmax, 'n_key_mumin': nkmin, 
                                        'm_check_mumax': mcmax, 'm_check_mumin': mcmin,
                                        'n_check_mumax': ncmax, 'n_check_mumin': ncmin}, ignore_index=True)
        pbar.close()
        return raw_keys

    # Basis reconciliation. Alice and Bob announce their basis and 
    # intensity choices over an authenticated public channel and identify the following sets:
    # X_k := {i: ai=bi=X and ki=k} and Z_k := {i: ai=bi=Z and ki=k}
    results = counting(df, block_length=block_length)

    import os
    if not os.path.exists('results'): os.mkdir('results')
    results.to_csv('results/countings_{}.csv'.format(block_length), index=False)

if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)