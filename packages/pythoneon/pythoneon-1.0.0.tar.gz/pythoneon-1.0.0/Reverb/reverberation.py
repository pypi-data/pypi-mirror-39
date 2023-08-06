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
# pythoneon/Reverb/reverberation.py
"""
fournit la classe Reverberation; on utilise surtout
   evt(signal, ratio),
   evtR(signal, profilratio) est à explorer;
il faudrait aussi explorer les différents paramètres initiaux.
"""

import numpy as np
from samplerate import SR, plus_petite_valeur
from Profils.profilbase import ProfilBase
from Maths.serie import Serie002
from origine import OrigineStr
from Canal.canal import CanalMono
from Reverb.traine import coupetraine

__author__ = """Copyright (c) 2005-13 René Bastian (Wissembourg, FRANCE)"""
__date__ = "2006.02.23, 07.09.15, 2012.01.18, 2012.06.02, 2013.01.20"

class Reverberation(OrigineStr):
    """
    encore un essai de reverb de plus,
    mais on a plaisir à l'utiliser ;
    essayer d'imposer une enveloppe spéciale avec une attaque molle
    pour éviter les répétitions percussives
    (voir essai dans mazus:floeter)
    intégrer cette manoeuvre dans cette classe ??
    """
    def __init__(self, dureeInitiale=1.0,
                 premierecart=0.050,
                 premiercoeff=0.125,
                 duree=4.,
                 ecartmin=0.04,
                 ecartmax=0.06,
                 upsilon=plus_petite_valeur,
                 #coupetraine=None,
                 alea=None):
        """
        installe une réverb ; les données initiales sont :
          premierecart=0.050
          premiercoeff=0.125
          duree=4.
          ecartmin=0.04
          ecartmax=0.06
        qu'on peut changer par 'change'.
        Il ne faut pas procéder par changement direct, car
        il faut faire effectuer les calculs par 'calcul'.
        """
        OrigineStr.__init__(self)
        self.dureeInitiale = dureeInitiale
        self.premierecart = premierecart
        self.premiercoeff = premiercoeff
        self.duree = duree
        self.ecartmin = ecartmin
        self.ecartmax = ecartmax
        self.upsilon = upsilon
        if alea is None:
            self.alea = Serie002(96785, 56347)
        else:
            self.alea = alea
        self.c = None
        self.coeff = None
        self.nreflexions = None
        #self.coupetraine = coupetraine
        # 'self.calcul()' calcule 'coeff' et 'nreflexions' donc doit être
        # placé après les mentions
        self.calcul()

    def calcul(self):
        """
        effectue les calculs nécessaires après un changement
        des valeurs.
        """
        ecartmoyen = (self.ecartmin + self.ecartmax) / 2.0
        self.coeff = np.exp((np.log(self.upsilon) - \
                             np.log(self.premiercoeff)) * \
                            ecartmoyen / self.duree)
        self.nreflexions = int(np.log(self.upsilon)/np.log(self.coeff)) + 1

    def __call__(self, signal):
        """
        retourne le signal réverbéré
        'signal' : le signal à réverbérer
        permet de séparer la réverb et le signal sec !
        """
        self.c = CanalMono(self.dureeInitiale)
        signal *= self.premiercoeff
        self.c.addT(0.0, signal)
        #print(self.ecartmin, self.ecartmax)
        #print(self.nreflexions)
        points = self.alea.uniform(self.ecartmin, self.ecartmax,
                                   self.nreflexions)
        #print("points.size", points #.size)
        try:
            points = np.add.accumulate(points)
        except TypeError:
            print(self)
        for pt in points:
            self.c.addT(pt, signal)
            signal = signal * self.coeff
        return self.c.a

    def evt(self, signal, ratio, btraine=True):
        """effectue un mélange sec/réverbéré
        'ratio' : proportion de signal sec
        coupetraine permet de ne garder rien de la traîne
           ou de garder une fraction de la traîne.
        """
        c = CanalMono(self.dureeInitiale)
        wrev = self(signal)
        c.addT(0.0, signal * ratio)
        c.addT(0.0, wrev * (1.0 - ratio))
        if btraine:
            return coupetraine(c.a)
        else:
            return c.a

    def evtR(self, signal, profilratio):
        """
        'profilratio' : description de l'évolution du ratio
           (proportion de signal direct)
        applique le 'profilratio' au signal pour:
           - envoyer un signal du premier plan vers le fond,
           - amener un signal du fond au premier plan.
        Le traitement de la traîne ne semble pas nécessaire.
        """
        dsignal = signal.size / float(SR)
        c = CanalMono(dsignal)
        w = self(signal)
        ratio = ProfilBase(profilratio).samples(w.size)
        #print(ratio.size, wrev.size)
        c.addT(0.0, w * ratio)
        c.addT(0.0, w * (1.0 - ratio))
        return c.a

    def change(self, dureeInitiale=None,
               premierecart=None,
               premiercoeff=None,
               duree=None,
               ecartmin=None,
               ecartmax=None,
               upsilon=None,
               #coupetraine=None,
               ccouple=None):
        """
        permet de changer les valeurs des attributs.
        """
        if dureeInitiale:
            self.dureeInitiale = dureeInitiale
        elif premierecart:
            self.premierecart = premierecart
        elif premiercoeff:
            self.premiercoeff = premiercoeff
        elif duree:
            self.duree = duree
        elif ecartmin:
            self.ecartmin = ecartmin
        elif ecartmax:
            self.ecartmax = ecartmax
        elif upsilon:
            self.upsilon = upsilon
        elif ccouple is not None:
            self.alea = Serie002(ccouple[0], ccouple[1])
        #elif coupetraine is not None:
            #self.bcoupetraine = bcoupetraine
        self.calcul()
