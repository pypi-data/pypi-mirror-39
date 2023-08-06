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
# ~/py../Ondes/FourierSynth/fourier3.py

"""
Synthèse d'ondes par superposition d'ondes plus ou moins sinusoïdales
"""

from samplerate import SR
from conversions import (prony2freq, extremum)
from profils import recta
from profilbase import ProfilBase
from canal import CanalMono
from origine import OrigineStr
from sinusrecursif import sinrec

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.07.25, 2012.09.18, 2014.04.14"

############################################################""
class ComposanteA(OrigineStr):
    """Construire un composant élémentaire :
    - un onde sinusoïdale évoluant dans le temps selon un profil,
    munie d'une enveloppe et d'une amplitude mais où
    la variation de hauteur peut être la somme de 2 ou plusieurs profils.
    Pour que la composante soit transposable il faut établir un niveau
    1.0 pour les fréquences (ou 0.0 pour les Pronys)

    On pourrait aussi dire:
       bruit = None
       vibrato = None
    1ère version mise en residus.py"""
    def __init__(self, pvfreq, pvenv, fonction=None):
        """
        pvfreq: description de la variation de fréquence
          #cette description doit être décrite par rapport à une
          #fréquence 1.0 Hz; donc evt doit indiquer la fréquence
          #réelle
        pvenv: description de l'enveloppe
        fonction=None ou autre fonction de génération d'onde):
        """
        OrigineStr.__init__(self)
        if isinstance(pvfreq, (list, tuple)):
            # pvfreq = normeProfil(1.0, pvfreq)
            self.vfreq = ProfilBase(pvfreq)
        elif isinstance(pvfreq, float):
            self.vfreq = ProfilBase([[recta, 1.0, 1.0, 1.0]])
        if isinstance(pvenv, (list, tuple)):
            self.venv = ProfilBase(pvenv)
        elif isinstance(pvenv, float):
            self.venv = ProfilBase([[recta, 1.0, pvenv, pvenv]])

        #self.vaddfreq = None
        #self.vaddenv = None
        if fonction is None:
            self.fonction = sinrec
        else:
            self.fonction = fonction

    def evt(self, duree, freq, optionsfreq=None, optionsenv=None):
        """ construction d'une composante
        optionsX: description de vecteurs additionnels (p.ex. bruit, vibrato)
        Syntaxe:
        freq : float
        optionsX:
           ("+", coeff, fonction, params de la fonction)
           ("*", coeff, fonction, params de la fonction)
           "+" ne produit que peu d'effet
           "*" demande à être bien dosé (dans ce cas ampli <= 2.0)
        Modèle: (voir testcomposante)
           duree, freq = 3.0, 500.0
           optionfreq1 = ("+", 0.10, bruitlocal, (duree, 2.0))
           w = comp.evt(duree, freq, optionsenv=[optionfreq1])
        """
        #from taudio import play64
        n = int(duree * SR)
        vf = self.vfreq.samples(n)
        vf /= vf[0] # autres variantes possibles
        vf *= freq
        ve = self.venv.samples(n)
        if optionsfreq is not None:
            for options in optionsfreq:
                signe, coeff, fonction = options[:3]
                ff = fonction(*options[3:]) * coeff
                #play64(ff, ff)
                #print(vf.max(), ff.max(),)
                if signe == "+":
                    vf += ff
                    #print(vf.max())
                elif signe == "-":
                    ve -= ff
                elif signe == "*":
                    vf *= (1.0 + ff)
                elif signe == "/":
                    vf /= (1.0 + ff)
                    #print(vf.max())
        if optionsenv is not None:
            for options in optionsenv:
                signe, coeff, fonction = options[:3]
                ff = fonction(*options[3:]) * coeff
                if signe == "+":
                    ve += ff
                elif signe == "-":
                    ve -= ff
                elif signe == "*":
                    ve *= (1.0 + ff)
                elif signe == "/":
                    ve /= (1.0 + ff)
        w = self.fonction(vf) * ve
        w /= extremum(w)
        return w

    def evtH(self, duree, hauteur, optionsfreq=None, optionsenv=None):
        " evt en Prony "
        freq = prony2freq(hauteur)
        return self.evt(duree, freq, optionsfreq, optionsenv)

    def change(self):
        """ pour changer """
        pass

############################################################""
class ComposanteF(OrigineStr):
    """Construire un composant élémentaire:
    - un onde sinusoïdale évoluant dans le temps selon un profil,
    munie d'une enveloppe et d'une amplitude mais où
    la variation de hauteur peut être la somme de 2 ou plusieurs profils.
    Pour que la composante soit transposable il faut établir un niveau
    1.0 pour les fréquences (ou 0.0 pour les Pronys)
    1ère version mise en residus.py"""
    def __init__(self, pvfreq, pvenv, fonction=None):
        """
        pvfreq: description de la variation de fréquence
          #cette description doit être décrite par rapport à une
          #fréquence 1.0 Hz; donc evt doit indiquer la fréquence
          #réelle
        pvenv: description de l'enveloppe
        fonction=None ou autre fonction de génération d'onde):
        """
        OrigineStr.__init__(self)
        if isinstance(pvfreq, (list, tuple)):
            # pvfreq = normeProfil(1.0, pvfreq)
            self.vfreq = ProfilBase(pvfreq)
        elif isinstance(pvfreq, float):
            self.vfreq = ProfilBase([[recta, 1.0, 1.0, 1.0]])
        if isinstance(pvenv, (list, tuple)):
            self.venv = ProfilBase(pvenv)
        elif isinstance(pvenv, float):
            self.venv = ProfilBase([[recta, 1.0, pvenv, pvenv]])

        #self.vaddfreq = None
        #self.vaddenv = None
        if fonction is None:
            self.fonction = sinrec
        else:
            self.fonction = fonction

    def evt(self, duree, freq, optionsfreq=None, optionsenv=None):
        """ construction d'une composante
        optionsX: description de vecteurs additionnels (p.ex. bruit, vibrato)
        Syntaxe:
        freq: float
        optionsX:
           ("+", coeff, fonction, params de la fonction)
           ("*", coeff, fonction, params de la fonction)
           "+" ne produit que peu d'effet
           "*" demande à être bien dosé (dans ce cas ampli <= 2.0)
        Modèle: (voir testcomposante)
           duree, freq = 3.0, 500.0
           optionfreq1 = ("+", 0.10, bruitlocal, (duree, 2.0))
           w = comp.evt(duree, freq, optionsenv=[optionfreq1])
        """
        #from taudio import play64
        n = int(duree * SR)
        vf = self.vfreq.samples(n)
        vf /= vf[0] # autres variantes possibles
        vf *= freq
        ve = self.venv.samples(n)
        if optionsfreq is not None:
            for options in optionsfreq:
                signe, coeff, fonction = options[:3]
                ff = fonction(*options[3:]) * coeff
                #play64(ff, ff)
                #print(vf.max(), ff.max(),)
                if signe == "+":
                    vf += ff
                    #print(vf.max())
                elif signe == "-":
                    ve -= ff
                elif signe == "*":
                    vf *= (1.0 + ff)
                elif signe == "/":
                    vf /= (1.0 + ff)
                    #print(vf.max())
        if optionsenv is not None:
            for options in optionsenv:
                signe, coeff, fonction = options[:3]
                ff = fonction(*options[3:]) * coeff
                if signe == "+":
                    ve += ff
                elif signe == "-":
                    ve -= ff
                elif signe == "*":
                    ve *= (1.0 + ff)
                elif signe == "/":
                    ve /= (1.0 + ff)
        w = self.fonction(vf) * ve
        w /= extremum(w)
        return w

    def evtH(self, duree, hauteur, optionsfreq=None, optionsenv=None):
        " evt en Prony "
        freq = prony2freq(hauteur)
        return self.evt(duree, freq, optionsfreq, optionsenv)

    def change(self):
        """ pour changer """
        pass

#####################################################

class ComposanteD(OrigineStr):
    """Construire une composante:
    - une onde sinusoïdale évoluant dans le temps selon un profil
    ('pvhauteur'), munie d'une enveloppe ('pvenv')
    et d'une amplitude ('ampli')
    - à laquelle peuvent s'ajouter une ou plusieurs variations
    attachées soit à la hauteur soit à l'enveloppe, chaque variation
    ayant éventuellement une variation de hauteur, une variation
    d'enveloppe et une ampli.
    Pour que la composante de hauteur de base soit transposable
    il faut établir un niveau 1.0 pour les fréquences
    (ou 0.0 pour les Pronys).
    """
    def __init__(self, pvfreq, pvenv, ampli=1.0, fonction=None,
                 bProny=False):
        """
        pvfreq: description de la variation de fréquence
        pvenv: description de l'enveloppe
        fonction=None ou autre fonction de génération d'onde
        bProny=False, si vrai, il faut faire la conversion
        'prony2freq'):
        """
        OrigineStr.__init__(self)
        self.ampli = ampli
        if isinstance(pvfreq, (list, tuple)):
            self.vfreq = ProfilBase(pvfreq)
        elif isinstance(pvfreq, float): # primaire ??
            self.vfreq = ProfilBase([[recta, 1.0, pvfreq, pvfreq]])

        if isinstance(pvenv, (list, tuple)):
            self.venv = ProfilBase(pvenv)
        elif isinstance(pvenv, float):
            self.venv = ProfilBase([[recta, 1.0, pvenv, pvenv]])

        if fonction is None:
            self.fonction = sinrec
        else:
            self.fonction = fonction
        self.bProny = bProny
        self.addVE = None
        self.addVH = None
        self.addH = None
        self.addE = None

    def adjH(self, pv, pvenv, ampli=1.0, bProny=True):
        """ composante sous forme de profil s'ajoutant à la
        variation de hauteur;
        peut être appelée plusieurs fois."""
        self.addH.append((pv, pvenv, ampli, bProny))

    def adjE(self, pv, pvenv, ampli=1.0, bProny=False):
        """ composante sous forme de profil s'ajoutant à l'enveloppe;
        peut être appelée plusieurs fois."""
        self.addE.append((pv, pvenv, ampli, bProny))

    def adjVH(self, vecteur, pvenv, ampli=1.0, bProny=True):
        """ composante sous forme de vecteur s'ajoutant à la
        variation de hauteur;
        peut être appelée plusieurs fois."""
        self.addVH.append((vecteur, pvenv, ampli, bProny))

    def adjVE(self, vecteur, pvenv, ampli=1.0, bProny=True):
        """ composante sous forme de vecteur s'ajoutant à la
        variation d'enveloppe;
        peut être appelée plusieurs fois."""
        self.addVE.append((vecteur, pvenv, ampli, bProny))

    def evtF(self, duree, freq):
        """ construit une composante de durée 'duree' et de
        fréquence 'freq'
        'duree' en sec
        'freq': float (car la variation se fera selon 'vfreq'"""
        n = int(duree * SR)
        vfreq = self.vfreq.samples(n)
        vfreq /= vfreq[0] # vfreq.mean(), vfreq.max(), extremum(vfreq)
        vfreq *= freq

        for c in self.addH:
            pv, pvenv, ampli, bProny = c
            cfreq = ProfilBase(pv).samples(n)
            if bProny:
                cfreq = prony2freq(cfreq)
            cfreq /= extremum(cfreq)
            cenv = ProfilBase(pvenv).samples(n)
            cenv /= extremum(cenv)
            cfreq *= (cenv * ampli)
            vfreq *= (1.0 + cfreq)

        for c in self.addVH:
            vecteur, pvenv, ampli, bProny = c
            if bProny:
                vecteur = prony2freq(vecteur)
            vecteur = vecteur[:n]
            vecteur /= extremum(vecteur)
            cenv = ProfilBase(pvenv).samples(n)
            cenv /= extremum(cenv)
            vecteur *= (cenv * ampli)
            vfreq *= (1.0 + cfreq)

        w = self.fonction(vfreq)
        env = self.venv.samples(n)

        w *= env
        return w

    def evtH(self, duree, hauteur):
        """ construit une composante de durée 'duree' et de
        hauteur 'hauteur' """
        freq = prony2freq(hauteur)
        return self.evtF(duree, freq)

#####################################################
class FourierSimple(OrigineStr):
    """ Réunit plusieurs sons sinusoïdaux, chaque son ayant sa propre
    enveloppe et son propre ampli. Si un multiplicateur de fréquence
    n'est pas donné, celui ci est égal au no d'ordre de l'enveloppe (n + 1).
    Le profil de variation de fréquence est identique pour tous
    """
    def __init__(self, profilVariaFreq, listeEnveloppes):
        """
        profilVariaFreq: profil de la variation de fréquence
        listeEnveloppes: liste des enveloppes selon la syntaxe
           (profilEnveloppe, ampli) ou
           (profilEnveloppe, ampli, multiplicateurFrequence)
           profilEnveloppe: liste
           ampli, multiplicateurFrequence: float64
        """
        OrigineStr.__init__(self)
        self.pvf = ProfilBase(profilVariaFreq)
        self.penv, self.amplis, self.nharms = [], [], []
        for i, p in enumerate(listeEnveloppes):
            self.penv.append(p[0])
            self.amplis.append(p[1])
            try:
                self.nharms.append(p[3])
            except IndexError:
                self.nharms.append(i+1)

    def evtNF(self, n, freq, opfreq=None):
        """ un événement, n: samples, freq: fréquence de base
        Au lieu de vfreq[0], d'autres  choix sont tout aussi
          raisonnables: vfreq.max(), vfreq.min(), vfreq.mean(),
                      vfreq[-1], vfreq[n/2], etc.
        """
        vfreq = self.pvf.samples(n)
        mSR = SR / 2
        vfreq *= (freq / vfreq[0]) # pour obtenir la fréquence voulue
        c = CanalMono()
        for pe, amp, nh in zip(self.penv, self.amplis, self.nharms):
            if vfreq.max() * nh >= mSR:
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


class FourierSynthStrict(OrigineStr):
    """ Réunit plusieurs composantes pour en faire un son synthétique;
    ces composantes sont réalisées dans des rapports numériques entiers
    allant de 1 à n
    """
    def __init__(self, profilVariaFreq, listeEnveloppes, amplis):
        """
        listeComposantes: liste d'objets de la classe 'ComposanteA'
        amplis: coefficients d'amplification par composante
        """
        OrigineStr.__init__(self)
        self.pvf = ProfilBase(profilVariaFreq)
        self.envs = [ProfilBase(p) for p in listeEnveloppes]
        self.amplis = amplis
        if len(self.amplis) != len(self.envs):
            print("FourierSynthStrict(OrigineStr):")
            print("-> len(self.amplis) != len(self.envs)")

    def evt(self, duree, h, bProny=False, info=False):
        """
        Construit un événement de hauteur et durée données.
        Les fréquences des composantes sont proportionnelles
        à la suite [1:]
        h: hauteur en Hz
        """
        c = CanalMono()
        pt = 0.0
        if bProny:
            freq = prony2freq(h)
        else:
            freq = h
        ndim = int(duree * SR)
        vh0 = self.pvf.samples(ndim)
        vh0 /= vh0.mean()
        vh0 *= freq
        harms = range(1, len(self.amplis)+1)
        for k, penv, ampli in zip(harms, self.envs, self.amplis):
            vh = vh0 * k
            if info:
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
        h: hauteur en Hz
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
        h: hauteur en Hz
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
