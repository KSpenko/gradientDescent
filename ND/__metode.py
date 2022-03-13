import numpy as np
import matplotlib.pyplot as plt

def gradSpustND(f, x0, par=[0.1, 0.001]):
    """ Metoda gradientnega spusta za mimizacijo funkcije več spremenljivk. """
    faktor, delta = par
    n = len(x0)
    xN = x0
    # izračunamo vse komponente gradienta
    for i in range(n):
        dx = np.zeros(n)
        dx[i] = 1.
        dfi = f(x0+dx*0.5*delta) - f(x0-dx*0.5*delta)
        naklon = dfi/delta
        # za vsako komponento naredimo premik
        xN -= faktor*naklon*dx
    if f(xN) > f(x0): par[1] = 0.5*par[1]
    return xN, par

def racunaj(metoda, f, x0, par, N=10, eps=1e-3, konv=False):
    """ Priročna funkcija za iteriranje oz. večkratno korakanje.
    Funkcija se lahko uporablja za končno število korakov: konv = False,
    ali pa dokler ne konvergira za dano vrednost eps: konv = True """
    tabPoints = []
    count = 0
    if konv: # Konvergiranje
        minimum = f(x0)
        while True and count < 1000:
            xN, par = metoda(f, x0, par)
            tabPoints.append( [x0, f(x0)] )
            x0 = xN
            fxyN = f(x0)
            if abs(minimum-fxyN) < eps: break
            minimum = min(minimum, fxyN)
            count += 1
    else: # Končno število korakov
        for i in range(N+1):
            xN, par = metoda(f, x0, par)
            tabPoints.append( [x0, f(x0)] )
            x0 = xN
            count += 1
    print(x0, f(x0), count)
    return x0