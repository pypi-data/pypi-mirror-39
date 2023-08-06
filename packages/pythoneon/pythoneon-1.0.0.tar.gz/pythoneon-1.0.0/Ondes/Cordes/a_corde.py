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
# Ondes/a_corde.py

"""
implémentation de la récurrence de la corde vibrante
La hauteur musicale correspond (presque) à la fréquence / ratio.
voir aussi e_corde.py
"""

import numpy as np
from samplerate import SR
from Outils.ajuster import prolongerN

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.12.28"

def violon0(duree, vexcit, freq, beta, filtre=None):
    """   y a-t-il une différence avec violon1 qui est plus simple"""
    gd = int(SR / freq)
    pd = int(gd * beta)
    n = int(duree * SR)
    a = np.zeros(n+gd)
    b = np.zeros(n+gd)
    for i in range(gd, n):
        a[i] = vexcit[i-pd] - vexcit[i]
        if filtre is None:
            b[i] = a[i-gd]
        else:
            b[i] = filtre(a[i-gd])
        a[i] += b[i]
    return b

def violon1(duree, vexcit, freq, beta, filtre=None):
    """
    'vexcit' : arroi d'excitation
    'freq' : hauteur fixe
    'beta' : ratio de la fréquence premier filtre à 'freq'
       freq1 = ratio * freq """
    gd = int(SR / freq)
    pd = int(gd * beta)
    n = int(duree * SR)
    w = np.zeros(n + gd)
    for i in range(gd, n):
        w[i] = vexcit[i - pd] - vexcit[i]
        if filtre is None:
            w[i] += w[i - gd]
        else:
            w[i] += filtre(w[i - gd])
    return w

def violonfluct0(duree, vexcit, vfreq, ratio):
    """
    'vexcit' : un arroi utilisé comme excitateur des filtres
             (p. ex. un bruit)
    'vfreq' : l'arroi de la variation de fréquence
    'ratio' : une fraction de vfreq
    Il ne faut pas exagérer les fluctuations car à SR==44100
    il y a des sauts de fréquence en escalier."""
    if vexcit.size != vfreq.size:
        vexcit, vfreq = prolongerN((vexcit, vfreq))
    vn = (SR / vfreq)
    vd = (vn * ratio)
    n = int(duree * SR)
    gd = int(vn.max())
    w = np.zeros(n + gd)
    for i in range(gd, n):
        w[i] = vexcit[int(i - vn[i])] - vexcit[i] + w[int(i - vd[i])]
    return w

def violonfluct1(duree, vexcit, vfreq, ratio):
    """
    'vexcit' : un arroi utilisé comme excitateur des filtres
             (p. ex. un bruit)
    'vfreq' : l'arroi de la variation de fréquence
    'ratio' : une fraction de vfreq
    NB:
       - on essaie de rapprocher la fréquence musicale de la fréquence
         physique;
       - des sauts de fréq. en escaliers"""
    if vexcit.size != vfreq.size:
        vexcit, vfreq = prolongerN((vexcit, vfreq))
    vn = (SR / vfreq) / ratio
    vd = (vn * ratio)
    n = int(duree * SR)
    gd = vn.max()
    w = np.zeros(n + int(gd))
    for i in range(int(gd), n):
        w[i] = vexcit[int(i - vn[i])] - vexcit[i] + w[int(i - vd[i])]
    return w
