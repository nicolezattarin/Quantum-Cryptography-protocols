import numpy as np
import pandas as pd
import argparse
from parameters import parameters

parser = argparse.ArgumentParser()
parser.add_argument("--use_data", default=False, help="decoy weak pulse intensity ", type=bool)
parser.add_argument("--alice_key_basis_prob", default=0.9, help="alice key basis probability ",type=float)
parser.add_argument("--alice_check_basis_prob", default=0.1, help="alice check basis probability ",type=float)
parser.add_argument("--bob_key_basis_prob", default=0.5, help="bob key basis probability ", type=float)
parser.add_argument("--bob_check_basis_prob", default=0.5, help="bob check basis probability ", type=float)
parser.add_argument("--decoy_strong_prob", default=0.7, help="decoy strong pulse probability ", type=float)
parser.add_argument("--decoy_weak_prob", default=0.3, help="decoy weak pulse probability ", type=float)
parser.add_argument("--decoy_strong_intensity", default=0.4699, help="decoy weak pulse intensity ", type=float)
parser.add_argument("--decoy_weak_intensity", default=0.1093, help="decoy weak pulse intensity ", type=float)


def main(use_data,
        alice_key_basis_prob, alice_check_basis_prob, 
        bob_key_basis_prob, bob_check_basis_prob,
        decoy_strong_prob, decoy_weak_prob,
        decoy_strong_intensity, decoy_weak_intensity):
    
    p = parameters(alice_key_basis_prob, alice_check_basis_prob, 
                    bob_key_basis_prob, bob_check_basis_prob,
                    decoy_strong_prob, decoy_weak_prob,
                    decoy_strong_intensity, decoy_weak_intensity) 

    if use_data:
        a = pd.read_csv('QKD_keys/decoded_keys_alice.csv')
        b = pd.read_csv('QKD_keys/decoded_keys_bob.csv')
        d = pd.read_csv('QKD_keys/decoded_keys_decoy.csv')
        a,b,d = a.drop(columns=['block_size']),b.drop(columns=['block_size']),d.drop(columns=['block_size'])

        a['key'] = a['key'].apply(lambda x: np.array(list(x), dtype=int))
        a['basis'] = a['basis'].apply(lambda x: np.array(list(x), dtype=int))
        b['key'] = b['key'].apply(lambda x: np.array(list(x), dtype=int))
        b['basis'] = b['basis'].apply(lambda x: np.array(list(x), dtype=int))

        df = pd.concat([a,b,d], axis=1)
        df.columns = ['alice_state', 'alice_key', 'alice_basis', 
                    'bob_state', 'bob_key', 'bob_basis', 'decoy_state']

        df['same_basis'] = df.apply(lambda x: x['alice_basis'] == x['bob_basis'], axis=1)
        df['same_bits'] = df.apply(lambda x: x['alice_key'] == x['bob_key'], axis=1)
        df['correctness'] = df.apply(lambda x: x['same_basis'] & x['same_bits'], axis=1)
        df.to_csv('QKD_keys/full_data.csv', index=False)

    else: df = pd.read_csv('QKD_keys/full_data.csv')



if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)