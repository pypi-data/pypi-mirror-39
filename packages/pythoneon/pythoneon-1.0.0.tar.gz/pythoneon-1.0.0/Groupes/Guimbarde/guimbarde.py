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
# Groupes/Guimbarde/guimbarde.py

"""
fournit
   la classe Guimbarde
   constrLAFpile(freq, n)
"""
import numpy as np

from origine import OrigineStr
from samplerate import SR
from conversions import extremum, prony2freq, freq2periode
from profils import recta
from profilbase import ProfilBase
from canal import CanalMono
from Ondes.pilesin import pileprofil

__author__ = "Copyright (c) 2005-09 René Bastian (Wissembourg, FRANCE)"
__date__ = "2007.07.26, 2009.03.24, 2012.10.23"

def constrLAFpile(freq, n):
    """
    construit une liste de 'n' tuples (ampli, env, freq)
    pour pilevariante ou pileprofil
    on pourrait classifier ...
    """
    duree = 1.
    r = []
    y1, y2 = 1., 0.5
    puiss1 = 0.5
    puiss2 = 1.
    puiss3 = 2.
    n = int(n)
    penv = [[recta, duree, 0., y1, puiss1],
            [recta, duree, y1, y2, puiss2],
            [recta, duree, y2, 0., puiss3]]
    for i in range(1, n+1):
        ampli = 1./i
        xfreq = i * freq
        pfreq = [[recta, duree, xfreq, xfreq]]
        r.append((ampli, penv, pfreq))
    return r

# ne pas expulser ce guimbepling ....
def guimbepling(amorce, duree, diviseur=2.5):
    "fabrique de guimbeplings"
    n = int(duree * SR)
    na = amorce.size
    w = np.zeros(n)
    w[:na] = amorce[:]
    for i in range(na, n):
        w[i] = (w[i-na] + w[i-na+1]) / diviseur
    return w

def guimbarde(microduree, listeFreq, n, ecart, nmicros):
    """
    'freq' : liste-profil de l'évolution de la Fréquence
    'n' : nombre de couches de la pile de fréquences
    'duree' : durée d'un micro-son
    'nmicros' : nombre de micro-sons
    n = 4
    freq = 116.
    microduree = 0.3
    ecart = 0.01
    """
    if isinstance(listeFreq, (list, tuple)):
        freqs = ProfilBase(listeFreq).samples(nmicros)
    elif isinstance(listeFreq, (float, int)):
        freqs = np.ones(nmicros, np.float64) * listeFreq
    c = CanalMono()
    pt = 0.0
    for freq in freqs:
        periode = freq2periode(freq)
        L = constrLAFpile(freq, n)
        amorce = pileprofil(L, periode)
        if microduree < periode:
            print(microduree, "<", periode)
        w = guimbepling(amorce, microduree)
        c.addT(pt, w)
        pt += ecart
    return c.a / extremum(c.a)

def guimbardeProny(microduree, listeProny, n, ecart, nmicros):
    """
    'listeProny' : liste-profil de l'évolution de la hauteur
    'n' : nombre de couches de la pile de fréquences
    'microduree' : durée d'un micro-son
    'nmicros' : nombre de microsons
    'ecart' : écart entre deux microsons
    'nmicros' : nombre de microsons
    """

    freqs = ProfilBase(listeProny).samples(nmicros)
    freqs = prony2freq(freqs)
    c = CanalMono()
    pt = 0.0
    for freq in freqs:
        periode = freq2periode(freq)
        L = constrLAFpile(freq, n)
        amorce = pileprofil(L, periode)
        if microduree < periode:
            print(microduree, "<", periode)
            boutmicro = periode / 10
        while True:
            try:
                w = guimbepling(amorce, microduree)
                break
            except ValueError:
                microduree += boutmicro
                print("Raccomoder guimbepling: microduree =", microduree)

        c.addT(pt, w)
        pt += ecart
    return c.a / extremum(c.a)

class Guimbarde(OrigineStr):
    "timbre ressemblant à une guimbarde, mais aussi cris de chouette"
    def __init__(self, n=4, microduree=0.3, ecart=0.01):
        """
        'n' : nombre de couches par constrLAFpile
        'microduree' : durée d'un microson
        'ecart' : ecart entre microsons
        """
        OrigineStr.__init__(self)
        self.n = n
        self.microduree = microduree
        self.ecart = ecart

    def change(self, n=None, microduree=None, ecart=None):
        " pour changer "
        if n is not None:
            self.n = n
        if microduree is not None:
            self.microduree = microduree
        if ecart is not None:
            self.ecart = ecart

    def evt(self, pFreq, n, ecart, nmicros):
        """
        'pFreq' : liste-profil de l'évolution de la Fréquence
        'n' : nombre de couches de la pile de fréquences
        'ecart' : micro-écart
        'duree' : durée d'un micro-son
        'nmicros' : nombre de micro-sons
        n = 4
        pFreq = 116.
        microduree = 0.3
        ecart = 0.01
        """
        if isinstance(pFreq, (list, tuple)):
            freqs = ProfilBase(pFreq).samples(nmicros)
        elif isinstance(pFreq, (float, int)):
            freqs = np.ones(nmicros, np.float64) * pFreq
        c = CanalMono()
        pt = 0.0
        for freq in freqs:
            periode = freq2periode(freq)
            L = constrLAFpile(freq, n)
            amorce = pileprofil(L, periode)
            if self.microduree < periode:
                print("Guimbarde:evt", self.microduree, "<", periode)
            w = guimbepling(amorce, self.microduree)
            c.addT(pt, w)
            pt += ecart
        return c.a / extremum(c.a)

    def evtE(self, pfreq, n, pecart, nmicros):
        """
        'pfreq' : liste-profil de l'évolution de la Fréquence
        'n' : nombre de couches de la pile de fréquences
        'pecart' : profil de la variation des micro-écarts
        'duree' : durée d'un micro-son
        'nmicros' : nombre de micro-sons
        n = 4; freq = 116.; microduree = 0.3; ecart = 0.01
        """
        if isinstance(pfreq, (list, tuple)):
            freqs = ProfilBase(pfreq).samples(nmicros)
        elif isinstance(pfreq, (float, int)):
            freqs = np.ones(nmicros, np.float64) * pfreq
        vecart = ProfilBase(pecart).samples(nmicros)
        c = CanalMono()
        pt = 0.0
        for ecart, freq in zip(vecart, freqs):
            periode = freq2periode(freq)
            L = constrLAFpile(freq, n)
            amorce = pileprofil(L, periode)
            if self.microduree < periode:
                print(self.microduree, "<", periode)
            w = guimbepling(amorce, self.microduree)
            c.addT(pt, w)
            pt += ecart
        return c.a / extremum(c.a)

    def evtProny(self, listeProny, n, ecart, nmicros):
        """
        'listeProny' : liste-profil de l'évolution de la hauteur
        'n' : nombre de couches de la pile de fréquences
        'microduree' : durée d'un micro-son
        'nmicros' : nombre de microsons
        'ecart' : écart entre deux microsons
        """
        freqs = ProfilBase(listeProny).samples(nmicros)
        freqs = prony2freq(freqs)
        c = CanalMono()
        pt = 0.0
        for freq in freqs:
            periode = freq2periode(freq)
            L = constrLAFpile(freq, n)
            amorce = pileprofil(L, periode)
            if self.microduree < periode:
                print(self.microduree, "<", periode)
                boutmicro = periode / 10
            while True:
                try:
                    w = guimbepling(amorce, self.microduree)
                    break
                except ValueError:
                    self.microduree += boutmicro
                    warn = "Raccomoder guimbepling: microduree ="
                    print(warn, self.microduree)

            c.addT(pt, w)
            pt += ecart
        return c.a / extremum(c.a)

    @staticmethod
    def evtProny2(microduree, listeProny, n, ecart, nmicros):
        """
        COMPORTEMENT HASARDEUX CAR microduree RISQUE D'ÊTRE TROP COURT
        microduree : durée d'un microélément
        'listeProny' : liste-profil de l'évolution de la hauteur
        'n' : nombre de couches de la pile de fréquences
        'microduree' : durée d'un micro-son
        'nmicros' : nombre de microsons
        'ecart' : écart entre deux microsons
        'nmicros' : nombre de microsons
        """
        freqs = ProfilBase(listeProny).samples(nmicros)
        freqs = prony2freq(freqs)
        c = CanalMono()
        pt = 0.0
        for freq in freqs:
            periode = freq2periode(freq)
            L = constrLAFpile(freq, n)
            amorce = pileprofil(L, periode)
            if microduree < periode:
                microduree = periode * 1.1
            w = guimbepling(amorce, microduree)
            c.addT(pt, w)
            pt += ecart
        return c.a / extremum(c.a)

    def double(self, freq, pecarts, nmicros):
        """
        'freq' : liste-profil de l'évolution de la Fréquence
        'pecarts' : liste-profil de l'évolution des ecarts
        'nmicros' : nombre de micro-sons
        """
        if isinstance(freq, (list, tuple)):
            freqs = ProfilBase(freq).samples(nmicros)
        elif isinstance(freq, (float, int)):
            freqs = np.ones(nmicros, np.float64)*freq
        if isinstance(pecarts, (list, tuple)):
            ecarts = ProfilBase(pecarts).samples(nmicros)
        elif isinstance(pecarts, (float, int)):
            ecarts = np.ones(nmicros, np.float64)*freq

        c = CanalMono()
        pt = 0.0
        for freq, ecart in zip(freqs, ecarts):
            periode = freq2periode(freq)
            L = constrLAFpile(freq, self.n)
            amorce = pileprofil(L, periode)
            w = guimbepling(amorce, self.microduree)
            c.addT(pt, w)
            pt += ecart
        return c.a / extremum(c.a)

    def alea(self, freq, vecarts, nmicros):
        """
        'freq' : liste-profil de l'évolution de la Fréquence
        'pecarts' : liste-profil de l'évolution des ecarts
        'nmicros' : nombre de micro-sons
        """
        if isinstance(freq, (list, tuple)):
            freqs = ProfilBase(freq).samples(nmicros)
        elif isinstance(freq, (float, int)):
            freqs = np.ones(nmicros, np.float64) * freq

        c = CanalMono()
        pt = 0.0
        for freq, ecart in zip(freqs, vecarts):
            periode = freq2periode(freq)
            L = constrLAFpile(freq, self.n)
            amorce = pileprofil(L, periode)
            w = guimbepling(amorce, self.microduree)
            c.addT(pt, w)
            pt += ecart
        #return c.a / extremum(c.a)
        return c.brut() / extremum(c.brut())

    def __call__(self, duree, Prony):
        """
        'duree' : durée de l'évènement
        'Prony' : évolution de la hauteur
        """
        nmicros = int(duree/self.ecart) + 1
        if isinstance(Prony, (list, tuple)):
            freqs = ProfilBase(Prony).samples(nmicros)
            freqs = prony2freq(freqs)
        elif isinstance(Prony, (float, int)):
            freqs = np.ones(nmicros, np.float64)*Prony
            freqs = prony2freq(freqs)

        c = CanalMono()
        pt = 0.
        for freq in freqs:
            periode = freq2periode(freq)
            L = constrLAFpile(freq, self.n)
            amorce = pileprofil(L, periode)
            w = guimbepling(amorce, self.microduree)
            c.addT(pt, w)
            pt += self.ecart
        return c.a / extremum(c.a)

class GuimbardeC(Guimbarde):
    "autre essai de guimbarde"
    def __init__(self, alea):
        """
        Le son est assez bruité - par l'instabilité sérielle des
        profils ??
        on pourrait :
        -- fournir une fonction telle que fonction(amorce, duree)
           donne le micro-son : ex.
        -- fournir une fonction de superposition des piles
        """
        Guimbarde.__init__(self)
        self.alea = alea

    def _constrLAFpile(self, freq, n):
        """
        construit une liste de (ampli, env, freq) pour pilevariante
        pourrait être remplacé par qq chose de plus complexe.
        """
        duree = 1.
        LAF = []
        y1 = self.alea.uniform(0.1, 1.)
        y2 = self.alea.uniform(0.1, 1.)
        puiss1 = self.alea.uniform(0.5, 2.)
        puiss2 = self.alea.uniform(0.5, 2.)
        puiss3 = self.alea.uniform(0.5, 2.)
        for i in range(n):
            ampli = 1./(i+1)
            penv = [[recta, duree, 0., y1, puiss1],
                    [recta, duree, y1, y2, puiss2],
                    [recta, duree, y2, 0., puiss3]
                   ]
            xfreq = (i+1)*freq
            pfreq = [[recta, duree, xfreq, xfreq]]
            LAF.append((ampli, penv, pfreq))
        return LAF

    def __call__(self, duree, prony):
        pass
