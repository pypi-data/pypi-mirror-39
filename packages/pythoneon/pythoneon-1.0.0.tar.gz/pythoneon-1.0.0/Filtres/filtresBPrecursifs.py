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
# filtresBPrecursifs.py
##DEBUT
"""
petite collection de fonctions qui calculent les
coeffs de filtres BP récursifs et qui les appliquent.

Il vaut mieux utiliser ou améliorer 'filtrebpvariable.py' où le
projet de la classe est mieux dessiné.

class FiltreBPVariable : voir vagues2.py
"""

import numpy as np
from samplerate import SR
#from conversions08 import prony2freq
from conversions import prony2freq

__author__ = "Copyright (c) René Bastian 2002-2006 <rbastian@free.fr>"
__date__ = "2003.08.11, 2004.05.22, 2006.02.13"
##FIN
__all__ = ["coeffsBPrecursif", "appliBPrecursif",
           "filtreBPrecursif", "appliBPrecursifProny",
           "coeffsBPrecursifVar", "appliFiltreVar", "appliBPrecursifPronyVar",
           "filtreBPrecursifPronyVar", "filtrePBRecursifProny",
           "filtrePBRecursif",
           "passebanderecursif"]
#"BRejectRecursif", "filtre3a2b", "filtreAB", "appliBPrecursifC", -> zpythoneon
##DEBUT
#------------- FILTRE BP RECURSIF : coeffs et appli -------------------
def _coeffsBPrecursif(pronycentral, deltaprony):
    """
    calcule les coeffs pour un filtre PB recursif
    centré sur 'pronycentral' avec atténuation de -3 db
    de 'pronycentral-deltaprony' à 'pronycentral+deltaprony'
    'pronycentral' : hauteur centrale en prony, float
    'deltaprony' : largeur en prony, float
    """
    freqc = prony2freq(pronycentral)
    freq1 = prony2freq(pronycentral - deltaprony)
    freq2 = prony2freq(pronycentral + deltaprony)
    bande = float(freq2-freq1)/SR
    fc = freqc * 1.0/SR
    omega = 2 * np.pi * fc
    cosomega = np.cos(omega)
    R = 1.0 - 3 * bande
    R2 = R * R
    try:
        K = (1.0 - 2 * R * cosomega + R2)/(2.0 - 2 * cosomega)
    except ZeroDivisionError:
        print("(2.0 - 2 * cosomega) =", (2.0 - 2 * cosomega), cosomega)
        return
    a0 = 1.0 - K
    a1 = 2 * (K - R) * cosomega
    a2 = R2 - K
    b1 = 2 * R * cosomega
    b2 = -R2
    return [a0, a1, a2], [0.0, b1, b2]

def coeffsBPrecursif(pronycentral, deltaprony):
    """
    calcule les coeffs pour un filtre PB recursif
    centré sur 'pronycentral' avec atténuation de -3 db
    de 'pronycentral-deltaprony' à 'pronycentral+deltaprony'
    'pronycentral' : hauteur centrale en prony, float
    'deltaprony' : largeur en prony, float
    """
    freqc = prony2freq(pronycentral)
    freq1 = prony2freq(pronycentral - deltaprony)
    freq2 = prony2freq(pronycentral + deltaprony)
    #bande = float(freq2-freq1)/SR
    bande = (freq2-freq1)/SR
    fc = freqc * 1.0/SR
    #print(freqc, freq1, freq2, fc, bande)
    omega = 2.0 * np.pi * fc
    cosomega = np.cos(omega)
    #print(omega, cosomega)
    R = 1.0 - 3 * bande
    R2 = R * R
    try:
        K = (1.0 - 2 * R * cosomega + R2)/(2.0 - 2 * cosomega)
    except ZeroDivisionError:
        print("(2.0 - 2 * cosomega) =", (2.0 - 2 * cosomega), cosomega)
        K = 1.0
    a0 = 1.0 - K
    a1 = 2 * (K - R) * cosomega
    a2 = R2 - K
    b1 = 2 * R * cosomega
    b2 = -R2
    return [a0, a1, a2], [0.0, b1, b2]

def passebanderecursif(freqcoupure, bandepassante):
    """
    identique à coeffsBPrecursif (mais hauteur = fréquences)
    calcule les coefficients (a0, a1, a2), (0.0, b1, b2)
    d'un filtre BP récursif caractérisé par
    sa fréquence centrale et sa bande passante
    'freqcoupure' : fréquence centrale
    'bandepassante' : bande passante
    """
    bande = bandepassante * 1.0/SR
    fc = freqcoupure * 1.0/SR
    omega = 2 * np.pi * fc
    cosomega = np.cos(omega)
    R = 1.0 - 3.0 * bande
    R2 = R * R
    K = (1.0 - 2 * R * cosomega + R2)/(2.0 - 2 * cosomega)
    a0 = 1.0 - K
    a1 = 2 * (K - R) * cosomega
    a2 = R2 - K
    b1 = 2 * R * cosomega
    b2 = -R2
    return [a0, a1, a2], [0.0, b1, b2]

def appliBPrecursif(x, a, b):
    """
    x : signal entrant
    a, b : liste coeffs
     = > b[0] == 0.0
    """
    x = np.concatenate((np.zeros(2, np.float64), x))
    y = np.zeros(len(x), np.float64)
    for i in range(2, len(x)-2):
        #print(i, y[i], x[i], a[0])
        y[i] = x[i] * a[0]+ \
             x[i-1] * a[1]+ \
             x[i-2] * a[2]+ \
             y[i-1] * b[1]+ \
             y[i-2] * b[2]
    return y

def filtreBPrecursif(signal, pronycentral, deltaprony):
    """
    calcule les coeffs a, b
    applique le filtre au signal
    """
    a, b = coeffsBPrecursif(pronycentral, deltaprony)
    #print(a, b)
    y = appliBPrecursif(signal, a, b)
    return y

def appliBPrecursifProny(signal, pronycentral, deltaprony):
    "idem que 'filtreBPrecursif'"
    return filtreBPrecursif(signal, pronycentral, deltaprony)

#-------------FILTRES BP FLUCTUANTS -------------------

def coeffsBPrecursifVar(liste):
    """
    liste  =  [[pronycentral, deltaprony], [pronycentral, deltaprony], ...]
    """
    A, B = [], []
    for c in liste:
        a, b = coeffsBPrecursif(c[0], c[1])
        A.append(a)
        B.append(b)
    return A, B

def appliFiltreVar(x, A, B):
    """
    appliFiltreVar applique une liste de coeffs de filtres généraux d'ordre 2
    x : signal entrant
    A, B : liste coeffs a & b
     = > B[i][0] == 0.0
    Normalement, len(x)== len(A)== len(B)
    """
    d = min(len(x), len(A), len(B))
    x = np.concatenate((np.zeros(2, np.float64), x))
    y = np.zeros(len(x), np.float64)
    #for i in range(2, d-2):
    for i in range(2, d): # changé le 14.02.08
        y[i] = x[i] * A[i][0]+x[i-1] * A[i][1]+x[i-2] * A[i][2]+ \
                y[i-1] * B[i][1]+y[i-2] * B[i][2]
    return y

def appliBPrecursifPronyVar(signal, liste):
    """
    liste  =  [[pronycentral, deltaprony], [pronycentral, deltaprony], ...]
    """
    A, B = coeffsBPrecursifVar(liste)
    y = appliFiltreVar(signal, A, B)
    return y

def filtreBPrecursifPronyVar(signal, liste):
    """
    liste  =  [[pronycentral, deltaprony], [pronycentral, deltaprony], ...]
    """
    A, B = coeffsBPrecursifVar(liste)
    y = appliFiltreVar(signal, A, B)
    return y

#

#------------------- FILTRES RECURSIFS ----------------------
def filtrePBRecursifProny(signal, pronycoupure, pronybandepassante):
    """
    applique un filtre BP à un signal
    'signal' : le signal à filtrer
    'pronycoupure' : la hauteur en prony de la frequence centrale de
    la bande
    'pronybandepassante' : l'intervalle en prony de la bande passante
    """
    freqcoupure = prony2freq(pronycoupure)
    bandepassante = prony2freq(pronybandepassante)
    a, b = passebanderecursif(freqcoupure, bandepassante)
    #print(a, b)
    return appliBPrecursif(signal, a, b)

def filtrePBRecursif(signal, freqcoupure, bandepassante):
    """
    application d'un filtre BP à un 'signal'
    selon une fréquence de coupure et une bande passante.
    """
    a, b = passebanderecursif(freqcoupure, bandepassante)
    return appliBPrecursif(signal, a, b)
##FIN
#if __name__ == "__main__":
#    import serie
#
#    alea = serie.Serie002(8976, 7564)
#    signal = alea.bruit(4 * SR)
#    print("test signal original")
#    audio.play(signal, signal)
#    print("test signal filtré h=86., largeur=0.5")
#    w = filtrePBRecursifProny(signal, 86., 0.5)
#    audio.play(w, w)


