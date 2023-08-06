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
#Partition/partition_simple.py
""" fournit la classe PartitionSimple qui a les avantages
de la partition traditionnelle : flexibilité du temps.
Elle prend la suite de Partition en se passant de deux
classes (Enregistreur, Multi) et du concept de tempo.
"""

import os
import numpy as np
from origine import OrigineStr
from canal import CanalMono, record
from fusionner import fusionner
from samplerate import sr, MAXINTEGER

__author__ = "Copyright (c) 2006-2010 René Bastian (Wissembourg, FRANCE)"
__date__ = "2006.05.08, 07.08.24, 09.10.05, 2010.06.12, 2014.08.07"

class PartitionSimple(OrigineStr):
    """classe permettant des opérations comparables à celles
    qui sont possibles avec une partition de musique habituelle;
    sans opérations sur le tempo."""
    def __init__(self, nomsouche, npistes=2, dureeInitiale=1.0):
        """
        'nomsouche' : nom des fichiers à réaliser
        'npistes' : nombre de canaux
        'dureeInitiale' : durée prévue; si on donne approximativement
        la durée prévue, cela évite de calculer des rallonges en cours
        de compilation
        """
        OrigineStr.__init__(self)
        self.nomsouche = nomsouche
        self.npistes = npistes
        self.f = []
        for i in range(npistes):
            fnom = "".join((nomsouche, ".", str(i), "f64"))
            self.f.append(open(fnom, "w+"))
        self.t = 0.0
        n = int(dureeInitiale * sr) + 1
        z = np.zeros(n, np.float64)
        for i in range(npistes):
            z.tofile(self.f[i])

    def _prolonger(self, necessaire):
        """ prolonge les fichiers pour atteindre 'necessaire' samples
        'necessaire' : nombre d'unités de type np.float64 requises
        """
        z = np.zeros(sr, np.float64)
        for f in self.f:
            f.seek(necessaire * 8)
            z.tofile(f)
        #self._dimension()

    def addit(self, nocanal, signal):
        """ additionne le signal au pt temporel actuel
        du canal 'nocanal' """
        n = self.t * sr
        noctets = n * 8
        d = signal.size
        xnom = "".join((self.nomsouche, ".", str(nocanal), "f64"))
        dimension = os.stat(xnom).st_size/8
        if dimension < (n + d):
            self._prolonger(n + d + 1)
        self.f[nocanal].seek(noctets)
        try:
            w = np.fromfile(self.f[nocanal], np.float64, d)
        except ValueError:
            print("Erreur:Partition:add:ValueError")
            mess = "noctets %20i dimension %20i signal %10i"
            print(mess % (noctets, self.dimension, d))
            return
        try:
            w += signal
        except ValueError:
            print("Erreur:Partition:add: w+= signal", w.size, signal.size)
            return
        self.f[nocanal].seek(noctets)
        w.tofile(self.f[nocanal])

    def evt(self, signals, binfo=False):
        " ajoute les signals au point temporel actuel "
        try:
            for i, signal in enumerate(signals):
                self.addit(i, signal)
        except IOError:
            print("PartitionSimple.evt: pas de signal")
            return
        if binfo:
            self.kt(signals)

    def pt(self, xt):
        "donne un nouveau point temporel absolu"
        self.t = xt

    def ptx(self):
        """ retourne la valeur du point temporel """
        return self.t

    def dr(self, ecart):
        """fixe le prochain point temporel en additiont 'ecart'
        au point temporel actuel."""
        self.t += ecart

    def ecart(self, ecart):
        "comme 'dr'"
        self.t += ecart

    def dimension(self):
        "retourne la durée actuelle de la partition"
        nom = self.nomsouche + ".0f64"
        return os.stat(nom).st_size/8

    def insert(self, souche, ampli=1.0):
        """ ajoute le son "fnom.Xf64" au point actuel """
        r = []
        for ncanal in range(self.npistes):
            nomf = "".join([souche, ".", str(ncanal), "f64"])
            w = np.fromfile(nomf, np.float64)
            w *= ampli
            r.append(w)
        self.evt(r, binfo=True)

    def kt(self, signals):
        """ point temporel actuels """
        d = 0
        for sig in signals:
            d = max(d, len(sig))
        tz = float(d) / sr
        print("t %8.3f + %8.3f -> %8.3f" % (self.t, tz, self.t+tz))

    def close(self):
        """ écrit le fichier raw """
        for i in range(self.npistes):
            self.f[i].close()
        fusionner(self.nomsouche, self.npistes, MAXINTEGER)

    def montage(self, instructions):
        """ insère les fichiers f64 aux points temporels donnés
        avec l'amplitude donnée
        Syntaxe:
          (["t"], souche, ecart|pt, ampli)
        "t" indique qu'on donne un nouveau point temporel,
        autrement on donne un écart."""
        for instr in instructions:
            r = []
            if instr[0] == "t":
                souche, pt, ampli = instr[1:]
                self.pt(pt)
            else:
                souche, ecart, ampli = instr
                self.dr(ecart)
            for ncanal in range(self.npistes):
                nomf = "".join([souche, ".", str(ncanal), "f64"])
                w = np.fromfile(nomf, np.float64)
                w *= ampli
                r.append(w)
            self.evt(r, binfo=True)

    def montageCanal(self, instructions):
        """ insère les fichiers f64 aux points temporels donnés
        avec l'amplitude donnée; uniquement en stéréo classique. """
        cg, cd = CanalMono(), CanalMono()
        for instr in instructions:
            souche, pt, ampli = instr
            print(souche, pt, ampli)
            nomf = souche + ".0f64"
            wg = np.fromfile(nomf, np.float64)
            wg *= ampli
            nomf = souche + ".1f64"
            wd = np.fromfile(nomf, np.float64)
            wd *= ampli
            cg.addT(pt, wg)
            cd.addT(pt, wd)
        record(cg.a, cd.a, self.nomsouche)
