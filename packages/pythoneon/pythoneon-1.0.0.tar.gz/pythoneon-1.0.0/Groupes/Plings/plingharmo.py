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
# Groupes/Plings/plingharmo.py

""" divers usages de Pling """

import numpy as np
from samplerate import SR
from profilbase import ProfilBase
from conversions import (prony2freq, extremum)
from profils import (profil, recta)
import canal
import serie

from origine import OrigineStr

__author__ = "Copyright (c) 2005-07 René Bastian (Wissembourg, FRANCE)"
__date__ = "2007.07.28"

__all__ = ["plingharmo", "plingProfil", "PlingHarmoM",
           "PlingHarmo", "PlingHarmo0"]

def generateurDentAlea(freq):
    """ fonction sérielle    """
    n = int(SR // freq)
    w = serie.Serie002().uniform(-1.0, +1.0, n)
    w.sort()
    return w

def plingharmo(prony, harmons, listeE):
    """ superpose les 'plings' correpondant aux 'harmons' fournis """
    c = canal.CanalMono()
    e = profil(listeE)
    diviseur = 2.0000005
    freq = prony2freq(prony)

    n = len(harmons)
    pt = 0.0
    for i in range(1, n):
        g = generateurDentAlea(freq * i)
        w = plingProfil(g, diviseur, e) * harmons[i-1]
        c.addT(pt, w)
    return c.a / extremum(c.a)

def plingProfil(generateur, diviseur, vprofil):
    """
    pling avec profil incorporé
    """
    dg = len(generateur)
    de = vprofil.size
    w = np.zeros(de, np.float64)
    w[0:dg] = generateur[:]
    for i in range(dg, de):
        w[i] = (w[i-dg]+w[i-dg+1])/diviseur
    return w * vprofil

# classe PlingHarmo0

class PlingHarmo0(OrigineStr):
    """
    version héritable
    """
    def __init__(self):
        """
        Fournit un son mouvant et lisse
        """
        OrigineStr.__init__(self)

    @staticmethod
    def generateurDentAlea(freq):
        """
        produit une 'dent de scie' aléatoire

        Algorithme:
         - n valeurs aléatoires entre -1 et +1
         - tri

        copie de 'generateurDentAlea(self, freq)'
        dans 'generateursAlea.py'
        """
        n = int(SR/freq)
        w = serie.Serie002().uniform(-1.0, +1.0, n)
        w.sort()
        return w

    @staticmethod
    def plingProfil(generateur, diviseur, vprofil):
        """
        effectue l'algorithme de base d'un 'pling'
        qui est multiplié par le 'profil incorporé
        """
        dg = len(generateur)
        de = vprofil.size
        w = np.zeros(de, np.float64)
        w[0:dg] = generateur[:]
        for i in range(dg, de):
            w[i] = (w[i-dg]+w[i-dg+1])/diviseur
        return w * vprofil

    def __call__(self, prony, harmons, listeE):
        """
        superpose plusieurs 'dent de scie' aléatoires
        superpose les 'plings' correpondant aux 'harmons' fournis
        """

        c = canal.CanalMono()
        e = profil(listeE)
        diviseur = 2.0000005
        freq = prony2freq(prony)
        n = len(harmons)
        pt = 0.0
        for i in range(1, n):
            g = self.generateurDentAlea(freq * i)
            w = self.plingProfil(g, diviseur, e) * harmons[i-1]
            c.addT(pt, w)
        return c.a / extremum(c.a)

# classe PlingHarmo

class PlingHarmo(PlingHarmo0):
    """
    Fournit presque le même son que PlingHarmo0.
    harmons=[8., 4., 2., 1., 2., 4., 8.]
    E=[[recta, 0.08, 0.0, 1.0], [recta, duree, 1.0, 0.0]]
    La même enveloppe est utilisée pour chaque harmonique.
    Envisager :
    [
      (ampli, multiplieur, Profil),
      ...
      ]
      pour obtenir une composition de plings.

    'plingharmo(prony, harmons, E)' appelle 'generateurDentAlea'
    mais il me semble plus simple de faire calculer l'onde
    par 'ProfilBase' et d'appeler le nombre de samples nécessaires.
    """
    def __init__(self, harmons, E,
                 Table=None,
                 rapport=0.1,
                 couple=(5534, 7424)):
        """
        crée une instance
        """
        if not Table:
            Table = [[recta, 1., -1., 1.]]
        PlingHarmo0.__init__(self)
        self.harmons = harmons
        self.nh = len(harmons)
        self.env = ProfilBase(E)
        self.diviseur = 2.0000005
        self.alea = serie.Serie002(*couple)
        try:
            self.table = ProfilBase(Table)
        except TypeError:
            self.table = np.array(Table)
        self.rapport = rapport

    def generateur(self, freq):
        """
        méthode interne pour examen visuel du générateur
        """
        ns = int(SR/freq)
        if self.table:
            g = self.table.samples(ns)
            g += self.alea.uniform(-self.rapport, self.rapport, ns)
        else:
            print("Table absente")
            g = self.alea.uniform(-1.0, +1.0, ns)

        g.sort()
        return g

    def evt(self, prony, duree):
        """
        comme __call__
        """
        return self(prony, duree)

    def evt0(self, prony, duree):
        """
        variante utilisant la fonction plingProfil héritée
        """
        c = canal.CanalMono()
        de = int(duree*SR)
        e = self.env.samples(de)
        freq = prony2freq(prony)
        pt = 0.0
        for i, k in enumerate(self.harmons):
            ns = int(SR/(freq*(i+1)))
            if self.table:
                g = self.table.samples(ns)
                g += self.alea.uniform(-self.rapport, self.rapport, ns)
            else:
                g = self.alea.uniform(-1.0, +1.0, ns)
            g.sort()
            w = self.plingProfil(g, self.diviseur, e)*k
            c.addT(pt, w)
        return c.a / extremum(c.a)

    def __call__(self, prony, duree):
        """
        superpose les 'plings' correpondant aux 'harmons' fournis
        lors de l'instanciation.
        """
        c = canal.CanalMono()
        de = int(duree*SR)
        e = self.env.samples(de)
        freq = prony2freq(prony)
        pt = 0.0
        for i, k in enumerate(self.harmons):
            ns = int(SR/(freq*(i+1)))
            if self.table:
                try:
                    g = self.table.samples(ns)
                except TypeError:
                    g = self.table
                    print(g)
                g += self.alea.uniform(-self.rapport, self.rapport, ns)
            else:
                g = self.alea.uniform(-1.0, +1.0, ns)
            g.sort()
            dg = len(g)
            w = np.zeros(de, np.float64)
            w[0:dg] = g
            for i in range(dg, de):
                w[i] = (w[i-dg] + w[i-dg+1])/self.diviseur
            w *= (e * k)
            c.addT(pt, w)
        return c.a / extremum(c.a)

class PlingHarmoM(PlingHarmo0):
    """
    variante
    """
    def __init__(self, harmons, E,
                 Table=None,
                 couple=(5534, 7424)):
        """
        harmons=[8., 4., 2., 1., 2., 4., 8.]
        E=[[recta, 0.08, 0.0, 1.0], [recta, duree, 1.0, 0.0]]
        La même enveloppe est utilisée pour chaque harmonique.
        Envisager :
        [
          (ampli, multiplieur, Profil),
          ...
          ]
          pour obtenir une composition de plings.

        'plingharmo(prony, harmons, E)' appelle 'generateurDentAlea'
        mais il me semble plus simple de faire calculer l'onde
        par 'ProfilBase' et d'appeler le nombre de samples nécessaires.
        """
        PlingHarmo0.__init__(self)
        self.harmons = harmons
        self.nh = len(harmons)
        self.env = ProfilBase(E)
        self.diviseur = 2.0000005
        self.alea = serie.Serie002(*couple)
        if Table is None:
            Table = [[recta, 1., -1., 1.]]
        self.table = ProfilBase(Table)

