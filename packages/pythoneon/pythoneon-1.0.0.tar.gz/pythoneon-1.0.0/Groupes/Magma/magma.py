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
# Groupes/Magma/magma.py

""" fournit la classe Magma """
import numpy as np
from samplerate import sr
from conversions import prony2freq
from profilbase import ProfilBase
from ondepartable import ondeTable
from filtrefixe import FiltreFixe
from multiplier import Multiplier
from canal import CanalMono
from origine import OrigineStr

__author__ = "Copyright (c) 2014 René Bastian (Wissembourg, FRANCE)"
__date__ = "2014.11.11"

class MagmaDroit(OrigineStr):
    """ pour construire des spectres complexes en superposant des
    formes d'ondes générées par tables
    avec variation de hauteur, enveloppe et amplitude propre
    au choix avec modulation en anneau, réverb cumulative, filtrage fixe
    ou variable
    """
    def __init__(self, table, filtre=None, bProny=False):
        """ tous les params sont initialisés à l'extérieur de la classe;
        table : table utilisée par le balayage
        filtre : filtre passe-bas
        multi : instance de Multi
        revcum : instance de ReverberationCumulative """
        OrigineStr.__init__(self)
        self.table = table
        if filtre is None:
            self.filtre = FiltreFixe("pb", 40)
        else:
            self.filtre = filtre
        self.multi = Multiplier()
        #self.revcum = revcum
        self.bProny = bProny

    def evt(self, freq, freqrm, duree, pEnv):
        """ construction d'un événement isolé
        freq : fréquence de base
        freqrm : fréquence de la modulation en anneau (Ringmodulation)"""
        if self.bProny:
            print("MagmaDroit n'utilise pas la hauteur en Prony ")
            return
        n = int(duree * sr)
        mf = np.ones(n) * freq
        w = ondeTable(self.table, mf)
        w = self.multi.evt(w, freqrm)
        w = self.filtre.evt(w)
        env = ProfilBase(pEnv).samples(w.size)
        w *= env
        return w

    def change(self):
        " pour changer "
        print(self)
        print("Pour changer: réinitialiser")

class Magma(OrigineStr):
    """ pour construire des spectres complexes en superposant des
    formes d'ondes générées par tables
    avec variation de hauteur, enveloppe et amplitude propre
    au choix avec modulation en anneau, réverb cumulative, filtrage fixe
    ou variable
    """
    def __init__(self, table, pProny, pEnv, filtre, multi, revcum, pRM,
                 bProny=True):
        """ tous les params sont initialisés à l'extérieur de la classe;
        pProny, pEnv, pRM sont des instances de ProfilBase;
        table : table utilisée par le balayage
        pProny : profil de la variation de hauteur (freq ou prony)
        pEnv : profil de l'enveloppe
        pRM : profil de la variation de hauteur de la RM
        filtre : filtre passe-bas
        multi : instance de Multi
        revcum : instance de ReverberationCumulative """
        OrigineStr.__init__(self)
        self.table = table
        self.pProny = ProfilBase(pProny)
        self.pEnv = ProfilBase(pEnv)
        self.pRM = ProfilBase(pRM)
        self.filtre = filtre
        self.multi = multi
        self.revcum = revcum
        self.bProny = bProny

    def change(self, table=None, pProny=None, pEnv=None, filtre=None,
               revcum=None, pRM=None, bProny=None):
        " pour changer "
        if table is not None:
            self.table = table
        if pProny is not None:
            self.pProny = ProfilBase(pProny)
        if pEnv is not None:
            self.pEnv = ProfilBase(pEnv)
        if filtre is not None:
            self.filtre = filtre
        if revcum is not None:
            self.revcum = revcum
        if pRM is not None:
            self.pRM = ProfilBase(pRM)
        if bProny is not None:
            self.bProny = bProny

    def evt(self, hprony, duree, hrm=None, pano=None):
        """ construction d'un événement isolé """
        mf = self.pProny.temps(duree)
        if self.bProny:
            mf += hprony
            mf = prony2freq(mf)
        else:
            mf *= hprony
        w = ondeTable(self.table, mf)
        # il faut décider si la RM est différente pour chaque evt ou non
        if hrm is not None:
            if self.bProny:
                vfreqrm = prony2freq(self.pRM.samples(w.size) + hrm)
            else:
                vfreqrm = self.pRM.samples(w.size) * hrm
            w = self.multi(w, vfreqrm)
        env = self.pEnv.samples(w.size)
        w *= env
        if pano is None:
            return w
        else:
            if isinstance(pano, list):
                pano = ProfilBase(pano).samples(w.size)
            wg = w * pano
            wd = w * (1. - pano)
            return wg, wd

    def evts(self, params, pano=None):
        """ un événement complexe
        Le timbre dépend de l'ordre des params"""
        c = CanalMono()
        pt = 0.0
        for h, d, a, ecart in params:
            w = self.evt(h, d) * a
            w = self.revcum.evt(w)
            c.addT(pt, w)
            pt += ecart
        if pano is None:
            return c.ex()
        else:
            w = c.ex()
            if isinstance(pano, list):
                pano = ProfilBase(pano).samples(w.size)
            wg = w * pano
            wd = w * (1. - pano)
            return wg, wd
