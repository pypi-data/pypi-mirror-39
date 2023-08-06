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
#Profils/profilbase2.py
"""
contient les classes ProfilBasePlus

La méthode est trop compliquée. Il vaut mieux
- 1. soit générer le profil directement
- 2. soit
  -- générer le profil support
  -- générer les profils de variation et les superposer
     en respectant un rapport donné
"""
from samplerate import SR
from conversions import extremum
from profils import recta, cubica, profil
from profilbase import ProfilBase
from Outils.ajuster import prolongerN
from serie import Serie002
from origine import OrigineStr

__author__ = "Copyright (c) 2005-12 René Bastian (Wissembourg, FRANCE)"
__date__ = "2007.06.14, 07.10.06, 09.02.04, 2012.08.08"

#__all__ = ["ProfilBasePlus"] #, "ProfilBaseMicro"]

class ProfilBasePlus(OrigineStr):
    """
    superpose un micro-profil au ProfilBase ;
    le micro-profil ne varie pas homothétiquement.
    À chaque appel, la classe calcule un micro-profil.

    Étendre cette classe en faisant générer un profil
    avec des 'dt' et de 'y' variant sériellement.
    """
    def __init__(self, P, courbures=None, alea=None):
        """
        'P' : le profil de base principal
        'courbures' : courbures appliquées dans le calcul des recta
        'c_bornesduree' : limites de la variation de dt
           (fournis lors de l'appel)
        'couple' : générateur sériel
        """
        OrigineStr.__init__(self)
        self.pb = ProfilBase(P)
        if alea is None:
            self.alea = Serie002(91143, 34119)
        else:
            self.alea = alea
        self.courbs = courbures
        self.genres = [recta, cubica]
        self.profilliste = []
        self.dtmin, self.dtmax = None, None

    def _micro(self, duree):
        """
        calcule le micro-profil pour une enveloppe (ne pas appliquer
        pour une mod.freq);
        pourquoi ?
        """
        t = 0.0
        T = []
        while t <= duree:
            try:
                dt = self.alea.uniform(self.dtmin, self.dtmax)
            except AttributeError:
                print(self.alea)
                return
            if t + dt <= duree:
                T.append(dt)
            else:
                T.append(duree - sum(T))
            t += dt
        M = []
        y0 = 0.0
        for dt in T:
            y1 = self.alea.uniform(0.0, 1.0)
            genre = self.alea.choice(self.genres)
            if genre == recta:
                try:
                    courbure = self.alea.uniform(self.courbs[0], self.courbs[1])
                except ValueError:
                    courbure = 1.0
                M.append([recta, dt, y0, y1, courbure])
            elif genre == cubica:
                M.append([cubica, dt, y0, 0., y1, 0.])
            t += dt
            y0 = y1
        # aussi bien dans recta - avec courbure ! - que dans cubica,
        # y1 est en position -2
        M[-1][-2] = 0.0
        #print(M[-1])
        self.profilliste = M
        p = profil(M)
        return p / extremum(p)

    def samples(self, n, rapport, c_bornesduree):
        """
        'n' : nombre d'échantillons
        'rapport' : en principe << 1.0, mais
        on obtient des profils tortueux si 0. < rapport < 1;
        'rapport' peut être un profil-liste pour évoluer dans le temps.
        'c_bornesduree' : (durée min, durée max) du fragment de profil
        """
        self.dtmin, self.dtmax = c_bornesduree
        px = self.pb.samples(n)
        duree = float(n)/SR
        if isinstance(rapport, list):
            rapport = ProfilBase(rapport).samples(n)
        micro = self._micro(duree)* rapport
        px, micro = prolongerN((px, micro))
        px *= (1. + micro)
        return px

    def temps(self, duree, rapport, c_bornesduree):
        """
        'duree' : durée du profil
        'rapport' : en principe << 1.0, mais
        on obtient des profils tortueux si 0. < rapport < 1.
        'rapport' peut être un profil-liste pour évoluer dans le temps.
        'c_bornesduree' : (durée min, durée max) du fragment de profil
        """
        self.dtmin, self.dtmax = c_bornesduree
        px = self.pb.temps(duree)
        #if type(rapport) == types.ListType:
        if isinstance(rapport, list):
            n = len(px)
            rapport = ProfilBase(rapport).samples(n)
        micro = self._micro(duree)* rapport
        px, micro = prolongerN((px, micro))
        px *= (1. + micro)
        return px

    def __call__(self, duree, params, temps=True):
        """
        'duree' : selon temps, durée en sec ou dimension en nombre
           d'échantillons
        '*params' : suite de tuples (c_bornesduree, rapport)

        L'appel permet de superposer au profil principal
        plusieurs couches de profils sériels ayant des
        durées de profils et des rapports différents.
        """
        if temps:
            px = self.pb.temps(duree)
        else:
            n = int(duree * SR)
            px = self.pb.samples(n)
        for c_bornesduree, rapport in params:
            print(c_bornesduree, rapport)
            self.dtmin, self.dtmax = c_bornesduree
            micro = self._micro(duree)
            if isinstance(rapport, list):
                rapport = ProfilBase(rapport).temps(duree)
                micro, rapport = prolongerN((micro, rapport))
            micro *= rapport
            px, micro = prolongerN((px, micro))
            px *= (1.0 + micro)
        #px /= extremum(px)
        print(min(px), max(px))
        return px



##########################################################
#class ProfilBasePlus_2009(OrigineStr):
#    """
#    superpose un micro-profil au ProfilBase ;
#    le micro-profil ne varie pas homothétiquement.
#    À chaque appel, la classe calcule un micro-profil.
#
#    Étendre cette classe en faisant générer un profil
#    avec des 'dt' et de 'y' variant sériellement.
#    """
#    def __init__(self, P, courbures=None, couple=(91143, 34119)):
#        """
#        'P' : le profil de base principal
#        'courbures' : courbures appliquées dans le calcul des recta
#        'c_bornesduree' : limites de la variation de dt
#            (fournis lors de l'appel)
#        'couple' : générateur sériel
#        """
#        OrigineStr.__init__(self)
#        self.pb = ProfilBase(P)
#        self.alea = Serie002(couple[0], couple[1])
#        self.courbs = courbures
#        self.genres = [recta, cubica]
#        self.profilliste = []
#        self.dtmin, self.dtmax = None, None
#
#    def _micro(self, duree):
#        """
#        calcule le micro-profil pour une enveloppe (ne pas appliquer
#        pour une mod.freq);
#        pourquoi ?
#        """
#        t = 0.0
#        T = []
#        while t <= duree:
#            dt = self.alea.uniform(self.dtmin, self.dtmax)
#            if t + dt <= duree:
#                T.append(dt)
#            else:
#                T.append(duree - sum(T))
#            t += dt
#        M = []
#        y0 = 0.0
#        for dt in T:
#            y1 = self.alea.uniform(0.0, 1.0)
#            genre = self.alea.choice(self.genres)
#            if genre == recta:
#                try:
#                    courbure = self.alea.uniform(self.courbs[0],
#                                self.courbs[1])
#                except ValueError:
#                    courbure = 1.0
#                M.append([recta, dt, y0, y1, courbure])
#            elif genre == cubica:
#                M.append([cubica, dt, y0, 0., y1, 0.])
#            t += dt
#            y0 = y1
#        # aussi bien dans recta - avec courbure ! - que dans cubica,
#        # y1 est en position -2
#        M[-1][-2] = 0.0
#        #print(M[-1])
#        self.profilliste = M
#        p = profil(M)
#        return p / extremum(p)
#
#    def samples(self, n, rapport, c_bornesduree):
#        """
#        'n' : nombre d'échantillons
#        'rapport' : en principe << 1.0, mais
#        on obtient des profils tortueux si 0. < rapport < 1;
#        'rapport' peut être un profil-liste pour évoluer dans le temps.
#        'c_bornesduree' : (durée min, durée max) du fragment de profil
#        """
#        self.dtmin, self.dtmax = c_bornesduree
#        px = self.pb.samples(n)
#        duree = float(n)/SR
#        if isinstance(rapport, list):
#            rapport = ProfilBase(rapport).samples(n)
#        micro = self._micro(duree)* rapport
#        px, micro = prolongerN(px, micro)
#        px *= (1. + micro)
#        return px
#
#    def temps(self, duree, rapport, c_bornesduree):
#        """
#        'duree' : durée du profil
#        'rapport' : en principe << 1.0, mais
#        on obtient des profils tortueux si 0. < rapport < 1.
#        'rapport' peut être un profil-liste pour évoluer dans le temps.
#        'c_bornesduree' : (durée min, durée max) du fragment de profil
#        """
#        self.dtmin, self.dtmax = c_bornesduree
#        px = self.pb.temps(duree)
#        #if type(rapport) == types.ListType:
#        if isinstance(rapport, list):
#            n = len(px)
#            rapport = ProfilBase(rapport).samples(n)
#        micro = self._micro(duree)* rapport
#        px, micro = prolongerN(px, micro)
#        px *= (1. + micro)
#        return px
###FIN
#    def __call__(self, duree, params, temps=True):
#        """
#        'duree' : selon temps, durée en sec ou dimension en nombre
#           d'échantillons
#        '*params' : suite de tuples (c_bornesduree, rapport)
#
#        L'appel permet de superposer au profil principal
#        plusieurs couches de profils sériels ayant des
#        durées de profils et des rapports différents.
#        """
#        if temps:
#            px = self.pb.temps(duree)
#        else:
#            px = self.pb.samples(n)
#        for c_bornesduree, rapport in params:
#            print(c_bornesduree, rapport)
#            self.dtmin, self.dtmax = c_bornesduree
#            micro = self._micro(duree)
#            if type(rapport) == types.ListType:
#                rapport = ProfilBase(rapport).temps(duree)
#                micro, rapport = prolongerN(micro, rapport)
#            micro *= rapport
#            px, micro = prolongerN(px, micro)
#            px *= (1.0 + micro)
#        #px /= extremum(px)
#        print(min(px), max(px))
#        return px
