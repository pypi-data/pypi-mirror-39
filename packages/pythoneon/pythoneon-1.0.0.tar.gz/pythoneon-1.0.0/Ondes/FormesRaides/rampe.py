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
# Ondes/FormesRaides/rampe.py

"""
fournit des fonctions de nature logique-mathématique :
'rampe', 'triangle', 'rectangle', 'triangleA', 'rectangleA'
"""

import numpy as np
from samplerate import sr
from profilbase import ProfilBase
from origine import OrigineStr

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.03.06"

def saege0_debug(f, r, srlocale):
    """ construction d'une dent de scie
    f : fréquence; r : rapport (rampe_montante/période)"""
    dp = 1.0 / f
    print("période", dp)
    nm = int(dp * r * srlocale)
    if nm == 0:
        nm = 1
    nd = int(dp * (1.0 - r) * srlocale)
    if nd == 0:
        nd = 1
    print("période", dp, nm, nd)
    am = np.arange(0.0, 2.0, 2.0 / nm)
    print(am)
    ad = np.arange(2.0, 0.0, -2.0 / nd)
    print(ad)
    return np.concatenate((am, ad))

def saege0(f, r, srlocale=sr):
    """ construction d'une dent de scie isolée
    f : fréquence
    r : rapport (rampe_montante/période)"""
    dp = 1.0 / f
    nm = int(dp * r * srlocale)
    if nm == 0:
        nm = 1
    nd = int(dp * (1.0 - r) * srlocale)
    if nd == 0:
        nd = 1
    am = np.arange(0.0, 2.0, 2.0 / nm)
    ad = np.arange(2.0, 0.0, -2.0 / nd)
    return np.concatenate((am, ad))

def saegeF(duree, freq, ratio, srlocale=sr):
    """ fréquence et ratio fixe """
    ncycles = int(duree * freq)
    w0 = saege0(freq, ratio, srlocale) - 1.0
    r = [w0 for _ in range(ncycles)]
    return np.concatenate(r)

def saegeV(vfreq, vratio, srlocale=sr):
    """ une dent de scie variable en fréquence et en ratio
    Il est préférable que srlocale soit un multiple de sr """
    if vfreq.size != vratio.size:
        print("saegeV(vfreq.size != vratio.size)")
        return
    print("vfreq", vfreq.size, "vratio", vratio.size)
    r = [saege0(freq, ratio, srlocale) for freq, ratio in zip(vfreq, vratio)]
    #print(len(r))
    w = np.concatenate(r)
    #print(w.size, w.size / srlocale)

    if sr != srlocale:
        ix = np.arange(0, w.size, srlocale/sr)
        return w[ix] - 1.0
    else:
        return w - 1.0

def saegez(duree0, pfreq, pratio, srlocale=sr, erreur=0.001):
    """ la fonction utilisable; voir v0-saegez
    Pour limiter le bruit de quantification, on utilise une
    sr locale qui est normalement un multiple de la sr"""
    dureex = 0.0
    duree = duree0
    bmauvais = True
    ncycle = 0
    while bmauvais:
        vfreq = ProfilBase(pfreq).temps(duree)
        vtemps = 1.0 / vfreq
        dureex = vtemps.sum()
        if dureex == duree0:
            bmauvais = False
        elif dureex > duree0:
            duree *= duree0 / dureex
            #duree -= erreur / 2 # mauvais
        elif dureex > duree0:
            duree *= dureex / duree0
            #duree += erreur / 2
        #coeff = dureex / duree0
        if abs(duree0 - dureex) <= erreur:
            bmauvais = False
        if ncycle >= 5:
            bmauvais = False
        print("->", dureex, duree, duree0, abs(duree0 - dureex))
        ncycle += 1
    ncontrole = int(duree0 * sr)
    print("K", ncontrole, "vfreq.size:", vfreq.size,
          "diff", ncontrole - vfreq.size)
    try:
        vratio = ProfilBase(pratio).samples(vfreq.size)
    except MemoryError:
        print("MemoryError", vfreq.size)
        return
    print("saegez.vratio", vratio.size)
    w = saegeV(vfreq, vratio, srlocale)
    print(float(w.size / float(sr)))
    print(("je quitte saegez"))
    return w

def rampe(freq, t): # OK
    """ rampe élémentaire entre -1 et +1
    Ne convient pas pour les sons glissés. """
    return ((2 * freq * t) % 2.0) - 1.0

def rampeV(vfreq): # OK
    """ rampe en son glissé
    vfreq : vecteur de la variation de fréquence """
    vdy = vfreq / sr
    n = vfreq.size
    w = np.zeros(n)
    for i in range(1, n):
        w[i] = w[i-1] + vdy[i]
    return (w % 2.0) - 1.0

class RampeV(OrigineStr):
    "forme c. de rampeV "
    def __init__(self):
        OrigineStr.__init__(self)

    def evt(self, vfreq):
        " une rampe selon vfreq "
        vdy = vfreq / sr
        n = vfreq.size
        w = np.zeros(n)
        for i in range(1, n):
            w[i] = w[i-1] + vdy[i]
        return (w % 2.0) - 1.0

def triangle(freq, t): # OK
    " triangle élémentaire entre -1 et +1 "
    x = ((2 * freq * t) % 2.0)
    return 2 * ((x * (x < 1.0)) + ((2.0 - x) * (x > 1.0))) - 1.0

def rectangle(freq, t): # OK
    " rectangle élémentaire entre -1 et +1 "
    x = 2 * ((2 * freq * t) % 2.0) - 1.0
    return 1.0 * (x < 1.0) - 1.0 * (x > 1.0)

def rectangleA(freq, t, amod): # OK
    """ rectangle asymétrique variable entre -1 et +1
    """
    x = 2 * ((2 * freq * t) % 2.0) - 1.0
    return 1.0 * (x < amod) - 1.0 * (x > amod)

def triangleA(freq, t, amod): # OK
    """ triangle asymétrique variable entre -1 et +1
    """
    x = ((2 * freq * t) % 2.0)
    return 2 * ((x * (x < amod)) + ((2.0 - x) * (x > amod))) - 1.0

#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
