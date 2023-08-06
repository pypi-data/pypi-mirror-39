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
# plingfiltre.py
"""
association d'un Pling et d'un filtre
"""

#import os
#import numarray as NA
#import numarray.fft as fft
#import pprint
#
#import utiles as _u
#import profils as _p
#import ondes as _o
#import canal
import numpy as np
from samplerate import sr
#from conversions08 import prony2freq
from serie import Serie002
#from profilbase import ProfilBase
from origine import Origine0
from filtrefixe import FiltreFixe
#import sys
#import types

__author__ = "Copyright (c) 2005-07 René Bastian (Wissembourg, FRANCE)"
__date__ = "2007.12.14, 09.10.24"

def plingfiltre(amorce, duree,
                hfiltre, genre, ncoeffs,
                debut=None, fin=None):
    """
    la hauteur du son est déterminée par la longueur de l'amorce
    """
    n = int(duree * sr)
    w = np.zeros(n, np.float64)
    na = len(amorce)
    filtre = FiltreFixe(genre, ncoeffs)
    coeffs = filtre.precalculs(hfiltre)
    w[:na] = amorce
    for i in range(na, n):
        x = (w[i-na] + w[i-na+1]) * 0.5
        x += coeffs * w[i-ncoeffs:i]
        w[i] = x
    if debut and fin:
        n0 = int(debut * sr)
        n1 = int(fin * sr)
        return w[n0:n1]
    else:
        return w

class PlingFiltre(Origine0):
    """
    associe un pling et un filtre
    """
    def __init__(self, cfiltre, xx=8457, xa=1279):
        """

        xx et xa installent le générateur 'alea'
        cfiltre : genre et accords du filtre
        """
        Origine0.__init__(self)
        self.alea = Serie002(xx, xa)
        self.cfiltre = cfiltre

    def evtvar(self, duree, vhauteur):
        """
        vhauteur : variation de la hauteur en prony
        """
        pass


    def evt(self, duree, hson, hfiltre):
        """
        hson : hauteur du son en prony
        hfiltre : hauteur du filtre en prony
        """
        pass


pf = PlingFiltre(("pb", 40))

print(pf)
