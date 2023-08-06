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
# ~/py../Ondes/FourierSynth/fourier.py

"""
Synthèse d'ondes par superposition d'ondes plus ou moins sinusoïdales

Voir aussi composantes.py et fourier?.py
"""
import numpy as np
from samplerate import SR
from conversions import (prony2freq, extremum)
from profils import (afficheprofil)
from profilbase import ProfilBase
from canal import CanalMono
from origine import OrigineStr
from sinusrecursif import sinrec

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.07.25, 2012.09.18, 2014.04.14"


#####################################################
class FourierSimple(OrigineStr):
    """ Réunit plusieurs sons sinusoïdaux, chaque son ayant sa propre
    enveloppe et son propre ampli. Si un multiplicateur de fréquence
    n'est pas donné, celui ci est égal au no d'ordre de l'enveloppe (n + 1).
    Le profil de variation de fréquence est identique pour tous
    les harmoniques.
    Un vibrato (ou autre variation de fréquence ajoutée) est aussi
    identique pour tous les harmoniques.
    """
    def __init__(self, profilVariaFreq, listeEnveloppes, binfo=False):
        """
        profilVariaFreq : profil de la variation de fréquence
        listeEnveloppes : liste des enveloppes selon la syntaxe
           (profilEnveloppe, ampli) ou
           (profilEnveloppe, ampli, multiplicateurFrequence)
           profilEnveloppe : liste
           ampli, multiplicateurFrequence : float64
        """
        OrigineStr.__init__(self)
        self.pvf = ProfilBase(profilVariaFreq)
        self.penv, self.amplis, self.nharms = [], [], []
        for i, p in enumerate(listeEnveloppes):
            self.penv.append(p[0])
            self.amplis.append(p[1])
            try:
                self.nharms.append(p[2])
            except IndexError:
                self.nharms.append(i+1)
        self.binfo = binfo

    def afficher(self):
        " afficher "
        afficheprofil(self.pvf.listep)
        for p in self.penv:
            afficheprofil(p)

    def setinfo(self, b):
        """ info ou pas """
        self.binfo = b

    def evtNF(self, n, freq, opfreq=None):
        """ un événement, n : samples, freq : fréquence de base
        Au lieu de vfreq[0], d'autres  choix sont tout aussi
          raisonnables: vfreq.max(), vfreq.min(), vfreq.mean(),
                      vfreq[-1], vfreq[n/2], etc.
        """
        vfreq = self.pvf.samples(n)
        print("vfreq", vfreq, n)
        msr = SR // 2
        vfreq *= (freq / vfreq[0]) # pour obtenir la fréquence voulue
        c = CanalMono()
        for _, pe, amp, nh in zip(range(len(self.penv)),
                                  self.penv, self.amplis, self.nharms):
            if int(vfreq.max()) * nh >= msr: # ???
                continue
            if opfreq is not None:
                pvibfreq, pvibenv, coeff = opfreq
                vibfreq = ProfilBase(pvibfreq).samples(n)
                vibenv = ProfilBase(pvibenv).samples(n)
                wvib = sinrec(vibfreq) * vibenv
                wvib /= extremum(wvib)
                wvib *= coeff
                vfreq *= (1.0 + wvib)
            env = ProfilBase(pe).samples(n)
            w = sinrec(vfreq * nh)
            w *= amp * env
            c.addT(0.0, w)
        return c.a / extremum(c.a)

    def evt(self, duree, hprony, opfreq=None):
        """ le cas général ? """
        n = int(duree * SR)
        freq = prony2freq(hprony)
        return self.evtNF(n, freq, opfreq)

    def change(self):
        " pour changer "
        pass

    def evtNFexplo(self, n, freq, opfreq=None):
        """ version d'exploration
        un événement, n : samples, freq : fréquence de base
        Au lieu de vfreq[0], d'autres  choix sont tout aussi
          raisonnables: vfreq.max(), vfreq.min(), vfreq.mean(),
                      vfreq[-1], vfreq[n/2], etc.
        """
        vfreq = self.pvf.samples(n)
        print("vfreq", vfreq, n)
        msr = SR // 2
        vfreq *= (freq / vfreq[0]) # pour obtenir la fréquence voulue
        c = CanalMono()
        for _, pe, amp, nh in zip(range(len(self.penv)),
                                  self.penv, self.amplis, self.nharms):
            if self.binfo:
                print("***", vfreq.max(), nh, msr)
            if int(vfreq.max()) * nh >= msr: # ???
                continue
            if opfreq is not None:
                pvibfreq, pvibenv, coeff = opfreq
                vibfreq = ProfilBase(pvibfreq).samples(n)
                vibenv = ProfilBase(pvibenv).samples(n)
                wvib = sinrec(vibfreq) * vibenv
                wvib /= extremum(wvib)
                wvib *= coeff
                vfreq *= (1.0 + wvib)
            if self.binfo:
                try:
                    afficheprofil(pe)
                except TypeError:
                    print("TypeError:pe", pe)
            env = ProfilBase(pe).samples(n)
            #env.tofile("fourier_env" + str(i)+".raw")
            w = sinrec(vfreq * nh)
            w *= amp * env
            c.addT(0.0, w)
        return c.a / extremum(c.a)

class FourierSynthStrict(OrigineStr):
    """ Réunit plusieurs composantes pour en faire un son synthétique;
    ces composantes sont réalisées dans des rapports numériques entiers
    allant de 1 à n
    """
    def __init__(self, profilVariaFreq, listeEnveloppes, amplis):
        """
        listeComposantes : liste d'objets de la classe 'ComposanteA'
        amplis : coefficients d'amplification par composante
        """
        OrigineStr.__init__(self)
        self.pvf = ProfilBase(profilVariaFreq)
        self.envs = [ProfilBase(p) for p in listeEnveloppes]
        self.amplis = amplis
        if len(self.amplis) != len(self.envs):
            print("FourierSynthStrict(OrigineStr):")
            print("len(amplis)", len(amplis), "!= len(envs)", len(self.envs))
            self.nharms = min(len(amplis), len(self.envs))
        else:
            self.nharms = len(amplis)
    def evt(self, duree, prony, binfo=False):
        """
        Construit un événement de hauteur et durée données.
        Les fréquences des composantes sont proportionnelles
        à la suite [1:]
        h : hauteur en Hz
        """
        c = CanalMono()
        pt = 0.0
        freq = prony2freq(prony)
        ndim = int(duree * SR)
        vh0 = self.pvf.samples(ndim)
        vh0 /= vh0.mean()
        vh0 *= freq
        vnharms = np.arange(1, self.nharms+1)
        for k, penv, ampli in zip(vnharms, self.envs, self.amplis):
            vh = vh0 * k
            if binfo:
                print("Harmonique", k, vh, penv, ampli)
            w = sinrec(vh)
            env = penv.samples(w.size)
            w *= env
            w *= ampli
            c.addT(pt, w)
        return c.a

    def change(self):
        "pour changer "
        pass

#####################################################

class FourierSynthInharm(OrigineStr):
    """ Réunit plusieurs composantes pour en faire un son synthétique;
    ces composantes sont réalisés dans des rapports numériques harmoniques
    ou non harmoniques.
    """
    def __init__(self, profilVariaFreq, listeEnvAmpHarm):
        """
        profilVariaFreq: profil de variation de la fréquence qui est
             appliqué à tous les composants;
        listeEnvAmpHarm: liste de tuples
             [(profil d'enveloppe, ampli, coefficient (in)harmonique),
              (profil d'enveloppe, ampli, coefficient (in)harmonique),
              ...
              (profil d'enveloppe, ampli, coefficient (in)harmonique)]
        """
        OrigineStr.__init__(self)
        self.pvf = ProfilBase(profilVariaFreq)
        self.envs, self.amplis, self.coeffs = [], [], []
        for e, a, c in listeEnvAmpHarm:
            self.envs.append(ProfilBase(e))
            self.amplis.append(a)
            self.coeffs.append(c)

    def evt(self, duree, h, bProny=False, info=False):
        """
        Construit un événement de hauteur et durée données.
        Les fréquences des composantes sont proportionnelles
        à la suite [1:]
        h : hauteur en Hz
        """
        c = CanalMono()
        pt = 0.0
        if bProny:
            freq = prony2freq(h)
        else:
            freq = h
        ndim = int(duree * SR)
        vh0 = self.pvf.samples(ndim)
        vh0 /= vh0.mean() # solution bancale ???
        vh0 *= freq
        for coeff, penv, ampli in zip(self.coeffs, self.envs, self.amplis):
            vh = vh0 * coeff
            if info:
                print("Harmonique", coeff, vh, penv, ampli)
            w = sinrec(vh)
            env = penv.samples(w.size)
            w *= env
            w *= ampli
            c.addT(pt, w)
        return c.a

    def change(self):
        "pour changer "
        pass

##########################################################"
class FourierSynthGenerale(OrigineStr):
    """ Réunit plusieurs composantes pour en faire un son synthétique.
    Chaque composante a sa propre enveloppe de variation de hauteur.
    """
    def __init__(self, listeFreqEnvAmpHarm):
        """
        profilVariaFreq: profil de variation de la fréquence qui est
             appliqué à tous les composants;
        listeEnvAmpHarm: liste de tuples
             [(profil de hauteur, profil d'enveloppe, ampli,
                  coefficient (in)harmonique),
              (profil de hauteur, profil d'enveloppe, ampli,
                  coefficient (in)harmonique),
              ...
              (profil de hauteur, profil d'enveloppe, ampli,
                  coefficient (in)harmonique)]
        """
        OrigineStr.__init__(self)
        self.pvf, self.envs, self.amplis, self.coeffs = [], [], [], []
        for h, e, a, c in listeFreqEnvAmpHarm:
            self.pvf.append(ProfilBase(h))
            self.envs.append(ProfilBase(e))
            self.amplis.append(a)
            self.coeffs.append(c)

    def evt(self, duree, h, bProny=False, info=False):
        """
        Construit un événement de hauteur et durée données.
        Les fréquences des composantes sont proportionnelles
        à la suite [1:]
        h : hauteur en Hz
        """
        c = CanalMono()
        pt = 0.0
        if bProny:
            freq = prony2freq(h)
        else:
            freq = h
        ndim = int(duree * SR)
        for vh0, coeff, penv, ampli in zip(self.pvf, self.coeffs,
                                           self.envs, self.amplis):
            vh = vh0.samples(ndim)
            vh /= vh.mean() # solution bancale ???
            vh = vh0 * freq * coeff
            if info:
                print("Harmonique", coeff, vh, penv, ampli)
            w = sinrec(vh)
            env = penv.samples(w.size)
            w *= env
            w *= ampli
            c.addT(pt, w)
        return c.a

    def change(self):
        "pour changer "
        pass
