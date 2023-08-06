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
# Groupes/croasses.py

""" le timbre Croasse est dérivé de Guimbarde
"""

import numpy as np

from samplerate import sr
from conversions import (prony2freq, extremum, freq2periode)
from profilbase import ProfilBase
from canal import (CanalMono)
from origine import OrigineStr
from Ondes.FormesRaides.rampe import saegeF
from Ondes.pilesin import pileprofil
from Structures.Empilements.empiler import (constrLAFpile1, constrLAFpile2)
# ou 2

__author__ = "Copyright (c) 2013 René Bastian (Wissembourg, FRANCE)"
__date__ = "2013.07.05"

def pling(amorce, duree, diviseur=2.5):
    "fabrique des plings"
    n = int(duree * sr)
    na = len(amorce)
    w = np.zeros(n)
    w[:na] = amorce[:]
    for i in range(na, n):
        w[i] = (w[i-na] + w[i-na+1]) / diviseur
    return w

class Croasse(OrigineStr):
    """ timbre ressemblant à une guimbarde, mais aussi cris de chouette;
    il utilise les fonctions 'pling' """
    def __init__(self, nepaisseur, dispersion,
                 microduree=1.0 / 10, rmicro=5, ratio=1.0):
        """ nepaisseur : nombre de fréquences au-dessus et en-dessous
        de la fréquence de base de l'événement;
        dispersion : intervalle en rapport de fréqu. par rapport à la
            fréquence centrale;
            si dispersion > 1.05 -> cluster de tons
            si dispersion ~ 1.02 -> interférances
        """
        OrigineStr.__init__(self)
        self.nepaisseur = nepaisseur
        self.dispersion = dispersion
        self.microduree = microduree
        self.rmicro = rmicro
        self.ratio = ratio

#def constrAmorce(self, freq0):
#    """ construction de l'amorce """
#    c, pt = CanalMono(), 0.0
#    w = saegeF(self.microduree, freq0, self.ratio)
#    c.addT(pt, w)
#    for i in range(1, self.nepaisseur + 1):
#        freq = freq0 * self.dispersion ** i)
#        w = saegeF(self.microduree, freq, self.ratio)
#        c.addT(pt, w)
#    for i in range(1, self.nepaisseur + 1):
#        #r.append(freq / self.dispersion ** i)
#    return c.ex()

    def constrAmorce(self, freq0):
        """ construction de l'amorce """
        ne = self.nepaisseur
        microd = self.microduree / self.rmicro
        if ne == 0:
            return saegeF(microd, freq0, self.ratio)
        else:
            freq = freq0 / self.dispersion ** ne
        c, pt = CanalMono(), 0.0
        for _ in range(2 * ne + 1):
            w = saegeF(microd, freq, self.ratio)
            c.addT(pt, w)
            freq *= self.dispersion
        return c.ex()

    def evt0(self, duree, freq0, pfreq, pecarts):
        """ evt. composite remplissant une durée 'duree'
        de microdurées variant selon 'pfreq' et espacés
        par des écarts variant selon 'pecarts'; l'onde
        résultante et enveloppée selon 'penv'.
        """
        c = CanalMono()
        vecarts = ProfilBase(pecarts).temps(duree)
        dx = vecarts.sum()
        #print("Durée avant", dx)
        vecarts = ProfilBase(pecarts).temps(duree * duree / dx)
        #print("Durée réelle", vecarts.sum(), "escomptée", duree )
        vfreqs = ProfilBase(pfreq).samples(vecarts.size) * freq0
        print(vecarts.size)
        pt = 0.0
        for freq, ecart in zip(vfreqs, vecarts):
            we = self.constrAmorce(freq)
            try:
                w = pling(we, self.microduree)
            except ValueError:
                continue
            c.addT(pt, w)
            pt += ecart
        return c.ex()

    @staticmethod
    def evtFreq(microduree, freqs, n, ecart, nmicros):
        """
        'freqs' : liste-profil de l'évolution de la Fréquence
        'n' : nombre de couches de la pile de fréquences
        'duree' : durée d'un micro-son
        'nmicros' : nombre de micro-sons
        n = 4
        freq = 116.
        microduree = 0.3
        ecart = 0.01
        """
        if isinstance(freqs, (list, tuple)):
            freqs = ProfilBase(freqs).samples(nmicros)
        elif isinstance(freqs, (float, int)):
            freqs = np.ones(nmicros, np.float64) * freqs
        c = CanalMono()
        pt = 0.0
        for freq in freqs:
            periode = freq2periode(freq)
            L = constrLAFpile1(freq, n) # ou 2
            amorce = pileprofil(L, periode)
            if microduree < periode:
                print(microduree, "<", periode)
            w = pling(amorce, microduree)
            c.addT(pt, w)
            pt += ecart
        return c.a / extremum(c.a)

    @staticmethod
    def evtProny(microduree, listeProny, n, ecart, nmicros):
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
            L = constrLAFpile2(freq, n) # ou 1
            amorce = pileprofil(L, periode)
            #self.plot(amorce)
            if microduree < periode:
                microduree = periode * 1.1
            w = pling(amorce, microduree)
            #self.plot(w)
            c.addT(pt, w)
            pt += ecart
        return c.a / extremum(c.a)
