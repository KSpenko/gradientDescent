import numpy as np
import matplotlib.pyplot as plt

def gradSpust(f, x0, par=[0.1, 0.001]):
    """ Metoda gradientnega spusta za mimizacijo funkcije ene spremenljivke. 
    Parametri:
        faktor - faktor s katerim pomnožimo odvod, s čimer določimo velikost koraka
        delta - interval v katerem izračunamo odvod 
    """
    faktor, delta = par
    # izračunamo odvod
    df = f(x0+0.5*delta) - f(x0-0.5*delta)
    naklon = df/delta
    # izvedemo korak po klancu navzdol
    xN = x0 - faktor*naklon
    return xN, par

def gradSpustMoment(f, x0, par=[0.1, 0.001, 1.0, 0.5, 0.]):
    """ Metoda gradientnega spusta za mimizacijo funkcije ene spremenljivke.
    Metodi je dodan moment oz. zalet, ki pomaga pri ubegu lokalnih ekstremov. 
    Parametri:
        faktor - faktor s katerim pomnožimo odvod, s čimer določimo velikost koraka
        delta - interval v katerem izračunamo odvod,
        dt - časovni korak, ki določa simulacijo zaleta
        trenje - faktor trenja, ki določa upočasnitev kotaljenja
        v0 - začetna hitrost kotaljenja
    """
    faktor, delta, dt, trenje, v0 = par
    # izračunamo odvod
    df = f(x0+0.5*delta) - f(x0-0.5*delta)
    # izračunamo kot klanca
    alfa = np.arctan2(df, delta)
    # simuliramo primitivno kotaljenje krogle po klancu nazvdol
    aX = faktor*( -np.sign(df)*np.sin( np.abs(alfa) ) -np.sign(v0)*trenje*np.cos( np.abs(alfa) )) 
    aX -= trenje*np.sign(v0)*(v0**2.)

    xN = x0 + v0*dt + (dt**2.)*0.5*aX
    vX = v0 + dt*aX
    v0 = par[-1]
    par[-1] = vX # hitrost se prenese v naslednji korak -> zalet
    return xN, par