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
# Ondes/cordepincee.py

""" fournit la classe CordePincee """

import numpy as np
from samplerate import SR
from conversions import prony2periode
from profilbase import ProfilBase
from profils import recta

class CordePincee(object):
    """
    usage : creer une instance
    puis fournir les parametres à la fonction f
    et inserer wg et wd dans un canal stereo
    exemple :
    """
    def __init__(self, alea, hmin, hmax, panomin=0.0, panomax=1.0):
        self.coeff = (panomax - panomin)/(hmax - hmin)
        self.hmin, self.hmax = hmin, hmax
        self.panomin, self.panomax = panomin, panomax
        self.hm = (hmax - hmin) / 2 #63.5
        self.alea = alea
        self.calculpano()
        self.format = "%7.3f %7.3f %7.3f %7.6f %7.6f\n"

    def calculpano(self):
        "calcule le pano en fonction de la hauteur"
        return self.panomin + self.coeff*(self.hm - self.hmin)

    def cordenylon(self, generateur, duree):
        """
        calcule la forme d'onde : ne pas appeler directement
        """
        #epsilon = 3.0 / SR
        dg = len(generateur)
        n = int(duree * SR)
        w = np.zeros(n, np.float64)
        w[0:dg] = generateur[:]
        cc = 2.0
        for i in range(dg, n/2):
            w[i] = (w[i - dg] + w[i - dg + 1])/cc
        for i in range(n/2, n):
            cc = self.alea.uniform(2.1, 2.4)
            w[i] = (w[i - dg] + w[i - dg + 1] + 0.01 * w[i - dg + 2]) / cc
        return w

    def evt(self, hauteur, duree, vneg=-0.5):
        """
        f retourne la note jouee avec le timbre
        """
        periode = prony2periode(hauteur)
        generateur = ProfilBase([[recta, 1.0, -1.0, 1.0]]).temps(periode)
        # jouer sur la profondeur
        #generateur *= self.alea.uniform(-0.5, 1., len(generateur))
        generateur *= self.alea.uniform(vneg, 1., len(generateur))
        w = self.cordenylon(generateur, duree)
        pano = self.calculpano()
        wg = w * pano
        wd = w * (1. - pano)
        return wg, wd
