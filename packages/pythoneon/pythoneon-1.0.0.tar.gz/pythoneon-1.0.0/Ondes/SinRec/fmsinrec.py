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
# fmsinrec.py

"""modulation de fréquence avec sinus récurrent """
import numpy as np
from samplerate import SR
from conversions import (extremum, prony2freq)
from profilbase import ProfilBase

__author__ = "Copyright (c) 2005 René Bastian (Wissembourg, FRANCE)"
__date__ = "2010.11.22"

def sinrec(freqs):
    """
    'freqs' : vecteur de fréquences
    utilisé dans 'disciotis' et 'sparassis'
    """
    n = len(freqs)
    k = 2*np.cos(2 * np.pi * freqs / SR)
    w = np.zeros(n, np.float64)
    w[1] = 1.0
    for i in range(2, n):
        w[i] = k[i] * w[i-1] - w[i-2]
    return w / extremum(w)

def fmsinrec(duree, phauteurc, pindex, phauteurm):
    """
    réaliser w = sin(fc * t + index * sin(fm * t))

    phauteurc : profil de la variation de hauteur en prony
    pindex : profil de la variation du ratio de modulation
    phauteurm : profil de la variation de la modulation en prony
    """
    n = int(duree * SR)
    vfreqc = ProfilBase(phauteurc).samples(n)
    vfreqc = prony2freq(vfreqc)
    vfreqm = ProfilBase(phauteurm).samples(n)
    vfreqm = prony2freq(vfreqm)
    vindex = ProfilBase(pindex).samples(n)
    wm = sinrec(vfreqm)
    wm *= vindex
    wm += vfreqc
    return sinrec(wm)
