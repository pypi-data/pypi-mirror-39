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
# Bruits/bruitstruct.py

"""
fournir un bruit contrôlé en fréquence par sa constitution au lieu
d'être contrôlé par un filtre
"""

import numpy as np

from samplerate import sr
from conversions import (prony2freq, extremum)
from profilbase import ProfilBase
from profils import recta
from canal import CanalMono
from ondepartable import ondeTable
from serie import Serie002
from origine import OrigineStr
from Outils.ajuster import prolongerN
from filtrefixe import FiltreFixeFreq
from Structures.Vibrer.vibrato import vibratoAleatoire

__author__ = "Copyright (c) 2013 René Bastian (Wissembourg, FRANCE)"
__date__ = "2013.03.07"

def sonido11_bs(choix, duree, freq, rvibrato, alea, pfreq, ratio):
    """construction d'un son
    _bs -> bruit structuré
    mais le bruit uniform est remplacé par un bruit structuré"""
    n = int(duree * sr)
    vvib = vibratoAleatoire(duree, alea, rvibrato,
                            maxfreqvib=6.0, dtmin=0.05, dtmax=0.2)
    vfreq = ProfilBase(pfreq).samples(n)
    vfreq += vvib
    if choix == 1:
        ve = Serie002(631, 137).uniform(-1.0, +1.0, n)
#    elif choix == 2:
#        ve = excitat(duree)
#    elif choix == 3:
#        vx, vy = gumowski_mira0(0.5, 0.008, 0.0, 0.5, int(duree * sr))
#        ninterpol = 16
#        dim = vx.size / ninterpol
#        ve = interpoler(vx[:dim], ninterpol)
    freqbasse, freqhaute = 100.0, 4000.0
    filtreB = FiltreFixeFreq("pb", 120, freqhaute)
    filtreH = FiltreFixeFreq("ph", 120, freqbasse)
    freq *= ratio
    if vfreq[0] < freqbasse:
        filtreB.change(freq=vfreq[0])
        #vef = filtreB.evt(ve)
        filtreB.change(freq=freqhaute)
        vw = violonfluct0(duree, ve, vfreq * freq, ratio)
    else:
        vw = violonfluct0(duree, ve, vfreq * freq, ratio)
    vw /= extremum(vw)
    filtreH.change(freq=vfreq[0])
    vw = filtreH.evt(vw)
    vw /= extremum(vw)
    return vw

def violonfluct0(duree, vexcit, vfreq, ratio):
    """
    'vexcit' : un arroi utilisé comme excitateur des filtres
             (p. ex. un bruit)
    'vfreq' : l'arroi de la variation de fréquence
    'ratio' : une fraction de vfreq"""
    if vexcit.size != vfreq.size:
        vexcit, vfreq = prolongerN((vexcit, vfreq))
    vn = sr / vfreq
    vd = vn * ratio
    n = int(duree * sr)
    gd = vn.max()
    w = np.zeros(n + int(gd))
    for i in range(int(gd), n):
        w[i] = vexcit[int(i - vn[i])] - vexcit[i] + w[int(i - vd[i])]
    return w

def aff(p):
    " pour afficher "
    for pp in p:
        print(pp)

class AccumulOndes(OrigineStr):
    """ construire une accumulation d'ondes """
    def __init__(self, pprofil, alea=None, table=None):
        """ """
        OrigineStr.__init__(self)
        self.pprofil = pprofil
        if alea is None:
            self.alea = Serie002(2057, 7205)
        else:
            self.alea = alea
        if table is None:
            table = [[recta, 0.25, 0.0, 1.0],
                     [recta, 0.50, 1.0, -1.0],
                     [recta, 0.25, -1.0, 0.0]]
        self.table = ProfilBase(table).samples(sr)

    def evtHaufen(self, duree, n, hinf, hsup, amplinf, amplsup):
        """ construit une accumulation sérielle
        hinf, hsup : Pronys"""
        c = CanalMono(duree)
        vf = self.alea.uniform(hinf, hsup, n)
        vf = prony2freq(vf)
        va = self.alea.uniform(amplinf, amplsup, n)
        vp0 = ProfilBase(self.pprofil).temps(duree)
        for freq, ampli in zip(vf, va):
            #print(freq)
            vp = vp0 * freq
            w = ondeTable(self.table, vp)
            w *= ampli
            c.addT(0.0, w)
        return c.a

    def evtScala(self, duree, n, hinf, hsup, amplinf, amplsup):
        """ construit une accumulation progressive
        hinf, hsup : Pronys"""
        c = CanalMono(duree)
        vf = np.linspace(hinf, hsup, n)
        vf = prony2freq(vf)
        va = self.alea.uniform(amplinf, amplsup, n)
        vp0 = ProfilBase(self.pprofil).temps(duree)
        for freq, ampli in zip(vf, va):
            #print(freq)
            vp = vp0 * freq
            w = ondeTable(self.table, vp)
            w *= ampli
            c.addT(0.0, w)
        return c.a

    def change(self, pprofil):
        " change les attributs "
        self.pprofil = pprofil
