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
# eventails.py
"""
fournit les classes
  - EventailGlobal (à faire)
  - EventailSucc
"""

from serie import Serie002
from profilbase import ProfilBase
from origine import OrigineStr
from .abanicos import interpoler

__date__ = "2009.06.29, 2012.07.03"
__author__ = "(c) 2009 René Bastian -- Wissembourg"

class Eventail(OrigineStr):
    """
    construit un simple éventail de profils par interpolation
    """
    def __init__(self, modele):
        """instancie
        modele = [(plage des y0), (plage des y1), fac: (plage des puiss)]
        """
        OrigineStr.__init__(self)
        self.modele = modele

    def evt(self, n):
        """
        retourne n profils dérivés
        """
        return interpoler(n, self.modele)

    def change(self, modele):
        """ change le modèle
        """
        self.modele = modele

class EventailSucc: #(Origine0):
    """
    Cette classe fournit un éventail de profils-rectas; cet éventail
    comprend 'nombre' profils allant de la valeur 'plage[0]
    à la valeur plage[1].
    Les profils varient donc selon les domaines donnés
    'brut' retourne des profils-listes
    'evt' retourne les profils-vecteurs
    """
    def __init__(self, nombre, modele):
        """instancie
        modele = [(plage des y0), (plage des y1), fac: (plage des puiss)]
        """
        #Origine0.__init__(self) #, xbruit=9675, abruit=1763)
        xbruit = 9675
        abruit = 1763
        self.modele = modele
        self.nombre = nombre
        self.compteur = 0
        self.r = []
        self.max = float(nombre) - 1.
        self.alea = Serie002(xbruit, abruit) #inutile dans certains cas
        self.succbrut()

    def succbrut(self, message=False):
        """
        retourne le profil-liste suivant
        """
        if self.compteur == self.nombre:
            if message:
                print("EventailSucc: un nouvel éventail")
            self.compteur = 0
        self.r = []
        for pm in self.modele:
            r = []
            for x in pm:
                if isinstance(x, tuple):
                    v = x[0] + (self.compteur/self.max) * (x[1] - x[0])
                    r.append(v)
                else:
                    r.append(x)
            self.r.append(r)
        self.compteur += 1
        return self.r

    def aleaevt(self):
        """
        calcule un profil dont les valeurs varient dans les limites
        données par le modèle.
        """
        res = []
        for pm in self.modele:
            r = []
            for x in pm:
                if isinstance(x, tuple):
                    v = self.alea.uniform(x[1], x[0])
                    r.append(v)
                else:
                    r.append(x)
            res.append(r)
        return res

    def aleaindex(self):
        """
        tire l'index sériel suivant et retourne le profil correspondant
        """
        ix = self.alea.randint(0, self.nombre)
        return self.r[ix]

    def succevtT(self, duree):
        """
        retourne le profil-vecteur suivant ayant une durée 'duree'
        """
        return ProfilBase(self.succbrut()).temps(duree)

    def succevtN(self, n):
        """
        retourne le profil-vecteur suivant ayant 'n' samples
        """
        return ProfilBase(self.succbrut()).samples(n)

#    def succevt(self):
#        """
#        retourne le profil-vecteur suivant
#        théorique : car en usage normal on passe par ProfilBase
#        """
#        return profil(self.succbrut)

