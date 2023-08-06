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
# profilaleatoire.py

"""
fournit la classe ProfilAleatoire2010
produisant un profil composé de rectas, cubicas, fluctuas
variant aléatoirement entre des valeurs données.

Application dans SoleilBlanc/Sinus
"""
from profils import recta, cubica, fluctua, profil
from samplerate import sr
from profilbase import ProfilBase
from serie import Serie002
from origine import OrigineStr

__author__ = "Copyright (c) 2010 René Bastian (Wissembourg, FRANCE)"
__date__ = "2010.08.01, 2012.07.31, 2012.10.04"

def fairedurees0(duree, laps1, laps2, alea):
    """ construit une liste de durées
    La durée totale réelle est en générale supérieure à 'duree'."""
    durees = []
    total = 0.0
    while total < duree:
        d = alea.uniform(laps1, laps2)
        durees.append(d)
        total += d
    return durees

def fairedurees1(dureeT, laps1, laps2, alea):
    """ construit une liste de durées
    La durée totale réelle est en générale supérieure à 'duree'."""
    durees = []
    total = 0.0
    while total < dureeT:
        d = alea.uniform(laps1, laps2)
        reste = dureeT - total
        if reste <= laps1:
            d = reste
        durees.append(d)
        total += d
    return durees

def fairedurees(dureeT, laps1, laps2, alea):
    """ construit une liste de durées telles que chaque durée 'd'
    soit laps1 < d <= laps2 et que le total soit 'dureeT'.
    La durée totale réelle est en générale supérieure à 'dureeT'.
    >>> from serie import Serie002
    >>> alea = Serie002(511, 677)
    >>> fairedurees(5.0, 0.2, 0.8, alea)
    [0.20009665647526118, 0.265436433751805, 0.7004656499719553,
     0.6152450310137334, 0.5208859962974145, 0.23981949334955752,
     0.757796997650432, 0.4285674093424191, 0.7401361248177181,
     0.47215650159500383, 0.5315502073297047]
    >>> a = fairedurees(5.0, 0.2, 0.8, alea)
    >>> a
    [0.24995157981754823, 0.41721953648013044, 0.2576261970482889,
     0.21293540169155944, 0.5572669451857298, 0.26972189073903574,
     0.6017200303271972, 0.3644605315124898, 0.5397798339555878,
     0.43094758793290133, 0.5515170305741566, 0.5770296987039176]
    >>> sum(a)
    5.030176263968542
    >>> max(a)
    0.6017200303271972
    >>> min(a)
    0.21293540169155944
    >>> len(a)
    12
    """
    durees = []
    total, reste = 0.0, dureeT
    while total < dureeT:
        if laps1 < reste <= laps2:
            d = reste
        else:
            d = alea.uniform(laps1, laps2)
        reste = dureeT - total
        durees.append(d)
        total += d
    return durees

class ProfilAleatoire(OrigineStr):
    """ La classe fournit des profils aléatoires composés de
    rectas, cubicas, fluctuas ou d'un choix de ces profils
    élémentaires dont on peut faire varier la valeur moyenne,
    le débattement moyen, la densité de la variation.
    """
    def __init__(self, ymoy, yvar, laps1, laps2, yini=None, yfin=None,
                 powmin=None, powmax=None, formes=None):
        """
        'ymoy' : valeur moyenne de l'ordonnée
        'yvar' : débattement de l'ordonnée
        'laps1' : durée minimum de chaque élément du profil
        'laps2' : durée maximum de chaque élément du profil
        'yini' : valeur de la première ordonnée
        'yfin' : valeur de la dernière ordonnée
        'powmin, powmax' : torsions appliquées
        voir aussi profilAlea, calculProfilMF dans profilsalea.py
          et 'geneprofils.py'
        """
        OrigineStr.__init__(self)
        self.ymoy, self.yvar = ymoy, yvar
        self.laps1, self.laps2 = laps1, laps2
        self.yini, self.yfin = yini, yfin
        self.powmin, self.powmax = powmin, powmax
        if formes is None:
            self.formes = [recta, cubica, fluctua]
        else:
            self.formes = formes
        #self.result = []
        self.profil = None
        self.pmin, self.pmax = -0.1, +0.1

    def evt(self, duree, alea, bvecteur=False):
        """ retourne un profil selon le gabarit donné
        'alea' : instance de serie.Serie002
        je remplace fluctua par une cubica ..."""
        durees = fairedurees(duree, self.laps1, self.laps2, alea)
        r = []
        if self.yini:
            y0 = self.yini
        else:
            y0 = alea.uniform(self.ymoy-self.yvar, self.ymoy+self.yvar)
        n = len(durees) - 1
        for i, duree in enumerate(durees):
            p = alea.choice(self.formes)
            if i == n:
                y1 = self.yfin
            else:
                y1 = alea.uniform(self.ymoy-self.yvar, self.ymoy+self.yvar)
            if p == recta:
                if self.powmin is None and self.powmax is None:
                    r.append([recta, duree, y0, y1])
                else:
                    puiss = alea.uniform(self.powmin, self.powmax)
                    r.append([recta, duree, y0, y1, puiss])
            elif p == cubica:
                p0 = alea.uniform(self.pmin, self.pmax)
                p1 = alea.uniform(self.pmin, self.pmax)
                r.append([cubica, duree, y0, p0, y1, p1])
            elif p == fluctua:
                r.append([cubica, duree, y0, 0.0, y1, 0.0])
            else:
                print("ProfilAleatoire.evt: Mauvaise direction")
            y0 = y1
        if bvecteur:
            return profil(r)
        else:
            return r

    def change(self, ymoy=None, yvar=None, laps1=None, laps2=None,
               yini=None, yfin=None, formes=None):
        " pour changer le gabarit "
        if ymoy is not None:
            self.ymoy = ymoy
        if yvar is not None:
            self.yvar = yvar
        if laps1 is not None:
            self.laps1 = laps1
        if laps2 is not None:
            self.laps2 = laps2
        if yini is not None:
            self.yini = yini
        if yfin is not None:
            self.yfin = yfin
        if formes is not None:
            self.formes = formes

ProfilAleatoire2010 = ProfilAleatoire

class ProfilSection(object):
    """ construction  d'une classe par sections """
    def __init__(self, lprofil, alea):
        """ lprofil : description du profil
        alea : une instance de Serie002
        Syntaxe de 'lprofil' :
          <seg> = <fonction> <elements>
          <elements> = <element>, <element>, ...
          <element> = nombre | (nombre, nombre)

         UNIQUEMENT AVEC RECTA
        """
        self.lprofil = lprofil
        self.alea = alea

    def evt(self):
        """ retourne le prochain profil sous forme de
        profil-liste"""
        p = []
        for seg in self.lprofil:
            pp = [seg[0]]
            if isinstance(seg[1], tuple):
                a0, a1 = seg[1]
                pp.append(self.alea.uniform(a0, a1))
            else:
                pp.append(seg[1])
            for objet in seg[2:]:
                if isinstance(objet, tuple):
                    a0, a1 = objet
                    x = self.alea.uniform(a0, a1)
                    pp.append(x)
                else:
                    if objet is not None:
                        pp.append(objet)
                    else:
                        pp.append(x)
            p.append(pp)
        return p

    def evtT(self, duree):
        " calcule le prochain profil pour une durée donnée "
        n = int(duree * sr)
        return self.evtN(n)

    def evtN(self, n):
        " calcule le prochain profil pour un nombre de samples donné "
        p = self.evt()
        return ProfilBase(p).samples(n)

    def changealea(self, xx, xa, xb=None):
        """ change l'alea """
        self.alea = Serie002(xx, xa, xb)

    def change(self, lprofil=None, alea=None):
        " changer 'lprofil' ou 'alea' "
        if lprofil:
            self.lprofil = lprofil
        if alea:
            self.alea = alea

