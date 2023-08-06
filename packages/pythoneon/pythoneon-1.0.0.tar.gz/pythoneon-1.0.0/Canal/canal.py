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
# canal.py

"""
fournit:
-- la classe CanalMono : collecteur monophonique de sons en RAM.
-- la classe CanalMulti : collecteur polyphonique de sons en RAM.
-- df record(wg, wd, souche=None, f64=True, raw=True, amorti=1.0)
-- df conforme(wg, wd, amorti=1.0, binfo=False)

#Il est souhaitable qu'il y ait une application 'raw2wav.sh' quelque part
#si on veut faire un en-tête (ou marquage) 'raw -> wav' !!!
PS: je rajoute 'ncompte' à CanalMono

S'il y a un manque de mémoire, utiliser h5canal.py
"""

import os
import subprocess
import numpy as np
from samplerate import SR, MAXINTEGER, plus_petite_valeur
from Outils.ajuster import prolongerZ
from conversions import (extremum, nunc)
from origine import OrigineStr
from Maths.serie import Serie002

__author__ = "Copyright (c) 2017 René Bastian (Wissembourg, FRANCE)"
__date__ = "2017.11.25"

def convert(fnom):
    """ conversion de raw en wav par sox """
    comm = " ".join(["sox -c2 -r44100 -e signed-integer -b16",
                     fnom + ".raw", fnom + ".wav"])
    subprocess.call(comm, shell=True)

def f64toraw(souche, bwav=False, bstereo=True):
    """ convertit souche.0f64 & souche.1f64 en souche.raw """
    if bstereo:
        wg = np.fromfile(souche + ".0f64")
        wd = np.fromfile(souche + ".1f64")
    else:
        wg = np.fromfile(souche + ".f64")
        wd = np.fromfile(souche + ".f64")
    if wg.size != wd.size:
        wg, wd = prolongerZ((wg, wd))
    w = conforme(wg, wd)
    if w.size % 1176 == 0:
        pass
    else:
        a = w.size / 1176
        n = (a + 1) * 1176
        queue = np.zeros(n - w.size, np.int16)
        w = np.concatenate((w, queue))
    w.tofile(souche + ".raw")
    if bwav:
        comm = " ".join(["sox -c2 -r44100 -e signed-integer -b16",
                         souche + ".raw", souche + ".wav"])
        try:
            subprocess.call(comm, shell=True)
        except OSError:
            print("record:conversion raw -> wav pas faite")

def record(wg, wd, souche, bf64=False, braw=True, bwav=True, amorti=1.0):
    """ enregistre les sons avec le nom de fichier 'souche'
    wg, wd : vecteurs doivent être en format 'numpy.ndarray'
    souche.0f64 et souche.1f64 sont nécessaires
    si bf64 -> fichier audio f64 stéréo
    si braw -> souche.raw """
    if wg.size != wd.size:
        wg, wd = prolongerZ((wg, wd))
    wg.tofile("f" + souche + ".0f64")
    wd.tofile("f" + souche + ".1f64")
    cc = np.array((wg, wd))
    cc = np.transpose(cc)
    cc = np.ravel(cc)
    if bf64:
        try:
            cc.tofile(souche + ".f64")
        except ValueError:
            print("record:cc.size", cc.size)
    if bwav:
        braw = True
    if braw:
        w = conforme(wg, wd, amorti)
    #    if w.size % 1176 == 0:
    #        pass
    #    else:
    #        a = w.size // 1176
    #        n = (a + 1) * 1176
    #        queue = np.zeros(n - w.size, np.int16)
    #        #print("record", type(n - w.size))
    #        #print("type n", type(n), "type w.size", type(w.size))
    #        w = np.concatenate((w, queue))
        w.tofile("r" + souche + ".raw")
    if bwav:
        comm = " ".join(["sox -c2 -r44100 -e signed-integer -b16",
                         "r" + souche +  ".raw", "w" + souche + ".wav"])
        try:
            subprocess.call(comm, shell=True)
        except OSError:
            print("record:conversion raw -> wav pas faite")

def recordMono(w, souche, braw=True, bwav=True):
    """ enregistre les sons avec le nom de fichier 'souche'
    w : vecteur doit être en format 'numpy.ndarray'
    souche.0f64 et souche.1f64 sont nécessaires
    si bf64 -> fichier audio f64 mono
    si braw -> souche.raw """
    nomf = "".join(("f", souche, ".0f64"))
    w.tofile(nomf)
    w = conformeMono(w)
    if bwav:
        braw = True
    if braw:
        w.tofile("r" + souche + ".raw")
    if bwav: # conversion raw -> wav
        comm = " ".join(["sox -c1 -r44100 -e signed-integer -b16",
                         "r" + souche +  ".raw", "w" + souche + ".wav"])
        #comm = "play test3Poil.wav" # pour tester
        try:
            subprocess.call(comm, shell=True)
        except OSError:
            print("record:conversion raw -> wav pas faite")
def transposeL(wa, wb, wc, wd):
    """ au lieu de np.transpose """
    c = np.zeros(wa.size * 4)
    for i in range(wa.size):
        c[i] = wa[i]
        c[i+1] = wb[i]
        c[i+2] = wc[i]
        c[i+3] = wd[i]
    return c

def record4(wg, wd, wrg, wrd, souche, bf64=False, braw=True, bwav=False,
            amorti=1.0):
    """ enregistre les sons avec le nom de fichier 'souche'
    wg, wd, wrg, wrd : vecteurs doivent être en format 'numpy.ndarray'
    souche.[0-3]f64 sont nécessaires
    si bf64 -> fichier audio f64 stéréo
    si braw -> souche.raw """
    wa, wb, wc, wd = prolongerZ((wg, wd, wrg, wrd))
    wa.tofile("f" + souche + ".0f64")
    wb.tofile("f" + souche + ".1f64")
    wc.tofile("f" + souche + ".2f64")
    wd.tofile("f" + souche + ".3f64")
    cc = np.array((wa, wb, wc, wd))
    cc = np.transpose(cc)
    cc = np.ravel(cc)
    #cc = transposeL(wa, wb, wc, wd)
    if bf64:
        try:
            cc.tofile(souche + ".f64")
        except ValueError:
            print("record:cc.size", cc.size)
    if bwav:
        braw = True
    if braw:
        # je ne trouve pas de nécessité au nombre 1176
        w = conforme4(wa, wb, wc, wd, amorti)
        #if w.size % 1176 == 0:
        #    pass
        #else:
        #    a = w.size // 1176
        #    n = (a + 1) * 1176
        #    queue = np.zeros(n - w.size, np.int16)
        #    #print("record", type(n - w.size))
        #    #print("type n", type(n), "type w.size", type(w.size))
        #    w = np.concatenate((w, queue))
        w.tofile("r" + souche + ".raw")
    if bwav:
        comm = " ".join(["sox -c4 -r192000 -e signed-integer -b32",
                         "r" + souche +  ".raw", "w" + souche + ".wav"])
        try:
            subprocess.call(comm, shell=True)
        except OSError:
            print("record:conversion raw -> wav pas faite")

def recordinfo(wg, wd, souche, *args):
    """ pour enregistrer
    Enregistre d'une part les fichiers audio dans les formats habituels
    (cd-audio, 0f64, 1f64);
    d'autre part un fichier '.info' contenant
    les params utilisés
    Le nom de fichier comprend la date et l'heure de l'enregistrement.
    AJOUTER LES OPTIONS POUR record ??"""
    zt = nunc()
    fnom = "".join([souche, zt])
    print(fnom)
    record(wg, wd, fnom)
    fnom = "".join([souche, zt, ".info"])
    r = []
    for arg in args:
        r.extend([arg[0], " ", str(arg[1]), "\n"])
    s = "".join(r)
    with open("i" + fnom, "w") as f:
        f.write(s)

def conformeMono(w, amorti=1.0, binfo=False):
    """ tricote . """
    cc = w
    if binfo:
        print("cc.max(), cc.min()", cc.max(), cc.min())
    m = max(cc.max(), np.abs(cc.min()))
    if SR == 44100 or SR == 48000:
        motdecalcul = np.int16
    else:
        motdecalcul = np.int32
    if m == 0.0:
        print("canal.conforme : maximum == 0.0")
    else:
        cc = cc * MAXINTEGER * amorti / m
    try:
        cc = cc.astype(motdecalcul)
    except TypeError:
        print("canal.conforme:np.array(cc, motdecalcul)", motdecalcul)
    return cc

def conforme(wg, wd, amorti=1.0, binfo=False):
    """ tricote le fichier stéréo à partir de deux
    canaux unidimensionnels. """
    cc = np.array((wg, wd))
    cc = np.transpose(cc)
    cc = np.ravel(cc)
    if binfo:
        print("cc.max(), cc.min()", cc.max(), cc.min())
    m = max(cc.max(), np.abs(cc.min()))
    if SR == 44100 or SR == 48000:
        motdecalcul = np.int16
    else:
        motdecalcul = np.int32
    if m == 0.0:
        print("canal.conforme : maximum == 0.0")
    else:
        cc = cc * MAXINTEGER * amorti / m
    try:
        cc = cc.astype(motdecalcul)
    except TypeError:
        print("canal.conforme:np.array(cc, motdecalcul)", motdecalcul)
    return cc

def conforme4(wg, wd, wgr, wdr, amorti=1.0, binfo=False):
    """ tricote le fichier quadro à partir de quatre
    canaux unidimensionnels. """
    cc = np.array((wg, wd, wgr, wdr))
    cc = np.transpose(cc)
    cc = np.ravel(cc)
    if binfo:
        print("cc.max(), cc.min()", cc.max(), cc.min())
    m = max(cc.max(), np.abs(cc.min()))
    if SR == 44100 or SR == 48000:
        motdecalcul = np.int16
    else:
        motdecalcul = np.int32

    if m == 0.0:
        print("canal.conforme : maximum == 0.0")
    else:
        cc = cc * MAXINTEGER * amorti / m
    try:
        cc = cc.astype(motdecalcul)
    except TypeError:
        print("canal.conforme:np.array(cc, motdecalcul)", motdecalcul)
    return cc

class CanalMono(OrigineStr):
    """ 2009.09.25
    permet de placer des vecteurs-sons en un point temporel précis ;
    cette classe est une des plus utilisées et quasiment indépendante
    de tout le reste de 'pythoneon', sauf :
    -- la fonction 'extremum' qui
       donne la plus grand valeur absolue dans un vecteur,
    -- la valeur 'SR' qui représente la fréquence d'échantillonnage,
    -- le contenu de 'numpy'.
    'fin' donne l'exacte mesure du signal - mais la différence n'est
    que de 1/10e de sec. Les grandes traînées quasi nulles proviennent
    des réverbs qui peuvent être coupées (cf coupetraine).
    """
    def __init__(self, dureeInitiale=1.0, divbuffer=0.1):
        """produit une instance d'une duree initiale donnée ;
        si cette durée initiale est insuffisante, elle est
        prolongée par paquets de 0.1 sec.
        La longueur du buffer est ajustable par 'divbuffer'.
        Un certain nombre d'attributs ou fonctions ont été rélégués
        en residus-canal.py
        """
        OrigineStr.__init__(self)
        self.buffer = np.zeros(int(divbuffer * SR)) # np.zeros(SR/divbuffer)
        n = int(dureeInitiale * SR)
        self.a = np.zeros(n)
        self.fin = 0
        self.ncompte = 0
        #print("Canal", SR) # OK

    def addT(self, pt, signal):
        """ajoute le 'signal' au point temporel 'pt'."""
        n = int(pt*SR)
        self.addN(n, signal)

    def addN(self, n, signal, binfo=False):
        """ajoute le signal à partir du sample d'indice 'n'."""
        #ns = len(signal)
        if binfo:
            print("sample", n)
        ns = signal.size
        self.ncompte += 1
        dim = n + ns
        self.fin = max(self.fin, dim)
        if dim > self.a.size:
            k = dim - self.a.size + 1
            self.buffer = np.zeros(k)
        #while dim > self.a.size:
            self.a = np.concatenate((self.a, self.buffer))
        try:
            self.a[n:n+ns] += signal
        except ValueError:
            print("CanalMono:addT/addN:ValueError", "signal", len(signal),)
            print("buffer", self.buffer.size, "n", n, "dim", dim)
            return

    def putT(self, pt, signal):
        """   comme addT mais n'additionne pas """
        n = int(pt*SR)
        self.putN(n, signal)

    def putN(self, n, signal):
        """ajoute le signal à partir du sample d'indice 'n'."""
        #ns = len(signal)
        ns = signal.size
        self.ncompte += 1
        dim = n + ns
        self.fin = max(self.fin, dim)
        if dim > self.a.size:
            k = dim - self.a.size + 1
            self.buffer = np.zeros(k)
        #while dim > self.a.size:
            self.a = np.concatenate((self.a, self.buffer))
        try:
            self.a[n:n+ns] = signal
        except ValueError:
            print("CanalMono:putT/putN:ValueError", "signal", len(signal),)
            print("buffer", self.buffer.size, "n", n, "dim", dim)
            return

    def ex(self, binfo=False):
        " c'est plus simple ... "
        if binfo and (extremum(self.a) > 1.0):
            print("CanalMono.ex(): max = ", extremum(self.a))
        return self.a

    def addX(self, n, y):
        """ additionne la valeur 'y' au sample d'indice 'n'.
        (usage exceptionnel) """
        self.ncompte += 1
        self.buffer = np.zeros(SR/10)
        while n > self.a.size-1:
            self.a = np.concatenate((self.a, self.buffer))
        self.fin = max(self.fin, n)
        self.a[n] += y

    def brut(self):
        """retourne le vecteur-signal, non normé"""
        return self.a[:self.fin]

    def dim(self):
        """retourne le nombre d'éléments du vecteur : len(self.a)"""
        return self.fin

    def duree(self):
        """retourne la durée du vecteur 'self.a'"""
        return float(self.fin) / SR

    def extrait(self, n0, n1):
        """ retourne la partie de vecteur allant de 'n0' à 'n1'
        en nombre de samples"""
        try:
            return self.a[n0:n1]
        except TypeError:
            print("Indice n1 incorrect : essai n0:")
            try:
                return self.a[n0:]
            except TypeError:
                print("Indice n0 incorrect !")
                return None

    def extraitT(self, t0, t1):
        """
        retourne la partie de vecteur allant de 't0' à 't1' en secondes
        """
        n0 = int(SR * t0)
        n1 = int(SR * t1)
        return self.extrait(n0, n1)

    def extraitTN(self, t0, n):
        """
        retourne la partie de vecteur allant de 't0' à 't1' en secondes
        """
        n0 = int(SR * t0)
        return self.a[n0:n0 + n]

    def affiche(self):
        """affiche longueur et durée du vecteur."""
        sforme = "Longueur %15i Duréee %10.5f"
        print(sforme % (self.a.size, float(self.a.size) / SR))

    def boucleT(self, vt, signal, amorti=1.0):
        """ insère le 'signal' aux points temporels donnés
        par 'vt'."""
        a, s = 1.0, signal[:]
        for pt in vt:
            self.ncompte += 1
            s *= a
            self.addT(pt, s)
            a *= amorti

    def boucleN(self, nt, signal, amorti=1.0):
        """ insère le 'signal' aux nos de samples donnés
        par 'nt'."""
        a, s = 1.0, signal[:]
        for n in nt:
            self.ncompte += 1
            s *= a
            self.addN(n, s)
            a *= amorti

    def rec(self, nom, numero, raw=False):
        """ pour écrire un fichier '?f64' """
        self.a.tofile(nom + "." + str(numero) + "f64")
        if raw:
            c = conforme(self.a, self.a)
            c.tofile(nom+".raw")

    def close(self):
        """pour faire semblant de finir."""
        pass


    def autoreverb(self, premiercoeff=0.125, duree=2.0,
                   ecartmin=0.04, ecartmax=0.06,
                   pt=0.0,
                   alea0=1955, alea1=9134):
        """
        Le contenu du canal, 'self.a', est additionné à
        lui-même en intercalant un délai et en appliquant
        un amortissement, ce qui simule une réverbération.
        'pt'  : point temporel en sec où débute la réverbération
        'premiercoeff' : float <=  1.0
        'duree' : durée de la réverb
        'ecartmin, ecartmax' : intervalle entre deux répétitions en sec

        utiliser:
        - premiercoeff = 0.625
        - duree = 3. ... 5.
        """
        epsil = plus_petite_valeur
        alea = Serie002(alea0, alea1)
        ecartmoyen = (ecartmin + ecartmax) / 2.0
        coeff = np.exp((np.log(epsil) - np.log(premiercoeff)) * \
                    ecartmoyen / duree)
        nreflexions = int(np.log(epsil)/np.log(coeff)) + 1
        points = alea.uniform(ecartmin, ecartmax, nreflexions)
        points = np.add.accumulate(points) + pt
        signal = self.a
        signal = signal * premiercoeff
        for ptr in points:
            self.addT(ptr, signal)
            signal = signal * coeff

class CanalMulti(OrigineStr):
    """ plusieurs canaux CanalMono """
    def __init__(self, ncanals, dureeInitiale=1.0, divbuffer=10):
        """produit une instance d'une duree initiale donnée ;
        si cette durée initiale est insuffisante, elle est
        prolongée par paquets de 0.1 sec.
        La longueur du buffer est ajustable, soit
        par 'divbuffer' soit par la méthode 'setbuffer'.
        """
        OrigineStr.__init__(self)
        self.b = [CanalMono(dureeInitiale, divbuffer)
                  for _ in range(ncanals)]
        self.ncanals = ncanals

    def addT(self, pt, signals):
        """ajoute les 'signals' au point temporel 'pt'."""
        for i, signal in enumerate(signals):
            self.b[i].addT(pt, signal)

    def addN(self, n, signals):
        """ajoute les signals à partir du sample d'indice 'n'."""
        for i, signal in enumerate(signals):
            self.b[i].addN(n, signal)

    def ex(self):
        """ retourne l'ensembel des vecteurs
        Comme les panos sont déjà affectés, les
        maxima sont laissés tels quels (pas de:mise à la norme 1.) """
        return [self.b[i].a for i in range(self.ncanals)]

    def brut(self):
        """ est identique à ex()
        retourne l'ensembel des vecteurs
        Comme les panos sont déjà affectés, les
        maxima sont laissés tels quels (pas de:mise à la norme 1.) """
        return self.ex()

    def dim(self):
        "la dimension la plus longue"
        a = 0
        for i in range(self.ncanals):
            a = max(self.b[i].dim(), a)
        return a

    def duree(self):
        "la durée la plus longue"
        return float(self.dim()) / SR

    def rec(self, nom64=None, nom=None, bwav=False):
        """ effectue l'enregistrement des canaux """
        if nom64 is not None:
            for i in range(self.ncanals):
                xnom = "".join([nom64, ".", str(i), "f64"])
                self.b[i].tofile(xnom)
        if (nom is not None) and self.ncanals == 2:
            c = conforme(self.b[0], self.b[1])
            c.tofile(nom+".raw")
            if bwav:
                comm = " ".join(["sox -c2 -r44100 -e signed-integer -b 16",
                                 nom+".raw", nom+".wav"])
                try:
                    os.system(comm)
                except TypeError:
                    print("sox: conversion en fichier wav impossible")
        return
