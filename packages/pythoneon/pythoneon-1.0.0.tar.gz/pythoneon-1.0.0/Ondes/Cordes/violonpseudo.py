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
# Ondes/Cordes/violonbrut.py
"""
implémentation de la récurrence de la corde vibrante
La hauteur musicale correspond à la fréquence / ratio.
"""

import time
import sys
import numpy as np
from samplerate import SR
from conversions import (prony2freq, freq2prony)
from profilbase import ProfilBase
from profils import recta
from canal import (CanalMono, recordMono)
from serie import Serie002
from taudio import play64
import versionneur

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.12.28, 2013.09.09"

def violonbrut(duree, vexcit, freq, ratio):
    """ construit un son de pseudo-corde
    'vexcit' : un vecteur utilisé comme excitateur des filtres
             (p. ex. un bruit)
    'freq' : fréquence
    'ratio' : une fraction de freq qui modifie le timbre et change la hauteur
    Si on souhaite une hauteur précise, il faut effectuer la
    compensation avant d'appeler cette fonction: cf violoncomp."""
    dn = int(SR / freq)
    vd = int(ratio * dn)
    n = int(duree * SR)
    w = np.zeros(n + dn)
    for i in range(vd, n):
        w[i] = vexcit[i - dn] - vexcit[i] + w[i - vd]
    return w

def violoncomp(duree, vexcit, hauteur, ratio):
    """ préparation des params avant l'appel de 'violonbrut' """
    freq = prony2freq(hauteur) * ratio
    return violonbrut(duree, vexcit, freq, ratio)

def violonbrutV(vexcit, freq, vratio):
    """ construit un son de pseudo-corde
    'vexcit' : un vecteur utilisé comme excitateur des filtres
             (p. ex. un bruit)
    'freq' : fréquence
    'vratio' : un vecteur de valeurs entre 0.0 et 1.0
    """
    if vratio.size != vexcit.size:
        print("violonbrutV(vexcit, freq, vratio): vratio.size != vexcit.size")
        return
    n = vexcit.size
    dn = int(SR / freq)
    vd = vratio * dn
    vd = vd.astype(int)
    w = np.zeros(n + dn)
    for i in range(vd[0], n):
        w[i] = vexcit[i - dn] - vexcit[i] + w[i - vd[i]]
    return w

def testviolonbrut():
    """test 21: test2 avec enveloppe
    La hauteur reste constante pendant l'émission du signal
    L'amorce excitante est un bruit de Serie002
    """
    c = CanalMono()
    xduree = 3.0
    n = int(xduree * SR)
    xve = Serie002(631, 137).uniform(-1.0, +1.0, n)
    gamme = np.array([36.0, 38., 40.0, 41.0, 43.0, 45.0, 47.0])
    gamme = prony2freq(gamme)
    freqs = np.concatenate((gamme * 0.5, gamme, gamme * 2, gamme * 4,
                            gamme * 8, gamme * 16, gamme * 32))

    penv = [[recta, 0.1, 0.0, 1.0],
            [recta, 0.8, 1.0, 1.0],
            [recta, 0.1, 1.0, 0.0]]
    pbenv = ProfilBase(penv)
    pt = 0.0
    ratios = [0.305, 0.31, 0.315]
    # ratios à essayer
    #ratios = [1. / 3]
    #ratios = [1. / 125] #dégradation vers bruit et grave
    #ratios = [1. / 2]
    #ratios = [1./6]
    #ratios = [0.99]
    #ratios = np.linspace(0.25, 0.35, 9)
    #forme = "freq %12.5f h %6.2f ratio %5.3f freq/ratio %12.5f h2 %6.2f"
    R = (
        [0.4],
        [0.305, 0.31, 0.315],
        [0.5, 0.6, 0.7, 0.8, 0.9],
        [0.5, 0.4, 0.3, 0.2, 0.1],
        [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        [1.0, 0.5, 0.25, 0.125, 0.0625],
        [0.25, 0.125, 0.0625]
        )
    ratios = R[6]
    H = (
        [48.0, 50.0, 52.0],
        [48.0, 55.0, 62.0, 69.0],
        [36.0, 38., 40.0, 41.0, 43.0, 45.0, 47.0, 48.0],
        [24.0, 26.0, 28., 29.0, 31.0, 33.0, 35.0, 36.0]
        )
    hliste = H[2]#[-1:]
    freqs = [prony2freq(h) for h in hliste]
    for freq in freqs:
        for ratio in ratios:
            print(freq, freq2prony(freq))
            vw = violonbrut(xduree, xve, freq, ratio)
            env = pbenv.samples(vw.size)
            vw *= env
            c.addT(pt, vw)
            pt += xduree
            play64(vw, vw)
    play64(c.a, c.a)
    recordMono(c.a, "violonpseudo")

def choix():
    " choisir la hauteur "
    xduree = 3.0
    n = int(xduree * SR)
    xve = Serie002(631, 137).uniform(-1.0, +1.0, n)
    penv = [[recta, 0.1, 0.0, 1.0],
            [recta, 0.8, 1.0, 1.0],
            [recta, 0.1, 1.0, 0.0]]
    pbenv = ProfilBase(penv)
    while True:
        h = input("Hauteur ? ")
        if h == 0:
            break
        ratio = input("Ratio 0.0] .. [1.0 ? ")
        freq = prony2freq(h) * ratio
        print(freq, ratio)
        vw = violonbrut(xduree, xve, freq, ratio)
        env = pbenv.samples(vw.size)
        vw *= env
        play64(vw, vw)

def explovioloncomp():
    """test 21: test2 avec enveloppe
    La hauteur reste constante pendant l'émission du signal
    L'amorce excitante est un bruit de Serie002
    """
    souche = "violoncomp"
    xduree = 2.0
    n = int(xduree * SR)
    xve = Serie002(631, 137).uniform(-1.0, +1.0, n)
    gamme0 = np.array([36.0, 38., 40.0, 41.0, 43.0, 45.0, 47.0])
    gamme = np.concatenate([gamme0 + i * 12 for i in range(-1, 7)])
    print(gamme, gamme.size)
    N = 41
    ratios = np.linspace(0.05, 0.95, N)
    print(ratios)

    penv = [[recta, 0.1, 0.0, 1.0],
            [recta, 0.8, 1.0, 1.0],
            [recta, 0.1, 1.0, 0.0]]
    pbenv = ProfilBase(penv)
    #forme = "freq %12.5f h %6.2f ratio %5.3f freq/ratio %12.5f h2 %6.2f"
    for h in gamme:
        c = CanalMono()
        pt = 0.0
        no = int(h)
        for ratio in ratios:
            print(h, ratio)
            vw = violoncomp(xduree, xve, h, ratio)
            env = pbenv.samples(vw.size)
            vw *= env
            c.addT(pt, vw)
            pt += xduree
            #play64(vw, vw)
        fnom = souche + str(no).zfill(3)
        # si wav == True, raw = True
        recordMono(c.a, fnom)

def variationlongue():
    """test: variation longue ne m'inspire pas
    essayer un vibrato"""
    xduree = 8.0
    n = int(xduree * SR)
    xve = Serie002(631, 137).uniform(-1.0, +1.0, n)
    freq = 125.0
    pratio = [[recta, 0.5, 0.1, 0.9], [recta, 0.5, 0.9, 0.1]]
    pratio = [[recta, 0.5, 0.9, 0.1], [recta, 0.5, 0.1, 0.1],
              [recta, 0.5, 0.1, 0.9], [recta, 0.5, 0.9, 0.9]]
    vratio = ProfilBase(pratio).samples(n)
    w = violonbrutV(xve, freq, vratio)
    play64(w, w)

def violonvibra():
    """test: variation longue ne m'inspire pas
    essayer un vibrato"""
    xduree = 8.0
    n = int(xduree * SR)
    xve = Serie002(631, 137).uniform(-1.0, +1.0, n)
    freq = 125.0
    pratio = [[recta, 0.5, 0.1, 0.9], [recta, 0.5, 0.9, 0.1]]
    pratio = [[recta, 0.5, 0.9, 0.1], [recta, 0.5, 0.1, 0.1],
              [recta, 0.5, 0.1, 0.9], [recta, 0.5, 0.9, 0.9]]
    vratio = ProfilBase(pratio).samples(n)
    w = violonbrutV(xve, freq, vratio)
    play64(w, w)

if __name__ == "__main__":

    t0 = time.time()

    try:
        ntest = int(sys.argv[-1])
    except ValueError:
        ntest = int(input("Quel test ? "))
    print("Test", ntest)

    if ntest == 0:
        pass
    elif ntest == 1:
        explovioloncomp()
    elif ntest == 2:
        variationlongue()
    elif ntest == 10:
        testviolonbrut()
    elif ntest == 11:
        choix()

    versionneur.fairecopienumero(__file__)
    t1 = time.time()
    print("Durée du calcul", t1 - t0)
