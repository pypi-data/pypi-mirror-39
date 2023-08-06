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

""" fournit la classe Vagues qui utilise la fonction evtR du
FiltreBPVariable (la largeur est exprimée en
ratio de fréquence au lieu de largeur absolue).  """

from origine import OrigineStr
from serie import Serie002
from profilbase import ProfilBase
from Filtres.filtrebpvariable import FiltreBPVariable
from conversions import extremum

__author__ = "Copyright (c) 2014 René Bastian (Wissembourg, FRANCE)"
__date__ = "2014.06.13"

class Vagues(OrigineStr):
    " construit un vague bruit de vague, de vent, de sifflement ..."
    def __init__(self, alea=None):
        """ alea = générateur de nombres pseudo-aléatoires
        """
        OrigineStr.__init__(self)
        if alea is None:
            self.alea = Serie002(312657, 64992)
        else:
            self.alea = alea
        self.fbpv = FiltreBPVariable()

    def evt(self, duree, pH, pL, pE, pPano=None):
        """
        duree : float
        pH : profil de la variation de hauteur
        pL : profil de la variation de largeur de la hauteur en proportion
             de la fréquence
        pE : profil de l'enveloppe
        pPano=None : profil de la variation panoramique
        """
        bruit = self.alea.noise(duree)
        w = self.fbpv.evtR(bruit, pH, pL)
        e = ProfilBase(pE).samples(w.size)
        w *= e
        try:
            w /= extremum(w)
        except ZeroDivisionError:
            print("VagueMono.evt: ZeroDivisionError")
            return
        if pPano is None:
            return w
        else:
            pano = ProfilBase(pPano).samples(w.size)
            wg = w * pano
            wd = w * (1.0 - pano)
            return wg, wd

    def change(self, alea=None):
        " pour changer "
        if alea is not None:
            self.alea = alea
