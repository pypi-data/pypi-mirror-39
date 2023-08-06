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
# Traitements/multiplier.py

""" la classe Multiplier doit fournir un traitement
ressemblant à une modulation en anneau; les modulations du signal sont
faites par des sinus mathématiques:
  evt(signal, une_fréquence fixe)
  profil(signal, un_profil décrivant une variation de fréquence)

Voir aussi Ondes/Combines/multiplier0.y et ringmod.py

OBSOLÈTE ??? UTILISER Ondes/Combines/multiplier.py ????
"""

from origine import OrigineStr
from conversions import prony2freq
from profilbase import ProfilBase
from Outils.ajuster import prolongerN
from Ondes.FormesRaides.sinusmath import sinusN
from Ondes.FormesRaides.sinusoides import sinusMF

__author__ = "Copyright (c) 2009 René Bastian (Wissembourg, FRANCE)"
__date__ = "2009.11.17, 2013.08.15"

class Multiplier(OrigineStr):
    """une classe pour produire un effet de 'modulateur en anneau'"""
    def __init__(self, bfreq=True):
        """
        'bfreq=True' : les hauteurs sont données en Hz
        """
        OrigineStr.__init__(self)
        self.bfreq = bfreq

    def evt(self, signal, hauteur):
        """ module le signal avec un sinus 'hauteur' """
        if self.bfreq:
            s = sinusN(hauteur, signal.size)
        else:
            s = sinusN(prony2freq(hauteur), signal.size)
        return signal * s

    def profil(self, signal, P, hoch=1.0):
        """ module le signal avec un sinus suivant le profil 'P';
        hoch semble n'avoir que peu d'influence. """
        p = ProfilBase(P).samples(signal.size)
        if not self.bfreq:
            p = prony2freq(p)
        m = sinusMF(p)
        signal, m = prolongerN((signal, m))
        if hoch != 1.0:
            m **= hoch
        return signal * m

    def change(self, bfreq):
        " pour changer "
        self.bfreq = bfreq
