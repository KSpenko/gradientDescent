import numpy as np
import matplotlib.pyplot as plt

def gradSpust2D(f, x0, y0, par=[0.1, 0.001]):
    """ Metoda gradientnega spusta za mimizacijo funkcije dveh spremenljivk. """
    faktor, delta = par
    # izračunamo dve komponenti odvoda oz. gradienta
    dfx = f([x0+0.5*delta, y0]) - f([x0-0.5*delta, y0])
    dfy = f([x0, y0+0.5*delta]) - f([x0, y0-0.5*delta])
    naklonX = dfx/delta
    naklonY = dfy/delta
    # izvedemo korak po klancu navzdol
    xN = x0 - faktor*naklonX
    yN = y0 - faktor*naklonY
    # Ali lahko izboljšamo konvergenco?
    # if f([xN, yN]) > f([x0, y0]): par[1] = 0.5*par[1]
    return xN, yN, par