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
# Structures/Vibrer/vibrato.py

"""
Le plus simple consiste à utiliser la fonction 'vibrato',
mais on peut aussi faire compliqué.

Le module fournit les classes Vibrato et VibratoBrut.

Projet:
- un vibrato de fréquence : fréquence, amplitude
- un vibrato d'amplitude de même fréquence : fréquence,
   pourcentage d'amplitude ou amplitude.

ProfilBase(ModFreq<liste>).temps(duree) -> ModFreq<vecteur>
sinusN(freq, len(ModFreq<vecteur>) -> Vibrato<vecteur>
ModFreq<vecteur>

ProfilBase(Ampli<liste>) -> Ampli<vecteur>
Ampli<vecteur> += (Vibrato<vecteur> * ampliVibratoAmpli).

Applications possibles:
-- ondeTableMF(table, modfreq)
donc =>
------- ProfilHarmonique -> table
                                 ) -> onde
------- Vibrato(params) -> modfreq

Le vibrato n'est pas seulement applicable au balayage de tables
mais aussi aux ondes par profils et au sinus par récurrence
"""
import numpy as np
from profilbase import ProfilBase
from samplerate import SR
from conversions import extremum, prony2freq, freq2prony
from Ondes.FormesRaides.sinusoides import sinusMF
from sinusrecursif import sinrec
from Outils.ajuster import prolongerN
from Profils.Generateurs.geneprofils import GenerateurProfil
from origine import OrigineStr

__author__ = "Copyright (c) 2008-12 René Bastian (Wissembourg, FRANCE)"
__date__ = """2008.06.30, 09.07.28, 11.02.15, 12.07.27, 2013.01.22"""

def vibrato(duree, pvibfreq, pvibampl, ratio):
    """ construit un vibrato
    Le calcul est effectué en fréquence et retourne un vecteur
    qui est à additionner au vecteur de variation de fréquence
    (en tant que hauteur).
    'ratio' conseillé: 0.005 ... 0.015
    duree : durée
    pvibfreq : profil de la variation de fréquence
    pvibampl : profil de la variation d'amplitude """
    n = int(duree * SR)
    return vibratoN(n, pvibfreq, pvibampl, ratio)

def vibratoN(n, pvibfreq, pvibampl, ratio=1.0, bfreq=True):
    """ construit un vibrato
    Le calcul est effectué en fréquence et retourne un vecteur
    de dimension 'n'.
    (qui est à additionner à un vecteur de variation de fréquence
    (en tant que hauteur).
    anciennement :'ratio' conseillé: 0.005 ... 0.025
    n : nombre de samples
    pvibfreq : profil de la variation de fréquence du vibrato
    pvibampl : profil de la variation d'amplitude du vibrato """
    vvibfreq = ProfilBase(pvibfreq).samples(n)
    vvibampl = ProfilBase(pvibampl).samples(n)
    vvibampl /= extremum(vvibampl)
    vvib = sinrec(vvibfreq) * vvibampl
    if ratio != 1.0:
        vvib *= ratio
    if bfreq:
        return vvib
    else:
        return freq2prony(vvib)

def vibratoV(vfreq, pvibfreq, pvibampl, freqmax, babsolu=False):
    """ ajoute à 'vfreq' un vibrato déterminé par
    'pvibfreq, pvibampl, ratio' """
    vib = vibratoN(vfreq.size, pvibfreq, pvibampl, freqmax)
    if babsolu: # si freqmax est donné en valeur absolue
        return vfreq + vib
    else: # si freqmax est donné en pourcentage de la fréq.max de vfreq
        return vfreq * (1.0 + vib)

def vibratoAleatoire(duree, alea, ratio=0.012, maxfreqvib=8.0,
                     dtmin=0.05, dtmax=0.2,
                     nfreq=None, nampl=None):
    """ construit un vibratoAleatoire.
    Le calcul est effectué en fréquence et retourne un vecteur
    qui est à additionner à le vecteur de variation de fréquence
    (en tant que hauteur).
    duree : durée
    alea : générateur sériel
    ratio : proportion de vibrato par rapport à une amplitude de 1.0
    maxfreqvib : fréquence maximum du vibrato
    dtmin, dtmax : durée min et max des segments du profil
    nfreq : nombre de fréquences différentes du vibrato
    nampl : nombre d'amplitudes différentes du vibrato
    C'est une solution insulaire."""
    dtmoyen = (dtmin + dtmax) / 2
    nseg = int(duree / dtmoyen)
    gp = GenerateurProfil(alea, dtmin, dtmax)
    if nfreq is None:
        nfreq = alea.randint(1, nseg + 4)
    pvibfreq = gp.evt(nfreq)
    if nampl is None:
        nampl = alea.randint(1, nseg + 4)
    pvibampl = gp.evt(nampl)
    n = int(duree * SR)
    vvibfreq = ProfilBase(pvibfreq).samples(n)
    vvibampl = ProfilBase(pvibampl).samples(n)
    vt = np.linspace(0.0, duree, n) * 2 * np.pi * vvibfreq
    vt *= maxfreqvib
    vvib = np.sin(vt) * vvibampl #* ratio #0.006 # 0.012, 0.02 est pas mal
    return vvib * ratio

class VibratoBrut(OrigineStr):
    """ Cette classe ne fournit pas un vecteur de modulation de fréquence
    prêt à être utilisé mais seulement le vecteur du vibrato.
    La fonction utilise le sinus par récurrence.
    """
    def __init__(self, fonctionvibrato=sinrec):
        OrigineStr.__init__(self)
        self.fct = fonctionvibrato

    def samples(self, n, modFreqVib, modAmpliFreqVib, rapport=1.0):
        """
        retourne un vecteur de vibrato de longueur 'n' non encore pondéré
        """
        modfreqvib = ProfilBase(modFreqVib).samples(n)
        modamplifreqvib = ProfilBase(modAmpliFreqVib).samples(n)
        vibr = self.fct(modfreqvib)
        vibr *= modamplifreqvib
        vibr /= extremum(vibr)
        if rapport != 1.0:
            return vibr * rapport
        else:
            return vibr

    def temps(self, duree, modFreqVib, modAmpliFreqVib, rapport=1.0):
        """
        retourne un vecteur de vibrato de durée 'duree' non encore pondéré
        """
        n = int(duree * SR)
        return self.samples(n, modFreqVib, modAmpliFreqVib, rapport)

    def change(self, fonctionvibrato=None):
        """
        Toutes les fonctions 'fct(v)' où 'v' est un vecteur de type
        'numpy.ndarray' conviennent. Donc en général des instances de
        classes ayant une méthode 'fct(v)'
        """
        if fonctionvibrato is not None:
            self.fct = fonctionvibrato

class Vibrato(OrigineStr):
    """ Cette classe fournit des vecteurs de modulation de fréquence
    prêts à être utilisés.
    """
    def __init__(self, fonctionvibrato=sinusMF):

        """
        'fonctionvibrato' ne peut être qu'une fonction
        réagissant à un param-vecteur de variation de hauteur.
        La classe doit réaliser un vibrato - sans trémolo - le schéma suivant:
        modFreqVib -> mfv

        mfv --------------> * PB(modAmpliFreqVib)
                            |
                            v
                            +
        modFreqSon    ----> mf  ---> sortie(mf)
        """
        OrigineStr.__init__(self)
        self.fct = fonctionvibrato

    def samplesF(self, n, modFreqSon, modFreqVib, modAmpliFreqVib, rapport):
        """ retourne un vecteur de modfreq avec vibrato.

        'duree' : durée de l'évènement
        'modFreqSon' : profil-liste de la variation de hauteur
        'modFreqVib' : profil-liste de la variation de fréquence du vibrato
        'modAmpliFreqVib' : profil-liste de la variation d'enveloppe
           de la fréquence du vibrato
        'rapport' : nombre donnant le rapport de l'amplitude du vibrato à la
           fréquence principale.
        """
        modfreqson = ProfilBase(modFreqSon).samples(n)
        modfreqvib = ProfilBase(modFreqVib).samples(n)
        modamplifreqvib = ProfilBase(modAmpliFreqVib).samples(n)
        vibr = self.fct(modfreqvib)
        vibr /= extremum(vibr)
        vibr = vibr * modamplifreqvib * rapport
        modfreqson += vibr
        return modfreqson

    def samplesH(self, n, ModHauteurSon, ModFreqVib, ModAmpliFreqVib, rapport):
        """ retourne un vecteur de modfreq avec vibrato.
        'duree' : durée de l'évènement
        'ModFreqSon' : profil-liste de la variation de hauteur
        'ModFreqVib' : profil-liste de la variation de fréquence du vibrato
        'ModAmpliFreqVib' : profil-liste de la variation d'enveloppe
                            de la fréquence du vibrato
        'rapport' : nombre donnant le rapport de l'amplitude du vibrato à la
           fréquence principale.
        """
        modfreqson = ProfilBase(ModHauteurSon).samples(n)
        modfreqson = prony2freq(modfreqson)
        modfreqvib = ProfilBase(ModFreqVib).samples(n)
        modamplifreqvib = ProfilBase(ModAmpliFreqVib).samples(n)
        vibr = self.fct(modfreqvib)
        vibr /= extremum(vibr)
        vibr, modamplifreqvib, modfreqson = \
            prolongerN((vibr, modamplifreqvib, modfreqson))
        try:
            vibr = vibr * modamplifreqvib * rapport
        except ValueError:
            print("Vibrato.samplesH")
            print("rapport", rapport, "vibr", type(vibr), vibr.size)
            print(type(modamplifreqvib), modamplifreqvib.size)
            return
        modfreqson += vibr
        return modfreqson

    def samples(self, n, modHSon, modFreqVib, modAmpliFreqVib, rapport):
        """ retourne un vecteur de modfreq avec vibrato.

        'duree' : durée de l'évènement
        'modFreqSon' : profil-liste de la variation de hauteur
        'modFreqVib' : profil-liste de la variation de fréquence du vibrato
        'modAmpliFreqVib' : profil-liste de la variation d'enveloppe
           de la fréquence du vibrato
        'rapport' : nombre donnant le rapport de l'amplitude du vibrato à la
           fréquence principale.
        """
        modfreqson = ProfilBase(modHSon).samples(n)
        modfreqson = prony2freq(modfreqson)
        modfreqvib = ProfilBase(modFreqVib).samples(n)
        modamplifreqvib = ProfilBase(modAmpliFreqVib).samples(n)
        vibr = self.fct(modfreqvib)
        vibr /= extremum(vibr)
        vibr = vibr * modamplifreqvib * rapport
        modfreqson += vibr
        return modfreqson

    def __call__(self, duree, modFreqSon, modFreqVib, modAmpliFreqVib,
                 rapport):
        """ retourne un vecteur de modfreq avec vibrato.
        'duree' : durée de l'évènement
        'modFreqSon' : profil-liste de la variation de hauteur principale
        'modFreqVib' : profil-liste de la variation de fréquence du vibrato
        'modAmpliFreqVib' : profil-liste de la variation d'enveloppe
           de la fréquence du vibrato
        'rapport' : nombre donnant le rapport de l'amplitude du vibrato à la
           fréquence principale.
        """
        n = int(duree * SR)
        return self.samplesF(n, modFreqSon, modFreqVib, modAmpliFreqVib,
                             rapport)

def vibrato_obsol_0(duree, phauteur, pfreqvib, pamplifreqvib, rapport):
    """ associe une variation de hauteur à un vibrato
    rapport: trop vague, il faut le mettre en relation avec une hauteur."""
    vh = ProfilBase(phauteur).temps(duree)
    vh = prony2freq(vh)
    vh /= extremum(vh)
    n = len(vh)
    vibra = ProfilBase(pfreqvib).samples(n)
    vampli = ProfilBase(pamplifreqvib).samples(n)
    vibra *= vampli
    vibra /= extremum(vibra)
    vibra *= rapport
    vh += vibra
    return vh

def vibrato_obsol_1(duree, pvibfreq, pvibampl, ratio, maxfreqvib=1.0):
    """ construit un vibrato
    Le calcul est effectué en fréquence et retourne un vecteur
    qui est à additionner à le vecteur de variation de fréquence
    (en tant que hauteur).
    'ratio' conseillé: 0.005 ... 0.015 """
    n = int(duree * SR)
    vvibfreq = ProfilBase(pvibfreq).samples(n)
    vvibampl = ProfilBase(pvibampl).samples(n)
    if maxfreqvib != 1.0:
        vvibfreq /= extremum(vvibfreq)
    vt = np.linspace(0.0, duree, n) * 2 * np.pi * vvibfreq * maxfreqvib
    vvib = np.sin(vt) * vvibampl
    return vvib * ratio

cPRONY = 0
cHz = 1

class VibFreq(OrigineStr):
    """ Cette classe fournit des vecteurs de modulation de fréquence
    prêts à être utilisés.
    Proximité avec modulation de fréquence.
    """
    def __init__(self, descrVF, descrVA,
                 niveauzero=0, fonctionvibrato=sinrec):
        """
        descrVF, descrVA : description de la variation de fréquence
          par un profil et de la variation d'amplitude de cette variation
          de fréquence
        descrVF: profil donnant la variation de fréquence
                  en valeur absolue
        descrVA: la variation d'amplitude correspond au débattement
            en fréquence;
            elle doit être inscrite entre 0.0 et 1.0 de sorte que
            des translations (+

        L'onde 'vf' (décrite par descrVF) a une amplitude de (-1.0, +1.0)
        Le profil 'va' (décrit par descrVA) est l'enveloppe imposée à 'vf'.
        Cette enveloppe de base évolue entre 0.0 et 1.0, ce qui permet
        par multiplication par une amplitude d'obtenir des débattements
         freq +/- ðfreq de n'importe quelle valeur.
        niveauzero : 0, -1, "mean", "median"
        """
        OrigineStr.__init__(self)
        self.fct = fonctionvibrato
        self.pbf = ProfilBase(descrVF, absolu=False)
        self.pba = ProfilBase(descrVA, absolu=False)
        self.nz = niveauzero
        self.bk = None

    def controle(self):
        """ voir si les niveaux sont réguliers """
        xa = self.pba.samples(SR)
        if xa.max() > 1.0:
            self.bk = True

    def temps(self, duree, fmult=1.0, fadd=0.0, fcoeff=1.0):
        """ construit les vecteurs d'une durée 'duree'
        voir 'samples' """
        n = int(duree * SR)
        return self.samples(n, fmult, fadd, fcoeff)

    def samples(self, n, fmult=1.0, fadd=0.0, fcoeff=1.0):
        """ construit les vecteurs de 'n' valeurs
        le profil de var. de fréq est multiplié par 'fcoeff'
        le profil de var. du débattement de la fréq est multiplié par 'fmult'
          et augmenté de 'fadd'
        """
        vibfreq = self.pbf.samples(n)
        vibampl = self.pba.samples(n)
        vibampl /= vibampl.max()
        vibampl = vibampl * fmult + fadd
        return fcoeff * vibfreq * vibampl
