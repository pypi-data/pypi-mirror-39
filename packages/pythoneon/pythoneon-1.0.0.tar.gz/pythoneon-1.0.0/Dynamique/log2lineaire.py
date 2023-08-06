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
# log2lineaire.py
# OBSOLETE ??
import numpy as np

class Log2Lineaire:
    """
    fournit les valeurs exponentiellement
    étagées entre vmin et vmax
    si m == 0      : x = vmin
    si m == degres : x = vmax
    x = self.vmin * exp(log(vmax/vmin)/degres)**m

    Il est p-ê préférable d'utiliser la classe Decibel
    """
    def __init__(self, vmin, vmax, degres):
        """
        instancie la classe
        """
        self.vmin = vmin
        self.degres = degres
        self.vmax = vmax
        if vmax == vmin :
            print("Log2Lineaire", vmax, vmin)
        """
        try:
            self.k = np.exp(np.log(vmax/vmin)/degres)
        except:
            print("Log2Lineaire : self.k")
        """
        self.k = np.exp(np.log(vmax/vmin)/degres)

    def v(self, m):
        return self.vmin * self.k**m

    def __call__(self, m):
        """
        retourne la valeur

        try:
            x = self.vmin * self.k**m
        except:
            print("Log2Lineaire", vmax, vmin)
        """
        return self.vmin * self.k**m

