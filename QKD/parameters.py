import warnings

class parameters():
    def __init__(self, alice_key_basis_prob, alice_check_basis_prob, 
                    bob_key_basis_prob, bob_check_basis_prob,
                    decoy_strong_prob, decoy_weak_prob,
                    decoy_strong_intensity, decoy_weak_intensity,
                    secrecy=1e-9, correctness = 1e-15):

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
