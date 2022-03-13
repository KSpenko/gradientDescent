import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

from __animacija2D import animacija2D
from __metode import gradSpust2D

# Uganiti želimo linearno funkcijo:
a, b, c = 0.62, 0.39, 0.25
def linear(x, a, b):
    return (x*a+b)

# Generiramo zašumljene podatke
n = 50
xrange = (-1, 1)
x = np.sort(np.random.random(n)*(xrange[1]-xrange[0])+xrange[0])
y = linear(x, a, b) + c*(np.random.random(n)-0.5)

# Pravo funkcijo bomo iskali preko cenovne funkcije
def MSE(x0):
    """ Mean Squared Error """
    ai, bi = x0
    vsota = 0.
    for i in range(n):
        vsota += np.power(y[i]-(x[i]*ai+bi), 2)
    return vsota/n
    
# Rešitev iščemo v režimu
xlim = (0.,1.)
ylim = (0.,1.)

# Primer še boljše metode, ki se uporablja v takšnih problemih!
print(least_squares(MSE, [0.9, 0.05]))

# Skiciranje funkcije
ani = animacija2D(MSE, xlim, ylim, fN=20)

# Risanje grafa linearnih funkcij
plt.figure()
plt.plot(x, y, linestyle="", marker="+")
plt.xlabel("x")
plt.ylabel("y")

# POSKUSI zagnati kakšno metodo več pod drugačnimi pogoji! (glej zakomentirane primere)
# Potek metod za par korakov-----------------------------------------------------------
a1, b1 = 0.1, 0.23
plt.plot(x, linear(x, a1, b1), linestyle=":")
a1, b1 = ani.racunaj(metoda=gradSpust2D, x0=a1, y0=b1, par=[0.1, 0.0001], N=50)
plt.plot(x, linear(x, a1, b1))

# a2, b2 = 0.96, 0.82
# plt.plot(x, linear(x, a2, b2), linestyle=":")
# a2, b2 = ani.racunaj(metoda=gradSpust2D, x0=a2, y0=b2, par=[0.1, 0.0001], N=50)
# plt.plot(x, linear(x, a2, b2))

# Potek metod do konvergence-----------------------------------------------------------
# a3, b3 = 0.9, 0.05
# plt.plot(x, linear(x, a3, b3), linestyle=":")
# a3, b3 = ani.racunaj(metoda=gradSpust2D, x0=a3, y0=b3, par=[0.1, 0.0001], eps=1e-5, konv=True)
# plt.plot(x, linear(x, a3, b3))

# Zagon animacije
ani.narisi(casAnimacije=500, verbose=1)
plt.show()