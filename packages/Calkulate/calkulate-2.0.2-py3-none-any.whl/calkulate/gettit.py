import numpy as np

def Dickson1981():
# Import simulated titration from Dickson (1981) Table 1
#  doi:10.1016/0198-0149(81)90121-7
    
    # Load titration data
    tdata = np.genfromtxt('dickson81tit.csv', delimiter=',', skip_header=1)
    
    # Extract acid mass and pH
    acid_mass = tdata[:,0] * 1e-3 # kg
    pH        = tdata[:,1]        # Free scale
    
    # Define other variables
    Tk = np.full_like(acid_mass,298.15) # K
    acid_conc   =  0.3 # mol/kg-soln
    sample_mass =  0.2 # kg
    sal         = 35.  # practical
    
    # Set concentrations
    AT = np.float_(0.00245) # Alkalinity / mol/kg-sw
    BT = np.float_(0.00042) # Borate     / mol/kg-sw
    CT = np.float_(0.00220) # Carbon     / mol/kg-sw
    ST = np.float_(0.02824) # Sulfate    / mol/kg-sw
    FT = np.float_(0.00007) # Fluoride   / mol/kg-sw
    PT = np.float_(0      ) # Phosphate  / mol/kg-sw
    XT = [AT, CT, BT, ST, FT, PT]
    
    # Set dissociation constants (Free pH scale)
    Kw     = np.float_(4.32e-14)
    KC1    = np.float_(1.00e-06)
    KC1KC2 = np.float_(8.20e-16)
    KC2    = KC1KC2 / KC1
    KB     = np.float_(1.78e-09)
    KHSO4  = 1/np.float_(1.23e+01)
    KHF    = 1/np.float_(4.08e+02)
    KX = [KC1, KC2, KB, Kw, KHSO4, KHF]
    
    return acid_mass, pH, Tk, acid_conc, sample_mass, sal, XT, KX
