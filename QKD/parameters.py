import warnings

class parameters():
    def __init__(self, alice_key_basis_prob, alice_check_basis_prob, 
                    bob_key_basis_prob, bob_check_basis_prob,
                    decoy_strong_prob, decoy_weak_prob,
                    decoy_strong_intensity, decoy_weak_intensity,
                    N_key_strong, N_key_weak, N_check_strong, N_check_weak,
                    secrecy=1e-9, correctness=1e-15,
                    lambda_EC=1.16):

        """
        Alice and Bob perform an error-correction step that reveals at most λEC bits of information
        """
        import numpy as np

        if alice_check_basis_prob + alice_key_basis_prob != 1:
            raise ValueError('Aice basis probability must sum to 1')
                                
        if alice_check_basis_prob > 1 or alice_check_basis_prob < 0 or \
            alice_key_basis_prob > 1 or alice_key_basis_prob < 0 :
            raise ValueError('Aice basis probability must be between 0 and 1')
        
        if bob_check_basis_prob + bob_key_basis_prob != 1:
            raise ValueError('Bob basis probability must sum to 1')
        
        if bob_check_basis_prob > 1 or bob_check_basis_prob < 0 or \
            bob_key_basis_prob > 1 or bob_key_basis_prob < 0 :
            raise ValueError('Bob basis probability must be between 0 and 1')
        
        if decoy_strong_prob + decoy_weak_prob != 1:
            raise ValueError('Decoy probability must sum to 1')
        
        if decoy_strong_prob > 1 or decoy_strong_prob < 0 or \
            decoy_weak_prob > 1 or decoy_weak_prob < 0 :
            raise ValueError('Decoy probability must be between 0 and 1')
        
        if decoy_strong_intensity < decoy_weak_intensity:
            warnings.warn('Decoy strong intensity must be greater than decoy weak intensity')
            decoy_strong_intensity, decoy_weak_intensity = decoy_weak_intensity, decoy_strong_intensity
        
        if lambda_EC < 0: raise ValueError('λEC must be positive, but it is {}'.format(lambda_EC))

        if N_key_strong < 0: raise ValueError('N_key_strong must be positive, but it is {}'.format(N_key_strong))
        if N_key_weak < 0: raise ValueError('N_key_weak must be positive, but it is {}'.format(N_key_weak))
        if N_check_strong < 0: raise ValueError('N_check_strong must be positive, but it is {}'.format(N_check_strong))
        if N_check_weak < 0: raise ValueError('N_check_weak must be positive, but it is {}'.format(N_check_weak))

        self.a_key_basis_prob = alice_key_basis_prob
        self.a_check_basis_prob = alice_check_basis_prob
        self.b_key_basis_prob = bob_key_basis_prob
        self.b_check_basis_prob = bob_check_basis_prob
        self.d_strong_prob = decoy_strong_prob
        self.d_weak_prob = decoy_weak_prob
        self.d_strong_intensity = decoy_strong_intensity
        self.d_weak_intensity = decoy_weak_intensity
        self.N_key_strong = N_key_strong
        self.N_key_weak = N_key_weak
        self.N_check_strong = N_check_strong
        self.N_check_weak = N_check_weak
        self.secrecy = secrecy
        self.correctness = correctness
        self.lambda_EC = lambda_EC
        
        #τn = sumk p_k e^(−k) k^n/n! is the total probability to send an n photon state.
        self.tau0 = self.d_weak_prob*np.exp(-self.d_weak_intensity) + \
                    self.d_strong_prob*np.exp(-self.d_strong_intensity)
        self.tau1 = self.d_weak_prob*np.exp(-self.d_weak_intensity)*self.d_weak_intensity +\
                    self.d_strong_prob*np.exp(-self.d_strong_intensity)*self.d_strong_intensity
        


