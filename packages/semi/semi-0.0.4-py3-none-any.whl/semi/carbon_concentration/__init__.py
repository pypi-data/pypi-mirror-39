import numpy as np

def transmittance_at_wn_570(t_cm):
    '''
    after SEMI draft 4681, section 10.3.1.3
    
    t_cm: sample thickness [cm]
    
    T_570: transmittance at wavenumer 570
    '''
    
    T_570 = 0.524 * np.exp(-1.4 * t_cm) / (1 - 0.076 * np.exp(-2.8 * t_cm))
    
    return T_570
    
    