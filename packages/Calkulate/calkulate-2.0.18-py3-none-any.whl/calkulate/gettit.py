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
    AT  = float_(0.00245) # Alkalinity / mol/kg-sw
    BT  = float_(0.00042) # Borate     / mol/kg-sw
    CT  = float_(0.00220) # Carbon     / mol/kg-sw
    ST  = float_(0.02824) # Sulfate    / mol/kg-sw
    FT  = float_(0.00007) # Fluoride   / mol/kg-sw
    PT  = float_(0      ) # Phosphate  / mol/kg-sw
    SiT = float_(0      ) # Silicate   / mol/kg-sw
    XT  = [AT, CT, BT, ST, FT, PT, SiT]
    
    # Set dissociation constants (all are Free pH scale)
    KH2O   = full_like(Macid,4.32e-14)
    KC1    = full_like(Macid,1.00e-06)
    KC1KC2 = full_like(Macid,8.20e-16)
    KC2    = KC1KC2 / KC1
    KB     = full_like(Macid,1.78e-09)
    KHSO4  = 1 / full_like(Macid,1.23e+01)
    KHF    = 1 / full_like(Macid,4.08e+02)
    KP1    = full_like(Macid,56.8)
    KP2    = full_like(Macid,8e-7)
    KP3    = full_like(Macid,1.32e-15) / KP2
    KSi    = full_like(Macid,1)
    KX = [KC1,KC2, KB, KH2O, KHSO4, KHF, KP1,KP2,KP3, KSi]
    
    return Macid, pH, Tk, Msamp, Cacid, sal, XT, KX
