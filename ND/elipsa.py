import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

from __metode import gradSpustND, racunaj

# Uganiti želimo obliko elipse:
a, b = 0.55, 0.49
h, k = 0.12, -0.08
alfa = np.pi*0.125
def elipsa(theta, *args):
    """ Funkcija za računanje rotirane elipse odmaknjena izven izhodišča. """
    par = args[0]
    defPar = [1., 1., 0., 0., 0.]
    m = len(par)
    for i in range(m):
        defPar[i] = par[i]
        if i == 0: defPar[1] = par[0]
    a, b, h, k, alfa = defPar
    x = h + a*np.cos(theta)*np.cos(alfa) - b*np.sin(theta)*np.sin(alfa)
    y = k + a*np.cos(theta)*np.sin(alfa) + b*np.sin(theta)*np.cos(alfa)
    return (x, y)

# Generiramo zašumljene podatke
n = 100
thetaRange = (0, 2.*np.pi)
theta = np.sort(np.random.random(n)*(thetaRange[1]-thetaRange[0])+thetaRange[0])
thetaR = np.linspace(thetaRange[0], thetaRange[1], 100)
x, y = elipsa(theta, [a, b, h, k, alfa])
c = 0.1
x = x + c*(np.random.random(n)-0.5)
y = y + c*(np.random.random(n)-0.5)
xr, yr = elipsa(thetaR, [a, b, h, k, alfa])

# Risanje grafa podatkov in prilagojenih elips
plt.figure()
plt.plot(x, y, linestyle="", marker="+")
plt.gca().set_aspect("equal")
plt.xlabel("x")
plt.ylabel("y")
plt.plot(xr, yr, color="k", linestyle=":")
plt.plot(x, y, linestyle="", marker="+")

# Pravo funkcijo bomo iskali preko cenovne funkcije
def MSE(*args):
    """ Mean Squared Error 
    V primeru elipse je uporaba te funkcije malo otežena. 
    Ker za rotirano elipso parametrična spremenljivka theta ne sovpada enako, 
    poiščemo točko, ki se najbolj prilega naši oceni. """
    xt, yt = elipsa(thetaR, *args)
    vsota = 0.
    for i in range(n):
        vsota += np.power( np.amin( np.sqrt( np.power(x[i]-xt, 2.) + np.power(y[i]-yt, 2.) ) ), 2)
    return vsota/n

def plot(init, color):
    """ Priročna funkcija za hkratno risanje in klicanje metod. """
    # Potek metode do konvergence-----------------------------------------------------------
    sol = racunaj(metoda=gradSpustND, f=MSE, x0=init, par=[0.1, 0.0001], eps=1e-5, konv=True)
    # Risanje
    xg, yg = elipsa(thetaR, sol)
    plt.plot(xg, yg, color=color, linestyle="-")
    # Primer še boljše metode, ki se uporablja v takšnih problemih!
    sc = least_squares(MSE, init)
    # print(sc)
    # Risanje
    xsc, ysc = elipsa(thetaR, sc.x)
    plt.plot(xsc, ysc, color=color, linestyle="--")

# POSKUSI zagnati kakšno metodo več pod drugačnimi pogoji! (glej zakomentirane primere)
# Oglej si kakšne rezultate dobiš pri različnem številu parametrov, ki jih želimo optimizirati
# Npr. če vzamemo samo 1 parameter bomo iskali krog, ki se najbolje prilega podatkom!
plot([1.], "red")
# plot([1., 1., 0., 0., 0.], "green")

# Prikaz grafov
plt.show()