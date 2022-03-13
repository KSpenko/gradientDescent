import numpy as np

from __animacija2D import animacija2D
from __metode import gradSpust2D

# Funkcijo katere minimume želimo poiskati
def sinCos(x):
    return np.sin(0.5*(x[0]**2) - 0.25*(x[1]**2) + 3)*np.cos(2.*x[0] -1. + np.exp(x[1]))*np.exp(-0.25*x[0]**2.-0.25*x[1]**2.)

# Omejimo se na specifičen del rešitev
xlim = (-2.,2.)
ylim = (-2.,2.)

# Skiciranje funkcije
ani = animacija2D(sinCos, xlim, ylim, fN=20)

# POSKUSI zagnati kakšno metodo več pod drugačnimi pogoji! (glej zakomentirane primere)
# Potek metod za par korakov-----------------------------------------------------------
ani.racunaj(metoda=gradSpust2D, x0=1.2, y0=0.5, par=[0.1, 0.0001], N=50)
# ani.racunaj(metoda=gradSpust2D, x0=-1.5, y0=0., par=[0.1, 0.0001], N=50)
# Potek metod do konvergence-----------------------------------------------------------
# ani.racunaj(metoda=gradSpust2D, x0=0.1, y0=-1., par=[0.1, 0.0001], eps=1e-3, konv=True)

# Zagon animacije
ani.narisi(casAnimacije=500, verbose=1)