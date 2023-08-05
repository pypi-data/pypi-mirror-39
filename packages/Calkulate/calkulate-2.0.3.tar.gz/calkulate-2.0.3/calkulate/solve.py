from numpy import exp, full, isnan, log, log10, logical_and, nan, nanmean, size
from numpy import abs as np_abs
from numpy import max as np_max
from scipy.optimize import least_squares as olsq
from scipy.stats    import linregress
from .      import sim
from .const import F, R


def EMF2H(EMF,EMF0,Tk):
    # DAA03 Eq. (13) with typo corrected (EMF and EMF0 switched)
    return exp((EMF - EMF0) * F / (R * Tk))


def H2EMF(H,EMF0,Tk):
    return EMF0 + log(H) * R * Tk / F


def F1(EMF,Tk,sample_mass,acid_mass):
    # DAA03 Eq. (10)
    return (sample_mass + acid_mass) * exp(EMF * F / (R * Tk))
    

def Gran_guess_AT(acid_mass,F1,acid_conc,sample_mass):
    
    grad,inty,_,_,_ = linregress(acid_mass,F1)
    intx = -inty/grad
    
    AT0 = intx * acid_conc / sample_mass
    
    return AT0
     

def Gran_guess_EMF0(EMF,Tk,sample_mass,acid_mass,acid_conc,AT):
    # DAA03 Eq. (11)
    return EMF - (R * Tk / F) \
        * log((-sample_mass*AT + acid_mass*acid_conc) \
                 / (sample_mass + acid_mass))



def lsqfun_MPH(AT,f,H,CT,K1,K2,BT,KB,Kw,ST,KS,FT,KF,mu,
               acid_mass,acid_conc,sample_mass):
    
    return sim.AT(f*H,CT,K1,K2,BT,KB,Kw,ST,KS,FT,KF,mu) - AT*mu \
        + acid_mass*acid_conc / (acid_mass + sample_mass)

def MPH(H,CT,K1,K2,BT,KB,Kw,ST,KS,FT,KF,acid_mass,acid_conc,sample_mass):

    mu = sample_mass / (sample_mass + acid_mass)
    
    return olsq(lambda opt: \
        lsqfun_MPH(opt[0],opt[1],H,CT,K1,K2,BT,KB,Kw,ST,KS,FT,KF,mu,
                   acid_mass,acid_conc,sample_mass),
        [0.002,1])['x']
    

def lsqfun_DAA03(AT,f,H,acid_mass,acid_conc,sample_mass,ST,FT,KS,KF):
    # DAA03 Eq. (14)
    Z = 1 + ST/KS
    return AT + ST / (1 + KS*Z/(f*H)) + FT / (1 + KF/(f*H)) \
        + ((sample_mass + acid_mass)/sample_mass) * f*H/Z \
        - acid_mass * acid_conc / sample_mass

def DAA03(H,acid_mass,acid_conc,sample_mass,ST,FT,KS,KF):
    
    return olsq(lambda opt: \
        lsqfun_DAA03(opt[0],opt[1],H,acid_mass,acid_conc,sample_mass,
                     ST,FT,KS,KF),
        [0.002,1])['x']
        
def DAA03_pH(H,acid_mass,acid_conc,sample_mass,ST,FT,KS,KF):
    
    return olsq(lambda opt: \
        lsqfun_DAA03(opt,1,H,acid_mass,acid_conc,sample_mass,
                     ST,FT,KS,KF),
        0.002)['x']


def lsqfun_Dickson1981(AT,CT,BT,f,H,acid_mass,sample_mass,acid_conc,
                       K1,K2,KB,Kw): 
    # Dickson (1981) Eq. (13)
    return sample_mass * (AT - CT * (1/(1 + f*H/K1) + 1/(1 + f*H/K2)) \
        - BT/(1 + f*H/KB)) + (sample_mass + acid_mass) * (f*H \
        - Kw/(f*H)) - acid_mass * acid_conc
           
                          
def Dickson1981(EMF,Tk,BT,acid_mass,sample_mass,acid_conc,K1,K2,KB,Kw):
    
    EMF0 = 630. # mV
    H = exp((EMF - EMF0) * F / (R * Tk))
    
    L = acid_mass <= 1.5
    
    Dsolve = olsq(lambda opt: \
       lsqfun_Dickson1981(opt[0],opt[1],BT,opt[2],
                          H[L],acid_mass[L],sample_mass,acid_conc,
                          K1,K2,KB,Kw),[0.002,0.002,1])['x']
    
    return Dsolve

def Gran(sample_mass,acid_mass,EMF,Tk,acid_conc,
         CT,KC1,ST,KHSO4,FT,KHF,BT,KB,Kw):
    
    Gran_mu = sample_mass / (sample_mass + acid_mass)

    Gran_reps = int(20)
    
    Gran_AT     = full( Gran_reps           ,nan)
    Gran_E0     = full( Gran_reps           ,nan)
    Gran_G_vec  = full((Gran_reps,size(EMF)),nan)
    Gran_E0_vec = full((Gran_reps,size(EMF)),nan)
    Gran_H_vec  = full((Gran_reps,size(EMF)),nan)
    Gran_pH_vec = full((Gran_reps,size(EMF)),nan)
    
    Gran_bicarb = full((Gran_reps,size(EMF)),nan)
    Gran_HSO4   = full((Gran_reps,size(EMF)),nan)
    Gran_HF     = full((Gran_reps,size(EMF)),nan)
    Gran_borate = full((Gran_reps,size(EMF)),nan)
    Gran_OH     = full((Gran_reps,size(EMF)),nan)
    
    for i in range(Gran_reps):
        
        print(i)
    
        if i == 0:
            Gran_G_vec[i] = F1(EMF,Tk,sample_mass,acid_mass)
            L2 = Gran_G_vec[i] > 0.1 * np_max(Gran_G_vec[i])
        else:
            L2 = logical_and(Gran_pH_vec[i-1] > 3,Gran_pH_vec[i-1] < 4)
                
        print(Gran_pH_vec)
        print(L2)
        Gran_AT[i] = Gran_guess_AT(acid_mass[L2],Gran_G_vec[i,L2],
            acid_conc,sample_mass)
        
        PPC = 0.001 # permitted % change in AT
        if i > 2:
            if np_abs(Gran_AT[i] - Gran_AT[i-1]) / Gran_AT[i] < PPC / 100:
                break
        
        if i == 0:
            Gran_E0_vec[i,L2] = Gran_guess_EMF0(EMF[L2],Tk[L2],
                sample_mass,acid_mass[L2],acid_conc,Gran_AT[i])
        else:
            Gran_E0_vec[i,L2] = EMF[L2] - (R * Tk[L2] / F) * log(      \
                ((acid_conc*acid_mass[L2] - sample_mass*Gran_AT[i])        \
                    - sample_mass * (Gran_HF[i-1,L2] + Gran_HSO4[i-1,L2])) \
                        / (sample_mass + acid_mass[L2]))
        
        Gran_E0[i] = nanmean(Gran_E0_vec[i])
        
        Gran_H_vec [i] = EMF2H(EMF,Gran_E0[i],Tk)
        Gran_pH_vec[i] = -log10(Gran_H_vec[i])
        
        Gran_bicarb[i] = Gran_mu * CT / (Gran_H_vec[i] / KC1 + 1)
        Gran_HSO4  [i] = Gran_mu * ST / (1 + KHSO4 / Gran_H_vec[i])
        Gran_HF    [i] = Gran_mu * FT / (1 + KHF   / Gran_H_vec[i])
        Gran_borate[i] = Gran_mu * BT / (1 + Gran_H_vec[i] / KB)
        Gran_OH    [i] = Kw / Gran_H_vec[i]
        
        if i < Gran_reps-1:
            Gran_G_vec[i+1] = (  Gran_H_vec [i]  \
                               + Gran_HSO4  [i]  \
                               + Gran_HF    [i]  \
                               - Gran_bicarb[i]  \
                               - Gran_OH    [i]  \
                               - Gran_borate[i]) * (sample_mass + acid_mass)
    
    Gran_AT_final = Gran_AT[~isnan(Gran_AT)][-1]
    Gran_E0_final = Gran_E0[~isnan(Gran_E0)][-1]
    
    return Gran_AT_final, Gran_E0_final
