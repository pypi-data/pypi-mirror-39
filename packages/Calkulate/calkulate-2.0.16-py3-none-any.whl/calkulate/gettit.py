from numpy import float_, full_like, genfromtxt
from .const import Tzero


def VINDTA(datfile):
    
    tdata = genfromtxt(datfile, delimiter='\t', skip_header=2)
    
    Vacid = tdata[:,0]         # ml
    EMF   = tdata[:,1]         # mV
    Tk    = tdata[:,2] + Tzero # K

    return Vacid, EMF, Tk


def Dickson1981():
# Import simulated titration from Dickson (1981) Table 1
#  doi:10.1016/0198-0149(81)90121-7
    
    # Load titration data
    tdata = genfromtxt('dickson81tit.csv', delimiter=',', skip_header=1)
    
    # Extract acid mass and pH
    Macid = tdata[:,0] * 1e-3 # kg
    pH    = tdata[:,1]        # Free scale
    
    # Define other variables
    Tk = full_like(Macid,298.15) # K
    Cacid =  0.3 # mol/kg-soln
    Msamp =  0.2 # kg
    sal   = 35.  # practical
    
    # Set concentrations
    AT = float_(0.00245) # Alkalinity / mol/kg-sw
    BT = float_(0.00042) # Borate     / mol/kg-sw
    CT = float_(0.00220) # Carbon     / mol/kg-sw
    ST = float_(0.02824) # Sulfate    / mol/kg-sw
    FT = float_(0.00007) # Fluoride   / mol/kg-sw
    PT = float_(0      ) # Phosphate  / mol/kg-sw
    XT = [AT, CT, BT, ST, FT, PT]
    
    # Set dissociation constants (Free pH scale)
    Kw     = float_(4.32e-14)
    KC1    = float_(1.00e-06)
    KC1KC2 = float_(8.20e-16)
    KC2    = KC1KC2 / KC1
    KB     = float_(1.78e-09)
    KHSO4  = 1/float_(1.23e+01)
    KHF    = 1/float_(4.08e+02)
    KP1    = float_(56.8)
    KP2    = float_(8e-7)
    KP3    = float_(1.32e-15) / KP2
    KX = [KC1, KC2, KB, Kw, KHSO4, KHF, KP1, KP2, KP3]
    
    return Macid, pH, Tk, Msamp, Cacid, sal, XT, KX
