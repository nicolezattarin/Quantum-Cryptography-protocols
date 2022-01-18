import numpy as np
import pandas as pd
import argparse
from parameters import parameters

parser = argparse.ArgumentParser()
parser.add_argument("--block_size", default=1500, help="block_size ",type=int)
parser.add_argument("--alice_key_basis_prob", default=0.9, help="alice key basis probability ",type=float)
parser.add_argument("--alice_check_basis_prob", default=0.1, help="alice check basis probability ",type=float)
parser.add_argument("--bob_key_basis_prob", default=0.5, help="bob key basis probability ", type=float)
parser.add_argument("--bob_check_basis_prob", default=0.5, help="bob check basis probability ", type=float)
parser.add_argument("--decoy_strong_prob", default=0.7, help="decoy strong pulse probability ", type=float)
parser.add_argument("--decoy_weak_prob", default=0.3, help="decoy weak pulse probability ", type=float)
parser.add_argument("--decoy_strong_intensity", default=0.4699, help="decoy weak pulse intensity ", type=float)
parser.add_argument("--decoy_weak_intensity", default=0.1093, help="decoy weak pulse intensity ", type=float)


def main(block_size,
        alice_key_basis_prob, alice_check_basis_prob, 
        bob_key_basis_prob, bob_check_basis_prob,
        decoy_strong_prob, decoy_weak_prob,
        decoy_strong_intensity, decoy_weak_intensity):
    
    p = parameters(alice_key_basis_prob, alice_check_basis_prob, 
                    bob_key_basis_prob, bob_check_basis_prob,
                    decoy_strong_prob, decoy_weak_prob,
                    decoy_strong_intensity, decoy_weak_intensity,
                    secrecy=1e-9, correctness=1e-15,
                    lambda_EC=1.16)
    
    df = pd.read_csv('results/countings_{}_{}frac.csv'.format(block_size, frac))
    df=df.drop(df.index[-1], axis=0)

    # errors on countings and finite key effect
    for c in df.columns[1:]:
        df[c+'_err'] = np.sqrt(df[c])

    df['n_key_tot'] = df['n_key_mumax'] + df['n_key_mumin']
    df['n_key_tot_err'] = np.sqrt(df['n_key_mumax_err']**2 + df['n_key_mumin_err']**2)

    df['n_check_tot'] = df['n_check_mumax'] + df['n_check_mumin']
    df['n_check_tot_err'] = np.sqrt(df['n_check_mumax_err']**2 + df['n_check_mumin_err']**2)

    df['m_key_tot'] = df['m_key_mumax'] + df['m_key_mumin']
    df['m_key_tot_err'] = np.sqrt(df['m_key_mumax_err']**2 + df['m_key_mumin_err']**2)

    df['m_check_tot'] = df['m_check_mumax'] + df['m_check_mumin']
    df['m_check_tot_err'] = np.sqrt(df['m_check_mumax_err']**2 + df['m_check_mumin_err']**2)

    deltaN_key = np.sqrt(0.5*df['n_key_tot']*np.log(19/p.secrecy))
    deltaM_key = np.sqrt(0.5*df['m_key_tot']*np.log(19/p.secrecy))
    deltaN_check = np.sqrt(0.5*df['n_check_tot']*np.log(19/p.secrecy))
    deltaM_check = np.sqrt(0.5*df['m_check_tot']*np.log(19/p.secrecy))

    strong_prefactor = np.exp(p.d_strong_intensity)/p.d_strong_prob
    weak_prefactor = np.exp(p.d_weak_intensity)/p.d_weak_prob

    df['n_key_mumax_plus'] = strong_prefactor*(df['n_key_mumax'] + deltaN_key)
    df['n_key_mumax_min'] = strong_prefactor*(df['n_key_mumax'] - deltaN_key)
    df['n_key_mumax_err'] = strong_prefactor*np.sqrt(df['n_key_mumax_err']**2 \
                                    +(np.log(19./p.secrecy)/(8*df['n_key_tot']))*df['n_key_tot_err']**2)

    df['n_key_mumin_plus'] = weak_prefactor*(df['n_key_mumin'] + deltaN_key)
    df['n_key_mumin_min'] = weak_prefactor*(df['n_key_mumin'] - deltaN_key)
    df['n_key_mumin_err'] = weak_prefactor*np.sqrt(df['n_key_mumin_err']**2 \
                                    +(np.log(19./p.secrecy)/(8*df['n_key_tot']))*df['n_key_tot_err']**2)

    df['n_check_mumax_plus'] = strong_prefactor*(df['n_check_mumax'] + deltaN_check)
    df['n_check_mumax_min'] = strong_prefactor*(df['n_check_mumax'] - deltaN_check)
    df['n_check_mumax_err'] = strong_prefactor*np.sqrt(df['n_check_mumax_err']**2 \
                                    +(np.log(19./p.secrecy)/(8*df['n_check_tot']))*df['n_check_tot_err']**2)

    df['n_check_mumin_plus'] = weak_prefactor*(df['n_check_mumin'] + deltaN_check)
    df['n_check_mumin_min'] = weak_prefactor*(df['n_check_mumin'] - deltaN_check)
    df['n_check_mumin_err'] = weak_prefactor*np.sqrt(df['n_check_mumin_err']**2 \
                                    +(np.log(19./p.secrecy)/(8*df['n_check_tot']))*df['n_check_tot_err']**2)

    df['m_key_mumax_plus'] = strong_prefactor*(df['m_key_mumax'] + deltaM_key)
    df['m_key_mumax_min'] = strong_prefactor*(df['m_key_mumax'] - deltaM_key)
    df['m_key_mumax_err'] = strong_prefactor*np.sqrt(df['m_key_mumax_err']**2 \
                                    +(np.log(19./p.secrecy)/(8*df['m_key_tot']))*df['m_key_tot_err']**2)

    df['m_key_mumin_plus'] = weak_prefactor*(df['m_key_mumin'] + deltaM_key)
    df['m_key_mumin_min'] = weak_prefactor*(df['m_key_mumin'] - deltaM_key)
    df['m_key_mumin_err'] = strong_prefactor*np.sqrt(df['m_key_mumin_err']**2 \
                                    +(np.log(19./p.secrecy)/(8*df['m_key_tot']))*df['m_key_tot_err']**2)

    df['m_check_mumax_plus'] = strong_prefactor*(df['m_check_mumax'] + deltaM_check)
    df['m_check_mumax_min'] = strong_prefactor*(df['m_check_mumax'] - deltaM_check)
    df['m_check_mumax_err'] = weak_prefactor*np.sqrt(df['m_check_mumax_err']**2 \
                                    +(np.log(19./p.secrecy)/(8*df['m_check_tot']))*df['m_check_tot_err']**2)

    df['m_check_mumin_plus'] = weak_prefactor*(df['m_check_mumin'] + deltaM_check)
    df['m_check_mumin_min'] = weak_prefactor*(df['m_check_mumin'] - deltaM_check)
    df['m_check_mumin_err'] = weak_prefactor*np.sqrt(df['m_check_mumin_err']**2 \
                                    +(np.log(19./p.secrecy)/(8*df['m_check_tot']))*df['m_check_tot_err']**2)

    # df=df[df.select_dtypes(include=[np.number]).ge(0).all(1)]
    # df.index=range(len(df))

    #qber
    df['QBER_key'] = df['m_key_tot']/df['n_key_tot']
    df['QBER_key_err'] = np.sqrt(df['m_key_tot_err']**2/df['n_key_tot']**2 + \
                                df['m_key_tot']**2*df['n_key_tot_err']**2/df['n_key_tot']**4)
    df['QBER_check'] = df['m_check_tot']/df['n_check_tot']
    df['QBER_check_err'] = np.sqrt(df['m_check_tot_err']**2/df['n_check_tot']**2 +\
                                df['m_check_tot']**2*df['n_check_tot_err']**2/df['n_check_tot']**4)

    # lower bound of zero photon detections
    df['s_key_0_low'] = (p.tau0/(p.d_strong_intensity-p.d_weak_intensity))*(p.d_strong_intensity*\
                        df['n_key_mumin_min'] - p.d_weak_intensity*df['n_key_mumax_plus'])
    df['s_key_0_low_err'] = (p.tau0/(p.d_strong_intensity-p.d_weak_intensity))* \
                            np.sqrt(p.d_strong_intensity**2*(df['n_key_mumin_err']**2 + \
                                    p.d_weak_intensity**2 * df['n_key_mumax_err']**2))
            
    # upper bound of zero photon detections
    df['s_key_0_up_strong'] = 2*(p.tau0*(np.exp(p.d_strong_intensity)/p.d_strong_prob)*\
                                df['m_key_mumax_plus']+np.sqrt(0.5*df['n_key_tot']*np.log(19/p.secrecy)))
    df['s_key_0_up_strong_err'] = 2*((p.tau0*(np.exp(p.d_strong_intensity)/p.d_strong_prob))**2* df['m_key_mumax_err']**2 \
                                    + (np.log(19/p.secrecy)/(8*df['n_key_tot']))*df['n_key_tot_err']**2)
    df['s_key_0_up_weak'] = 2*(p.tau0*(np.exp(p.d_weak_intensity)/p.d_weak_prob)\
                                *df['m_key_mumin_plus']+np.sqrt(0.5*df['n_key_tot']*np.log(19/p.secrecy)))
    df['s_key_0_up_weak_err'] = 2*((p.tau0*(np.exp(p.d_weak_intensity)/p.d_weak_prob))**2* df['m_key_mumax_err']**2 \
                                    + (np.log(19/p.secrecy)/(8*df['n_key_tot']))*df['n_key_tot_err']**2)


    # lower bound of one photon detections key
    df['s_key_1_low'] = (p.tau1*p.d_strong_intensity/(p.d_weak_intensity*(p.d_strong_intensity-p.d_weak_intensity)))\
                        * (df['n_key_mumin_min'] \
                        - (p.d_weak_intensity/p.d_strong_intensity)**2 *df['n_key_mumax_plus']\
                        - (p.d_strong_intensity**2-p.d_weak_intensity**2)/(p.d_strong_intensity**2)*(df['s_key_0_up_weak']/p.tau0))
                        
    df['s_key_1_low_err'] = (p.tau1*p.d_strong_intensity/(p.d_weak_intensity*(p.d_strong_intensity-p.d_weak_intensity)))\
                            * np.sqrt((df['n_key_mumin_err']**2 + \
                            + (p.d_weak_intensity/p.d_strong_intensity)**4 *df['n_key_mumax_err']**2\
                            + ((p.d_strong_intensity**2-p.d_weak_intensity**2)/(p.d_strong_intensity**2))**2*(df['s_key_0_up_weak_err']/p.tau0)**2))




    # lower bound of one photon detections check everything needed fot phase error
    df['s_check_0_up_weak'] = 2*(p.tau0*(np.exp(p.d_weak_intensity)/p.d_weak_prob)\
                                *df['m_check_mumin_plus']+np.sqrt(0.5*df['n_check_tot']*np.log(19/p.secrecy)))
    df['s_check_0_up_weak_err'] = 2*((p.tau0*(np.exp(p.d_weak_intensity)/p.d_weak_prob))**2* df['m_check_mumax_err']**2 \
                                    + (np.log(19/p.secrecy)/(8*df['n_check_tot']))*df['n_check_tot_err']**2)


    df['s_check_1_low'] = (p.tau1*p.d_strong_intensity/(p.d_weak_intensity*(p.d_strong_intensity-p.d_weak_intensity)))\
                        * (df['n_check_mumin_min'] \
                        - (p.d_weak_intensity/p.d_strong_intensity)**2 *df['n_check_mumax_plus']\
                        - (p.d_strong_intensity**2-p.d_weak_intensity**2)/(p.d_strong_intensity**2)*(df['s_check_0_up_weak']/p.tau0))
                        
    df['s_check_1_low_err'] = (p.tau1*p.d_strong_intensity/(p.d_weak_intensity*(p.d_strong_intensity-p.d_weak_intensity)))\
                            * np.sqrt((df['n_check_mumin_err']**2 + \
                            + (p.d_weak_intensity/p.d_strong_intensity)**4 *df['n_check_mumax_err']**2\
                            + ((p.d_strong_intensity**2-p.d_weak_intensity**2)/(p.d_strong_intensity**2))**2*(df['s_check_0_up_weak_err']/p.tau0)**2))

    df['v_check_1_up'] = (p.tau1/(p.d_strong_intensity-p.d_weak_intensity))*(df['m_check_mumax_plus'] - df['m_check_mumin_min'])
    df['v_check_1_up_err'] = (p.tau1/(p.d_strong_intensity-p.d_weak_intensity))*np.sqrt(df['m_check_mumax_err']**2 + df['m_check_mumin_err']**2)

