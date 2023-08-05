from numpy import exp, full, isnan, log, log10, logical_and, nan, nanmean, size
from numpy import abs as np_abs
from numpy import max as np_max
from scipy.optimize import least_squares as olsq
from scipy.stats    import linregress
from .      import conc, dens, dissoc, gettit, sim
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

    
def Gran_guess_AT(Macid,F1,Cacid,Msamp):
    
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
    

def lsqfun_MPH(Macid,H,Msamp,Cacid,f,AT,CT,BT,ST,FT,PT,*KX):
    
    mu = Msamp / (Msamp + Macid)
    
    return sim.AT(f*H,mu,AT,CT,BT,ST,FT,PT,*KX) \
        - AT*mu + Macid*Cacid / (Macid + Msamp)


def MPH_VINDTA(datfile,Vsamp,Cacid,S,CT,PT):
    
    Vacid, EMF, Tk = gettit.VINDTA(datfile)
    
    Macid = Vacid * dens.acid(Tk)      * 1e-3 # kg
    Msamp = Vsamp * dens.sw  (Tk[0],S) * 1e-6 # kg
    
    XT = conc.XT(S,CT,PT)
    KX = dissoc.KX_F(Tk,S,XT[3],XT[4])
    
    F1_  = F1(Macid,EMF,Tk,Msamp)
    LF = F1_ > 0.1*np_max(F1_)
    AT0  = Gran_guess_AT(Macid[LF],F1_[LF],0.1,Msamp)
    EMF0 = nanmean(Gran_EMF0(Macid[LF],EMF[LF],Tk[LF],Msamp,0.1,AT0))
    
    H0 = EMF2H(EMF,EMF0,Tk)
    pH0 = -log10(H0)
    L = logical_and(pH0 > 3.,pH0 < 4.)
    
    KXL = [KXi[L] for KXi in KX]
    
    return MPH(Macid[L],H0[L],Msamp,Cacid,*XT,KXL)


def MPH(Macid,H,Msamp,Cacid,xATx,CT,BT,ST,FT,PT,KX):

    return olsq(lambda AT_f: \
        lsqfun_MPH(Macid,H,Msamp,Cacid,AT_f[1],AT_f[0],
                   CT,BT,ST,FT,PT,*KX),
        [0.002,1])['x']
        
        
def MPH_pH(Macid,H,Msamp,Cacid,f,xATx,CT,BT,ST,FT,PT,KX):

    return olsq(lambda AT: \
        lsqfun_MPH(Macid,H,Msamp,Cacid,f,AT,CT,BT,ST,FT,PT,*KX),
        0.002)['x'][0]
    
    
def MPH_CRM_VINDTA(datfile,Vsamp,AT_cert,S,CT,PT):
    
    Vacid, EMF, Tk = gettit.VINDTA(datfile)
    
    Macid = Vacid * dens.acid(Tk)      * 1e-3 # kg
    Msamp = Vsamp * dens.sw  (Tk[0],S) * 1e-6 # kg
    
    XT = conc.XT(S,CT,PT)
    KX = dissoc.KX_F(Tk,S,XT[3],XT[4])
    
    F1_  = F1(Macid,EMF,Tk,Msamp)
    LF = F1_ > 0.1*np_max(F1_)
    AT0  = Gran_guess_AT(Macid[LF],F1_[LF],0.1,Msamp)
    EMF0 = nanmean(Gran_EMF0(Macid[LF],EMF[LF],Tk[LF],Msamp,0.1,AT0))
    
    H0 = EMF2H(EMF,EMF0,Tk)
    pH0 = -log10(H0)
    L = logical_and(pH0 > 3.,pH0 < 4.)
    
    KXL = [KXi[L] for KXi in KX]
    
    return MPH_CRM(Macid[L],H0[L],Msamp,AT_cert,*XT,KXL)
    
    
def MPH_CRM(Macid,H,Msamp,AT_cert,xATx,CT,BT,ST,FT,PT,KX):
    
    return olsq(lambda Cacid_f: \
        MPH_pH(Macid,H,Msamp,Cacid_f[0],Cacid_f[1],xATx,CT,BT,ST,FT,PT,KX) \
        - AT_cert,[0.1, 1.])['x']
    
    
def MPH_CRM_pH(Macid,H,Msamp,AT_cert,f,xATx,CT,BT,ST,FT,PT,KX):
    
    return olsq(lambda Cacid: \
        MPH_pH(Macid,H,Msamp,Cacid,f,xATx,CT,BT,ST,FT,PT,KX) - AT_cert,
        0.1)['x'][0]
    

#----- Dickson et al. (2003) method -------------------------------------------


def lsqfun_DAA03(Macid,H,Msamp,Cacid,f,
                 AT,xCTx,xBTx,ST,FT,xPTx,xKC1x,xKC2x,xKBx,xKwx,KHSO4,KHF):
    # DAA03 Eq. (14)
    Z = 1 + ST/KHSO4
    return AT + ST / (1 + KHSO4*Z/(f*H)) + FT / (1 + KHF/(f*H)) \
        + ((Msamp + Macid)/Msamp) * f*H/Z \
        - Macid * Cacid / Msamp


def DAA03(Macid,H,Msamp,Cacid,xATx,xCTx,xBTx,ST,FT,xPTx,*KX):
    
    return olsq(lambda opt: \
        lsqfun_DAA03(Macid,H,Msamp,Cacid,opt[1],opt[0],
                     xCTx,xBTx,ST,FT,xPTx,*KX),
        [0.002,1])['x']
     
        
# With fixed factor f=1
def DAA03_pH(Macid,H,Msamp,Cacid,xATx,xCTx,xBTx,ST,FT,xPTx,*KX):
    
    return olsq(lambda opt: \
        lsqfun_DAA03(Macid,H,Msamp,Cacid,1,opt,xCTx,xBTx,ST,FT,xPTx,*KX),
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
#====== GRAN PLOT METHOD ======================================================


def Gran(Macid,EMF,Tk,Msamp,Cacid,
         xATx,CT,BT,ST,FT,PT,KC1,xKC2x,KB,Kw,KHSO4,KHF,KP1,KP2,KP3,
         pHrange=[3.,4.], suppress_warnings=False):
    
    mu = Msamp / (Msamp + Macid)

    Gran_reps = int(20)
    
    Gran_AT     = full( Gran_reps           ,nan)
    Gran_E0     = full( Gran_reps           ,nan)
    Gran_G_vec  = full((Gran_reps,size(EMF)),nan)
    Gran_E0_vec = full((Gran_reps,size(EMF)),nan)
    Gran_H_vec  = full((Gran_reps,size(EMF)),nan)
    Gran_pH_vec = full((Gran_reps,size(EMF)),nan)
    
    Gran_HSO4   = full(size(EMF),0.)
    Gran_HF     = full(size(EMF),0.)
    
    converged = False
    
    for i in range(Gran_reps):
    
        if i == 0:
            Gran_G_vec[i] = F1(Macid,EMF,Tk,Msamp)
            L2 = Gran_G_vec[i] > 0.1 * np_max(Gran_G_vec[i])
        else:
            L2 = logical_and(Gran_pH_vec[i-1] > pHrange[0],
                             Gran_pH_vec[i-1] < pHrange[1])
                
        Gran_AT[i] = Gran_guess_AT(Macid[L2],Gran_G_vec[i,L2],
            Cacid,Msamp)
        
        PPC = 0.001 # permitted % change in AT
        if i > 2:
            if np_abs(Gran_AT[i] - Gran_AT[i-1]) / Gran_AT[i] < PPC / 100:
                converged = True
                break
        
        Gran_E0_vec[i,L2] = Gran_EMF0(Macid[L2],EMF[L2],Tk[L2],
            Msamp,Cacid,Gran_AT[i],Gran_HSO4[L2],Gran_HF[L2])
                   
        Gran_E0[i] = nanmean(Gran_E0_vec[i])
        
        Gran_H_vec [i] = EMF2H(EMF,Gran_E0[i],Tk)
        Gran_pH_vec[i] = -log10(Gran_H_vec[i])
        
        Gran_bicarb = mu * CT / (Gran_H_vec[i] / KC1 + 1)
        Gran_HSO4   = mu * ST / (1 + KHSO4 / Gran_H_vec[i])
        Gran_HF     = mu * FT / (1 + KHF   / Gran_H_vec[i])
        Gran_borate = mu * BT / (1 + Gran_H_vec[i] / KB)
        Gran_OH     = Kw / Gran_H_vec[i]
        Gran_P_P2   = mu * PT * (1 - KP1*KP2/(Gran_H_vec[i]**2)) \
            / (1 + KP1/Gran_H_vec[i] + KP2*KP3/Gran_H_vec[i]**2  \
                 + KP1*KP2*KP3/Gran_H_vec[i]**3)
        
        if i < Gran_reps-1:
            Gran_G_vec[i+1] = (  Gran_H_vec [i]  \
                               + Gran_HSO4       \
                               + Gran_HF         \
                               - Gran_bicarb     \
                               - Gran_OH         \
                               - Gran_borate     \
                               + Gran_P_P2     ) * (Msamp + Macid)
    
    if converged:
        Gran_AT_final = Gran_AT[~isnan(Gran_AT)][-1]
        Gran_E0_final = Gran_E0[~isnan(Gran_E0)][-1]
        
    else:
        if not suppress_warnings:
            print('Calkulate: Gran plot iterations did not converge!')
        Gran_AT_final = nan
        Gran_E0_final = nan
    
    return Gran_AT_final, Gran_E0_final, i, Gran_E0_vec[i-1], Gran_pH_vec[i-1]


def Gran_VINDTA(datfile,Msamp,Cacid,S,CT,PT,Tk_force=None):
    
    Vacid, EMF, Tk = gettit.VINDTA(datfile)

    if Tk_force is not None:
        Tk[:] = Tk_force
    
    Macid = Vacid * dens.acid(Tk) * 1e-3 # kg
    
    XT = conc.XT(S,CT,PT)
    KX = dissoc.KX_F(Tk,S,XT[3],XT[4])
    
    return Gran(Macid,EMF,Tk,Msamp,Cacid,*XT,*KX)


def Gran_CRM(Macid,EMF,Tk,Msamp,AT_cert,XT,KX):
    
    Cacid = olsq(lambda Cacid: Gran(Macid,EMF,Tk,
        Msamp,Cacid,*XT,*KX,suppress_warnings=True)[0] - AT_cert,0.1)
    
    return Cacid['x'][0]


def Gran_CRM_VINDTA(datfile,Vsamp,AT_cert,S,CT,PT):
    
    Vacid, EMF, Tk = gettit.VINDTA(datfile)
    
    Macid = Vacid * dens.acid(Tk)      * 1e-3 # kg
    Msamp = Vsamp * dens.sw  (Tk[0],S) * 1e-3 # kg
    
    XT = conc.XT(S,CT,PT)
    KX = dissoc.KX_F(Tk,S,XT[3],XT[4])
    
    return Gran_CRM(Macid,EMF,Tk,Msamp,AT_cert,XT,KX)
