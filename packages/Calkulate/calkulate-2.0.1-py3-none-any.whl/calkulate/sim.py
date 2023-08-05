from scipy.optimize import least_squares as olsq
from numpy import full_like, nan


def AT(H,CT,K1,K2,BT,KB,Kw,ST,KS,FT,KF,mu):
       
    # CT, BT, ST, FT are values at start of titration
    
    CO2aq  = mu * CT / (1 + K1/H + K1*K2/H**2)
    bicarb = K1 * CO2aq  / H
    carb   = K2 * bicarb / H
    
    B4 = mu * BT * KB / (H + KB)
    
    OH = Kw / H
    
    HSO4 = mu * ST * H / (KS + H)
    HF   = mu * FT * H / (KF + H)
    
    return bicarb + 2*carb + B4 + OH - H - HSO4 - HF


def H(AT0,acid_mass,acid_conc,sample_mass,CT,K1,K2,BT,KB,Kw,ST,KS,FT,KF):
    
    H = full_like(acid_mass,nan)
    
    mu = sample_mass / (sample_mass + acid_mass)
    
    for i,am in enumerate(acid_mass):
    
        H[i] = olsq(lambda H: \
            AT(H,CT,K1,K2,BT,KB,Kw,ST,KS,FT,KF,mu[i]) - mu[i] * AT0 \
                + acid_mass[i]*acid_conc / (acid_mass[i] + sample_mass),
            1e-8)['x']
        
    return H
