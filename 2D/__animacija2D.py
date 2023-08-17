import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation

from IPython.display import HTML
from IPython.display import display

class animacija2D:
    def __init__(self, f, xInterval, yInterval, fN=20):
        """ Priprava grafa in skiciranje funkcije. """
        self.f = f
        self.xlim = xInterval
        self.ylim = yInterval
        self.fN = fN
        self.runs = []

        x = np.linspace(self.xlim[0], self.xlim[1], 30)
        y = np.linspace(self.ylim[0], self.ylim[1], 30)
        X, Y = np.meshgrid(x, y)
        fxy = np.zeros(X.shape)
        for i in range(len(fxy)):
            for j in range(len(fxy[0])):
                fxy[i,j] = self.f([X[i,j], Y[i,j]])

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.ax.plot_surface(X, Y, fxy, cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha=0.5)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('f(x,y)')

        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        zlim = [np.amin(fxy), np.amax(fxy)]
        self.zlim = (zlim[0]-0.1*abs(zlim[1]-zlim[0]), zlim[1]+0.1*abs(zlim[1]-zlim[0]))
        self.ax.set_zlim(self.zlim)
        
    def racunaj(self, metoda, x0, y0, par, N=10, eps=1e-3, konv=False):
        """ Priročna funkcija za iteriranje oz. večkratno korakanje.
        Funkcija se lahko uporablja za končno število korakov: konv = False,
        ali pa dokler ne konvergira za dano vrednost eps: konv = True """
        tabPoints = []
        count = 0
        if konv:
            minimum = self.f([x0, y0])
            while True and count < 1000:
                xN, yN, par = metoda(self.f, x0, y0, par)
                tabPoints.append( [x0, y0, self.f([x0, y0])] )
                x0 = xN
                y0 = yN
                fxyN = self.f([x0, y0])
                if abs(minimum-fxyN) < eps: break
                minimum = min(minimum, fxyN)
                count += 1
        else:
            for i in range(N+1):
                xN, yN, par = metoda(self.f, x0, y0, par)
                tabPoints.append( [x0, y0, self.f([x0, y0])] )
                x0 = xN
                y0 = yN
                count += 1
        self.runs.append( tabPoints )
        print((x0, y0), self.f([x0, y0]), count)
        return x0, y0

    def zacetekAnimacije(self):
        """ Podmetoda za zacetek animacije. """
        self.fig.suptitle("0")
        self.artists = []
        artists = []
        for j in range(len(self.runs)):
            sc, = self.ax.plot( self.runs[j][0][0], self.runs[j][0][1], self.runs[j][0][2], linestyle="", marker="o" )
            self.artists.append( sc )
            artists.append(sc)
        return artists

    def animiraj(self, i):
        """ Podmetoda za animiranje. """
        self.fig.suptitle(str(i))
        artists = []
        for j in range(len(self.runs)):
            col = self.artists[j].get_color()
            if i == len(self.runs[j])-1:
                vline = self.ax.plot([self.runs[j][-1][0],self.runs[j][-1][0]], [self.runs[j][-1][1],self.runs[j][-1][1]], [self.zlim[0], self.zlim[1]], linestyle="--", color=col)
                artists.append(vline)
            elif i >= len(self.runs[j]): continue

            if self.verbose == 0:
                self.artists[j].set_data( self.runs[j][i][0], self.runs[j][i][1])
                self.artists[j].set_3d_properties( self.runs[j][i][2] )
                artists.append( self.artists[j] )
            elif self.verbose == 1:
                arw = self.ax.quiver( self.runs[j][i-1][0], self.runs[j][i-1][1], self.runs[j][i-1][2], self.runs[j][i][0]-self.runs[j][i-1][0], self.runs[j][i][1]-self.runs[j][i-1][1], self.runs[j][i][2]-self.runs[j][i-1][2], color=col)
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