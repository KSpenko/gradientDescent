import numpy as np
from scipy.optimize import golden, fmin_cg
from __animacija1D import animacija1D
from __metode import gradSpust, gradSpustMoment

# Funkcija, ki jo želimo minimizirati
def polynomial(x):
    skalirniFaktor = 30.13
    return skalirniFaktor * (x-0.15)*(x-0.28)*(x-0.46)*(x-0.95)*(x-1.25)*(x-1.45)

# Metode iz strokovnih knjižnic
print(fmin_cg(polynomial, 1.5))
print(golden(polynomial, brack=[0.2, 1.2]))

# Skiciramo funkcijo
ani = animacija1D(polynomial, (0.,0.5*np.pi), fN=100)

# POSKUSI zagnati kakšno metodo več pod drugačnimi pogoji! (glej zakomentirane primere)
# Potek metod za par korakov-----------------------------------------------------------
ani.racunaj(metoda=gradSpust, x0=1.5, par=[0.01, 0.0001], N=20)
# ani.racunaj(metoda=gradSpust, x0=0.1, par=[0.01, 0.0001], N=20)
# ani.racunaj(metoda=gradSpustMoment, x0=1.5, par=[0.01, 0.001, 1.0, 2.0, -0.1], N=40)

# Potek metod do konvergence-----------------------------------------------------------
# ani.racunaj(metoda=gradSpust, x0=0.1, par=[0.01, 0.0001], eps=1e-5, konv=True)
# ani.racunaj(metoda=gradSpustMoment, x0=1.5, par=[0.01, 0.001, 1.0, 2.0, -0.1], eps=1e-5, konv=True)

# Zaženemo animacijo
ani.narisi(casAnimacije=500, verbose=0)