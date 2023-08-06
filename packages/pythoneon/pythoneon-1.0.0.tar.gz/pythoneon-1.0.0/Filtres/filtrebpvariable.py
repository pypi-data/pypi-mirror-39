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
# Filtres/filtrebpvariable.py
# NB: cette version n'a plus besoin de la fonction 'concordance'

"""
fournit la classe FiltreBPVariable et calcule les
coefficients du filtre par vecteurs complets.
"""
import numpy as np
from origine import OrigineStr
from filtrefixe import FiltreFixe
from samplerate import SR
from conversions import extremum, prony2freq
from profilbase import ProfilBase
from ajuster import prolongerN

__author__ = "Copyright (c) 2005-13 René Bastian (Wissembourg, FRANCE)"
__date__ = """2006.08.28, 10.17, 2008.10.06, 2009.02.08, 2013.07.09,
           2013.10.08"""

__all__ = ["FiltreBPVariable"]

class FiltreBPVariable(OrigineStr):
    """
    fournit un filtre passe-bande dont la hauteur et la largeur
    peuvent varier selon un profil en 'prony'.

    L'usage préconisé:
    - initialisation
    - evt(signal, pHauteurProny, pLargeurProny)
    """
    def __init__(self, btest=False):
        """
        initialise mais ne fait rien d'autre
        """
        OrigineStr.__init__(self)
        self.coeffs = None
        self.btest = btest

    def calcul_coeffs(self, freqcoupure, bandepassante):
        """
        calcule les coefficients (a0, a1, a2), (0.0, b1, b2)
           d'un filtre BP récursif caractérisé par
           sa fréquence centrale et sa bande passante
        'freqcoupure' : fréquence centrale ou vecteur de la variation
        'bandepassante' : bande passante ou vecteur de la bande passante
        source: cf.Steven W. Smith p.326
        On manipule des vecteurs: a0, a1, etc sont d'abord des vecteurs
           qui sont mis dans le bon ordre par 'np.transpose';
        On pourrait faire une outre méthode où la bande passante est
        exprimé en ratio de la fréquence centrale.
        """
        bande = np.array(bandepassante) / float(SR) # par précaution
        fc = np.array(freqcoupure) / float(SR) # par précaution
        omega = 2 * np.pi * fc
        cosomega = np.cos(omega)
        R = 1.0 - 3.0 * bande
        R2 = R * R
        K = (1.0 - 2 * R * cosomega + R2)/(2.0 - 2 * cosomega)
        a0 = 1.0 - K
        a1 = 2 * (K - R) * cosomega
        a2 = R2 - K
        b1 = 2 * R * cosomega
        b2 = -R2
        self.coeffs = [a0, a1, a2, b1, b2]
        self.coeffs = np.transpose(self.coeffs)

    def appli(self, x):
        """
        applique les coeffs calculés par calcul_coeffs à
        'x' : signal entrant, np.ndarray
        """
        d = min(x.size, self.coeffs.size)
        x = np.concatenate((np.zeros(2, np.float64), x))
        y = np.zeros(x.size, np.float64)
        for i in range(2, d-2):
            a0, a1, a2, b1, b2 = self.coeffs[i]
            y[i] = x[i] * a0 + x[i-1] * a1 + x[i-2] * a2 + \
                    y[i-1] * b1 + y[i-2] * b2
        return y

    def __call__(self, signal, vfreq, vlargeur):
        """ NE PLUS UTILISER
        'signal' : un signal
        'vfreq' : vecteur de la variation de fréquence centrale en Hz
        'vlargeur' : vecteur de la variation de largeur de bande en Hz
        """
        #print(type(signal), type(vfreq), type(vlargeur))
        vfreq, vlargeur = prolongerN((vfreq, vlargeur))
        self.calcul_coeffs(vfreq, vlargeur)
        y = self.appli(signal)
        return y / extremum(y)

    def evtF(self, signal, vfreq, vlargeur):
        """
        'signal' : un signal
        'vfreq' : vecteur de la variation de fréquence centrale en Hz
        'vlargeur' : vecteur de la variation de largeur de bande en Hz
        """
        #print(type(signal), type(vfreq), type(vlargeur))
        vfreq, vlargeur = prolongerN((vfreq, vlargeur))
        self.calcul_coeffs(vfreq, vlargeur)
        y = self.appli(signal)
        return y / extremum(y)

    def evt(self, signal, profilHauteurs, profilLargeurs):
        """
        'signal' : le signal à filtrer
        'profilHauteurs, profilLargeurs' : listes-profils en Prony
           décrivant la variation de la hauteur centrale et
           la largeur du filtre en pronys.
        """
        n = signal.size
        if isinstance(profilHauteurs, list):
            vH = ProfilBase(profilHauteurs).samples(n)
        elif isinstance(profilHauteurs, float):
            vH = np.ones(n) * profilHauteurs
        else:
            print("FiltreBPVariable.evt:profilHauteurs inconnu")
            print(type(profilHauteurs))
        vH = prony2freq(vH)
        if isinstance(profilLargeurs, list):
            vL = ProfilBase(profilLargeurs).samples(n)
        elif isinstance(profilLargeurs, float):
            vL = np.ones(n) * profilLargeurs
        else:
            print("FiltreBPVariable.evt:profilLargeurs inconnu")
            print(type(profilLargeurs))
        vL = prony2freq(vL)
        if self.btest:
            print("FiltreBPVariable.evt")
            print("vH", type(vH), vH.shape, "vL", type(vL), vL.shape)
        return self.evtF(signal, vH, vL)

    def evtMax(self, signal, profilHauteurs, profilLargeurs):
        """
        'signal' : le signal à filtrer
        'profilHauteurs, profilLargeurs' : listes-profils en Prony
        décrivant la variation de la hauteur centrale et
        la largeur du filtre en pronys.
        """
        n = signal.size
        if isinstance(profilHauteurs, list):
            pH = ProfilBase(profilHauteurs).samples(n)
        elif isinstance(profilHauteurs, float):
            pH = np.ones(n) * profilHauteurs
        else:
            print("FiltreBPVariable.evt:profilHauteurs inconnu")
            print(type(profilHauteurs))
        pH = prony2freq(pH)
        if isinstance(profilLargeurs, list):
            pL = ProfilBase(profilLargeurs).samples(n)
        elif isinstance(profilLargeurs, float):
            pL = np.ones(n) * profilLargeurs
        else:
            print("FiltreBPVariable.evt:profilLargeurs inconnu")
        pL = prony2freq(pL)

        return self.evtF(signal, pH, pL), pH.max()

    def evtPB(self, signal, profilHauteurs, profilLargeurs,
              nc=SR/88, bmax=False):
        """ comme evt, mais rajoute un filtre passe-bas fixe
        dont la fréquence d'accord est la plus haute fréquence
        du profilHauteurs; le nombre de coefficients du filtre fixe
        est 501 par défaut.
        'signal' : le signal à filtrer
        'profilHauteurs, profilLargeurs' : listes-profils
        décrivant la variation de la fréquence centrale et
        la largeur du filtre en pronys.
        """
        w, freqmax = self.evtR(signal, profilHauteurs, profilLargeurs,
                               bmax=True)
        fx = FiltreFixe("pb", nc)
        if bmax:
            return fx.evtF(w, freqmax), freqmax
        else:
            return fx.evtF(w, freqmax)

    def evtR(self, signal, profilHauteurs, profilLargeurs, bmax=False):
        """
        signal : le signal à filtrer
        profilHauteurs : liste-profils en Prony
        profilLargeurs : liste-profils en ratio de fréquence
          décrivant la variation de la hauteur centrale et
          la largeur du filtre en proportion de la fréquence d'accord
          du filtre.
        """
        n = signal.size
        if isinstance(profilHauteurs, list):
            vH = ProfilBase(profilHauteurs).samples(n)
        elif isinstance(profilHauteurs, float):
            vH = np.ones(n) * profilHauteurs
        else:
            print("FiltreBPVariable.evt:profilHauteurs inconnu")
        vH = prony2freq(vH)
        if isinstance(profilLargeurs, list):
            vL = ProfilBase(profilLargeurs).samples(n)
        elif isinstance(profilLargeurs, float):
            vL = np.ones(n) * profilLargeurs
        else:
            print("FiltreBPVariable.evt:profilLargeurs inconnu")
        vL = vH * vL
        if bmax:
            return self(signal, vH, vL), vH.max()
        else:
            return self(signal, vH, vL)
