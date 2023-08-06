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
# Ondes/Combines/multiplier.py
"""
contient la classe Multiplier qui produit un effet 'modulateur en anneau'
par multiplication d'un signal par un sinus.
On peut aussi utiliser RingMod (ringmod.py) mais qu'il faut mettre en forme.
"""
from profilbase import ProfilBase
from conversions import prony2freq
from Outils.ajuster import prolongerN
from sinusrecursif import SinusRecursif
from Ondes.FormesRaides.sinusoides import sinusMF
from origine import OrigineStr

__author__ = "Copyright (c) 2005-12 René Bastian (Wissembourg, FRANCE)"
__date__ = "2007.09.20, 2012.11.13, 2013.07.17"
__all__ = ["Multiplier"]

class Multiplier(OrigineStr):
    """produit l'effet 'modulateur en anneau'"""
    def __init__(self, bfreq=True, sin=None):
        """
        'bfreq=True' : les hauteurs sont données en Hz
        sin : fonction sinus utilisée par défaut
        """
        OrigineStr.__init__(self)
        self.bfreq = bfreq
        if sin is None:
            self.sin = SinusRecursif().sinFixeN

    def evt(self, signal, hauteur):
        """
        module le signal avec un sinus 'hauteur'
        hauteur : float ou np.array
        """
        if self.bfreq:
            s = self.sin(signal.size, hauteur)
        else:
            s = self.sin(signal.size, prony2freq(hauteur))
        return signal * s

    def __call__(self, signal, hauteur):
        " comme evt "
        return self.evt(signal, hauteur)

    def profil(self, signal, P):
        """
        module le signal avec un sinus suivant le profil 'P'
        """
        p = ProfilBase(P).samples(signal.size)
        if not self.bfreq:
            p = prony2freq(p)
        m = sinusMF(p)
        signal, m = prolongerN((signal, m))
        return signal * m
#FIN
#from profils import recta
#    def puissance(self, signal, P, hoch=1):
#        """
#        module le signal avec un sinus suivant le profil 'P'
#        à la puissance 'hoch' ;
#        différence minime ...
#        """
#        if isinstance(P, float):
#            P = [[recta, 1., P, P]]
#        p = ProfilBase(P).samples(len(signal))
#        if not self.bfreq:
#            p = prony2freq(p)
#        m = sinusMF(p)
#        signal, m = prolongerN((signal, m))
#        m **= hoch
#        return signal * m
