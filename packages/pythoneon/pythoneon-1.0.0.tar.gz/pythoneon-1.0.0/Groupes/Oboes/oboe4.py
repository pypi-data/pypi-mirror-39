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
# oboe4.py

"""
fournit la classe Oboe09 ;
voir la fonction oboe pour les préliminaires.
"""

__author__ = "Copyright (c) 2005 René Bastian (Wissembourg, FRANCE)"
__date__ = "2006.09.26, 2009.10.08, 2013.08.04"

import numpy as np
from samplerate import sr
from conversions import (prony2freq, extremum)
from origine import OrigineStr
from profilbase import ProfilBase
#from profilbaseplus import ProfilBasePlus
from profils import recta
from ondepartable import ondeTable
from serie import Serie002
from faireprofils import FaireTable
from profil08 import Profil08
#from guirlande0 import Guirlande2 as Guirlande
#from canal import CanalMono

class Oboe(OrigineStr):
    """
    la classe Oboe construit un timbre ayant une
    ressemblance avec le haut-bois ... ou avec l'accordéon :-)
    Il ne faut pas hésiter à changer le 'ProfilHarmonique'
    ou le 'nombre' d'harmoniques.

    Mais n'est-il pas plus efficace de dessiner la forme d'onde et de
    regarder l'analyse harmonique que de vouloir dessiner
    le profil harmonique pour obtenir une table d'onde ?
    """
    def __init__(self, profiltable=None, minimum=0.7, alea=None,
                 multi=1):
        """
        'profiltable' : profil dessinant la table
        'minimum' : minimum de la valeur que peut prendre une harmonique
        alea : générateur sériel
        multi : multiplicateur de la dimension de la table
        """
        OrigineStr.__init__(self)
        self.multi = int(multi)
        self.dimtable = self.multi * sr
        if profiltable is None:
            self.profiltable = [[recta, 0.1, 0.0, 1.0],
                                [recta, 2.0, 1.0, 0.5],
                                [recta, 1.0, 0.5, 0.0]]
        self.table = ProfilBase(self.profiltable).samples(self.dimtable)
        if alea is None:
            self.alea = Serie002(765641, 532988)
        else:
            self.alea = alea
        self.minimum = minimum
        bruit = self.alea.uniform(self.minimum, 1.0, self.dimtable)
        self.table *= bruit
        # ? avoir une table brute et une table sérielle ?
        #print("longueur de la table", self.table.size)

    def evt(self, duree, h, bprony=True):
        " un événement "
        if isinstance(h, float):
            vh = ProfilBase([[recta, 1.0, h, h]]).temps(duree)
            if bprony:
                vh = prony2freq(vh)
        elif isinstance(h, np.ndarray):
            # duréee est inutile ?
            if bprony:
                vh = prony2freq(h)
        elif isinstance(h, list):
            vh = ProfilBase(h).temps(duree)
            if bprony:
                vh = prony2freq(vh)
        w = self.evtV(vh)
        return w / extremum(w)

    def evtTBrut(self, duree, pH):
        """
        construit un son de durée 'duree' selon pH
        pH : variation de la hauteur en prony
        """
        n = int(duree * self.multi * sr)
        return self.evtNBrut(n, pH)

    def evtNBrut(self, n, pH):
        """
        construit un son de dimension 'n' selon pH
        pH : variation de la hauteur en prony
        """
        varf = ProfilBase(pH).samples(n)
        varf = prony2freq(varf)
        return self.evtV(varf)

    def evtV(self, varf):
        """ applique le vecteur de variation de fréquence à la table """
        w = ondeTable(self.table, varf)
        ix = np.arange(0, w.size, self.multi)
        return w[ix]

    def change(self, profiltable=None, minimum=None, alea=None,
               multi=None):
        " pour changer "
        if profiltable is not None:
            self.profiltable = profiltable
        if alea is not None:
            self.alea = alea
        if minimum is not None:
            self.minimum = minimum
        if multi is not None:
            self.multi = int(multi)
        self.dimtable = self.multi * sr
        self.table = ProfilBase(self.profiltable).samples(self.dimtable)
        bruit = self.alea.uniform(self.minimum, 1.0, self.dimtable)
        self.table *= bruit

class Oboe000(OrigineStr):
    """
    la classe Oboe000 construit un timbre ayant une
    ressemblance avec le haut-bois ... ou avec l'accordéon :-)
    Il ne faut pas hésiter à changer le 'ProfilHarmonque'
    ou le 'nombre' d'harmoniques.
    Cette version a été utilisée dans Tussilago
    Critique:
      - def mf est inutile
      - __call__ est à renommer
      - def evt est à nettoyer
      - def evtPlus est à simplier ou à complexifier plus intelligemment
      - def evtFreq est à refaire
    """
    def __init__(self, profilHarmonique = None, nombre = 12, minimum = 0.7,
                 xx=765641, xa=532988):
        """
        'minimum' : minimum de la valeur que peut prendre une harmonique
        """
        OrigineStr.__init__(self)
        if not profilHarmonique:
            profilHarmonique = [[recta, 0.1, 0.0, 1.0],
                                [recta, 2.0, 1.0, 0.5],
                                [recta, 1.0, 0.5, 0.0]]
        ft = FaireTable(profilHarmonique, nombre, minimum, xx, xa)
        print(ft)
        self.table = ft()
        #ft.plot()

    def mf(self, freqs):
        "retourne le signal correspondant à 'freqs'"
        return ondeTable(self.table, freqs)

    def __call__(self, duree, ProfilVarProny, debug=False):
        """
        retourne une onde dont la hauteur suit 'ProfilVarProny'
        et de durée 'duree'.
        'ProfilVarProny' : profil-liste en prony
        """
        mf = ProfilBase(ProfilVarProny).temps(duree)
        if debug:
            print("Oboe000", duree, "->", len(mf)/float(sr))
            print(ProfilVarProny)
        mf = prony2freq(mf)
        w = ondeTable(self.table, mf)
        # j'ai constaté que certaines ondes ne sont pas sym autour de l'axe
        # mais ce n'est pas le meilleur moyen ...
        xmin, xmax = w.min(), w.max()
        dx = (xmax - xmin) / 2
        w -= dx
        return w

    def evt(self, duree, ProfilVarFreq):
        """
        retourne une onde dont la hauteur suit 'ProfilVarFreq'
        et de durée 'duree'.
        'ProfilVarFreq' : profil-liste en Hz
        """
        #print(duree, ProfilVarFreq)
        try:
            mf = ProfilBase(ProfilVarFreq).temps(duree)
        except TypeError:
            mf = Profil08(ProfilVarFreq).temps(duree)
        return ondeTable(self.table, mf) #Tables/ondepartable.py
#
#    def evtPlus(self, duree, ProfilVarProny, rapport, dt):
#        """
#        retourne une onde dont la hauteur suit 'ProfilVarProny'
#        et de durée 'duree'.
#        'ProfilVarProny' : profil-liste en prony
#        'rapport' : rapport de variation sérielle-aléatoire
#        'dt' : couple de valeurs de laps de temps '(dtmin, dtmax)'
#          dans lequel varie la durée du fragment de profil
#        """
#        mf = ProfilBasePlus(ProfilVarProny).temps(duree, rapport, dt)
#        mf = prony2freq(mf)
#        return ondeTable(self.table, mf)

    def evtFreq(self, h, duree):
        """ construit une onde avec un profil de hauteur fixe """
        P = [[recta, duree, h, h]]
        return self.evt(duree, P)

#class Oboe001(Oboe000):
#    """
#    la classe Oboe001 construit un timbre ayant une
#    ressemblance avec le haut-bois (classe Oboe000)
#    et retourne des traits.
#    """
#    def __init__(self, profilHarmonique=None, nombre=12, minimum = 0.7,
#                 xx=765641, xa=532988):
#        """
#        'minimum' : minimum de la valeur que peut prendre une harmonique
#        """
#        if not profilHarmonique:
#            profilHarmonique = [[recta, 0.1, 0.0, 1.0],
#                                [recta, 2.0, 1.0, 0.5],
#                                [recta, 1.0, 0.5, 0.0]]
#        Oboe000.__init__(self, profilHarmonique, nombre, minimum, xx, xa)
#        ft = FaireTable(profilHarmonique, nombre, minimum, xx, xa)
#        self.table = ft()
#        self.alea = Serie002(xx, xa)
#        self.g = Guirlande()
#        self.e = ProfilBase([[recta, (0.02), 0.0, 1.0],
#                                [recta,  1.,    1.0, 1.0],
#                                [recta, (0.02), 1.0, 0.0]])
#
#        #self.p = ProfilBase([[recta, 1.0, 0.0, 1.0]])
#        self.p = ProfilBase([[recta, 1.0, self.alea.uniform(0.0, 1.0),
#                                 self.alea.uniform(0.0, 1.0)]])
#
#    def setEnv(self, enveloppe):
#        "pour entrer l'enveloppe"
#        self.e = ProfilBase(enveloppe)
#
#    def setPano(self, pano):
#        "pour entrer le pano"
#        self.p = ProfilBase(pano)
#
#    def __call__(self, Suite):
#        """
#        cette méthode utilise l'Enveloppe et le Pano
#        précédemment installés ;
#        suites = [(methode, duree, dt, Freqs),
#        (methode, duree, dt, Freqs),
#        (methode, duree, dt, Freqs), ...]
#        plutôt
#        suites = [(duree, dt, Freqs),
#                  (duree, dt, Freqs),
#                  (duree, dt, Freqs), ...]
#        """
#        MF = []
#        for suite in Suite:
#            MF.append(self.g.fac(*suite))
#        mf = np.concatenate(MF)
#        #print(len(mf))
#        w = ondeTable(self.table, mf)
#        env = self.e.samples(w.size)
#        pano = self.p.samples(w.size)
#        #w, env, pano = _a.prolongerN(w, env, pano)
#        w = w * env
#        wg = w * pano
#        wd = w * (1. - pano)
#        extr = max(extremum(wg), extremum(wd))
#        wg, wd = wg/extr, wd/extr
#        return wg, wd
#
#    def evt(self, Suite):
#        return self.__call__(Suite)
#
#    def evtR(self, Suite, Reverb):
#        """
#        comme evt mais avec une réverb unique
#        (je pense qu'il est inutile de mettre une réverb par guirlande)
#        """
#        wg, wd = self.evt(Suite)
#        retard, dureeRev, dtRevMin, dtRevMax = Reverb
#        #cg = CanalMono2()
#        #cd = CanalMono2()
#        cg = CanalMono()
#        cd = CanalMono()
#
#        cg.addT(0.0, wg)
#        cd.addT(0.0, wd)
#        #cg.autoreverb(retard, dureeRev, dtRevMin, dtRevMax)
#        #cd.autoreverb(retard, dureeRev, dtRevMin, dtRevMax)
#        return cg.a, cd.a
#
#    def evtF(self, LFreqs, duree, dt, Env, Pano):
#        """
#        guirlande de sons haut-sylvestres ;
#        Env et Pano sont renouvelés à  chaque appel ;
#        'LFreqs' : liste des fréquences
#        'duree' : duree d'un ton de guirlande
#        'dt' : temps de transition entre deux tons
#        'Env' : enveloppe (profil-liste) de l'ensemble
#        'Pano' : pano  (profil-liste) de l'ensemble
#        duree, dt = 1./12, 1./96
#        Env = [[recta, (dt), 0.0, 1.0],
#           [recta, 5.0, 1.0, 1.0],
#           [recta, 4.0, 1.0, 0.0]]
#        Pano = [[recta, 2.0, 0.5, 0.5],
#            [recta, 1.0, 0.5, 0.25],
#            [recta, 1.0, 0.25, 0.75]]
#        """
#        self.e = ProfilBase(Env)
#        #mf = self.g.traitG(duree, dt, LFreqs)
#        mf = self.g.evt(duree, dt, LFreqs)
#        w = ondeTable(self.table, mf)
#        env = self.e.samples(w.size)
#        self.p = ProfilBase(Pano)
#        pano = self.p.samples(w.size)
#        #w, env, pano = _a.prolongerN(w, env, pano)
#        w = w * env
#        wg = w * pano
#        wd = w * (1. - pano)
#        extr = max(extremum(wg), extremum(wd))
#        wg, wd = wg/extr, wd/extr
#        #print(extremum(wg), extremum(wd))
#        return wg, wd
#
#    def evtFR(self, LFreqs, duree, dt, Env, Pano,
#              retard, dureeRev, dtRevMin, dtRevMax):
#        """
#        méthode la plus complète (__call__ ??)
#        évènement avec réverb
#        'retard' : retard initial de la réverb
#        'dureeRev' : durée de la réverb
#        'dtRevMin, dtRevMax' : ecarts min et max entre deux
#        échos ;
#        les autres params comme dans evtF ;
#        dureeRev = 2.0
#        dtRev = dt*2
#        retard = 0.125
#        """
#        wg, wd = self.evtF(LFreqs, duree, dt, Env, Pano)
#        cg = CanalMono()
#        cd = CanalMono()
#        cg.addT(0.0, wg)
#        cd.addT(0.0, wd)
#        #cg.autoreverb(retard, dureeRev, dtRevMin, dtRevMax)
#        #cd.autoreverb(retard, dureeRev, dtRevMin, dtRevMax)
#        return cg.a, cd.a
#
#class Oboe002(Oboe000):
#    """
#    la classe Oboe001 construit un timbre ayant une
#    ressemblance avec le haut-bois (classe Oboe000)
#    et retourne des traits.
#    """
#    def __init__(self,
#                 profilHarmonique = None,
#                 nombre = 12,
#                 minimum = 0.7,
#                 xx=765641, xa=532988):
#        """
#        'minimum' : minimum de la valeur que peut prendre une harmonique
#        """
#        if not profilHarmonique:
#            profilHarmonique = [[recta, 0.1, 0.0, 1.0],
#                                [recta, 2.0, 1.0, 0.5],
#                                [recta, 1.0, 0.5, 0.0]]
#        Oboe000.__init__(self, profilHarmonique, nombre, minimum, xx, xa)
#        ft = FaireTable(profilHarmonique, nombre, minimum, xx, xa)
#        self.table = ft()
#        self.alea = Serie002(xx, xa)
#        self.g = Guirlande()
#        self.e = ProfilBase([[recta, (0.02), 0.0, 1.0],
#                                [recta,  1.,    1.0, 1.0],
#                                [recta, (0.02), 1.0, 0.0]])
#
#        #self.p = ProfilBase([[recta, 1.0, 0.0, 1.0]])
#        self.p = ProfilBase([[recta, 1.0, self.alea.uniform(0.0, 1.0),
#                                 self.alea.uniform(0.0, 1.0)]])
#
#    def setEnv(self, enveloppe):
#        "pour entrer l'enveloppe"
#        self.e = ProfilBase(enveloppe)
#
#    def setPano(self, pano):
#        "pour entrer le pano"
#        self.p = ProfilBase(pano)
#
