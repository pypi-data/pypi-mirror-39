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
# /pythoneon/Profils/abanicos.py

""" génération d'ondes à partir de profils en éventail

Défaut: la description d'un éventail a besoin d'une écriture spécifique
(les tuples). Dans 'interpolationlineaire.py', j'essaie de
faire une transition entre deux descriptions de profil
voir eventails.py, v0-eventails.py, v0-abanicos.py
 """

import numpy as np
from profilbase import ProfilBase
from conversions import prony2periode
from canal import CanalMono
from samplerate import sr
from filtrefixe import FiltreFixe
from origine import OrigineStr

__author__ = "Copyright (c) 2009 René Bastian (Wissembourg, FRANCE)"
__date__ = "2009.06.29, 2012.07.30"
#http://music.cnx.rice.edu/Brandt/expository/schoenberg_fantasy.mp3

def interpolervecteurs(va, vb, n, bAR=True):
    """
    interpole n fois entre va et vb
    va, vb : np.ndarray
    bAR : aller-retour
    """
    if va.size != vb.size:
        print("interpolervecteurs(va, vb, n, bAR=False): va.size != vb.size")
        return
    r = []
    for i in range(va.size):
        r.append(np.linspace(va[i], vb[i], n))
    r = np.array(r)
    if bAR:
        v = np.transpose(r)
        vr = v[1:-1]
        return np.concatenate((v, vr[::-1]))
    else:
        return np.transpose(r)

def interpoler(n, peventail):
    """ calcule n interpolations si 'peventail'
    est donné sous forme de profil-liste à tuples"""
    nmax = float(n)
    coll = []
    for i in range(n):
        q = []
        for pm in peventail:
            r = []
            for x in pm:
                if isinstance(x, tuple):
                    v = x[0] + i/nmax * (x[1] - x[0])
                    r.append(v)
                else:
                    r.append(x)
            q.append(r)
        coll.append(q)
    return coll

class AbanicosD:
    """ classe pour générer une suite d'ondes
    par transitions - doù le nom 'AbanicosD' : éventails

    alternatives:
     - pano fixe | pano continue | pano dispersée
     - hmod fixe | hmod continue | hmod dispersée

     Les méthodes 'ajout' et 'suite' sont problématiques.
    """
    def __init__(self, listepeventails, bprony=True):
        """ peventail est le profil de la forme d'onde
        syntaxe de peventail:
          <forme> <intervalle des durées> <intervalle des données>+

        collecte : recueille les listes-profils calculés
        """
        self.listepeventails = listepeventails
        self.bprony = bprony
        self.collecte = []

    def developpe(self, n):
        """ faire n interpolations """
        self.collecte = interpoler(n, self.listepeventails)

    def change(self, listepeventails):
        " pour changer les profils de base "
        self.listepeventails = listepeventails

    def ajout(self, listepeventails):
        " pour ajouter des profils aux profils de base "
        self.listepeventails.extend(listepeventails)

    def suite(self, listen, nouveau=False):
        """ construit une suite de profils interpolés qui seront
        ajoutés à 'collecte' si 'nouveau == False'
        Ruptures éventuelles ..."""
        if len(listen) != len(self.listepeventails):
            print("nbre d'interpolations", len(listen), \
                  "nbre de profils", len(self.listepeventails))
        if nouveau:
            self.collecte = []
        for n, listep in zip(listen, self.listepeventails):
            self.collecte.extend(interpoler(n, listep))
        return self.collecte

    def evtMono(self, pperiodes, pecarts, ini=None, fin=None,
                filtrer=False):
        """ construit un évènement d'ondes monocanal

        pperiodes : liste-profil de periodes
        pecarts   : liste-profil d'écarts
        ini, fin : index permettant de choisir une sous-liste
                   des profils dans self.collecte

        Sans gestion des erreurs éventuelles
        """
        if ini is None:
            ini = 0
        if fin is None:
            fin = len(self.collecte)
        n = fin - ini - 1
        periodes = ProfilBase(pperiodes).samples(n)
        if self.bprony:
            periodes = prony2periode(periodes)
        ecarts = ProfilBase(pecarts).samples(n)
        if self.bprony:
            ecarts = prony2periode(ecarts)
        duree = np.sum(ecarts)
        #print("Durée", duree)
        c = CanalMono(duree)
        pt, hfiltre = 0.0, 120.0
        for periode, ecart, lp in zip(periodes, ecarts,
                                      self.collecte[ini:fin]):
            y = ProfilBase(lp).temps(periode)
            if filtrer:
                filtre = FiltreFixe("pb", len(y)/4)
                y = filtre.evt(y, hfiltre)
            c.addT(pt, y)
            pt += ecart
        return c.a

    def evtStereo(self, pperiodes, pecarts, ppanos, ini=None, fin=None):
        """ construit un évènement d'ondes stéréo
        params comme dans evtMono avec en plus
        une liste-profils ppanos """
        if ini is None:
            ini = 0
        if fin is None:
            fin = len(self.collecte)
        n = fin - ini
        periodes = ProfilBase(pperiodes).samples(n)
        ecarts = ProfilBase(pecarts).samples(n)
        panos = ProfilBase(ppanos).samples(n)
        duree = np.sum(ecarts)
        cg = CanalMono(duree)
        cd = CanalMono(duree)
        pt = 0.0
        for periode, ecart, lp, pano in zip(periodes, ecarts,
                                            self.collecte[ini, fin],
                                            panos):
            y = ProfilBase(lp).temps(periode)
            yg, yd = y * pano, y * (1.0 - pano)
            cg.addT(pt, yg)
            cd.addT(pt, yd)
            pt += ecart
        return cg.a, cd.a

class Abanico(OrigineStr):
    """ classe pour générer une suite d'ondes
    par transitions - d'où le nom 'Abanico' : éventail
    Défaut: il faut une écriture spéciale (les tuples);
    """
    def __init__(self, listepeventails, sens=2, bprony=True):
        """ peventail est le profil de la forme d'onde
        syntaxe de peventail:
          <forme> <intervalle des durées> <intervalle des données>+

        collecte : recueille les listes-profils calculés
        """
        OrigineStr.__init__(self)
        self.listepeventails = listepeventails
        self.bprony = bprony
        self.sens = sens
        self.collecte = []

    def change(self, listepeventails, sens=2, bprony=True):
        " pour changer le profil de base "
        self.listepeventails = listepeventails
        self.bprony = bprony
        self.sens = sens

    def evtT(self, duree, pperiodes, pecarts):
        """ construit un évènement d'ondes monocanal
        duree : durée occupée
        pperiodes : liste-profil de periodes
        pecarts   : liste-profil d'écarts
        """
        xduree = sum([t[1] for t in pecarts])
        n = int(xduree * sr)
        ecarts = ProfilBase(pecarts).samples(n)
        if self.bprony:
            ecarts = prony2periode(ecarts)
        xduree = np.sum(ecarts)
        n = int(n * duree / xduree)
        periodes = ProfilBase(pperiodes).samples(n)
        if self.bprony:
            periodes = prony2periode(periodes)
        ecarts = ProfilBase(pecarts).samples(n)
        if self.bprony:
            ecarts = prony2periode(ecarts)
        c = CanalMono(duree)
        pt = 0.0
        eventail = interpoler(n, self.listepeventails)
        if self.sens == 2:
            eventail = eventail + eventail[::-1]
        for periode, ecart, ponde in zip(periodes, ecarts, eventail):
            y = ProfilBase(ponde).temps(periode)
            c.addT(pt, y)
            pt += ecart
        return c.a

class AbanicoP(OrigineStr):
    """
    On donne deux profils et on en déduit 'n' intermédiaires
    """
    def __init__(self, pA, pB):
        """
        pA, pB : deux profils ayant le même nombre de constituants
        """
        OrigineStr.__init__(self)
        self.pA, self.pB = pA, pB

    def change(self, pA=None, pB=None):
        " pour changer "
        if pA is not None:
            self.pA = pA
        if pB is not None:
            self.pB = pB

    def evtUnique(self, n):
        " construit la suite des profils intermédiaires "
        rg = []
        for pa, pb in zip(self.pA, self.pB):
            r = [[] for j in range(n)]
            for a, b in zip(pa, pb):
                if a == b:
                    for i in range(n):
                        r[i].append(a)
                else:
                    for i in range(n):
                        k = (b - a) / (n - 1)
                        r[i].append(k * i + a)
            rg.append(r)
        a = []
        ni = len(rg)
        nj = len(rg[0])
        for j in range(nj):
            b = []
            for i in range(ni):
                b.append(rg[i][j])
            a.append(b)
        return a

    def evtAR(self, n):
        " construit une suite aller-retour des profils intermédiaires "
        a = self.evtUnique(n)
        b = a[:-1]
        b.reverse()
        return a + b

