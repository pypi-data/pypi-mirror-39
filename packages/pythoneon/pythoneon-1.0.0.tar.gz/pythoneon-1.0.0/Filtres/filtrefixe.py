# -*- encoding: utf-8 -*-
#
# Copyright (C) 2003-2018 René Bastian  <rbastian@musiques-rb.org>
#
# Tpythoneon is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Tpythoneon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tpythoneon; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
#-*-coding:utf-8-*-
# filtrefixe.py
##DEBUT
"""
fournit la classe FiltreFixe selon la littérature concernant le
traitrement du signal.
voir p. ex. Tisserand p. 180

En laisssant, dans passe_haut,  '1.0 - 2*a_inf', on n'obtient pas
'ho' comme indiqué dans Tisserand p. 183.
mais auditivement c'est ce qu'il faut ...
"""

import numpy as np
from samplerate import SR
from conversions import extremum, prony2freq, freq2prony, prony2samples
from Profils.profilbase import ProfilBase
from origine import OrigineStr

__author__ = "Copyright (c) 2007-12 René Bastian (Wissembourg, FRANCE)"
__date__ = "2008.09.21, 09.02.03, 2012.10.03"

def construire_coeffs(a, centre):
    """ construit le vecteur des coefficients """
    return np.concatenate((a[::-1], np.array([centre]), a))

def dcKiller(vx, a=0.995):
    """ filtre la composante continue """
    n = vx.size
    vy = np.zeros(n + 1)
    for i in range(1, n):
        vy[i] = vx[i] - vx[i-1] + a * vy[i-1]
    return vy

def sinc(a, nc):
    "calcule les coefficients de base"
    K = np.arange(1., nc+1, 1.) * 2 * np.pi * a
    g = 2 * a * np.sin(K) / K
    return g

def filtreContinu(signal, fcoupure=12.0, ncoeffs=20):
    """
    éliminer la composante continue du signal.
    On peut donner la fréquence de coupure 'fcoupure' et
    le nombre de coefficients 'ncoeffs'.
    """
    signal -= signal.mean()
    filtre = FiltreFixe("ph", ncoeffs)
    return filtre.evt(signal, freq2prony(fcoupure))

def filtreContinu2(signal):
    "filtre passe-haut; enlève la composante continue dans un signal"
    n = len(signal)
    w = np.zeros(n)
    for i in range(1, n):
        w[i] = (signal[i] - signal[i-1]) * 0.5
    return w

class FiltreFixe(OrigineStr):
    """
    une classe de filtres à fréquence de coupure fixes
    (passe-bas, passe-haut, passe-bande, coupe-bande)
    NB : e, général, il faut appeler evtF !
    À DECIDER SI ON CHANGE CELA
    """
    def __init__(self, genre, nc, prony=None):
        """
        'nc' : nombre de coefficients;
               si SR != 44100: nc = int(nc * float(SR) / 44100)
        'genre' : "pb", "lp" -> passe-bas
                  "ph", "hp" -> passe-haut
                  "xb" -> coupe-bande
                  "bp" -> passe-bande
                  "cr" -> croisé : passe-bande <-> coupe-bande
        Le nombre final de coefficients est 'nc*2 + 1'.
        le fenêtrage peut se faire par un profil.
        prony : hauteur de la fréquence de filtrage
        """
        OrigineStr.__init__(self)
        self.genre = genre
        if SR == 44100:
            self.nc = nc
        else:
            self.nc = int(nc * float(SR) / 44100)
        self.coeffs = None
        if prony is not None:
            self.precalculs(prony)

    @staticmethod
    def construire_coeffs(a, centre):
        """ construit le vecteur des coefficients
        a[::-1], [centre], a
        où centre = freq / SR
        """
        return np.concatenate((a[::-1], np.array([centre]), a))

    def __str__(self):
        "pour avoir les données sous forme de string"
        return self.__class__.__name__  + str(self.__dict__)

    def affiche(self, lprofil=None):
        "pour afficher"
        print("FiltreFixe", self.genre)
        print("nc", self.nc, "->", 2*self.nc+1, "coeffs")
        if self.coeffs is not None:
            print(self.coeffs)
        else:
            print("Il n'y a pas encore de coeffs.")
        if lprofil:
            for p in lprofil:
                print(p)

    def sinc(self, a):
        "calcule les coefficients de base"
        K = np.arange(1., self.nc+1, 1.) * 2 * np.pi * a
        g = 2 * a * np.sin(K) / K
        return g

    def coeffsPasseBas(self, freq):
        """
        n = nombre de coefficients "a" à calculer
        freq = fréquence de coupure
        """
        a_sup = freq / SR
        x = self.sinc(a_sup)
        self.coeffs = self.construire_coeffs(x, 2*a_sup)
        return self.coeffs

    def coeffsPasseHaut(self, fc):
        """
        n = nombre de coefficients "a" à calculer
        fc= fréquence de coupure
        """
        a_inf = fc / SR
        x = -self.sinc(a_inf)
        #self.coeffs = np.concatenate((x[::-1], 1.0 - 2*a_inf, x))
        #self.coeffs = np.concatenate((x[::-1], np.array([1.0 - 2*a_inf]), x))
        self.coeffs = self.construire_coeffs(x, 1.0 - 2*a_inf)
        return self.coeffs

    def coeffsPasseBande(self, fcinf, fcsup):
        """
        n = nombre de coefficients "a" à calculer
        fcxxx= fréquences de coupure
        """
        a_inf = fcinf / SR
        a_sup = fcsup / SR
        x = self.sinc(a_sup) - self.sinc(a_inf)
        #self.coeffs = np.concatenate((x[::-1],
        # np.array([2*(a_sup - a_inf)]), x))
        self.coeffs = self.construire_coeffs(x, a_sup - a_inf)
        return self.coeffs

    def coeffsCoupeBande(self, fcinf, fcsup):
        """
        n = nombre de coefficients "a" à calculer
        fcxx= fréquences de coupure
        """
        a_inf = fcinf / SR
        a_sup = fcsup / SR
        x = self.sinc(a_inf) - self.sinc(a_sup)
        #self.coeffs = np.concatenate((x[::-1], 2*(a_inf - a_sup) + 1., x))
        self.coeffs = self.construire_coeffs(x, a_inf - a_sup)
        return self.coeffs

    def precalculs(self, prony=None, nc=None):
        """
        effectue tous les calculs préalables
        """
        if nc:
            self.nc = nc
        if isinstance(prony, float):
            freq = prony2freq(prony)
            if self.genre in ["pb", "lp"]:
                self.coeffsPasseBas(freq)
            elif self.genre in ["ph", "hp"]:
                self.coeffsPasseHaut(freq)
        elif isinstance(prony, (tuple, list)):
            pronyinf, pronysup = prony
            freqinf = prony2freq(pronyinf)
            freqsup = prony2freq(pronysup)
            if self.genre in ["xb"]:
                self.coeffsCoupeBande(freqinf, freqsup)
            elif self.genre in ["bp"]:
                self.coeffsPasseBande(freqinf, freqsup)
        else:
            print("FiltreFixe Incohérent")
            return
        return self.coeffs

    def __call__(self, signal, prony=None, nc=None): #, premier=True):
        """
        effectue le filtrage du signal
        on peut accélérer en sachant que les coeffs sont déjà calculés
        (temps de calcul / 2 !!)
        mais la chose n'est pas encore au point
        CONFLIT : PRONY EST NECESSAIRE
        """
        return self.evt(signal, prony, nc)

    def evt(self, signal, prony=None, nc=None):
        """ effectue le filtrage du signal,
        prony (option) : hauteur de coupure
        nc (option): nombre de coefficients"""
        assert extremum(signal) > 0.0, "FiltreFixe.evt: signal == 0.0"
        if nc is None:
            nc = self.nc
        if prony is not None:
            self.precalculs(prony, nc)
        w = np.convolve(signal, self.coeffs)
        return w / extremum(w)

    def evtF(self, signal, freq):
        """ effectue le filtrage du signal
        freq: frequence de coupure"""
        if extremum(signal) == 0.0:
            print("FiltreFixe: signal nul")
            return signal
        self.precalculs(freq2prony(freq), self.nc)
        return np.convolve(signal, self.coeffs)

class FiltreFixeTemps(FiltreFixe):
    """
    une classe de filtres à fréquence de coupure fixes
    (passe-bas, passe-haut, passe-bande, coupe-bande)
    Le nombre de coefficients est donnée indépendamment
    de la 'SR'.
    """
    def __init__(self, genre, dureefiltre, prony=None):
        nc = int(dureefiltre * SR)
        FiltreFixe.__init__(genre, nc, prony)

#---------------------------------------------------------------
def filtregenerateur(duree, hauteur, alea, ncoeffs):
    """ un genre de pling
    ok, mais les timbres sont trop simples et peuvent être
    obtenus de manière plus économique."""
    n = int(duree * SR)
    nsamples = prony2samples(hauteur)
    freq = prony2freq(hauteur)
    a_sup = freq / SR
    x = sinc(a_sup, ncoeffs)
    coeffs = construire_coeffs(x, 2 * a_sup)
    ncoeffs = coeffs.size
    k = coeffs.sum()
    coeffs /= k # pour que le vecteur garde son niveau
    #print(coeffs, coeffs.sum())
    y = np.zeros(ncoeffs + n + 1)
    y[ncoeffs:nsamples+ncoeffs] = alea.uniform(-1.0, +1.0, nsamples)
    n0 = ncoeffs + nsamples
    n1 = n0 + n
    for i in range(n0, n1):
        try:
            v = y[i-nsamples:i+ncoeffs-nsamples] * coeffs

        except ValueError:
            break
        try:
            y[i] = v.sum()
        except IndexError:
            break
    return y[n0:]

def filtreinsitu(y, nini, nfin, hauteurs, ncoeffs):
    """ effectue un filtrage in situ sur le signal;
    y : le signal
    nini, nfin : index de début de fin
    hauteurs : hauteur, fixe ou vecteur ou profil
    ncoeffs : nombre de coefficients, fixe ou variable """
    if isinstance(hauteurs, float) and isinstance(ncoeffs, int):
        return filtreinsitufixe(y, nini, nfin, hauteurs, ncoeffs)
    else:
        print("TypeError:filtreinsitu: revenez plus tard")

def filtreinsitufixe(y, nini, nfin, freq, ncoeffs):
    """ comme filtreinsitumultiforme mais freq
    et ncoeffs fixes """
    afreq = freq / SR
    x = sinc(afreq, ncoeffs)
    coeffs = construire_coeffs(x, 2 * afreq)
    nfin = min(nfin, y.size - ncoeffs)
    for i in range(nini, nfin):
        y[i] = y[i:i+ncoeffs] * coeffs
    return y

def filtreinsituvecteur(y, nini, nfin, vfreq, ncoeffs):
    """ comme filtreinsitumultiforme mais freq
    et ncoeffs fixes """
    afreq = vfreq / SR
    x = sinc(afreq, ncoeffs)
    coeffs = construire_coeffs(x, 2 * afreq)
    nfin = min(nfin, y.size - ncoeffs)
    for i in range(nini, nfin):
        y[i] = y[i:i+ncoeffs] * coeffs
    return y


def filtrePBvar(signal, genre, pronyP, ncP):
    """ filtre le signal soit en passe-bas (genre=="b")
    soit en passe-haut (genre="h") la fréquence d'accord
    variant selon le profil de hauteur 'pronyP' et le
    nombre de coefficients selon le profil 'ncP'
    """
    def enleverzeros(w):
        " enlève les zéros inutiles"
        i = 0
        while w[i] == 0.0:
            i += 1
        return w[i:]

    n = signal.size
    vnc = ProfilBase(ncP).samples(n)
    vnc = vnc.astype(int)
    vfreq = ProfilBase(pronyP).samples(n)
    vfreq = prony2freq(vfreq) / SR
    ncmax = vnc.max()
    x = np.concatenate(np.zeros(ncmax), signal, np.zeros(ncmax))
    y = np.zeros(x.size)
    nsignal = np.arange(ncmax, signal.size+ncmax)
    if genre == "b":
        for i, asup, nc in zip(nsignal, vfreq, vnc):
            xsinc = sinc(asup, nc)
            coeffs = construire_coeffs(xsinc, 2*asup)
            y[i] = np.cumsum(x[i+ncmax:i+ncmax+nc] * coeffs)
    elif genre == "h":
        for i, asup, nc in zip(nsignal, vfreq, vnc):
            xsinc = -sinc(asup, nc)
            coeffs = construire_coeffs(xsinc, 2*asup)
            y[i] = np.cumsum(x[i+ncmax:i+ncmax+nc] * coeffs)
    else:
        return None
    return enleverzeros(y)
##FIN
class FiltreFixeMulti(FiltreFixe):
    """
    classe très expérimentale
    """
    def __init__(self, nc):
        """
        'nc' : nombre de coefficients
        Le nombre final de coefficients est 'nc*2 + 1'.
        le fenêtrage peut se faire par un profil.
        voir Tisserand p. 180
        """
        genre = 1 # ??
        FiltreFixe.__init__(self, genre, nc)
        self.nc = nc
        self.coeffs = None
        self.mcoeffs = None

    def calcul(self, P):
        """
        on peut concevoir un filtre constitué de différentes bandes
        avec la convention :
          genre == 1  : filtre passe-bas
          genre == -1 : filtre passe-haut
        """
        self.mcoeffs = np.zeros(self.nc*2+1, np.float64)
        sampli = 0.0
        for p in P:
            #print(p)
            prony, ampli, genre = p
            freq = prony2freq(prony)
            sampli += ampli
            if genre == 1:
                self.mcoeffs += self.coeffsPasseBas(freq) * ampli
            elif genre == -1:
                self.mcoeffs += self.coeffsPasseHaut(freq) * ampli
        self.mcoeffs /= sampli

    def bandes(self, signal, P):
        """
        ???
        """
        self.calcul(P)
        w = np.convolve(signal, self.mcoeffs)
        return w / extremum(w)

    def affiche(self, P=None):
        """
        afficher les données
        """
        #FiltreFixe.affiche() ???
        self.affiche()
        print("nc", self.nc, "->", 2*self.nc+1, "coeffs")
        if P:
            for p in P:
                print(p)
        print(self.mcoeffs)

class FiltreFixeFreq(OrigineStr):
    """ refonte de FiltreFixe pour une utilisation en fréquence
    semble être plus cohérent:
       pour changer de genre, on crée une nouvelle instance
       pour changer 'nc' ou 'freq': on utilise 'change' """
    def __init__(self, genre, nc, freq):
        """
        'duree' : durée qui détermine le nombre de coefficients
        'genre' : "pb", "lp" -> passe-bas
                  "ph", "hp" -> passe-haut
                  "xb" -> coupe-bande
                  "bp" -> passe-bande
                  "cr" -> croisé : passe-bande <-> coupe-bande
        nc est déterminé par la durée du filtre
        Le nombre final de coefficients est 'nc*2 + 1'.
        le fenêtrage peut se faire par un profil.
        prony : hauteur de la fréquence de filtrage
        """
        OrigineStr.__init__(self)
        self.genre = genre
        self.nc = nc
        self.coeffs = None
        self.freq = freq
        self.precalculs(freq)

    def sinc(self, a):
        "calcule les coefficients de base"
        k = np.arange(1., self.nc+1, 1.) * 2 * np.pi * a
        return 2*a*np.sin(k) / k

    def coeffsPasseBas(self, freq):
        """
        n = nombre de coefficients "a" à calculer
        fc= fréquence de coupure
        """
        a_sup = freq / SR
        x = self.sinc(a_sup)
        self.coeffs = construire_coeffs(x, 2*a_sup)
        return self.coeffs

    def coeffsPasseHaut(self, freq):
        """
        n = nombre de coefficients "a" à calculer
        fc= fréquence de coupure
        """
        a_inf = freq / SR
        x = -self.sinc(a_inf)
        #self.coeffs = np.concatenate((x[::-1], 1.0 - 2*a_inf, x))
        #self.coeffs = np.concatenate((x[::-1], np.array([1.0 - 2*a_inf]), x))
        self.coeffs = construire_coeffs(x, 1.0 - 2*a_inf)
        return self.coeffs

    def coeffsPasseBande(self, fcinf, fcsup):
        """
        n = nombre de coefficients "a" à calculer
        fcxxx= fréquences de coupure
        """
        a_inf = fcinf / SR
        a_sup = fcsup / SR
        x = self.sinc(a_sup) - self.sinc(a_inf)
        #self.coeffs = np.concatenate((x[::-1],
        # np.array([2*(a_sup - a_inf)]), x))
        self.coeffs = construire_coeffs(x, a_sup - a_inf)
        return self.coeffs

    def coeffsCoupeBande(self, fcinf, fcsup):
        """
        n = nombre de coefficients "a" à calculer
        fcxx= fréquences de coupure
        """
        a_inf = fcinf / SR
        a_sup = fcsup / SR
        x = self.sinc(a_inf) - self.sinc(a_sup)
        #self.coeffs = np.concatenate((x[::-1], 2*(a_inf - a_sup) + 1., x))
        self.coeffs = construire_coeffs(x, a_inf - a_sup)
        return self.coeffs

    def precalculs(self, freq):
        """
        effectue tous les calculs préalables
        """
        if isinstance(freq, float):
            if self.genre in ["pb", "lp"]:
                self.coeffsPasseBas(freq)
            elif self.genre in ["ph", "hp"]:
                self.coeffsPasseHaut(freq)
        elif isinstance(freq, (tuple, list)):
            freqinf, freqsup = freq
            if freqinf > freqsup:
                freqinf, freqsup = freqsup, freqinf
            if self.genre in ["xb"]:
                self.coeffsCoupeBande(freqinf, freqsup)
            elif self.genre in ["bp"]:
                self.coeffsPasseBande(freqinf, freqsup)
        else:
            print("FiltreFixeFreq.precalculs: Incohérence")
            print("type(freq)", type(freq), freq)
            print(self)
            return
        return self.coeffs

    def evt(self, signal):
        """ effectue le filtrage du signal """
        if extremum(signal) == 0.0:
            print("FiltreFixeFreq: signal nul")
            return signal
        w = np.convolve(signal, self.coeffs)
        try:
            return w / extremum(w)
        except ZeroDivisionError:
            print("FiltreFixe: le resultat est un vecteur nul")
            print("coeffs", self.coeffs)
            print("min, max, extremum", w.min(), w.max(), extremum(w))
            return w

    def change(self, nc=None, freq=None):
        """ pour changer 'nc' ou 'freq' """
        if nc is not None:
            self.nc = nc
        if freq is not None:
            self.freq = freq
        self.precalculs(self.freq)
