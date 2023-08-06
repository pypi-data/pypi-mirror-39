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
# Groupes/MultiTables/multitable.py

""" construire un timbre en superposant plusieurs ondes dont la
hauteur moyenne se situe dans une bande d'épaisseur donnée.
"""

import numpy as np

from samplerate import sr
from ondepartable import ondeTable # (table, modfreq)
from conversions import prony2freq, extremum

from profilbase import ProfilBase
from profils import recta #, cubica, affprofil
from canal import CanalMono #, record
#from reverberation import Reverberation
#from serie import Serie002
from origine import OrigineStr
#from visualiser import graphiqueInteractif, graphique

__author__ = "Copyright (c) 2014 René Bastian (Wissembourg, FRANCE)"
__date__ = "2014.02.09"

class MultiTable1(OrigineStr):
    """ une seule table """
    def __init__(self, table, nsons, deltahauteur, alea, reverb, ratioreverb):
        """ table: la table utilisée
        nsons : nombre de sons
        deltah : débattement en Prony
        alea : générateur sériel
        """
        OrigineStr.__init__(self)
        self.table = table
        self.alea = alea
        self.dh = deltahauteur
        self.nsons = nsons
        self.reverb = reverb
        self.ratio = ratioreverb # part de son direct dans la réverb

    def evtFixe(self, duree, hauteur):
        """ construit un événement de hauteur moyenne fixe mais dont
        les hauteurs internes varient suivant un profil en triangle
        Une réverb trop sèche perturbe ..."""
        n = int(duree * sr)
        c = CanalMono(duree)
        pt = 0.0
        for _ in range(self.nsons):
            h0 = self.alea.uniform(hauteur-self.dh, hauteur+self.dh)
            h1 = self.alea.uniform(hauteur-self.dh, hauteur+self.dh)
            h2 = self.alea.uniform(hauteur-self.dh, hauteur+self.dh)
            ph = [[recta, 0.1, h0, h1], [recta, 0.1, h1, h2]]
            vh = ProfilBase(ph).samples(n)
            vh = prony2freq(vh)
            w = ondeTable(self.table, vh)
            c.addT(pt, w)
        w = self.reverb.evt(c.a, self.ratio)
        w = w[:n]
        return w / extremum(w)

    def evtProfilMF(self, duree, phauteur):
        """ construit un événement de hauteur variant par profil """

    def evtVecteur(self, duree, vhauteur):
        """ construit un événement de hauteur variant par vecteur """

    def evt(self, duree, hauteur):
        """ construit un événement """
        if isinstance(hauteur, (float, int)):
            return self.evtFixe(duree, hauteur)
        elif isinstance(hauteur, list):
            return self.evtProfilMF(duree, hauteur)
        elif isinstance(hauteur, np.ndarray):
            return self.evtVecteur(duree, hauteur)
        else:
            print("MultiTable1.evt: cas non prévu", hauteur)

class MultiTable2(OrigineStr):
    """ plusieurs tables """
    def __init__(self, tables, nsons, deltahauteur, alea):
        """ tables: liste de tables à utiliser
        nsons : nombre de sons
        deltah : débattement en Prony
        alea : générateur sériel
        """
        OrigineStr.__init__(self)
        self.tables = tables
        self.alea = alea
        self.dh = deltahauteur
        self.nsons = nsons
#
#class MultiTable3(OrigineStr):
#    """ avec générateur de tables: les générer à l'extérieur"""
#    def __init__(self, genetables, nsons, deltahauteur, alea):
#        """ tables: liste de tables à utiliser
#        nsons : nombre de sons
#        deltah : débattement en Prony
#        alea : générateur sériel
#        """
#        OrigineStr.__init__(self)
#        self.gtables = genetables
#        self.alea = alea
#        self.dh = deltahauteur
#        self.nsons = nsons

if __name__ == "__main__":
    ftest = "test_multitable.py"

