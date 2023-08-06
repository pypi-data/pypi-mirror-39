# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:14:18 2015

@author: 5nm
"""

from ..modules import *

# Kondo spectra

import scipy.optimize as so
import scipy.integrate as integrate


kb = C.Boltzmann
ec = C.elementary_charge
me = C.electron_mass
hbar = C.Planck/2*np.pi

def FermiFunc(en,T):
    #energies in volts
    #the assumption is that the energy vector will be correspondingly offset by the voltage if needed

    return 1.0 / (np.exp(ec*(en) / (kb * T)) + 1)


def TransmissionCoefficient(en,V,phiS,phiT,z):

    _a = np.sqrt((ec*me/hbar**2)*(phiS+phiT-2*en+V))

    return np.exp(-2*z*_a)

def TersoffHamann(en, rhoS,rhoT,V, T_T=300, T_S=300):
    #the arguments should already be arrays as a function of energy
    fT = FermiFunc(en-V,T_T)
    fS = FermiFunc(en, T_S)
    TE = TransmissionCoefficient(en, V, 4, 4, 0.5e-9)
    int2 = rhoS*rhoT*TE*(-fT+fS)

    return np.trapz(int2,en)

def Dynes(en,gap=5e-3,gammaD=4e-5):
    #return (en-gammaD*1j)
    #return (np.sqrt((en - gammaD * 1j) ** 2 - gap ^ 2))
    return np.abs(np.real((en - gammaD * 1j) / (np.sqrt((en - gammaD * 1j) ** 2 - gap ** 2))))
    #return np.real((en+gammaD*1j)/(np.sqrt((en+gammaD*1j)**2-gap**2)))

def IV(Vrange,rhoS,rhoT,T=300):
    #here rhoS and rhoT should be functions
    en = np.arange(-1,1,0.0005)
    _iv = []
    for v in Vrange:
        _iv.append(TersoffHamann(en, rhoS(en-v), rhoT(en), v, T_T=T, T_S=T))
    return _iv
        #_iv.append(np.trapz(TersoffHamann(en,rhoS(en),rhoT(en-v),v,T_T=T,T_S=T),en))


####KONDO functions
##from Gupta Nano Lett. DOI:10.1021/nl1024563

def fano(V, e0=0, G=10e-3, q=0):
    ep = (V - e0) / G
    return (ep + q) ** 2 / (1 + ep ** 2)



# def fitfunc(x, a, b, c):
#     return a * x ** c + b
#
#
# x = np.linspace(0, 10, 50)
# y = x ** 2 + 6
#
# popt, pcov = so.curve_fit(fitfunc, x, y)
#
# vvec = np.linspace(-50e-3, 50e-3, 200)
# cst = {'ec': 1.60217657e-19}

#
# fig, ax = plt.subplots(2, 1)
# ax[0].plot(vvec)
# ax[1].plot(vvec, fano(vvec, q=10, G=2e-3))


