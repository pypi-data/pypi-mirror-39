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
# sinusmath.py

""" contient les fonctions
  sinus(freq, duree=None)
  sinusN(freq, n)
  sinusV(vfreq)
calculant des sinus à l'aide de fonctions de numpy """

import numpy as np
from samplerate import sr

__author__ = "Copyright (c) 2013 René Bastian (Wissembourg, FRANCE)"
__date__ = "2013.06.04"

def sinus(freq, duree=None):
    " calcule un sinus de fréquence 'freq' et durée 'duree' "
    if duree is None and isinstance(freq, np.ndarray):
        return sinusV(freq)
    else:
        n = int(duree * sr)
    return sinusN(freq, n)

def sinusN(freq, n):
    " calcule un sinus de fréquence 'freq' et de 'n' samples "
    vt = np.arange(0, n) * 2 * np.pi * freq / sr
    return np.sin(vt)

def sinusV(vfreq):
    " vfreq : vecteur de la variation de fréquence en Hz "
    vt = np.cumsum(vfreq) * 2 * np.pi / sr
    return np.sin(vt)
