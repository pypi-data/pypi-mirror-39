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

""" tentative d'extension des plings
"""

import numpy as np
from samplerate import SR
from origine import OrigineStr
#from profilgeneral import recta
from profilbase import ProfilBase
from conversions import prony2freq, prony2samples, extremum
import serie
#from canal import record
#from ondepartable import ondeTable
from tablegenerale import TableG

__author__ = "Copyright (c) 2005-15 René Bastian (Wissembourg, FRANCE)"
__date__ = "2007.12.17, 2015.11.13"


class PlingParallele(OrigineStr):
    """
    Par cette classe, l'onde finale est le résultat de la
    réinjection et d'un apport parralèle.

    Mais c'est l'apport parall qui fait tout ...
    """
    def __init__(self, couple=None):
        OrigineStr.__init__(self)
        if couple is None:
            self.alea = serie.Serie002(7563, 3463)
        else:
            self.alea = serie.Serie002(couple[0], couple[1])

    def evt(self, duree, vHauteur, nvecteur, table, EnvParallele):
        """
        'duree' : durée en secondes
        'vHauteur' : profil-liste en prony de l'évolution de la hauteur
        'nvecteur' : tuple du nombre min et max des coeffs du vecteur
           de réinjection
        'table' : profil-liste en prony de la table
        'EnvParallele' : profil-liste en prony de l'évolution de l'enveloppe
        """
        vh = ProfilBase(vHauteur).temps(duree)
        vn = prony2samples(vh)
        vf = prony2freq(vh)
        wp = TableG(table).evt(vf)
        ep = ProfilBase(EnvParallele).samples(len(wp))
        wp *= ep * 0.5
        #play64(wp, wp); print("-------")
        m = vn[0]
        n = int(SR * duree)
        w = np.zeros(n)
        try:
            kmin, kmax =  nvecteur
            k = self.alea.randint(kmin, kmax)
        except StandardError:
            k = nvecteur
        #k = min(m, k)
        x = self.alea.uniform(0., 1., k)
        x = x / sum(x)
        x *= 0.5
        for i in range(m, n):
            w[i] = wp[i] + sum(w[i-vn[i]:i-vn[i]+k] * x)
        return w

    @staticmethod
    def evt1(duree, vHauteur, xvecteur, wparallele):
        """
        EN PANNE ?
        'duree'      : durée en secondes
        'vHauteur'   : profil-liste en prony de l'évolution de la hauteur
        'xvecteur'   : vecteur de réinjection
        'wparallele' : vecteur d'entretien
        """
        vh = ProfilBase(vHauteur).temps(duree)
        vn = prony2samples(vh)
        # manips pour éviter les emballements
        wp = 0.5 * wparallele / extremum(wparallele)
        print(extremum(wp))
        xv = (xvecteur / sum(xvecteur)) * 0.5
        k = len(xv)
        m = vn[0]
        n = int(SR * duree)
        w = np.zeros(n)
        w[:len(wp)] = wp
        for i in range(m, n):
            try:
                #w[i] = wp[i] + sum(w[i-vn[i]:i-vn[i]+k] * xv)
                w[i] = sum(w[i-vn[i]:i-vn[i]+k] * xv)
            except StandardError:
                w[i] = sum(w[i-vn[i]:i-vn[i]+k] * xv)

        return w
