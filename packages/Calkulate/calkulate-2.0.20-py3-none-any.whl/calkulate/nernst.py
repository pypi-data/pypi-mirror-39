import numpy as np

R = np.float_(8.3144621)  # Gas constant     / J /K /mol
F = np.float_(96.4853365) # Faraday constant / kC/mol

def nernst(tk):
    return R * tk / F # J/kC
