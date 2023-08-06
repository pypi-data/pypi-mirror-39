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
# ~/pythoneon/Ondes/SinRec/sinusrecursif.py

"""
la classe SinusRecursif montre que la fonction
sinus est calculable avec une multiplication et une
soustraction ; elle prend env. 20 fois plus de temps
que la fonction sinus de numpy, mais cette méthode
a l'avantage d'éviter quelques ennuis de repliement.

Les fonctions
'sinusrecursif(freq, duree)' et 'sinrec(freqs)'
en cas d'appels directs.

La classe 'SinusRecursif' est utile si on veut
indiquer la durée et une évolution de la hauteur
par une liste-profil en midi.
"""

import numpy as np
from samplerate import SR
from profilbase import ProfilBase
from conversions import (extremum, prony2freq, freq2ksin,
                         freq2samples)

__author__ = "Copyright (c) 2005 René Bastian (Wissembourg, FRANCE)"
__date__ = "2006., 2013.07.19, 016.08.16"

__all__ = ["kalcul", #"sinusrecursif", "SinusRecursif",
           #"SinusRecursifUnique",
           "combine", #(duree, freq, amorce):
           "sinusrecursifelementaire", #(k, n, ph1=1.0, amorti=1.0, borne=None):
           "sinrecursif", #(k, n):
           "sinrecursifamorti", #(k, n, amorti):
           "sinusrecursif", #(h, duree, prony=False, samples=False, amorti=1.0):
           "sinusrecursifN", #(freq, n):
           "sinrecF", #(freq, n):
           "sinrec", #(vfreqs):
           "nsinrec", #(freqs, p):
           "sinusmfrecursif", #(duree, pF, pM, pA):
           "sinusmfrecursif", #(duree, pliste):
           "sinusmfrecursif00", #(duree, pF, pM, pA, test=False):
          ]

def kalcul(freq):
    """ calcul le coeff k """
    return 2*np.cos(2*np.pi*freq/SR)

def combine(duree, freq, amorce):
    """ essai de combinaison de deux fréquences
    amorce : vecteur de type np.ndarray
    ????
    voir varsinus.py
    """
    k = freq2ksin(freq)
    n = int(duree * SR)
    no = amorce.size
    w = np.zeros(n + no)
    w[:amorce.size] = amorce
    w[no-1] = 1.0
    w[no-2] = 0.0
    for i in range(no, n + no):
        w[i] = (w[i-no] + w[i-no+1]) * 0.25 + (k*w[i-1] - w[i-2]) * 0.5
        #w[i] = (w[i-no] + w[i-no+1]) * (k*w[i-1] - w[i-2]) #* 0.5
    return w[no:]

def sinusrecursifelementaire(k, n, ph1=1.0, amorti=1.0, borne=None):
    """ fonction élémentaire pour jouer avec le coeff 'k'
    k = 2*np.cos(2*np.pi*freqs/SR) """
    w = np.zeros(n, np.float64)
    w[1] = ph1
    if borne is not None:
        cinverse = (1./amorti) ** borne
    for i in range(2, n):
        w[i] = k * w[i-1] - w[i-2]
        w[i] *= amorti
        if borne and (i % borne == 0):
            w[i] *= cinverse
    return w

def sinrecursif(k, n):
    "fonction élémentaire pour jouer avec le coeff 'k'"
    w = np.zeros(n, np.float64)
    w[1] = 1.0
    for i in range(2, n):
        w[i] = k * w[i-1] - w[i-2]
    return w / extremum(w)

def sinrecursifamorti(k, n, amorti):
    """fonction élémentaire pour jouer avec le coeff 'k'
    amorti: <= 1.0 fait monter la hauteur
    PROBLÉMATIQUE : NE PAS UTILISER"""
    w = np.zeros(n, np.float64)
    w[1] = 1.0
    for i in range(2, n):
        #w[i] = (k * w[i-1] - w[i-2]) * amorti
        w[i] = k * w[i-1] - w[i-2] * amorti
    return w / extremum(w)

def sinusrecursif(h, duree, bprony=False, bsamples=False, amorti=1.0):
    """
    'h' : hauteur, prony ou Hz,
    'duree' : durée en sec ou samples
    'bprony', 'bsamples' : critères
    'amorti': un coeff d'amortissement
    """
    if bprony:
        freq = prony2freq(h)
    else:
        freq = h
    if not bsamples:
        n = int(duree * SR)
    else:
        n = duree
    k = 2*np.cos(2 * np.pi * freq/SR)
    if amorti == 1.0:
        return sinrecursif(k, n)
    else:
        return sinrecursifamorti(k, n, amorti)

def sinusrecursifN(freq, n):
    """
    'freq, n' : fréquence, nombre de samples
    utilisé dans expo00
    """
    k = 2 * np.cos(2 * np.pi * freq / SR)
    return sinrecursif(k, n)

##FIN
def sinrecF(freq, n):
    """
    'freq' :
    'n' : samples
    """
    k = 2*np.cos(2 * np.pi * freq / SR)
    w = np.zeros(n, np.float64)
    w[1] = 1.0
    for i in range(2, n):
        w[i] = k * w[i-1] - w[i-2]
    return w / extremum(w)

def sinrec(vfreq, phase0=0.0, phase1=1.0):
    """
    'vfreq' : vecteur de fréquences
    phasesX: valeurs initiales
    utilisé dans 'audubons', 'disciotis' et 'sparassis'
    """
    if isinstance(vfreq, (list, tuple)):
        vfreq = np.array(vfreq)
    n = vfreq.size
    k = 2 * np.cos(2 * np.pi * vfreq / SR)
    w = np.zeros(n, np.float64)
    w[0] = phase0
    w[1] = phase1
    for i in range(2, n):
        w[i] = k[i] * w[i-1] - w[i-2]
    return w / extremum(w)

def nsinrec(freqs, p):
    """
    'freqs' : vecteur de fréquences
    'p' : nombre de multiples de 'freq'
    jamais utilisé dans une pièce
    """
    n = len(freqs)
    r = np.zeros(n, np.float64)
    for _ in range(1, p+1):
        for i in range(1, p+1):
            k = 2*np.cos(2*np.pi*freqs*p/SR)
            w = np.zeros(n, np.float64)
            w[1] = 1.0
            for i in range(2, n):
                w[i] = k[i]*w[i-1] - w[i-2]
        r += w
    return r/extremum(r)

def sinusmfrecursif(duree, pF, pM, pA):
    """
    'duree' : durée
    'pF' : variation de la fréquence de base
    'pM' : variation de la fréquence de modulation
    'pA' : enveloppe de la modulation de fréquence
    Il faut comparer l'onde avec celle obtenue par pileprofil.
    jamais utilisé dans une pièce
    """
    n = int(duree * SR)
    f = ProfilBase(pF).samples(n)
    a = ProfilBase(pA).samples(n)
    m = ProfilBase(pM).samples(n)
    mf = a * sinrec(m) + f
    w = sinrec(mf)
    return w / extremum(w)

def sinusmfrecursif01(duree, pliste):
    """
    'duree' : durée
    'pF' : variation de la fréquence de base
    'pM' : variation de la fréquence de modulation
    'pA' : enveloppe de la modulation de fréquence
    """
    n = int(duree * SR)
    vmf = np.zeros(n)
    for triple in pliste:
        pF, pA, pM = triple
        if isinstance(pF, list):
            vf = ProfilBase(pF).samples(n)
        if pA is None:
            va = np.ones(n)
        elif isinstance(pA, list):
            va = ProfilBase(pA).samples(n)
        if pM is None:
            vm = np.zeros(n)
        elif isinstance(pM, list):
            vm = ProfilBase(pM).samples(n)
        mf = va * sinrec(vf) + vm
        vmf += mf
    w = sinrec(vmf)
    return w / extremum(w)

def sinusmfrecursif00(duree, pF, pM, pA):
    """
    'duree' : durée
    'pF' : variation de la fréquence de base
    'pM' : variation de la fréquence de modulation
    'pA' : enveloppe de la modulation de fréquence
    Il faut comparer l'onde avec celle obtenue par pileprofil.
    jamais utilisé dans une pièce
    """
    n = int(duree * SR)
    f = ProfilBase(pF).samples(n)
    a = ProfilBase(pA).samples(n)
    m = ProfilBase(pM).samples(n)
    mf = a * sinrec(m) + f
    w = sinrec(mf)
    return w / extremum(w)

def doublerecursif3(freq1, freq2, n, xini=1.0):
    """ algorithme récursif : sinus amorti
    produit une sorte de balancement avec effet RM
    0.99  : amorti trop fort duree = 5:0
    0.995 : 14:00
    0.996 : 20:00
    0.997 : 37:00
    0.998 : 48.00 avec crescendo ...
    L'examen des extremums n'est pas concluant parce qu'il peut être atteint
    en très peu de temps au début
    """
    k1 = kalcul(freq1)
    k2 = kalcul(freq2)
    b1 = freq2samples(freq1)
    b2 = freq2samples(freq2)
    b = max(b1, b2)
    w1, w2 = np.zeros(n), np.zeros(n)
    w1[0] = w2[0] = 0.0
    w1[1] = w2[1] = -xini/2
    w1[2] = w2[2] = xini
    coeff = 0.00005
    for i in range(3, n):
        #if (i % b1 == 0) or (i % b2 == 0):
        if i % b == 0:
            coeff = -coeff
            # 0.99 -> extremum =26.7661561552 97.0093189261
            # 0.9 -> 25.6315252484 93.0001022969
            # 0.8 -> 25.6315252484 93.0001022969

            w1[i-3:i] *= 0.998
            w2[i-3:i] *= 0.998
        w1[i] = k1*w1[i-1] - w1[i-2] + k1*w2[i-3]*coeff
        w2[i] = k2*w2[i-1] - w2[i-2] - k2*w1[i-3]*coeff
    print(extremum(w1), extremum(w2))
    return w1, w2

def sinusrecursifAmorti(k, n, coeff=0.0002, xini=1.0):
    """ algorithme récursif : sinus amorti, ??"""
    w = np.zeros(n)
    w[0] = 0.0
    w[1] = -xini/2
    w[2] = xini
    for i in range(3, n):
        w[i] = k*w[i-1] - w[i-2] + k*w[i-3] * coeff
    return w
