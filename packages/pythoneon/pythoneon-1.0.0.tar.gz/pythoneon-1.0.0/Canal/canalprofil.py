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
# Canal/canalp.py

"""
canal spécialisé pour faire de l'addition de profils
"""
import numpy as np
from conversions import extremum, freq2prony, prony2freq
from samplerate import SR
from canal import CanalMono
from profilbase import ProfilBase

__author__ = """Copyright (c) 2015 René Bastian (Wissembourg, FRANCE)"""
__date__ = """2015.11.23"""

class CanalMonoP():
    """ pour additionner des profils de différentes sortes
    à chaque fois, on donne la durée demandée"""
    def __init__(self, bsamples=False, dureeInitiale=1.0, divbuffer=0.1):
        """ comme dans CanaMono """
        self.c = CanalMono(dureeInitiale, divbuffer)
        self.bsamples = bsamples

    def lin2db(self, duree, p, coeff, pt=0.0):
        """ conversion du profil de linéaire en db
        NON IMPLÉMENTÉ """
        if self.bsamples:
            n = duree
        else:
            n = int(duree * SR)
        v = ProfilBase(p).samples(n)
        v /= extremum(v)
        v *= coeff
        #self.c.addT(pt, v)
        print("lin2db NON IMPLÉMENTÉ")
        print(duree, p, coeff, pt, v.size, "ça peut attendre")


    def db2lin(self, duree, p, coeff, pt=0.0):
        """ conversion du profil de db en linéaire """
        if self.bsamples:
            n = duree
        else:
            n = int(duree * SR)
        v = ProfilBase(p).samples(n)
        v /= extremum(v)
        v *= coeff
        v = np.exp(v / 10.0)
        self.c.addT(pt, v)

    def lin2prony(self, duree, p, coeff, pt=0.0):
        """ conversion du profil de linéaire en prony """
        if self.bsamples:
            n = duree
        else:
            n = int(duree * SR)
        v = ProfilBase(p).samples(n)
        v /= extremum(v)
        v *= coeff
        v = freq2prony(v)
        self.c.addT(pt, v)

    def prony2lin(self, duree, p, coeff, pt=0.0):
        """ conversion du profil de prony en linéaire """
        if self.bsamples:
            n = duree
        else:
            n = int(duree * SR)
        v = ProfilBase(p).samples(n)
        v /= extremum(v)
        v *= coeff
        v = prony2freq(v)
        self.c.addT(pt, v)
