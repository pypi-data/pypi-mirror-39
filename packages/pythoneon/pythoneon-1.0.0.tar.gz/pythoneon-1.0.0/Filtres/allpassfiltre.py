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
# allpassfiltre.py
"""
On peut essayer de déduire ces filtres de la
classe FiltrePeigneGeneral dans fpeigne.py

Comb-filters ou filtres en peigne d'après Julius O. Smith
Allpass_Two_Combs.html

y[i] = b0 * x[i] - a1 * y[i-M]
M = nombre d'annulations entre 0 Hz et sr Hz

b: fraction de signal direct
a: réinjection

y[i] = b0 * x[i] + a1 * y[i-M]
M = nombre d'accentuations entre 0 Hz et sr Hz

a = abs(a)

NB: faire une initiation avec largeur de bande en midi

Cas général:
y[i] = b0 * signal[i] + b1 * signal[i-M] - a1 * y[i-M]
voir fpeigne.py

Allpass Filter:
b1 = 1
y[i] = b0 * signal[i] + signal[i-M] - a1 * y[i-M]
y[i] = g * signal[i] + signal[i-M] - g * y[i-M]

Feedback Comb Filter: FBC_Filter (récursif)
b1 = 0
y[i] = b0 * signal[i] - a1 * y[i-M]

Feedforward Comb Filter: FWC_Filter (non récursif)
a = 0
y[i] = b0 * signal[i] + b1 * signal[i-M]
ce cas peut être traité non récursivement par
y = b0 * x
y[M:] = b1 * x[:-M]
Autres cas:
b0 = 0

"""
import numpy as np
from samplerate import SR
from conversions import prony2freq, extremum, prony2samples
from Profils.profilbase import ProfilBase
from Profils.profil08 import Profil08
from origine import OrigineStr

__author__ = "Copyright (c) 2005 René Bastian (Wissembourg, FRANCE)"
__date__ = "2006.01.31, 06.08.29, 09.10.04, 2010.12.13"

#__all__ = ["FiltrePeigne", "FiltrePeigneM", "FiltrePeigneF", "CombFilter"]

class AllpassFilter(OrigineStr):
    """ classe installant un 'allpassfilter'
    cette classe est peu utilisée directement """
    def __init__(self, m, a, b0=1.0):
        " "
        OrigineStr.__init__(self)
        self.a = a
        self.b0 = b0
        self.m = m

    def filtrer(self, signal):
        "application du filtre"
        if self.b0 == 1.0:
            self.filtrerdirect(signal)
        n = signal.size + self.m + 1
        b0 = self.b0
        a = self.a
        m = self.m
        y = np.zeros(n)
        for i in range(m):
            y[i] = b0 * signal[i]
        for i in range(m, n-m):
            try:
                y[i] = b0 * signal[i] + signal[i-m] - a * y[i-m]
            except IndexError:
                print("AllpassFilter:filtrer:IndexError", i, i-m)
        for i in range(n-m, n):
            y[i] = -a * y[i-m]
        return y

    def filtrerdirect(self, signal):
        " application du filtre avec b0=1.0 "
        n = signal.size + self.m + 1
        a = self.a
        m = self.m
        y = np.zeros(n)
        for i in range(m):
            y[i] = signal[i]
        for i in range(m, n-m):
            try:
                y[i] = signal[i] + signal[i-m] - a * y[i-m]
            except IndexError:
                print("AllpassFilter:filtrer:IndexError", i, i-m)
        for i in range(n-m, n):
            y[i] = -a * y[i-m]
        return y

    def change(self, m=None, a=None, b0=None):
        " pour changer les attributs "
        if m:
            self.m = m
        if a:
            self.a = a
        if b0:
            self.b0 = b0

class CombFilter(OrigineStr):
    """
    Les fréquences 'fa' accentuées sont telles que
    'fa = i*SR / m for i in range(0, m)'
    'm': nombre de bandes
    'a': coefficient
    'b0': 0. < 'b0' < 1.
    si b0 == a: on obtient un allpass
    """
    def __init__(self, m, a, b0=1.0):
        " "
        OrigineStr.__init__(self)
        self.a = a
        self.b0 = b0
        self.m = m

    def __str__(self):
        s = "a:%7.5f b0:%7.5f m :%5i" % (self.a, self.b0, self.m)
        H = [i*SR/self.m for i in range(self.m)]
        print(H)
        return s

    def filtrer(self, signal):
        "application du filtre"
        if self.b0 == 1.:
            return self._direct(signal)
        n = signal.size + self.m + 1
        b0 = self.b0
        a = self.a
        m = self.m
        y = np.zeros(n)
        for i in range(m):
            y[i] = b0 * signal[i]
        for i in range(m, n-m):
            try:
                y[i] = b0 * signal[i] + signal[i-m] - a * y[i-m]
            except IndexError:
                print("CombFilter:filtrer:IndexError i", i, "i-m", i-m)
                break
        for i in range(n-m, n):
            y[i] = -a * y[i-m]
        return y / extremum(y)

    def _direct(self, signal):
        "application du filtre avec b0 == 1."
        n = signal.size + self.m
        a = self.a
        m = self.m
        y = np.zeros(n)
        y[:m] = signal[:m]
        for i in range(m, n-m):
            y[i] = signal[i] - a * y[i-m]
        for i in range(n-m, n):
            y[i] = -a * y[i-m]
        return y / extremum(y)

    def _direct_debug(self, signal):
        "application avec possib. de débogage du filtre avec b0 == 1."
        n = signal.size + self.m
        a = self.a
        m = self.m
        y = np.zeros(n)
        y[:m] = signal[:m]
        for i in range(m, n-m):
            try:
                bidon = signal[i]
            except IndexError:
                print("CombFilter:_direct:IndexError1: i ", i, "i-m", i-m)
                break
            try:
                bidon = y[i-m]
            except IndexError:
                print("CombFilter:_direct:IndexError2: i ", i, "i-m", i-m)
                #y[i] = signal[i] + signal[i-m] - a * y[i-m]
            try:
                y[i] = signal[i] - a * y[i-m]
            except IndexError:
                print("CombFilter:_direct:IndexError3: i ", i, "i-m", i-m)
                break
        for i in range(n-m, n):
            y[i] = -a * y[i-m]
        return y / extremum(y)

    def varia(self, signal, ProfilPronyVar, ProfilAVar=None):
        """
        application du filtre avec b0 == 1.
        'ProfilPronyVar': profil de variation de 'm'
        'ProfilAVar': profil de variation du coefficient de finesse
        """
        if ProfilAVar is not None:
            return self.varia2(signal, ProfilPronyVar, ProfilAVar)
        pmv = ProfilBase(ProfilPronyVar).samples(signal.size)
        pmv = prony2samples(pmv)
        pmvmax = pmv.max()
        n = signal.size + pmvmax
        #y = np.zeros(n, np.Float64)
        y = np.zeros(n)
        y[:pmvmax] = signal[:pmvmax]
        for i in range(pmvmax, n-pmvmax):
            try:
                y[i] = signal[i] + signal[i-self.m] - self.a * y[i-pmv[i]]
            except IndexError:
                pass
        for i in range(n-pmvmax, n):
            try:
                y[i] = -self.a * y[i-pmv[i]]
            except IndexError:
                pass
        return y / extremum(y)

    def varia2(self, signal, ProfilPronyVar, ProfilAVar):
        """
        Le filtre est appliqué avec b0 == 1.
        application du filtre avec b0 == 1.
        'ProfilPronyVar': profil de variation de 'm'
        'ProfilAVar': profil de variation du coefficient de finesse
        """
        pmv = ProfilBase(ProfilPronyVar).samples(signal.size)
        pmv = prony2samples(pmv)
        pmvmax = pmv.max()
        n = signal.size + pmvmax
        #y = np.zeros(n, np.Float64)
        y = np.zeros(n)
        y[:pmvmax] = signal[:pmvmax]
        a = ProfilBase(ProfilAVar).samples(n)
        a /= -100.
        #print(a, len(a))
        for i in range(pmvmax, n-pmvmax):
            try:
                y[i] = signal[i] + signal[i-self.m] - a[i] * y[i-pmv[i]]
            except IndexError:
                pass
        for i in range(n-pmvmax, n):
            try:
                y[i] = -a[i] * y[i-pmv[i]]
            except IndexError:
                pass
        return y / extremum(y)

    def varia_analytique(self, signal, ProfilPronyVar):
        """
        application du filtre avec b0 == 1.
        Le retard 'm' varie selon 'ProfilPronyVar'

        On pourrait même varier 'a'.
        """
        print("a", self.a, self.a) # ????????)
        pmv = ProfilBase(ProfilPronyVar).samples(signal.size)
        pmv = prony2samples(pmv)
        pmvmax = pmv.max()
        n = signal.size + pmvmax #+ 1
        #y = np.zeros(n, np.Float64)
        y = np.zeros(n)
        y[:pmvmax] = signal[:pmvmax]
        for i in range(pmvmax, n-pmvmax):
            try:
                y[i] = signal[i] + signal[i-self.m] - self.a * y[i-pmv[i]]
            except IndexError:
                print("IndexError 1", i, i-self.m)
                ierror1 = i
                break
        ierror1 = 0
        for i in range(n-pmvmax, n):
            try:
                y[i] = -self.a * y[i-pmv[i]]
            except IndexError:
                print("IndexError 2", i, i-self.m)
                ierror2 = i
                break
        print("signal", signal.size, "y", len(y), "index", ierror1, ierror2)
        return y / extremum(y)

    def bande(self, i0, i1):
        """
        provisoire: concerne le combfiltre
        dans gnuplot: plot[0:1] 2*abs(cos(pi*x*m))
        """
        def v(t):
            "petite fonction calculant des coeffs"
            return 2 * abs(np.cos(np.pi * t * self.m))

        T = np.arange(0.0, 0.5, 1.0/SR)
        return v(T[i0:i1])

#    def trace(self, i0=0, i1=SR/2):
#        """
#        pour visualiser pas à pas
#        """
#        g = Gnuplot.Gnuplot()
#        g.title("Spectre")
#        g.plot(self.bande(i0, i1))
#        input("ENTER pour continuer"))
#        g.reset()

class FiltrePeigne(CombFilter):
    """
    classe pour une utilisation facile des classes de CombFilter
    """
    def __init__(self, prony, finesse, b0=1.0):
        """
        finesse: valeur en %
        prony: hauteur en prony
        """
        freq = prony2freq(prony)
        self.m = int(SR / freq)
        self.a = -finesse/100.0
        self.b0 = b0
        CombFilter.__init__(self, self.m, self.a, self.b0)

    def filtrer_analytique(self, signal):
        "application du filtre"
        n = signal.size + self.m + 1
        b0 = self.b0
        a = self.a
        m = self.m
        print("n %i b0 %f a %f m %i" % (n, b0, a, m))
        #y = np.zeros(n, np.Float64)
        y = np.zeros(n)
        for i in range(m):
            y[i] = b0 * signal[i]
        for i in range(m, n-m):
            try:
                y[i] = b0 * signal[i] + signal[i-m] - a * y[i-m]
            except IndexError:
                print("FiltrePeigne:filtrer_analytique:IndexError", i, i-m)

        for i in range(n-m, n):
            y[i] = -a * y[i-m]

        return y

    def evt(self, signal):
        "filtrer rapidement"
        if self.b0 == 1.0:
            return self._direct(signal)

class FiltrePeigneVecteur(OrigineStr):
    """
    autre version de filtre en peigne
    """
    def __init__(self):
        OrigineStr.__init__(self)

    def __call__(self, signal, Pronys, Finesses, b0=1.):
        """
        'signal', 'Pronys', 'Finesses' ont même longueur.
        b0 = 1 pourrait aussi être varié.
        """
        VM = prony2freq(Pronys)
        VM = SR / VM
        VM = VM.astype(np.int32)
        VA = -Finesses / 100.0
        Mmax = VM.max() # normalement, pas de VM_i négatifs
        n = signal.size + Mmax + 1
        y = np.zeros(n)
        for i in range(Mmax):
            y[i] = b0 * signal[i]
        for i in range(Mmax, n-Mmax):
            try:
                y[i] = b0 * signal[i] + signal[i-VM[i]] - VA[i] * y[i-VM[i]]
            except IndexError:
                print("IndexError")
                print("FiltrePeigne:vecteurs(1)", i, n, Mmax, signal.size)

        for i in range(n-Mmax, n):
            try:
                y[i] = -VA[i] * y[i-VM[i]]
            except IndexError:
                print("IndexError")
                print("FiltrePeigne:vecteurs(2):", i, n, Mmax, signal.size)
            return y
        return y

    def profils(self, varH, varFinesse):
        """ pas de variation de b0 """
        pass

    def _profils(self, signal, Pronys, Finesses, b0=1.):
        """
        'signal', 'Pronys', 'Finesses' ont même longueur.
        b0 = 1 pourrait aussi être varié.
        """
        VM = Profil08(Pronys).samples(signal.size)
        VM = prony2freq(Pronys)
        VM = SR / VM
        VM = VM.astype(np.int32)
        n = signal.size + VM.max()
        VM = Profil08(Pronys).samples(n)
        VM = prony2freq(Pronys)
        VM = SR / VM
        VM = VM.astype(np.int32)

        VA = -Profil08(Finesses).samples(n) / 100.0

        Mmax = VM.max() # ????????????
        y = np.zeros(n)
        for i in range(Mmax):
            y[i] = b0 * signal[i]
        for i in range(Mmax, n-Mmax):
            try:
                y[i] = b0 * signal[i] + signal[i-VM[i]] - VA[i] * y[i-VM[i]]
            except IndexError:
                print("IndexError")
                print("FiltrePeigne:vecteurs(1):", i, n, Mmax, signal.size)
                break
        for i in range(n-Mmax, n):
            try:
                y[i] = -VA[i] * y[i-VM[i]]
            except IndexError:
                print("IndexError")
                print("FiltrePeigne:vecteurs(2):", i, n, Mmax, signal.size)
                return y
        return y

class FiltrePeigneM(CombFilter):
    """
    autre version de filtre en peigne
    """
    def __init__(self, prony=None, finesse=1., b0=1.0):
        """
        finesse: valeur en %
        prony: hauteur en prony
        """
        if prony is not None:
            freq = prony2freq(prony)
            self.m = int(SR / freq)
        else:
            self.m = None
        self.a = -finesse/100.0
        self.b0 = b0
        CombFilter.__init__(self, self.m, self.a)

class FiltrePeigneF(CombFilter):
    """
    autre version de filtre en peigne
    """
    def __init__(self, freq, finesse, b0=1.0):
        """
        finesse: valeur en %
        freq: hauteur en fréquence
        """
        self.m = int(SR / freq)
        self.a = -finesse/100.0
        self.b0 = b0
        CombFilter.__init__(self, self.m, self.a)

