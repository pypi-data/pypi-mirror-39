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
# decibel.py

##DEBUT
"""apporte les classes Decibel et Amplis
mais je ne suis pas satisfait des calculs effectués,
d'abord peu pratiques et, à mon avis, erronés.
"""

import math
import serie
#from origine import Origine0
import numpy as np

__author__ = "Copyright (c) 2005 René Bastian (Wissembourg, FRANCE)"
__date__ = "2006.05.08"
##FIN
__all__ = ["Decibel", "DecibelSerie", "Amplis"]

class Decibel0:
    """
    classe pour passer des nombres aux db;
    ne doit pas être appliqué à des enveloppes.
    """
    def __init__(self, base=1.0):
        self.base = base
        self.a = None
        self.db = None

    def x2db(self, x):
        "retourne la valeur en décibels de l'amplitude x"
        self.a = x
        self.db = 10.0*math.log(x)*self.base
        return self.db

    def db2x(self, xdb):
        "retourne l'amplitude à partir de x en décibels"
        self.db = xdb
        self.a = math.exp(xdb/10.0/self.base)
        return self.a

    def __call__(self, xdb):
        "retourne l'amplitude à partir de x en décibels"
        return  math.exp(xdb/10.0/self.base)

    def affscala(self, lim0, lim1):
        "affiche les valeurs"
        print("%10s %22s %30s" % ("x", "x2db(x)", "db2x(x2db(x))"))
        sforme = "%10.0f %22.18f %30.18f"
        x = lim0
        while x < (lim1+1):
            dd = self.x2db(x)
            xx = self.db2x(dd)
            print(sforme % (x, dd, xx))
            x = x*2

    def initxlogx(self, x, logx):
        "change la base de calcul"
        self.base = logx/math.log(x)


##DEBUT
class Decibel:
    """
    classe pour passer des nombres aux db
    Il vaut mieux utiliser 'PBel'
    """
    def __init__(self, base=1.0):
        "crée une instance avec 'base'"
        self.base = base

    def x2db(self, x):
        "retourne la valeur en décibels de l'amplitude x"
        return 10.0*np.log(x)*self.base

    def db2x(self, xdb):
        "retourne l'amplitude à partir de x en décibels"
        return np.exp(xdb/10.0/self.base)

    def __call__(self, xdb):
        """retourne l'amplitude à partir de x en décibels
        Appel 1:
          db = decibel.Decibel()
          x = alea(4., 12.)
          ampli = db(x)
        Appel :
          ampli = Decibel()(4.)
        """
        return  np.exp(xdb/10.0/self.base)

class DecibelSerie(Decibel):
    """
    une classe qui permet une variation sérielle-aléatoire
    des valeurs.
    """
    def __init__(self, base=1.0, couple=(8967, 3567)):
        "crée une instance de DecibelSerie"
        Decibel.__init__(self, base)
        self.alea = serie.Serie002(couple[0], couple[1])
        self.dbmin, self.dbmax = None, None

    def limites(self, dbmin, dbmax):
        """
        donne un intervalle
        """
        if dbmax < dbmin:
            dbmax, dbmin = dbmin, dbmax
        self.dbmin, self.dbmax = dbmin, dbmax

    def seq(self, dbmin, dbmax):
        """
        retourne une valeur inverse d'un valeur en db
        sérielle entre 'dbmin' et 'dbmax'.
        """
        if dbmax < dbmin:
            dbmax, dbmin = dbmin, dbmax
        x = self.alea.uniform(dbmin, dbmax)
        return self.db2x(x)

class Amplis:
    """
    La classe Amplis fournit des valeurs d'amplitudes
    sériellement calculées entre 'dbmin' et 'dbmax'.
    """
    def __init__(self, dbmin, dbmax, base=1.0, couple=(773353, 11129)):
        """
        'dbmin, dbmax' : l'intervalle de choix
        'base' : base de la classe Decibel
        'couple' : semence du générateur sériel.
        """
        self.alea = serie.Serie002(couple[0], couple[1])
        self.dbmin, self.dbmax = dbmin, dbmax
        self.db = Decibel(base)

    def __call__(self, n=1, dbmin=None, dbmax=None):
        """
        'n' : nombre de valeurs en retour
        'dbmin, dbmax' : comme dans __init__
        """
        if dbmin is not None:
            self.dbmin = dbmin
        if dbmax is not None:
            self.dbmax = dbmax
        if n == 1:
            return self._valeur()
        else:
            return [self._valeur() for _ in range(n)]

    def _valeur(self):
        """
        effectue les calculs.
        """
        v = self.alea.uniform(self.dbmin, self.dbmax)
        return self.db.db2x(v)

##FIN
