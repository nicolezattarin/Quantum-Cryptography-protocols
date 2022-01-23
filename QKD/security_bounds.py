import numpy as np
import pandas as pd
import argparse
from parameters import parameters

parser = argparse.ArgumentParser()
parser.add_argument("--block_size", default=int(1e6), help="block_size ",type=int)
parser.add_argument("--frac_data", default=0.05, help="fracrtion of data to read ",type=float)
parser.add_argument("--time_evolution", default=True, help="if true, time evolutiohn is studied",type=bool)
parser.add_argument("--alice_key_basis_prob", default=0.9, help="alice key basis probability ",type=float)
parser.add_argument("--alice_check_basis_prob", default=0.1, help="alice check basis probability ",type=float)
parser.add_argument("--bob_key_basis_prob", default=0.5, help="bob key basis probability ", type=float)
parser.add_argument("--bob_check_basis_prob", default=0.5, help="bob check basis probability ", type=float)
parser.add_argument("--decoy_strong_prob", default=0.7, help="decoy strong pulse probability ", type=float)
parser.add_argument("--decoy_weak_prob", default=0.3, help="decoy weak pulse probability ", type=float)
parser.add_argument("--decoy_strong_intensity", default=0.4699, help="decoy weak pulse intensity ", type=float)
parser.add_argument("--decoy_weak_intensity", default=0.1093, help="decoy weak pulse intensity ", type=float)


def main(block_size,frac_data, time_evolution,
        alice_key_basis_prob, alice_check_basis_prob, 
        bob_key_basis_prob, bob_check_basis_prob,
        decoy_strong_prob, decoy_weak_prob,
        decoy_strong_intensity, decoy_weak_intensity):
    """
    Computes QBER and SKR with the respective error as it is proposed in 

    [1] Davide Rusca, Alberto Boaron, Fadri Gru ̈nenfelder, Anthony Martin, and Hugo Zbinden. 
    Finite- key analysis for the 1-decoy state qkd protocol. Applied Physics Letters, 
    112(17):171104, 2018. doi: 10.1063/1.5023340. URL https://doi.org/10.1063/1.5023340.

    [2] Charles Ci Wen Lim, Marcos Curty, Nino Walenta, Feihu Xu, and Hugo Zbinden. 
    Concise security bounds for practical decoy-state quantum key distribution. 
    Phys. Rev. A, 89:022307, Feb 2014. doi: 10.1103/PhysRevA.89.022307. 
    URL https://link.aps.org/doi/10.1103/PhysRevA.89.022307.


    Parameters
    ----------
    block_size : int
        block size
    frac_data : float
        fraction of data to read
    alice_key_basis_prob : float
        probability of Alice using the key basis
    alice_check_basis_prob : float
        probability of Alice using the check basis
    bob_key_basis_prob : float
        probability of Bob using the key basis
    bob_check_basis_prob : float
        probability of Bob using the check basis
    decoy_strong_prob : float
        probability of the decoy being the strong one
    decoy_weak_prob : float
        probability of the decoy being the weak one
    decoy_strong_intensity : float
        intensity of the strong decoy
    decoy_weak_intensity : float
        intensity of the weak decoy
    

    """
    
    p = parameters(alice_key_basis_prob, alice_check_basis_prob, 
                    bob_key_basis_prob, bob_check_basis_prob,
                    decoy_strong_prob, decoy_weak_prob,
                    decoy_strong_intensity, decoy_weak_intensity,
                    secrecy=1e-9, correctness=1e-15,
                    lambda_EC=1.16)

    if not time_evolution:
        df = pd.read_csv('results/countings_{}_{}frac.csv'.format(block_size, frac_data))
        df = df.drop(df.index[-1], axis=0)
    else: 
        df = pd.read_csv('results/time_evolution.csv')

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
    df['n_key_mumax_err_Hoeff'] = strong_prefactor*np.sqrt(df['n_key_mumax_err']**2 \
                                    + (np.log(19./p.secrecy)/(8*df['n_key_tot']))*df['n_key_tot_err']**2)


    df['n_key_mumin_plus'] = weak_prefactor*(df['n_key_mumin'] + deltaN_key)
    df['n_key_mumin_min'] = weak_prefactor*(df['n_key_mumin'] - deltaN_key)
    df['n_key_mumin_err_Hoeff'] = weak_prefactor*np.sqrt(df['n_key_mumin_err']**2 \
                                    + (np.log(19./p.secrecy)/(8*df['n_key_tot']))*df['n_key_tot_err']**2)

    df['n_check_mumax_plus'] = strong_prefactor*(df['n_check_mumax'] + deltaN_check)
    df['n_check_mumax_min'] = strong_prefactor*(df['n_check_mumax'] - deltaN_check)
    df['n_check_mumax_err_Hoeff'] = strong_prefactor*np.sqrt(df['n_check_mumax_err']**2 \
                                    + (np.log(19./p.secrecy)/(8*df['n_check_tot']))*df['n_check_tot_err']**2)

    df['n_check_mumin_plus'] = weak_prefactor*(df['n_check_mumin'] + deltaN_check)
    df['n_check_mumin_min'] = weak_prefactor*(df['n_check_mumin'] - deltaN_check)
    df['n_check_mumin_err_Hoeff'] = weak_prefactor*np.sqrt(df['n_check_mumin_err']**2 \
                                    + (np.log(19./p.secrecy)/(8*df['n_check_tot']))*df['n_check_tot_err']**2)

    df['m_key_mumax_plus'] = strong_prefactor*(df['m_key_mumax'] + deltaM_key)
    df['m_key_mumax_min'] = strong_prefactor*(df['m_key_mumax'] - deltaM_key)
    df['m_key_mumax_err_Hoeff'] = strong_prefactor*np.sqrt(df['m_key_mumax_err']**2 \
                                    + (np.log(19./p.secrecy)/(8*df['m_key_tot']))*df['m_key_tot_err']**2)

    df['m_key_mumin_plus'] = weak_prefactor*(df['m_key_mumin'] + deltaM_key)
    df['m_key_mumin_min'] = weak_prefactor*(df['m_key_mumin'] - deltaM_key)
    df['m_key_mumin_err_Hoeff'] = strong_prefactor*np.sqrt(df['m_key_mumin_err']**2 \
                                    + (np.log(19./p.secrecy)/(8*df['m_key_tot']))*df['m_key_tot_err']**2)

    df['m_check_mumax_plus'] = strong_prefactor*(df['m_check_mumax'] + deltaM_check)
    df['m_check_mumax_min'] = strong_prefactor*(df['m_check_mumax'] - deltaM_check)
    df['m_check_mumax_err_Hoeff'] = weak_prefactor*np.sqrt(df['m_check_mumax_err']**2 \
                                    + (np.log(19./p.secrecy)/(8*df['m_check_tot']))*df['m_check_tot_err']**2)

    df['m_check_mumin_plus'] = weak_prefactor*(df['m_check_mumin'] + deltaM_check)
    df['m_check_mumin_min'] = weak_prefactor*(df['m_check_mumin'] - deltaM_check)
    df['m_check_mumin_err_Hoeff'] = weak_prefactor*np.sqrt(df['m_check_mumin_err']**2 \
                                    + (np.log(19./p.secrecy)/(8*df['m_check_tot']))*df['m_check_tot_err']**2)

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
                            np.sqrt(p.d_strong_intensity**2*(df['n_key_mumin_err_Hoeff']**2 + \
                                    p.d_weak_intensity**2 * df['n_key_mumax_err_Hoeff']**2))
            
    # upper bound of zero photon detections
    df['s_key_0_up_strong'] = 2*(p.tau0*df['m_key_mumax_plus']\
                            + np.sqrt(0.5*df['n_key_tot']*np.log(19/p.secrecy)))
    df['s_key_0_up_strong_err'] = 2*np.sqrt((p.tau0*df['m_key_mumax_err_Hoeff'])**2 \
                            + (np.log(19/p.secrecy)/(8*df['n_key_tot']))*df['n_key_tot_err']**2)

    # lower bound of one photon detections key
    df['s_key_1_low'] = (p.tau1*p.d_strong_intensity/(p.d_weak_intensity*(p.d_strong_intensity-p.d_weak_intensity)))\
                        * (df['n_key_mumin_min'] \
                        - (p.d_weak_intensity/p.d_strong_intensity)**2*df['n_key_mumax_plus']\
                        - (p.d_strong_intensity**2-p.d_weak_intensity**2)/(p.d_strong_intensity**2*p.tau0)*df['s_key_0_up_strong'])
                        
    df['s_key_1_low_err'] = (p.tau1*p.d_strong_intensity/(p.d_weak_intensity*(p.d_strong_intensity-p.d_weak_intensity)))\
                            * np.sqrt((df['n_key_mumin_err_Hoeff']**2 + \
                            + (p.d_weak_intensity/p.d_strong_intensity)**4*df['n_key_mumax_err_Hoeff']**2\
                            + ((p.d_strong_intensity**2-p.d_weak_intensity**2)/(p.d_strong_intensity**2))**2*(df['s_key_0_up_strong_err']/p.tau0)**2))

    # lower bound of one photon detections check everything needed fot phase error
    df['s_check_0_up_weak'] = 2*(p.tau0*df['m_check_mumin_plus']+np.sqrt(0.5*df['n_check_tot']*np.log(19/p.secrecy)))
    df['s_check_0_up_weak_err'] = 2*np.sqrt((p.tau0*df['m_check_mumax_err_Hoeff'])**2 \
                                + (np.log(19/p.secrecy)/(8*df['n_check_tot']))*df['n_check_tot_err']**2)

    df['s_check_1_low'] = (p.tau1*p.d_strong_intensity/(p.d_weak_intensity*(p.d_strong_intensity-p.d_weak_intensity)))\
                        * (df['n_check_mumin_min'] \
                        - (p.d_weak_intensity/p.d_strong_intensity)**2 *df['n_check_mumax_plus']\
                        - (p.d_strong_intensity**2-p.d_weak_intensity**2)/(p.d_strong_intensity**2)*(df['s_check_0_up_weak']/p.tau0))
                        
    df['s_check_1_low_err'] = (p.tau1*p.d_strong_intensity/(p.d_weak_intensity*(p.d_strong_intensity-p.d_weak_intensity)))\
                            * np.sqrt((df['n_check_mumin_err_Hoeff']**2 + \
                            + (p.d_weak_intensity/p.d_strong_intensity)**4 *df['n_check_mumax_err_Hoeff']**2\
                            + ((p.d_strong_intensity**2-p.d_weak_intensity**2)/(p.d_strong_intensity**2*p.tau0))**2*df['s_check_0_up_weak_err']**2))

    df['v_check_1_up'] = (p.tau1/(p.d_strong_intensity-p.d_weak_intensity))*(df['m_check_mumax_plus'] - df['m_check_mumin_min'])
    df['v_check_1_up_err'] = (p.tau1/(p.d_strong_intensity-p.d_weak_intensity))*np.sqrt(df['m_check_mumax_err_Hoeff']**2 + df['m_check_mumin_err_Hoeff']**2)

    def gamma(a,b,c,d, eb, ec, ed): #not considering error on a
            log = np.log(((c+d)/(c*d*b*(1-b)))*(21/a)**2)
            gamma_p = np.sqrt(((c+d)*(1-b)*b)/(c*d)*log)
            gamma = gamma_p/np.log(2)
            partial_b = ((c+d)*(2*b-1)*(log-1))/(2*c*d*np.log(2)*gamma_p)
            partial_c = (b*(b-1)*(log+1))/(2*c*c*np.log(2)*gamma_p)
            partial_d = (b*(b-1)*(log+1))/(2*d*d*np.log(2)*gamma_p)
            error = np.sqrt(eb**2*partial_b**2 + ec**2*partial_c**2 + ed**2*partial_d**2)
            return gamma, error
    err_temp = np.sqrt((df['v_check_1_up_err']/df['s_check_1_low'])**2\
                        +(df['v_check_1_up']*df['s_check_1_low_err']/df['s_check_1_low']**2)**2)
    df['gamma'], df['gamma_err'] = gamma(p.secrecy,df['v_check_1_up']/df['s_check_1_low'],
                                        df['s_key_1_low'],df['s_check_1_low'],
                                        err_temp, df['s_key_1_low_err'], df['s_check_1_low_err'])
    #phase error finally
    df['phi_up'] = df['v_check_1_up']/df['s_check_1_low'] + df['gamma']
    df['phi_up_err'] = np.sqrt(err_temp**2 + df['gamma_err']**2)

    df[df<0]=0 #set to zero non physical values 

    def bin_entropy(x, ex):
            entropy = -x*np.log2(x)-(1-x)*np.log2(1-x)
            error = (np.log(1-x)-np.log(x))*ex/np.log(2)
            return entropy, error

    entropy, error = bin_entropy(df['phi_up'], df['phi_up_err'])
    p.lambda_EC, _ = bin_entropy(np.mean(df['QBER_key']), 0)
    p.lambda_EC = p.lambda_EC*1.16
    df['secret_key_length'] = df['s_key_0_low']+df['s_key_1_low']*(1-entropy)\
                            - p.lambda_EC - 6*np.log2(19/p.secrecy) - np.log2(2/p.correctness)

    df['secret_key_length_err'] = np.sqrt(df['s_key_0_low_err']**2 \
                                    + (df['s_key_1_low_err']*(1-entropy))**2 \
                                    + (df['s_key_1_low_err']*error)**2) 

    repetition_rate = 1
    df['SKR'] = df['secret_key_length']*repetition_rate/df['total_pulses']
    df['SKR_err'] = np.sqrt( (df['secret_key_length_err']*repetition_rate/df['total_pulses'])**2 \
                    + (df['secret_key_length']*repetition_rate*df['total_pulses_err']/df['total_pulses']**2)**2)

    if not time_evolution:
        df.to_csv('results/{}block_{}frac_results.csv'.format(block_size, frac_data), index=False)
    else: 
        df.to_csv('results/time_evolution_result.csv', index=False)

if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)