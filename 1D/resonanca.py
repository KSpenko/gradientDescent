import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import golden, fmin_cg
from __animacija1D import animacija1D
from __metode import gradSpust, gradSpustMoment

class harmOscilator:
    """ Model za sumilacijo vzbujenega dušenega nihala: https://en.wikipedia.org/wiki/Resonance """
    def __init__(self, w0=10., sigma=0.1, m=1.):
        """ Parametri simulacije:
        w0    - lastna frekvenca nihala,
        sigma - razmerje dušenja,
        m     - masa nihala, """
        self.w0 = w0
        self.sigma = sigma
        self.m = m
        self.freq = [13.,20.,31.]

    def ode(self, t, y):
        """ Sistem diferencialnih enačb """
        return np.array([y[1], self.extForce(t)/self.m - 2.*self.sigma*self.w0*y[1] - (self.w0**2.)*y[0]])

    def extForce(self, t):
        """ Zunanja sila vzbujanja """
        signal = np.sin(self.freq[0]*t)
        for i in range(1,len(self.freq)):
            signal += np.sin(self.freq[i]*t)
        return signal
    
    def f(self, x):
        """ Funkcija za minimizacijo, ki nam izračuna amplituda nihanja ob motnji. 
        Nihalo uglasimo na lastno frekvenco x in pogledamo kako dobro se odzove na zunanjo silo. """
        skalirniFaktor = -1500.
        try: n = len(x)
        except Exception as e: x = [x]
        amp = []
        for w in x:
            self.w0 = w
            sol = solve_ivp(self.ode, [0, 20], [0., 0.], max_step=1e-2)
            # return np.mean(np.power(np.abs(sol.y[0,len(sol.y[0])//2:]),2.))
            amp.append( np.amax(sol.y[0,len(sol.y[0])*2//3:]) )
        if len(amp) == 1: amp = amp[0]
        return skalirniFaktor * np.array(amp)
    
    def samplePlot(self, w):
        """ Funkcija za priročno risanje grafov. """
        self.w0 = w
        sol = solve_ivp(self.ode, [0, 20], [0., 0.], max_step=1e-1)
        plt.figure()
        plt.plot(sol.t, sol.y[0])
        plt.plot(sol.t, np.abs(sol.y[0]))
        plt.show()

# Zagon simulacije
ho = harmOscilator()
# ho.samplePlot(5.)

# Metode iz strokovnih knjižnic
# print(fmin_cg(ho.f, 1.5))
# print(golden(ho.f, brack=[0.2, 1.2]))

# Skiciramo funkcijo
ani = animacija1D(ho.f, (5.,40.), fN=100)

# POZOR: Program je počasen!
# POSKUSI zagnati kakšno metodo več pod drugačnimi pogoji! (glej zakomentirane primere)
# Potek metod za par korakov-----------------------------------------------------------
ani.racunaj(metoda=gradSpust, x0=23., par=[0.1, 0.001], N=100)
# ani.racunaj(metoda=gradSpust, x0=7., par=[0.1, 0.001], N=100)
# ani.racunaj(metoda=gradSpustMoment, x0=23., par=[0.1, 0.001, 1.0, 0.2, -1.7], N=100)

# Potek metod do konvergence-----------------------------------------------------------
# ani.racunaj(metoda=gradSpust, x0=0.1, par=[0.01, 0.0001], eps=1e-5, konv=True)
# ani.racunaj(metoda=gradSpustMoment, x0=1.5, par=[0.01, 0.001, 1.0, 2.0, -0.1], eps=1e-5, konv=True)

# Zaženemo animacijo
ani.narisi(casAnimacije=500, verbose=0, save="resonanca")