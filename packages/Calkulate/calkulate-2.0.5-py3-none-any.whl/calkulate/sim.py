from scipy.optimize import least_squares as olsq
from numpy import full_like, nan


def AT(H,mu,xATx,CT,BT,ST,FT,PT,KC1,KC2,KB,Kw,KHSO4,KHF,KP1,KP2,KP3):
       
    # XT are values at start of titration
    
    CO2aq  = mu * CT / (1 + KC1/H + KC1*KC2/H**2)
    bicarb = KC1 * CO2aq  / H
    carb   = KC2 * bicarb / H
    
    B4 = mu * BT * KB / (H + KB)
    
    OH = Kw / H
    
    HSO4 = mu * ST * H / (KHSO4 + H)
    HF   = mu * FT * H / (KHF   + H)
    
    P0 = mu * PT / (1 + KP1/H + KP1*KP2/H**2 + KP1*KP2*KP3/H**3)
    P2 = mu * PT / (H**2/(KP1*KP2) + H/KP2 + 1 + KP3/H)
    P3 = mu * PT / (H**3/(KP1*KP2*KP3) + H**2/(KP2*KP3) + H/KP3 + 1)
    
    return bicarb + 2*carb + B4 + OH - H - HSO4 - HF - P0 + P2 + 2*P3


def H(Macid,Msamp,Cacid,*XT_KX):
    
    H = full_like(Macid,nan)
    
    mu = Msamp / (Msamp + Macid)
    
    for i,am in enumerate(Macid):
    
        H[i] = olsq(lambda H: \
            AT(H,mu[i],*XT_KX) - mu[i] * XT_KX[0] + Macid[i]*Cacid                       \
                / (Macid[i] + Msamp),
            1e-8)['x']
        
    return H
