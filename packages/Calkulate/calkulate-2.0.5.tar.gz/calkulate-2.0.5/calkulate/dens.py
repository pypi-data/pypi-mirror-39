from .const import Tzero

def sw(Tk,S):
    
    Tc = Tk - Tzero
    
    return  999.842594                       \
          +   6.793952e-2 * Tc               \
          -   9.095290e-3 * Tc**2            \
          +   1.001685e-4 * Tc**3            \
          -   1.120083e-6 * Tc**4            \
          +   6.536336e-9 * Tc**5            \
      + (     0.824493                       \
          -   4.0899e-3   * Tc               \
          +   7.6438e-5   * Tc**2            \
          -   8.2467e-7   * Tc**3            \
          +   5.3875e-9   * Tc**4 ) * S      \
      + ( -   5.72466e-3                     \
          +   1.0227e-4   * Tc               \
          -   1.6546e-6   * Tc**2 ) * S**1.5 \
      +       4.8314e-4             * S**2

# =============================================================================
#
# --- Estimate HCl titrant density --------------------------------------------
#
# Uses a second-order polynomial, fit through temperature/density points:
#    
# Tk = [288.15, 290.65, 293.15, 295.65, 298.15, 300.65, 
#       303.15, 305.65, 308.15] # K
# D  = [1.029691, 1.029084, 1.028426, 1.02772 , 1.026966, 1.026169,
#       1.025328, 1.024446, 1.023524] # kg/l
#
# These density points were calculated using E-AIM
#  [http://www.aim.env.uea.ac.uk/aim/density/density_electrolyte.php]
#  with option "rho, at the total solute mass fraction"
#  and the concentrations:
#    H+ : 0.1 mol/l
#   Na+ : 0.7 mol/l
#   Cl- : 0.8 mol/l
# This represents (approximately) a 0.1 molar HCl titrant in an NaCl solution
#  with ionic strength equal to that of seawater
    
def acid(Tk):

    return - 3.59047619e-06 * Tk**2 \
           + 1.83214095e-03 * Tk    \
           + 7.99883606e-01
      