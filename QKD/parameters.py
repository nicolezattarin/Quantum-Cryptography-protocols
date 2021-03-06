import warnings

class parameters():
    def __init__(self, alice_key_basis_prob, alice_check_basis_prob, 
                    bob_key_basis_prob, bob_check_basis_prob,
                    decoy_strong_prob, decoy_weak_prob,
                    decoy_strong_intensity, decoy_weak_intensity,
                    secrecy=1e-9, correctness=1e-15,
                    lambda_EC=1.16):

        """
        Parameters
        ----------
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
        secrecy : float
            secrecy of the protocol
        correctness : float
            correctness of the protocol
        lambda_EC : float
            Alice and Bob perform an error-correction step that 
            reveals at most λEC bits of information
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

        self.a_key_basis_prob = alice_key_basis_prob
        self.a_check_basis_prob = alice_check_basis_prob
        self.b_key_basis_prob = bob_key_basis_prob
        self.b_check_basis_prob = bob_check_basis_prob
        self.d_strong_prob = decoy_strong_prob
        self.d_weak_prob = decoy_weak_prob
        self.d_strong_intensity = decoy_strong_intensity
        self.d_weak_intensity = decoy_weak_intensity
        self.secrecy = secrecy
        self.correctness = correctness
        self.lambda_EC = lambda_EC
        
        #τn = sumk p_k e^(−k) k^n/n! is the total probability to send an n photon state.
        self.tau0 = self.d_weak_prob*np.exp(-self.d_weak_intensity) + \
                    self.d_strong_prob*np.exp(-self.d_strong_intensity)
        self.tau1 = self.d_weak_prob*np.exp(-self.d_weak_intensity)*self.d_weak_intensity +\
                    self.d_strong_prob*np.exp(-self.d_strong_intensity)*self.d_strong_intensity
        #fixed parameters
        self.a = 6
        self.b = 19


