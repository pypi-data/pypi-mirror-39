from numpy import exp, log
from . import conc


def Istr(S):
    return 19.924 * S / (1000 - 1.005 * S)


def K2AMP(Tk,S):
# The 2-aminopyridine stoichiometric dissociation constant
# Empirically determined in synthetic seawater [BE86]
# pH on Seawater scale

    pKstarSWS_AMP =   2498.31   /     Tk        \
                    -   15.3274                 \
                    +    2.4050 * log(Tk)       \
                    + (   0.012929              \
                        - 2.9417e-5 * Tk  ) * S

    return 10**-pKstarSWS_AMP


def KC1_KC2(Tk,S):
# Carbonic acid stoichiometric equilibrium constants, Total pH [LDK00]

    pKstarT_C1 = 3633.86      /     Tk  \
               -   61.2172              \
               +    9.6777    * log(Tk) \
               -    0.011555  * S       \
               +    0.0001152 * S**2

    pKstarT_C2 =  471.78      /     Tk  \
               +   25.929               \
               -    3.16967   * log(Tk) \
               -    0.01781   * S       \
               +    0.0001122 * S**2

    return 10**-pKstarT_C1, 10**-pKstarT_C2


def KB(Tk,S):
# Boric acid equilibrium constant, Total pH scale
# Equation 23 [D90a]

    ln_KB =   ( - 8966.90                        \
                - 2890.53   * S**0.5             \
                -   77.942  * S                  \
                +    1.728  * S**1.5             \
                -    0.0996 * S**2   ) /     Tk  \
            + 148.0248                           \
            + 137.1942  * S**0.5                 \
            +   1.62142 * S                      \
            - (     24.4344                      \
                +   25.085  * S**0.5             \
                +    0.2474 * S      ) * log(Tk) \
            +   0.053105    * S**0.5   *     Tk

    return exp(ln_KB)


def KH2O(Tk,S):
# The ion product of water on the Total pH scale, and

    ln_KH2O =     148.96502                       \
              - 13847.26    /     Tk              \
              -    23.6521  * log(Tk)             \
              + (   118.67   /     Tk             \
                  -   5.977                       \
                  +   1.0495 * log(Tk) ) * S**0.5 \
              - 0.01615                 * S

    return exp(ln_KH2O)


def KHSO4(Tk,S):
# The bisulfate stoichiometric dissociation constant on the Free pH scale

    # Ionic strength
    I = Istr(S)

    # Bisulfate dissociation
    ln_KHSO4 = - 4276.1   /     Tk                  \
               +  141.328                           \
               -   23.093 * log(Tk)                 \
               + ( - 13856     /     Tk             \
                   +   324.57                       \
                   -    47.986 * log(Tk) ) * I**0.5 \
               + (   35474     /     Tk             \
                   -   771.54                       \
                   +   114.723 * log(Tk) ) * I      \
               - (    2698     /     Tk)   * I**1.5 \
               + (    1776     /     Tk)   * I**2   \
               + log(1 - 0.001005 * S)

    return exp(ln_KHSO4)


def KHF_PF87(Tk,S):
# Hydrogen fluoride dissociation constant, Total pH scale
# Inputs: <T> = temperature / K; <S> = salinity
# Source: Perez & Fraga (1987) Mar Chem 21(2), doi:10.1016/0304-4203(87)90036-3
# Check value: T = 298.15 & S = 35 -> lnKHF = -6.09
# MATLAB script written by Matthew P. Humphreys; last updated 2015-01-20
# Converted to Python 2018-11-29
    
    ln_KHF = - ( - 874     / Tk        \
                 -   0.111 * S **0.5   \
                 +   9.68            )
             
    return exp(ln_KHF)
             

def KHF(Tk,S):
    
    # Ionic strength
    I = Istr(S)
    
    # Sulfate info for pH scale conversion
    ST = conc.ST(S)
    KS = KHSO4(Tk,S)
    
    # Evaluate HF dissociation constant
    ln_KF =   1590.2   / Tk       \
            -   12.641            \
            +    1.525 * I **0.5  \
            + log(1 - 0.001005*S) \
            + log(1 + ST/KS)
            
    return exp(ln_KF)
    