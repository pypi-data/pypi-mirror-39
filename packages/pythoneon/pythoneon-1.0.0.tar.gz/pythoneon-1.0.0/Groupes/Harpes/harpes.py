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
# harpes.py
"""
fournit la classe Harpe barissante
"""

import numpy as np
from samplerate import SR
from Filtres.allpassfiltre import FiltrePeigne
from Profils.profilbase import ProfilBase
from conversions import prony2freq, freq2prony, extremum
from Ondes.Tables.ondepartable import ondeTable

__author__ = "Copyright (c) 2005 René Bastian (Wissembourg, FRANCE)"
__date__ = "2006.09.17, 2009.08.29, 2010.12.10, 2012.12.14"

class Harpe(object):
    """
    classe pour un timbre passant une onde à travers un filtre en peigne.
    """
    def __init__(self, pTable, prony, finesse):
        """
        installe une table d'onde et un filtre en peigne ;
        'pTable' : table de forme d'onde
        'prony' : écart du filtre en peigne entre deux bandes
        'finesse' : finesse du filtre en %
        """
        self.prony = prony
        self.finesse = finesse
        self.fp = FiltrePeigne(prony, finesse)
        #self.table = ProfilBase(pTable).temps(1.0)
        if isinstance(pTable, list):
            self.table = ProfilBase(pTable).samples(SR)
        elif isinstance(pTable, np.ndarray):
            self.table = pTable

    def __call__(self, duree, varprony, enveloppe, pano=None):
        """
        on fournit une durée, un profil brut de variation
        de hauteur, des profils bruts de variation d'enveloppe
        et de variation panoramique ; l'instance effectue
        le balayage de la table, le filtrage et la mise
        en forme.
        'duree' : durée de l'événement (avant filtrage)
        'VarProny' : profil de la variation de hauteur en prony
        'Enveloppe' : enveloppe de l'événement
        'Pano' : évolution panoramique.
        """

        mf = ProfilBase(varprony).temps(duree)
        mf = prony2freq(mf)
        w = ondeTable(self.table, mf)
        w = self.fp.filtrer(w)
        n = len(w)
        w *= ProfilBase(enveloppe).samples(n)
        w /= extremum(w)
        if not pano:
            return w
        if isinstance(pano, (int, float)):
            return w * pano, w * (1.0 - pano)
        else:
            pano = ProfilBase(pano).samples(n)
            return w * pano, w * (1.0 - pano)

    def evt(self, duree, varprony, enveloppe, pano=None):
        "compatible avec version 0"
        return self.__call__(duree, varprony, enveloppe, pano)

    def charger(self, pTable=None, prony=None, finesse=None):
        "introduire des valeurs"
        if pTable:
            self.table = ProfilBase(pTable).temps(1.0)
        if prony and finesse:
            self.prony = prony
            self.finesse = finesse
            self.fp = FiltrePeigne(prony, finesse)
        elif prony and not finesse:
            self.prony = prony
            self.fp = FiltrePeigne(prony, self.finesse)
        elif not prony and finesse:
            self.finesse = finesse
            self.fp = FiltrePeigne(self.prony, finesse)

    def futur(self):
        """
        essayer:
           une évolution des params du filtre
           d'autres filtres ? ce n'est plus une harpe
           d'autres formes d'ondes ? il faut maintenir la variation de hauteur
        """
        pass

class Harpe01(object):
    """ classe pour un timbre passant une onde
    à travers un filtre en peigne avec choix de la fonction """
    def __init__(self, cfiltre, ptable=None):
        """
        installe un filtre en peigne et un mode de génération
        d'onde
        'pTable' : table de forme d'onde
        'prony' : écart du filtre en peigne entre deux bandes
        'finesse' : finesse du filtre en %
        """
        if cfiltre[0] == 1:
            self.ecartfiltre = freq2prony(cfiltre[1])
        elif cfiltre[0] == 0:
            self.ecartfiltre = cfiltre[1]
        self.finesse = cfiltre[2]
        self.fp = FiltrePeigne(self.ecartfiltre, self.finesse)
        #self.table = ProfilBase(pTable).temps(1.0)
        if isinstance(ptable, list):
            self.table = ProfilBase(ptable).temps(1.0)
        elif isinstance(ptable, np.ndarray):
            self.table = ptable
        else:
            self.table = None

    def evt(self, duree, varprony, enveloppe, pano=None):
        """ on fournit une durée, un profil brut de variation
        de hauteur, des profils bruts de variation d'enveloppe
        et de variation panoramique ; l'instance effectue
        la création de l'onde, le filtrage et la mise
        en forme.
        'duree' : durée de l'événement (avant filtrage)
        'VarProny' : profil de la variation de hauteur en prony
        'Enveloppe' : enveloppe de l'événement
        'Pano' : évolution panoramique.
        """
        pass
