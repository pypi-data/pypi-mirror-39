from .const import S_Cl, RMM_B, RMM_F

def BT(S):
# Estimate total boron from practical salinity in mol/kg-sw [LKB10]
    return S * 0.1336e-3 / RMM_B

def FT(S):
# Estimate total fluoride from practical salinity [W71] in mol/kg
    return S * 6.75e-5 / (RMM_F * S_Cl)

def ST(S):
    return (0.14 / 96.062) * (S / S_Cl)
