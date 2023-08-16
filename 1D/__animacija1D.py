import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from IPython.display import HTML
from IPython.display import display

class animacija1D:
    def __init__(self, f, xInterval, fN=20):
        """ Priprava grafa in skiciranje funkcije. """
        self.f = f
        self.xInterval = xInterval
        self.fN = fN
        self.runs = []

        self.fig, self.ax = plt.subplots()
        x = np.linspace(self.xInterval[0], self.xInterval[1], fN)
        y = self.f(x)
        self.ax.plot(x, y, zorder=-1, linewidth=0.1)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_xlim(self.xInterval)
        
        max = np.amax(self.f(x))
        min = np.amin(self.f(x))
        razpon = max-min
        self.yInterval = (min-0.1*razpon, max+0.1*razpon)
        self.ax.set_ylim((min-0.1*razpon, max+0.1*razpon))

    def racunaj(self, metoda, x0, par, N=10, eps=1e-3, konv=False):
        """ Priročna funkcija za iteriranje oz. večkratno korakanje.
        Funkcija se lahko uporablja za končno število korakov: konv = False,
        ali pa dokler ne konvergira za dano vrednost eps: konv = True """
        tabPoints = []
        count = 0
        if konv:
            minimum = self.f(x0)
            while True and count < 1000:
                xN, par = metoda(self.f, x0, par)
                tabPoints.append( [x0, self.f(x0)] )
                x0 = xN
                fxN = self.f(x0)
                if abs(minimum-fxN) < eps: break
                minimum = min(minimum, fxN)
                count += 1
        else:
            for i in range(N+1):
                xN, par = metoda(self.f, x0, par)
                tabPoints.append( [x0, self.f(x0)] )
                x0 = xN
                count += 1
        self.runs.append( tabPoints )
        print(x0, self.f(x0), count)
        return x0

    def zacetekAnimacije(self):
        """ Podmetoda za zacetek animacije. """
        self.fig.suptitle("0")
        self.artists = []
        artists = []
        for j in range(len(self.runs)):
            sc = self.ax.scatter( [self.runs[j][0][0]], [self.runs[j][0][1]] )
            self.artists.append( sc )
            artists.append(sc)
        return artists

    def animiraj(self, i):
        """ Podmetoda za animiranje. """
        self.fig.suptitle(str(i))
        artists = []
        for j in range(len(self.runs)):
            col = self.artists[j].get_facecolors()
            if i == len(self.runs[j])-1:
                vline = self.ax.vlines(self.runs[j][-1][0], self.yInterval[0], self.yInterval[1], linestyles="--", color=col[0])
                artists.append(vline)
            elif i >= len(self.runs[j]): continue

            if self.verbose == 0:
                self.artists[j].set_offsets( [self.runs[j][i]] )
                artists.append( self.artists[j] )
            elif self.verbose == 1:
                arw = self.ax.arrow( self.runs[j][i-1][0], self.runs[j][i-1][1], self.runs[j][i][0]-self.runs[j][i-1][0], self.runs[j][i][1]-self.runs[j][i-1][1], length_includes_head=True, color=col[0], head_width=0.01)
                self.artists.append( arw )
                artists.append(arw)
        return artists

    def maxIteration(self):
        """ Podmetoda za izračun števila slik. """
        maxN = 0
        for i in range(len(self.runs)):
            maxN = max(maxN, len(self.runs[i]))
        return maxN

    def narisi(self, casAnimacije=500, verbose=0, save=False, jupyter=False):
        """ Funkcija za risanje animacij. """
        self.verbose = verbose
        ani = animation.FuncAnimation(self.fig, self.animiraj, np.arange(1, self.maxIteration()), interval=casAnimacije, init_func=self.zacetekAnimacije, repeat=False)
        if save != False: ani.save(save+".gif", dpi=80, writer="imagemagick")
        if jupyter:
            display(HTML(ani.to_jshtml()))
        else: plt.show()