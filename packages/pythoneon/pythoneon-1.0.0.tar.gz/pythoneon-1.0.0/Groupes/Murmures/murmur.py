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
# Tpythoneon/Groupes/Murmures/murmurs.py

""" construit des sortes de murmures """
import numpy as np
from samplerate import SR
from serie import Serie002
from conversions import (prony2freq, freq2prony, nunc)
from profilbase import ProfilBase
from canal import CanalMono
from origine import OrigineStr
from profils import affprofil

__author__ = "Copyright (c) 2016 René Bastian (Wissembourg, FRANCE)"
__date__ = "2016.08.19"

class Murmur(OrigineStr):
    """ des bruits divers
    Principe:
      par 'add' sont mélangés dans un canal des sons et des bruits;
      par 'evt' le mélangé final est retourné et enregistré
      si 'souche' est donné"""
    def __init__(self, genep, fonction, alea=None, bprony=True):
        OrigineStr.__init__(self)
        if alea is None:
            self.alea = Serie002(1741, 207)
        else:
            self.alea = alea
        self.bprony = bprony
        self.c = CanalMono()
        self.gp = genep
        self.f = fonction
        self.info = [str(self)]

    def infoappend(self, *args):
        """ ajoute des params à l'info """
        r = []
        for arg in args:
            r.append(str(arg))
        self.info.append(" ".join(r))

#    def add(self, hauteur, duree, nw, deviation, amplimin, amplimax):
#        """ ajout INUTILE ?
#        hauteur: hauteur moyenne en prony ou Hz
#        duree: durée souhaitée
#        nw: nombre d'ondes superposées (== densité)
#        deviation: variation maximum de la hauteur
#        amplimin, -max: variation de l'amplitude """
#        n = int(duree * SR)
#        for _ in range(nw):
#            penv = self.gp.evtEnvDuree(duree)
#            env = ProfilBase(penv).samples(n)
#            phauteur = self.gp.evtPronyDuree(duree, deviation, h0=hauteur)
#            vf = ProfilBase(phauteur).samples(n)
#            if self.bprony:
#                vf = prony2freq(vf)
#            ampli = self.alea.uniform(amplimin, amplimax)
#            print(vf)
#            w = self.f(vf)
#            w *= env * ampli
#            self.c.addT(0.0, w)
#        self.infoappend(self.add, hauteur, duree, nw, deviation,
#                        amplimin, amplimax)

    def addEchelle(self, hmin, hmax, nombre, puissance, duree, deviation,
                   amplimin, amplimax, bprony=True):
        """ ajoute une liste de hauteurs d'une échelle
        Il vaut mieux que puissance > 0.0
        Si 0.0 < puissance < 1.0, les résultats s'agglutinent vers le haut
        si 1.0 < puissance, les résultats s'agglutinent vers le bas
        bprony vaut pour toutes les hauteurs (donc deviation
        est donné en Prony"""
        vh = np.linspace(0.0, 1.0, nombre) ** puissance
        vh = hmin + vh * (hmax - hmin)
        if bprony:
            vh = prony2freq(vh)
        n = int(duree * SR)
        for h in vh:
            penv = self.gp.evtEnvDuree(duree)
            env = ProfilBase(penv).samples(n)
            if not bprony:
                deviation = freq2prony(deviation)
            phauteur = self.gp.evtPronyDuree(duree, deviation, h0=h)
            vf = ProfilBase(phauteur).samples(n)
            ampli = self.alea.uniform(amplimin, amplimax)
            #print(self.f, vf)
            w = self.f(vf)
            w *= env * ampli
            self.c.addT(0.0, w)
        self.infoappend(self.addEchelle,
                        hmin, hmax, nombre, puissance, duree, deviation,
                        amplimin, amplimax, bprony)

    def addBande(self, hmin, hmax, nombre, duree, deviation,
                 amplimin, amplimax, bprony=True, binfo=False):
        """ ajoute une liste de hauteurs sériés dans une bande
        bprony vaut pour toutes les hauteurs (donc deviation
        est donné en Prony"""
        vh = self.alea.uniform(hmin, hmax, nombre)
        if bprony:
            vh = prony2freq(vh)
        n = int(duree * SR)
        for h in vh:
            penv = self.gp.evtEnvDuree(duree)
            if binfo:
                affprofil(penv)
            env = ProfilBase(penv).samples(n)
            if not bprony:
                deviation = freq2prony(deviation)
            phauteur = self.gp.evtPronyDuree(duree, deviation, h0=h)
            if binfo:
                affprofil(phauteur)
            vf = ProfilBase(phauteur).samples(n)
            ampli = self.alea.uniform(amplimin, amplimax)
            #print(self.f, vf)
            w = self.f(vf)
            w *= env * ampli
            self.c.addT(0.0, w)
        if binfo:
            print("addBande", self.c.a.size, self.c.a.max(), self.c.a.min())
        self.infoappend(self.addBande,
                        hmin, hmax, nombre, duree, deviation,
                        amplimin, amplimax, bprony)

# ajouter une def où le profil est un macroproil + un microprofil

    def addStries(self, args, binfo=True):
        """ conglomérat de addBande; cette méthode
        peut remplacer la loi de probabilité par profil."""
        bprony = True
        for  hmin, hmax, nombre, duree, deviation, \
                 amplimin, amplimax, bprony in args:
            if binfo:
                print(hmin, hmax, nombre, duree, deviation,
                      amplimin, amplimax, bprony)
            self.addEchelle(hmin, hmax, nombre, duree, deviation,
                            amplimin, amplimax, bprony)

    def addBandeV(self, hmin, hmax, nombre, duree, deviation,
                  pvarH, amplimin, amplimax, bprony=True):
        """ ajoute une liste de hauteurs sériés dans une bande
        bprony vaut pour toutes les hauteurs (donc deviation
        est donné en Prony
        Dans evtPronyDuree, h0=0.0 puisque la déviation
        est appliquée à l'extérieur (ici)"""
        vh = self.alea.uniform(hmin, hmax, nombre)
        #if bprony:
        #    vh = prony2freq(vh)
        n = int(duree * SR)
        vv0 = ProfilBase(pvarH).samples(n)
        #if bprony:
        #    vv0 = prony2freq(vv0)
        for h in vh:
            penv = self.gp.evtEnvDuree(duree)
            env = ProfilBase(penv).samples(n)
            if not bprony:
                deviation = freq2prony(deviation)
            microphauteur = self.gp.evtPronyDuree(duree, deviation, h0=0.0)
            microvf = ProfilBase(microphauteur).samples(n)
            vf = vv0 + h + microvf
            print(vv0.max(), vv0.min(), "--", h, "--",
                  microvf.max(), microvf.min())
            print(vf.max(), vf.min())
            ampli = self.alea.uniform(amplimin, amplimax)
            if bprony:
                vf = prony2freq(vf)
            w = self.f(vf)
            w *= env * ampli
            self.c.addT(0.0, w)
        self.infoappend(self.addBandeV,
                        hmin, hmax, nombre, duree, deviation,
                        pvarH, amplimin, amplimax, bprony)

    def clear(self):
        """ mettre le canal collecteur à zéro """
        self.c = CanalMono()

    def close(self, souche):
        """ enregistre le bruit construit et les params de sa
        construction """
        nf = "".join([souche, ".f64"])
        self.c.a.tofile(nf)
        nf = "".join([souche, ".info"])
        self.info.append(nunc())
        s = "\n".join(self.info)
        with open(nf, "w") as f:
            f.write(s)

class MurmurT(Murmur):
    """ Murmur avec des pts temporels """
    def __init__(self, genep, fonction, alea=None, bprony=True):
        Murmur.__init__(genep, fonction, alea, bprony)

    @staticmethod
    def calcul_pts(nombre=None, p=None):
        """ calcul des pts temporels
        args possibles:
         (None, nombre)
         (list, nombre)
         (None, ndarray)
         (float, nombre)"""
        if p is None:
            return np.zeros(nombre)
        elif isinstance(p, list):
            return ProfilBase(p).samples(nombre)
        elif isinstance(p, np.ndarray):
            return p
        elif isinstance(p, float):
            v = np.ones(nombre) * p
            return np.cumsum(v)

    def addEchelle(self, hmin, hmax, nombre, puissance, duree, deviation,
                   amplimin, amplimax, pTemps, bprony=True):
        """ ajoute une liste de hauteurs d'une échelle
        Il vaut mieux que puissance > 0.0
        Si 0.0 < puissance < 1.0, les résultats s'agglutinent vers le haut
        si 1.0 < puissance, les résultats s'agglutinent vers le bas
        bprony vaut pour toutes les hauteurs (donc deviation
        est donné en Prony"""
        vh = np.linspace(0.0, 1.0, nombre) ** puissance
        vh = hmin + vh * (hmax - hmin)
        vpts = self.calcul_pts(nombre, pTemps)
        if bprony:
            vh = prony2freq(vh)
        n = int(duree * SR)
        for h, pt in zip(vh, vpts):
            penv = self.gp.evtEnvDuree(duree)
            env = ProfilBase(penv).samples(n)
            if not bprony:
                deviation = freq2prony(deviation)
            phauteur = self.gp.evtPronyDuree(duree, deviation, h0=h)
            vf = ProfilBase(phauteur).samples(n)
            ampli = self.alea.uniform(amplimin, amplimax)
            #print(self.f, vf)
            w = self.f(vf)
            w *= env * ampli
            self.c.addT(pt, w)
        self.infoappend(self.addEchelle,
                        hmin, hmax, nombre, puissance, duree, deviation,
                        amplimin, amplimax, bprony)

    def addBande(self, hmin, hmax, nombre, duree, deviation,
                 amplimin, amplimax, pTemps, bprony=True):
        """ ajoute une liste de hauteurs sériés dans une bande
        bprony vaut pour toutes les hauteurs (donc deviation
        est donné en Prony"""
        vh = self.alea.uniform(hmin, hmax, nombre)
        vpts = self.calcul_pts(nombre, pTemps)
        if bprony:
            vh = prony2freq(vh)
        n = int(duree * SR)
        for h, pt in zip(vh, vpts):
            penv = self.gp.evtEnvDuree(duree)
            env = ProfilBase(penv).samples(n)
            if not bprony:
                deviation = freq2prony(deviation)
            phauteur = self.gp.evtPronyDuree(duree, deviation, h0=h)
            vf = ProfilBase(phauteur).samples(n)
            ampli = self.alea.uniform(amplimin, amplimax)
            #print(self.f, vf)
            w = self.f(vf)
            w *= env * ampli
            self.c.addT(pt, w)
        self.infoappend(self.addBande,
                        hmin, hmax, nombre, duree, deviation,
                        amplimin, amplimax, bprony)

    def addStries(self, args, binfo=True):
        """ conglomérat de addBande; cette méthode
        peut remplacer la loi de probabilité par profil."""
        bprony = True
        for  hmin, hmax, nombre, duree, deviation, \
                 amplimin, amplimax, pTemps, bprony in args:
            if binfo:
                print(hmin, hmax, nombre, duree, deviation,
                      amplimin, amplimax, pTemps, bprony)
            self.addEchelle(hmin, hmax, nombre, duree, deviation,
                            amplimin, amplimax, pTemps, bprony)

    def addBandeV(self, hmin, hmax, nombre, duree, deviation,
                  pvarH, amplimin, amplimax, pTemps, bprony=True):
        """ ajoute une liste de hauteurs sériés dans une bande
        bprony vaut pour toutes les hauteurs (donc deviation
        est donné en Prony
        Dans evtPronyDuree, h0=0.0 puisque la déviation
        est appliquée à l'extérieur (ici)"""
        vh = self.alea.uniform(hmin, hmax, nombre)
        vpts = self.calcul_pts(nombre, pTemps)
        #if bprony:
        #    vh = prony2freq(vh)
        n = int(duree * SR)
        vv0 = ProfilBase(pvarH).samples(n)
        for h, pt in zip(vh, vpts):
            penv = self.gp.evtEnvDuree(duree)
            env = ProfilBase(penv).samples(n)
            if not bprony:
                deviation = freq2prony(deviation)
            microphauteur = self.gp.evtPronyDuree(duree, deviation, h0=0.0)
            microvf = ProfilBase(microphauteur).samples(n)
            vf = vv0 + h + microvf
            print(vv0.max(), vv0.min(), "--", h, "--",
                  microvf.max(), microvf.min())
            print(vf.max(), vf.min())
            ampli = self.alea.uniform(amplimin, amplimax)
            if bprony:
                vf = prony2freq(vf)
            w = self.f(vf)
            w *= env * ampli
            self.c.addT(pt, w)
        self.infoappend(self.addBandeV,
                        hmin, hmax, nombre, duree, deviation,
                        pvarH, amplimin, amplimax, bprony)

