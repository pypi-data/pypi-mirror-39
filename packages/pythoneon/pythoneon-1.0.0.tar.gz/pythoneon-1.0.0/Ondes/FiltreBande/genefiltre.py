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
# Ondes/Filtre/genefiltre.py

""" une onde d'excitation est envoyée dans un filtre """

import numpy as np

from samplerate import sr
from conversions import prony2freq, extremum, freq2samples
from profilbase import ProfilBase
from origine import OrigineStr
from Filtres.filtrebpvariable import FiltreBPVariable
from Outils.ajuster import prolongerN

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2013.03.18"

class GeneBP(OrigineStr):
    """ quand ça va bien, on obtient un sinus ..."""
    def __init__(self):
        """ """
        OrigineStr.__init__(self)
        self.filtre = FiltreBPVariable()

    def evt(self, duree, vexcit, profilHauteurs, profilLargeurs):
        """
        Les coeffs a s'appliquent à vexcit
        Les coeffs b s'appliquent à w
           (et non l'inverse :)
        """
        n = int(duree * sr)
        if isinstance(profilHauteurs, list):
            pH = ProfilBase(profilHauteurs).samples(n)
        elif isinstance(profilHauteurs, float):
            pH = np.ones(n) * profilHauteurs
        else:
            print("FiltreBPVariable.evt:profilHauteurs inconnu")
        vfreq = prony2freq(pH)
        if isinstance(profilLargeurs, list):
            pL = ProfilBase(profilLargeurs).samples(n)
        elif isinstance(profilLargeurs, float):
            pL = np.ones(n) * profilLargeurs
        else:
            print("FiltreBPVariable.evt:profilLargeurs inconnu")
        vlargeur = prony2freq(pL)
        vfreq, vlargeur = prolongerN((vfreq, vlargeur))
        self.filtre.calcul_coeffs(vfreq, vlargeur)
        w = np.zeros(n + 2)
        for i in range(2, n):
            a0, a1, a2, b1, b2 = self.filtre.coeffs[i]
            q = vexcit[i] * a0 - vexcit[i-1] * a1 + vexcit[i-2] * a2 + \
                w[i-1] * b1 + w[i-2] * b2
            w[i] = vexcit[i] + q
        return w / extremum(w)

    def evt2(self, duree, vexcit, profilHauteurs, profilLargeurs):
        """
        Les coeffs a s'appliquent à vexcit
        Les coeffs b s'appliquent à w
           (et non l'inverse :)
        """
        n = int(duree * sr)
        if isinstance(profilHauteurs, list):
            pH = ProfilBase(profilHauteurs).samples(n)
        elif isinstance(profilHauteurs, float):
            pH = np.ones(n) * profilHauteurs
        else:
            print("FiltreBPVariable.evt:profilHauteurs inconnu")
        vfreq = prony2freq(pH)
        if isinstance(profilLargeurs, list):
            pL = ProfilBase(profilLargeurs).samples(n)
        elif isinstance(profilLargeurs, float):
            pL = np.ones(n) * profilLargeurs
        else:
            print("FiltreBPVariable.evt:profilLargeurs inconnu")
        vlargeur = prony2freq(pL)
        vfreq, vlargeur = prolongerN((vfreq, vlargeur))
        #print(type(vfreq), vfreq.size)
        nfreq = freq2samples(vfreq)
        nfreq.astype(np.int32)
        #print("Min, max", nfreq.min(), nfreq.max())
        self.filtre.calcul_coeffs(vfreq, vlargeur)
        nmax = nfreq.max() + 2
        w = np.zeros(n + nmax)
        for i in range(nmax, n):
            a0, a1, a2, b1, b2 = self.filtre.coeffs[i]
            q = vexcit[i] * a0 + vexcit[i-1] * a1 + vexcit[i-2] * a2 + \
                w[i-1] * b1 + w[i-2] * b2 #- \
                    #w[i-nfreq[i]] * 1.5
                    #w[i-1] * b1 + w[i-2] * b2
            w[i] = q + w[i-nfreq[i]] * 0.000125
        return w / extremum(w)

    def change(self):
        " pour changer "
        pass
#
#def modeleviolonfluct0(duree, vexcit, vfreq, ratio):
#    """
#    'vexcit' : un arroi utilisé comme excitateur des filtres
#             (p. ex. un bruit)
#    'vfreq' : l'arroi de la variation de fréquence
#    'ratio' : une fraction de vfreq"""
#    if (vexcit.size != vfreq.size):
#        vexcit, vfreq = prolongerN((vexcit, vfreq))
#    vn = sr / vfreq
#    vd = vn * ratio
#    n = int(duree * sr)
#    gd = vn.max()
#    w = np.zeros(n + int(gd))
#    for i in range(int(gd), n):
#        w[i] = vexcit[int(i - vn[i])] - vexcit[i] + w[int(i - vd[i])]
#    return w

def gfiltre(duree, vexcit, vfreq, ratio):
    """
    'vexcit' : un arroi utilisé comme excitateur des filtres
             (p. ex. un bruit)
    'vfreq' : l'arroi de la variation de fréquence
    'ratio' : une fraction de vfreq
    et la largeur ?"""
    if vexcit.size != vfreq.size:
        vexcit, vfreq = prolongerN((vexcit, vfreq))
    vn = sr / vfreq
    vd = vn * ratio
    n = int(duree * sr)
    gd = vn.max()
    w = np.zeros(n + int(gd))
    for i in range(int(gd), n):
        w[i] = vexcit[i] + w[+int(i - vd[i])]
    return w
