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
# enregistrer.py

""" module des classes 'Enregistreur' et 'Multi' """

import os
import numpy as np
from samplerate import SR #, MAXINTEGER
#from ajuster import prolongerZ
from origine import OrigineStr
#from conversions import extremum
from fusionner import fusionner
#from audiodirectalsa import play

__author__ = """Copyright (c) 2005-12 René Bastian (Wissembourg, FRANCE)
et Alexandre Fayolle pour la méthode fusion (2006)"""
__date__ = """2005.01.07, 2005.10.24, 2006.01.26, 2006.02.04, 2006.11.06,
           2012.06.10, 2013.02.08"""
__all__ = ["Multi", "Enregistreur"]

bdebug = True # boléen général pour débogage

class Enregistreur(OrigineStr):
    """
    Enregistre des signaux dans un fichier au format 'float64'.
    Les opérations se font au niveau du disque (tandis que la
    classe 'Partition' agit au niveau du concept musical).
    Certaines méthodes ont été expulsées dans 'enregistrer12.py'.
    """
    def __init__(self, nom, dureeTotale=1.0, bnouveau=True):
        """
        Si bnouveau: un nouveau fichier est créé pour
           lectur et écriture;
        sinon:
           si le fichier 'nom' existe, ouvre le fichier
           pour lecture et écriture;
           sinon, crée un fichier de zéros de durée minimum
           égale à 'dureeTotale'.
        'nom' : nom du fichier
        'dureeTotale' : durée en secondes
        """
        OrigineStr.__init__(self)
        self.nom = nom
        if not os.path.exists(nom) or bnouveau:
            self.dimension = int(dureeTotale * SR) + 1
            z = np.zeros(self.dimension, np.float64)
            z.tofile(nom)
        self.f = open(nom, "r+")
        self.dimension = os.fstat(self.f.fileno()).st_size / 8
        self.maximum = None

    def close(self):
        """ ferme les fichiers """
        self.f.close()

    def ajouter(self, signal, pt):
        """ additionne l'arroi 'signal' dans le fichier au
        point temporel donné.
        Cette fonction tient compte de ce que la fonction 'seek'
        prolonge automatiquement le fichier.
        'signal' : vecteur de nombres, de type 'numpy.ndarray.float64'
        'pt' : point temporel en secondes, type 'float'
        """
        assert pt >= 0.0
        n = int(pt * SR)
        noctets = n * 8
        try:
            d = signal.size
        except AttributeError:
            print("ajouter ligne 70", type(signal), "pt", pt)
            return
        if self.dimension < (n + d):
            self._prolonger(n + d + 1)
            self.dimension = os.fstat(self.f.fileno()).st_size / 8
        self.f.seek(noctets)
        try:
            w = np.fromfile(self.f, np.float64, d)
        except ValueError:
            print("Enregistreur:ajouter:ValueError")
            print("noctets %20i dimension %20i signal %10i" % \
                  (noctets, self.dimension, d))
            return
        try:
            w += signal
        except ValueError:
            print("Enregistreur:ajouter w+= signal", w.size, signal.size)
            return
        self.f.seek(noctets)
        w.tofile(self.f)
        self._dimension()

    def _dimension(self):
        """ met à jour la dimension du fichier """
        self.dimension = os.fstat(self.f.fileno()).st_size / 8

    def _prolonger(self, necessaire):
        """ prolonge le fichier pour atteindre 'necessaire' samples
        'necessaire' : nombre d'unités de type Float64 requises
        """
        z = np.zeros(SR, np.float64)
        self.f.seek(necessaire * 8)
        z.tofile(self.f)
        self._dimension()

class Multi(OrigineStr):
    """ installe un enregistreur multipistes; chaque piste
    est une instance de 'Enregistreur'.
    Compile une séquence de 1200 seq en env 600 sec.
    """
    def __init__(self, nomsouche, npistes, dureeInitiale=1.0,
                 nouveau=True):
        """
        'nomsouche' : nom générique pour les fichiers
        'npistes' : nombre de pistes
        'nouveau' :
            si True, l'existant est effacé
            si False, les signaux sont ajoutés à l'existant
        """
        OrigineStr.__init__(self)
        self.pistes = []
        for i in range(npistes):
            fnom = "".join([nomsouche, ".", str(i), "f64"])
            f = Enregistreur(fnom, dureeInitiale, nouveau)
            self.pistes.append(f)
        self.ext = 0
        self.npistes = npistes
        self.nomsouche = nomsouche

    def ajouter(self, pt, ncanal, signal):
        """ ajoute le 'signal' au point temporel 'pt' dans le
        canal 'ncanal'.
        """
        self.pistes[ncanal].ajouter(signal, pt)

    def close(self):
        """
        clôt toutes les pistes ouvertes
        """
        for f in self.pistes:
            f.close()

    def fusion(self, amorti=1.0):
        """ lit les fichiers 'self.nomsouche'+".?f64" et les réunit en un
        fichier 'self.nomsouche'+".raw".
        'amorti' : prévu pour adapter le signal s'il y a des dépassements. """
        assert amorti == 1.0
        self.close()
        v = fusionner(self.nomsouche, self.npistes)
        return v
