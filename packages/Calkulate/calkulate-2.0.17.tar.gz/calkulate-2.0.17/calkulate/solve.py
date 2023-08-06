from numpy import exp, full, isnan, log, log10, logical_and, mean, nan, \
                  nanmean, size, zeros
from numpy import abs as np_abs
from numpy import max as np_max
from scipy.optimize import least_squares as olsq
from scipy.stats    import linregress
from .      import sim
from .const import F, R


#==============================================================================
#====== EMF to [H+] CONVERSIONS ===============================================


def EMF2H(EMF,EMF0,Tk):
    # DAA03 Eq. (13) with typo corrected (EMF and EMF0 switched)
    return exp((EMF - EMF0) * F / (R * Tk))


def H2EMF(H,EMF0,Tk):
    return EMF0 + log(H) * R * Tk / F


def f2dEMF0(Tk,f):
    return (R * Tk / F) * log(f)


#==============================================================================
#====== GRAN ESTIMATOR FUNCTIONS ==============================================


def F1(Macid,EMF,Tk,Msamp):
    # DAA03 Eq. (10)
    return (Msamp + Macid) * exp(EMF * F / (R * Tk))

    
def Gran_guess_AT(Macid,F1,Msamp,Cacid):
    
    grad,inty,_,_,_ = linregress(Macid,F1)
    intx = -inty/grad
    
    AT0 = intx * Cacid / Msamp
    
    return AT0

     
def Gran_EMF0(Macid,EMF,Tk,Msamp,Cacid,AT,HSO4=0,HF=0):
    # DAA03 Eq. (11)
    return EMF - (R * Tk / F) * log(((Macid*Cacid - Msamp*AT) \
        - Msamp * (HF + HSO4)) / (Msamp + Macid))


#==============================================================================
#====== LEAST SQUARES SOLVERS =================================================


#----- MP Humphreys method ----------------------------------------------------
         
        
def lsqfun_MPH(Macid,EMF,Tk,Msamp,Cacid,EMF0,AT,CT,BT,ST,FT,PT,SiT,KX):
    
    mu = Msamp / (Msamp + Macid)
    
    H = EMF2H(EMF,EMF0,Tk)
    
    return sim.AT(H,mu,AT,CT,BT,ST,FT,PT,SiT,*KX)[0] \
        - AT*mu + Macid*Cacid / (Macid + Msamp)
        
        
def MPH(Macid,EMF,Tk,Msamp,Cacid,xATx,CT,BT,ST,FT,PT,SiT,KX):
    
    F1g = F1(Macid,EMF,Tk,Msamp)

    Lg = logical_and(F1g > 0.1*np_max(F1g), F1g < 0.9*np_max(F1g))
    
    ATg   =  Gran_guess_AT(Macid[Lg],F1g[Lg],Msamp,Cacid)
    EMF0g = mean(Gran_EMF0(Macid[Lg],EMF[Lg],Tk[Lg],Msamp,Cacid,ATg))
    
    pHg = -log10(EMF2H(EMF,EMF0g,Tk))
    
    L = logical_and(pHg > 3, pHg < 4)
    KXL = [KXi[L] for KXi in KX]

    AT_EMF0 = olsq(lambda AT_EMF0: \
        lsqfun_MPH(Macid[L],EMF[L],Tk[L],Msamp,Cacid,AT_EMF0[1],AT_EMF0[0],
                   CT,BT,ST,FT,PT,SiT,KXL),
        [ATg,EMF0g], x_scale=[1e-6,1], method='lm')
        
    return AT_EMF0
    

#----- Dickson et al. (2003) method -------------------------------------------


def lsqfun_DAA03(Macid,H,Msamp,Cacid,f,
                 AT,xCTx,xBTx,ST,FT,xPTx,xSiTx,
                 xKC1x,xKC2x,xKBx,xKwx,KHSO4,KHF,xKSix):
    # DAA03 Eq. (14)
    Z = 1 + ST/KHSO4
    return AT + ST / (1 + KHSO4*Z/(f*H)) + FT / (1 + KHF/(f*H)) \
        + ((Msamp + Macid)/Msamp) * f*H/Z \
        - Macid * Cacid / Msamp


def DAA03(Macid,H,Msamp,Cacid,xATx,xCTx,xBTx,ST,FT,xPTx,xSiTx,*KX):
    
    return olsq(lambda opt: \
        lsqfun_DAA03(Macid,H,Msamp,Cacid,opt[1],opt[0],
                     xCTx,xBTx,ST,FT,xPTx,xSiTx,*KX),
        [0.002,1])['x']
     
        
# With fixed factor f=1
def DAA03_pH(Macid,H,Msamp,Cacid,xATx,xCTx,xBTx,ST,FT,xPTx,xSiTx,*KX):
    
    return olsq(lambda opt: \
        lsqfun_DAA03(Macid,H,Msamp,Cacid,1,opt,xCTx,xBTx,ST,FT,xPTx,xSiTx,*KX),
        0.002)['x'][0]


#----- Dickson (1981) method --------------------------------------------------


def lsqfun_Dickson1981(AT,CT,BT,f,H,Macid,Msamp,Cacid,
                       K1,K2,KB,Kw): 
    # Dickson (1981) Eq. (13)
    return Msamp * (AT - CT * (1/(1 + f*H/K1) + 1/(1 + f*H/K2)) \
        - BT/(1 + f*H/KB)) + (Msamp + Macid) * (f*H \
        - Kw/(f*H)) - Macid * Cacid
           
                          
def Dickson1981(Macid,EMF,Tk,Msamp,Cacid,BT,K1,K2,KB,Kw):
    
    EMF0 = 630. # mV
    H = exp((EMF - EMF0) * F / (R * Tk))
    
    L = Macid <= 1.5
    
    Dsolve = olsq(lambda opt: \
       lsqfun_Dickson1981(opt[0],opt[1],BT,opt[2],
                          H[L],Macid[L],Msamp,Cacid,
                          K1,K2,KB,Kw),[0.002,0.002,1])['x']
    
    return Dsolve


#==============================================================================
#====== HALF-GRAN PLOT METHOD =================================================


def halfGran(Macid,EMF,Tk,Msamp,Cacid,xATx,CT,BT,ST,FT,PT,xSiTx,
             KC1,xKC2x,KB,Kw,KHSO4,KHF,KP1,KP2,KP3,xKSix,
             pHrange=[3.,4.], suppress_warnings=False):
    
    mu = Msamp / (Msamp + Macid)

    Gran_reps = int(20)
    
    step_AT = full(Gran_reps,nan)
    step_E0 = full(Gran_reps,nan)

    Gran_HSO4 = zeros(size(EMF))
    Gran_HF   = zeros(size(EMF))
    
    Gran_G  = full((Gran_reps,size(EMF)),nan)
    Gran_E0 = full((Gran_reps,size(EMF)),nan)
    Gran_H  = full((Gran_reps,size(EMF)),nan)
    Gran_pH = full((Gran_reps,size(EMF)),nan)
    
    converged = False
    
    for i in range(Gran_reps):
    
        if i == 0:
            Gran_G[i] = F1(Macid,EMF,Tk,Msamp)
            LG = Gran_G[i] > 0.1 * np_max(Gran_G[i])
        else:
            LG = logical_and(Gran_pH[i-1] > pHrange[0],
                             Gran_pH[i-1] < pHrange[1])
                
        step_AT[i] = Gran_guess_AT(Macid[LG],Gran_G[i,LG],Msamp,Cacid)
        
        PPC = 5e-3 # permitted % change in AT
        if i > 2:
            if np_abs(step_AT[i] - step_AT[i-1]) / step_AT[i] < PPC / 100:
                converged = True
                break
        
        Gran_E0[i,LG] = Gran_EMF0(Macid[LG],EMF[LG],Tk[LG],
            Msamp,Cacid,step_AT[i],Gran_HSO4[LG],Gran_HF[LG])
                   
        step_E0[i] = nanmean(Gran_E0[i])
        
        Gran_H [i] = EMF2H(EMF,step_E0[i],Tk)
        Gran_pH[i] = -log10(Gran_H[i])
        
        Gran_bicarb = mu * CT / (Gran_H[i] / KC1 + 1)
        Gran_HSO4   = mu * ST / (1 + KHSO4 / Gran_H[i])
        Gran_HF     = mu * FT / (1 + KHF   / Gran_H[i])
        Gran_borate = mu * BT / (1 + Gran_H[i] / KB)
        Gran_OH     = Kw / Gran_H[i]
        Gran_P_P2   = mu * PT * (1 - KP1*KP2/(Gran_H[i]**2)) \
            / (1 + KP1/Gran_H[i] + KP2*KP3/Gran_H[i]**2  \
                 + KP1*KP2*KP3/Gran_H[i]**3)
        
        if i < Gran_reps-1:
            Gran_G[i+1] = (  Gran_H [i]  \
                               + Gran_HSO4       \
                               + Gran_HF         \
                               - Gran_bicarb     \
                               - Gran_OH         \
                               - Gran_borate     \
                               + Gran_P_P2     ) * (Msamp + Macid)
    
    if converged:
        final_AT = step_AT[~isnan(step_AT)][-1]
        final_E0 = step_E0[~isnan(step_E0)][-1]
        
    else:
        if not suppress_warnings:
            print('Calkulate: Gran plot iterations did not converge!')
        final_AT = nan
        final_E0 = nan
    
    return final_AT, final_E0
