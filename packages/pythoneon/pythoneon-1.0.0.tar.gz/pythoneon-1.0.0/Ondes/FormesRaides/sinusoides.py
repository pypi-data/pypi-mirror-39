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
# Ondes/FormesRaides/sinusoides.py

"""rassemble des fonctions
permettant de produire des formes d'ondes
à l'aide de tables ou fonctions sinus.
Test: t_sinusoides.py"""

import numpy as np
from samplerate import SR
from conversions import prony2freq

__date__ = "2002, 2010.08.15, 2012, rév. python3 2016"
__author__ = "Copyright (c) 2002-16 René Bastian (Wissembourg, FRANCE)"

#------------ SINUSITES ----------------------

Tvecteur = np.arange(0.0, 1.0, 1.0/SR)
Sinus = np.sin(2*np.pi*Tvecteur)

def sinus(freq, duree, valeur=0.0, phase=0.0, puiss=None):
    """
    produit un sinus de fréquence, durée et phase données.
    Attention: dans cette fonction valeur n'est pas un angle, mais
    une valeur initiale ! (suite à une remarque de Éric Marzolf)
    Mais on peut arranger ça pour concorder avec
    les maths traditionnelles."""
    if freq > SR:
        print("Attention:sinus:freq > SR", freq, SR)
        freq = freq % (SR/2)
    if phase == 0.0 and valeur == 0.0:
        vT = np.arange(0.0, duree, 1.0/SR)*2*np.pi*freq
    elif valeur != 0.0:
        v = np.arcsin(valeur)
        vT = np.arange(v, duree + v, 1.0/SR)*2*np.pi*freq
    elif phase != 0.0:
        vT = np.arange(phase, duree + phase, 1.0/SR)*2*np.pi*freq
    else:
        print("J'sais pas quoi faire dans sinus(freq, duree, ...)")
        return None
    if puiss is not None:
        return np.sin(vT)**puiss
    else:
        return np.sin(vT)

def sinus_2(freq, duree, valeur=0.0, phase=0.0, puiss=0.0):
    """ produit un sinus de fréquence, durée et phase données.
    Attention: dans cette fonction valeur n'est pas un angle, mais
    une valeur initiale ! (suite à une remarque de Éric Marzolf)
    Mais on peut arranger ça pour concorder avec
    les maths traditionnelles."""
    if freq > SR/2:
        print("Attention:sinus(freq, duree ...):freq > SR/2", freq, SR)
    if valeur != 0.0 and phase != 0.0:
        print("sinus(freq, duree, ...: Pas de solution")
        print("valeur & phase != 0.0")
        return None
    if phase == 0.0 and valeur == 0.0:
        T = np.arange(0.0, duree, 1.0/SR)*2*np.pi*freq
    elif valeur != 0.0:
        v = np.arcsin(valeur)
        print(v, np.sin(v))
        v /= 2*np.pi*freq
        T = np.arange(v, duree+v, 1.0/SR)*2*np.pi*freq
    elif phase != 0.0: # cas peu probable:-)
        T = np.arange(phase, duree + phase, 1.0/SR)*2*np.pi*freq
    else:
        print("J'sais pas quoi faire dans sinus(freq, duree, ...)")
        return None
    if puiss > 0.0:
        return np.sin(T) ** puiss
    elif puiss < 0.0:
        print("sinus(freq, duree, ...puiss < 0.0: Pas de solution")
        return None
    else:
        return np.sin(T)

def sinusN(freq, n):
    """retourne une sinusoïde de n échantillons et hauteur freq."""
    vT = np.arange(0.0, float(n), 1.0)*2*np.pi*freq/SR
    return np.sin(vT)

def sinusN_2(freq, n, valeur=0.0, phase=0.0, puiss=None):
    """ produit un vecteur de n samples selon un sinus de fréquence donnée
    valeur initiale ou phase donnée
    Le procédé est litigieux à cause des arrondis, mais semble
    être acceptable en pratique."""
    if freq > SR/2:
        print("Attention:sinusN(freq, duree ...):freq > SR", freq, SR)
    if valeur != 0.0 and phase != 0.0:
        print("sinusN(freq, duree, ...: Pas de solution")
        print("valeur & phase != 0.0")
        return None
    duree = float(n) / SR
    return sinus(freq, duree, valeur, phase, puiss)

def sinusRM(freq1, freq2, duree, n1, n2):
    """devrait retourner un effet modulateur en anneau.
    freq1, freq2
    duree
    n1: entier ou liste
    n2: entier ou liste
    """
    if isinstance(n1, int): #type(n1) == types.IntType:
        L1 = range(1, n1)
    else:
        L1 = n1
    if isinstance(n2, int): #type(n2) == types.IntType:
        L2 = range(1, n2)
    else:
        L2 = n2
    vT = np.arange(0.0, duree, 1.0/SR)*2*np.pi
    w = np.zeros(int(duree*SR))
    dim = min(len(vT), len(w))
    vT = vT[0:dim]
    w = w[0:dim]
    #print(len(w), len(vT))
    #for i in range(len(L1)):
    #    for j in range(len(L2)):
    #        w = w + np.sin(vT*(L1[i]*freq1 + L2[j]*freq2))
    for x1 in L1:
        for x2 in L2:
            w = w + np.sin(vT*(x1*freq1 + x2*freq2))
    return w

def sinusTable(freq, duree, ph=0.0):
    """retourne un sinus de hauteur freq et duree données
    à partir de la table Sinus."""

    n = int(duree * SR)
    X = np.arange(ph, (n * freq) + ph, freq) % SR
    X = X.astype(np.int32)
    return Sinus[X]

def sinusNTable(freq, n, phase=0.0):
    """retourne une sinusoïde de n samples."""

    X = np.arange(phase, (n * freq) + phase, freq) % SR
    X = X.astype(np.int32)
    return Sinus[X]

def sinusMF_dev(vfreq):
    """
    w = np.sin(2*np.pi*t*freq/SR)
    """
    if isinstance(vfreq, list):
        vfreq = np.array(vfreq)
    n = vfreq.size
    dt = 1./SR
    vT = np.arange(0.0, n*dt, dt) * 2 * np.pi
    vT *= vfreq
    return np.sin(vT)

def _sinusMF_NULLL(vfreq, ph=0.0):
    """
    vfreq: vecteur-profil dessinant la variation de freq
    ph: phase initiale
    """
    ph = np.array([ph])
    vfreq = np.concatenate((ph, vfreq))
    X = np.add.accumulate(vfreq) % SR
    X = X.astype(np.int32)
    return Sinus[X]

def sinusMF(vfreq):
    """
    vfreq: vecteur-profil dessinant la variation de freq
    """
    X = np.add.accumulate(vfreq) % SR
    X = X.astype(np.int32)
    return Sinus[X]

def multisinusTable(minfreq, maxfreq, duree, coeff, alea):
    """retourne une onde dont la hauteur varie aléatoirement.
    minfreq, maxfreq: hauteurs en Hz
    duree: durée
    coeff: int(coeff*minfreq) == critère pour changer
    de fréquence
    alea: générateur tel que random ou Serie002 ;
    coeff peut varier de 0.1 à 3.0 ;
    le son varie entre clapotis et bruité.
    Voir si coeff peut être un profil."""
    n = int(duree * SR)
    iph = 0
    ph = 0.0
    crit = int(minfreq * coeff)
    y = np.zeros(n, np.float64)
    for i in range(n):
        y[i] = Sinus[iph]
        if i % crit == 0:
            freq = alea.uniform(minfreq, maxfreq)
        ph += freq
        iph = int(ph) % SR
    return y

def sinusmf(freqc, freqm, t, indexf):
    """valeur ponctuelle d'une modulation de phase.
    Expérimental: pas encore sûr si indexf doit être une
    fonction - car on peut aussi envisager que
    freqc, freqm et indexf sont des vecteurs,
    générés par des profils.
    freqc: fréquence (réel)
    freqm: fréquence (réel)
    t   : point temporel (réel)
    indexf: fonction connue de Python ou définie
    par l'utilisateur.
    """
    return np.sin(2*np.pi*freqc*t + indexf(t)*np.sin(2*np.pi*freqm*t))

def sinusfreq(hauteur, duree, nfreqs, alea, deviation,
              bprony=False, bduree=True):
    """produit des sons complexes intéressants.
    hauteur: hauteur centrale
    duree: nombre d'échantillons
    nfreqs: nombre de fréquences superposées du complexe
    alea: générateur sériel
    deviation: variation autour de la fréquence centrale."""
    if bprony:
        freq0 = prony2freq(hauteur)
    else:
        freq0 = hauteur
    if bduree:
        n = int(duree * SR)
    else:
        n = duree
    vT = np.arange(0.0, n, 1.0)*2*np.pi*freq0/SR
    R = np.sin(vT)
    for _ in range(nfreqs):
        dev = alea.uniform(1.0 - deviation, 1.0 + deviation)
        freq = freq0 * dev
        vT = np.arange(0.0, n, 1.0) * 2 * np.pi * freq / SR
        R = R + np.sin(vT)
    return R

def sinusNfreq(freq0, n, nfreqs, alea, deviation):
    """produit des sons complexes intéressants.
    freq0: hauteur centrale
    n: nombre d'échantillons
    nfreqs: nombre de fréquences superposées du complexe
    alea: générateur sériel
    deviation: variation autour de la fréquence centrale."""
    print("SinusNfreq: Obsolète -> sinusfreq")
    return sinusfreq(freq0, n, nfreqs, alea, deviation,
                     bprony=False, bduree=False)

def sinusDfreq(freq0, duree, nfreqs, alea, deviation):
    """produit des sons complexes intéressants.
    freq0: hauteur centrale
    duree: durée
    nfreqs: nombre de fréquences du complexe
    alea: générateur sériel
    deviation: variation autour de la fréquence centrale."""
    print("SinusDfreq: Obsolète -> sinusfreq")
    return sinusfreq(freq0, duree, nfreqs, alea, deviation,
                     bprony=False, bduree=True)
