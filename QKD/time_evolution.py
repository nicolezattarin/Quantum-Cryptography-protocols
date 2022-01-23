import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()

def main():
    """
    
    """
    df = pd.read_csv('results/1000000block_1frac_results.csv')
    result = pd.DataFrame({'time': [], 'total_pulses': [], 'm_key_mumax': [], 'm_key_mumin': [], 
                                'n_key_mumax': [], 'n_key_mumin': [], 'm_check_mumax': [], 
                                'm_check_mumin': [], 'n_check_mumax': [], 'n_check_mumin': []})
    for i in range(len(df)):
        a = df[:i+1]
        a = a.sum()
        result = result.append({'time': a['time'], 'total_pulses': a['total_pulses'], 
                                            'm_key_mumax': a['m_key_mumax'], 'm_key_mumin': a['m_key_mumin'],
                                            'n_key_mumax': a['n_key_mumax'], 'n_key_mumin': a['n_key_mumin'], 
                                            'm_check_mumax': a['m_check_mumax'], 'm_check_mumin': a['m_check_mumin'],
                                            'n_check_mumax': a['n_check_mumax'], 'n_check_mumin': a['n_check_mumin']}, ignore_index=True)
    
    import os
    if not os.path.exists('results'): os.mkdir('results')
    result.to_csv('results/time_evolution.csv', index=False)

if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)