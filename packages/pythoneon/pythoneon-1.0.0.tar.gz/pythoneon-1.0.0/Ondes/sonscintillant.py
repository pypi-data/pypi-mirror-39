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
# sonscintillant.py

"""
fournit la classe  SonScintillant
provient de AventiKermo
"""
import numpy as np

from profilbase import ProfilBase
from profils import recta
from ondepartable import ondeTable
from conversions08 import prony2freq
from samplerate import sr

__author__ = "Copyright (c) 2006 René Bastian (Wissembourg, FRANCE)"
__date__ = "2009.09.01"


class EnveloppeScintillante(object):
    """
    essai pour une classe dont les parties varient
    en des durées variables d'où p-ê un effet scintillant.

    Le son comporte les habituels artéfacts de dépassement de sr.
    """
    def __init__(self, alea, y0=0.0, y1=1.0, puiss0=None, puiss1=None):
        """
        'alea' instance de Serie002
        """
        self.alea = alea
        self.y0 = y0
        self.y1 = y1
        self.puiss0 = puiss0
        self.puiss1 = puiss1

    def calcul(self, xdts, n):
        """
        construit le profil
        xdts : vecteur de valeurs de durées
        """
        #print(self.alea)
        py = self.alea.uniform(self.y0, self.y1, n)
        #print(duree, sduree, n, py)
        if self.puiss0:
            pp = self.alea.uniform(self.puiss0, self.puiss1, n)
        else:
            pp = np.ones(n)
        y0 = py[0]
        r = [[recta, xdts[0], 0.0, y0, pp[0]]]
        for  dt, y1, puiss in zip(xdts[1:-1], py[1:-1], pp[1:-1]):
            r.append([recta, dt, y0, y1, puiss])
            y0 = y1
        r.append([recta, xdts[-1], y0, 0.0, pp[-1]])
        #print(xdts)
        return r

    def _calcul(self, xdts, n):
        """
        construit le profil
        xdts : vecteur de valeurs de durées
        puissX == 1.0
        """
        py = self.alea.uniform(self.y0, self.y1, n)
        y0 = py[0]
        r = [[recta, xdts[0], 0.0, y0]]
        for  dt, y1, puiss in zip(xdts[1:-1], py[1:-1]]):
            r.append([recta, dt, y0, y1])
            y0 = y1
        r.append([recta, xdts[-1], y0, 0.0]])
        return r

    def temps(self, duree, listedurees):
        """
        'listedurees' : liste-profil d'évolution des durées
        'duree' : durée totale souhaitée
        si on ne donne pas de durée et qu'on attend tout de
        ProfilBase on risque d'obtenir du bruit
        adapte la 'listeduree' à 'duree'
        """
        pd = ProfilBase(listedurees).temps(duree)
        sduree = pd.sum()
        n = int((duree * len(pd)) / sduree) + 1
        dts = ProfilBase(listedurees).samples(n)
        if self.puiss0 and self.puiss1:
            return self.calcul(dts, n)
        else:
            return self._calcul(dts, n)

#    def suitealea(self, duree, vecteur):
#        """
#        'duree' : durée totale souhaitée
#        'vecteur' : valeurs relatives des divers éléments du profil
#        """
#        if isinstance(vecteur, list):
#            vecteur = np.array(vecteur)
#        sduree = vecteur.sum()
#        dts = vecteur * duree / sduree
#        n = len(dts)
#        return self.calcul(dts, n)
#        
#    def samples(self, n, listedurees):
#        """
#        'listedurees' : liste-profil d'évolution des durées
#        'n' : nombre de samples souhaité
#        """
#        pd = ProfilBase(listedurees).samples(n)
#        sduree = pd.sum()
#        n = int((duree * len(pd)) / sduree) + 1
#        dts = ProfilBase(listedurees).samples(n)
#        py = self.alea.uniform(self.y0, self.y1, n)
#        #print(duree, sduree, n, py)
#        if self.puiss0:
#            pp = self.alea.uniform(self.puiss0, self.puiss1, n)
#        else:
#            pp = np.ones(n)
#        y0 = py[0]
#        r = [[recta, dts[0], 0.0, y0, pp[0]]]
#        for  dt, y1, puiss in zip(dts[1:-1], py[1:-1], pp[1:-1]):
#            r.append([recta, dt, y0, y1, puiss])
#            y0 = y1
#        r.append([recta, dts[-1], y0, 0.0, pp[-1]])
#        #print(dts)
#        return r
#            

class SonScintillant:
    """
    son avec des enveloppes scintillantes
    """
    def __init__(self, table,
                 alea, y0=0.0, y1=1.0, puiss0=None, puiss1=None):
        """
        'table' : vecteur de longueur = 1.0 sec
        'alea', : instance de Serie002
        y0=0.0, y1=1.0, puiss0=None, puiss1=None :
            params pour EnveloppeScintillante
        """
        self.envscint = EnveloppeScintillante(alea, y0, y1, puiss0, puiss1)
        self.table = ProfilBase(table).samples(sr)
        self.alea = alea

    def evt(self, duree, vhoehe, venv, vmicrod, vpano=None):
        """
        'duree' : durée 
        'vhoehe' : liste-profil de la variation de hauteur
        'vmicrod' : liste-profil de la variation de micro-durées de l'enveloppe
        'venv' : liste-profil de la variation de l'enveloppe
        En raison des difficultés de calcul, on commence par l'enveloppe
        """
        microe = self.envscint.temps(duree, vmicrod)
        microe = ProfilBase(microe).temps(duree)
        n = len(microe)
        vh = ProfilBase(vhoehe).samples(n)
        vh = prony2freq(vh)
        w = ondeTable(self.table, vh)
        #print(microe)
        w *= microe
        #print(venv)
        #print(n, len(w))
        e = ProfilBase(venv).samples(n)
        
        w *= e
        if vpano:
            pano = ProfilBase(vpano).samples(n)
            wg, wd = w * pano, w * (1. - pano)
            return wg, wd
        else:
            return w
