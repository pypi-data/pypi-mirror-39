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
# Maths/Sommes/sommes.py

"""
traduction en Python de formules de sommation qui figurent dans
la doc de CLM.
"""
import sys
#import os
import time
#import types
import numpy as np
from samplerate import SR
from conversions import (extremum, prony2freq)
from profils import (recta)
from profilbase import ProfilBase
#import ondes as _o
from canal import (recordMono)
#import serie
import versionneur

__author__ = "Copyright (c) 2005-07 René Bastian (Wissembourg, FRANCE)"
__date__ = "2008.04.27"

#sinusrecursifN(freq, n)

def sinrec(freqs):
    """
    'freqs': vecteur de fréquences
    """
    n = len(freqs)
    k = 2*np.cos(2*np.pi*freqs/SR)
    w = np.zeros(n, np.Float64)
    w[1] = 1.0
    for i in range(2, n):
        w[i] = k[i]*w[i-1] - w[i-2]
    return w/extremum(w)

def ncos_math(x, p):
    """
    d'après
    fournit une onde selon w = Sigma(cos(kx) [k=0..n]"""
    return 0.5 * (np.sin((p + 0.5) * x) / (np.sin(x / 2)))

def nsin_math(x, p):
    """
    cf wkipedia
    calcule Sigma(sin(k x) pour k = 0..n
    'p': entier
    'x': float
    """
    x = x/2
    return np.sin(x * (p+1))*np.sin(x * p) / np.sin(x)

def nsinrec(freqs, n):
    " calcule une fonction de somme "
    n = len(freqs)
    k = 2*np.cos(2*np.pi*freqs/SR)
    k1 = k * (n+1)/2
    k2 = k * n/2
    return sinrec(k1)*sinrec(k2)/sinrec(k)

def ncos(hauteur, duree, n, bprony=True):
    """retourne ncos_math(hauteur, n) quand hauteur est
    une liste-profil ou une hauteur fixe."""
    if isinstance(hauteur, list):
        h = ProfilBase(hauteur).temps(duree)
        if bprony:
            h = prony2freq(h)
        h = 2 * np.pi * h
    elif isinstance(hauteur, np.float64):
        if bprony:
            hauteur = prony2freq(hauteur)
        h = 2 * np.pi * hauteur * np.arange(0., duree, 1./SR)

    # reste le cas où hauteur est déjà un vecteur soit de freqs ou de pronys
    # qu'on peut traiter directement par ncos_math
    return ncos_math(h, n)

def ncosrecursif(hauteur, duree, p, bprony=True):
    """retourne ncos_math(hauteur, n) quand hauteur est
    une liste-profil ou une hauteur fixe."""
    if isinstance(hauteur, list):
        h = ProfilBase(hauteur).temps(duree)
        if bprony:
            h = prony2freq(h)
        h = 2 * np.pi * h
    elif isinstance(hauteur, np.float64):
        if bprony:
            hauteur = prony2freq(hauteur)
        h = 2 * np.pi * hauteur * np.arange(0., duree, 1./SR)
    # reste le cas où hauteur est déjà un vecteur soit de freqs ou de pronys
    # qu'on peut traiter directement par ncos_math
    return (0.5 * np.sin((p + 0.5) * h)) / (np.sin(h / 2))

def test1():
    " teste une fonction "
    t = np.arange(0., 4., 1./SR)
    x = 2*np.pi*440.0*t
    n = 10
    w = ncos_math(x, n)
    recordMono(w, "t1_sommes")

def test2():
    """
    la hauteur dépend plus de n que de la fréquence
    """
    hauteur = [[recta, 1., 72., 71.8]]
    #hauteur = 72.0
    duree = 5.
    n = 700
    w = ncos(hauteur, duree, n, bprony=True)
    recordMono(w, "t2_sommes")

def test3():
    " test "
    hauteur = [[recta, 1., 72., 71.8]]
    #hauteur = 72.0
    duree = 5.
    n = 40
    t = np.arange(0., duree, 1./SR)
    hauteur = 2*np.pi*440.0*t
    w = nsinrec(hauteur, n)
    recordMono(w, "t3_sommes")

def test4():
    " bof ... "
    pass

if __name__ == "__main__":
    t0 = time.time()

    try:
        ntest = int(sys.argv[-1])
    except IndexError:
        ntest = int(input("Quel test ? "))
    print("Test", ntest)

    if ntest == 1:
        test1()
    elif ntest == 2:
        test2()
    elif ntest == 3:
        test3()
    elif ntest == 4:
        test4()
    versionneur.fairecopienumero(__file__)
    t1 = time.time()
    print("Durée du calcul", t1 - t0)
