import numpy as np
import pandas as pd
import argparse
from parameters import parameters

parser = argparse.ArgumentParser()
parser.add_argument("--alice_key_basis_prob", default=0.9, help="alice key basis probability ",type=float)
parser.add_argument("--alice_check_basis_prob", default=0.1, help="alice check basis probability ",type=float)
parser.add_argument("--bob_key_basis_prob", default=0.5, help="bob key basis probability ", type=float)
parser.add_argument("--bob_check_basis_prob", default=0.5, help="bob check basis probability ", type=float)
parser.add_argument("--decoy_strong_prob", default=0.7, help="decoy strong pulse probability ", type=float)
parser.add_argument("--decoy_weak_prob", default=0.3, help="decoy weak pulse probability ", type=float)
parser.add_argument("--decoy_strong_intensity", default=0.4699, help="decoy weak pulse intensity ", type=float)
parser.add_argument("--decoy_weak_intensity", default=0.1093, help="decoy weak pulse intensity ", type=float)
parser.add_argument("--N_key_strong", default=1000, help="block size (in bits) for the key, strong decoy", type=int)
parser.add_argument("--N_key_weak", default=10000, help="block size (in bits) for the key, weak decoy", type=int)
parser.add_argument("--N_check_weak", default=1000, help="block size (in bits) for the check, weak decoy", type=int)
parser.add_argument("--N_check_strong", default=1000, help="block size (in bits) for the check, strong decoy", type=int)

def main(use_data,
        alice_key_basis_prob, alice_check_basis_prob, 
        bob_key_basis_prob, bob_check_basis_prob,
        decoy_strong_prob, decoy_weak_prob,
        decoy_strong_intensity, decoy_weak_intensity,
        N_key_strong, N_key_weak, N_check_strong, N_check_weak):
    
    p = parameters(alice_key_basis_prob, alice_check_basis_prob, 
                    bob_key_basis_prob, bob_check_basis_prob,
                    decoy_strong_prob, decoy_weak_prob,
                    decoy_strong_intensity, decoy_weak_intensity,
                    N_key_strong, N_key_weak, N_check_strong, N_check_weak,
                    secrecy=1e-9, correctness=1e-15,
                    lambda_EC=1.16)
