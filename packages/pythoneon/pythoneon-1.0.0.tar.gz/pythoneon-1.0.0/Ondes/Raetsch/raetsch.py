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
# raetsch.py
##DEBUT
"""
fournit la classe Raetsch
"""

import numpy as np
from samplerate import SR
from conversions import (extremum, freq2periode)
from profilbase import ProfilBase
import canal
from profils import recta
#from guimbarde09 import constrLAFpile
from Ondes.pilesin import pileprofil

__author__ = "Copyright (c) 2011 René Bastian (Wissembourg, FRANCE)"
__date__ = "2011.03.28"

def constrLAFpile(freq, n):
    """
    construit la liste des (ampli, env, freq) pour pilevariante
    """
    duree = 1.
    LAF = []
    y1, y2 = 1., 0.5
    puiss1 = 0.5
    puiss2 = 1.
    puiss3 = 2.
    n = int(n)
    penv = [[recta, duree, 0., y1, puiss1],
            [recta, duree, y1, y2, puiss2],
            [recta, duree, y2, 0., puiss3]]
    for i in range(n):
        ampli = 1./(i+1)
        xfreq = (i+1)*freq
        pfreq = [[recta, duree, xfreq, xfreq]]
        LAF.append((ampli, penv, pfreq))
    return LAF

def plingraetsch(amorce, duree, diviseur=2.5):
    "fabrique des plings"
    n = int(duree * SR)
    na = len(amorce)
    w = np.zeros(n)
    w[:na] = amorce[:]
    for i in range(na, n):
        w[i] = (w[i-na] + w[i-na+1]) / diviseur
    return w

class Raetsch(object):
    """ un timbre dérivé de 'Guimbarde' """
    def __init__(self):
        self.varh = None
        self.varnpile = None
        self.varmicro = None
        self.varecarts = None

    def __str__(self):
        """ affiche presque tout."""
        try:
            n = max([len(str(x)) for x in self.__dict__])
            xformat = "%-" + str(n) + "s : %s \n"
        except ValueError:
            print("Raetsch(object):__str__ (1)")
        R = [self.__class__.__name__+"\n"]
        try:
            for x in self.__dict__:
                s = xformat % (str(x), self.__dict__[x])
                R.append(s)
        except ValueError:
            print("Raetsch(object):__str__ (2)")
        if self.varh is None:
            print("varh non défini")
        if self.varnpile is None:
            print("varnpile non défini")
        if self.varmicro is None:
            print("varmicro non défini")
        if self.varecarts is None:
            print("varmicro non défini")
        s = "".join(R)
        print(s)

    def evt(self, duree, varecarts=None, varh=None,
            varnpile=None, varmicro=None, info=False):
        """un timbre de sarrussophone, de guimbarde, de raetsch.
        varecarts : liste-profil des ecarts entre les micro-évts
        varh : liste-profil de la variation des hauteurs
        varnpile : liste-profil de la variation des épaisseurs de la pile
        varmicro : liste-profil de la variation des microdurées
        """
        if varh:
            self.varh = varh
        else:
            varh = self.varh
        if varnpile:
            self.varnpile = varnpile
        else:
            varnpile = self.varnpile
        if varmicro:
            self.varmicro = varmicro
        else:
            varmicro = self.varmicro
        if varecarts:
            self.varecarts = varecarts
        else:
            varecarts = self.varecarts
        xn = int(duree * SR)
        ecarts = ProfilBase(varecarts).samples(xn)
        dureeprov = sum(ecarts)
        xn = int(xn * (duree / dureeprov))
        ecarts = ProfilBase(varecarts).samples(xn)
        n = len(ecarts)
        freqs = ProfilBase(varh).samples(n)
        ecarts = ProfilBase(varecarts).samples(n)
        npiles = ProfilBase(varnpile).samples(n)
        npiles = npiles.astype(np.int32)
        micros = ProfilBase(varmicro).samples(n)
        c = canal.CanalMono()
        pt = 0.0
        for freq, ecart, npile, microduree in zip(freqs, ecarts, \
    					          npiles, micros):
            periode = freq2periode(freq)
            L = constrLAFpile(freq, npile)
            amorce = pileprofil(L, periode)
            if (microduree < periode) and info:
                print(microduree, "<", periode)
            w = plingraetsch(amorce, microduree)
            c.addT(pt, w)
            pt += ecart
        return c.a / extremum(c.a)

    def change(self, varecarts=None, varh=None,
               varnpile=None, varmicro=None):
        " pour changer les attributs "
        if varh:
            self.varh = varh,
        if varnpile:
            self.varnpile = varnpile
        if varmicro:
            self.varmicro = varmicro
        if varecarts:
            self.varecarts = varecarts



