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
# Tpythoneon/Reverb/reverbcumul.py

"""
les sons s'accumulent dans la reverb
et on obtient ainsi des sons percussifs.
"""

import numpy as np
from serie import Serie002
from canal import CanalMono
from samplerate import epsilon as peps
from origine import OrigineStr

class Reverberation12(OrigineStr):
    """ Toutes les réflexions s'accumulent """
    def __init__(self, alea, bcumul=False, dureeInitiale=1.0,
                 premierecart=0.050,
                 premiercoeff=0.125,
                 duree=4.,
                 ecartmin=0.04,
                 ecartmax=0.06,
                 epsilon=peps):
        """
          premierecart = 0.050
          premiercoeff = 0.125
          duree = 4.
          ecartmin = 0.04
          ecartmax = 0.06
        qu'on peut changer par 'change'.
        Il ne faut pas procéder par changement direct, car
        il faut faire effectuer les calculs par 'calcul'.
        """
        OrigineStr.__init__(self)
        self.bcumul = bcumul
        self.dureeInitiale = dureeInitiale
        self.premierecart = premierecart
        self.premiercoeff = premiercoeff
        self.duree = duree
        self.ecartmin = ecartmin
        self.ecartmax = ecartmax
        self.epsilon = epsilon
        self.alea = alea
        self.nreflexions = None
        self.coeff = None
        self.nreflexions = None
        self.calcul()
        self.c = CanalMono(self.dureeInitiale)

    def calcul(self):
        """ effectue les calculs nécessaires après un changement
        des valeurs. """
        ecartmoyen = (self.ecartmin + self.ecartmax) / 2.0
        self.coeff = np.exp((np.log(self.epsilon) - \
                             np.log(self.premiercoeff)) * \
                            ecartmoyen / self.duree)
        self.nreflexions = int(np.log(self.epsilon)/np.log(self.coeff)) + 1

    def evt(self, signal):
        " effectue la réverb du signal"
        if not self.bcumul:
            self.c = CanalMono()
        signal *= self.premiercoeff
        self.c.addT(0.0, signal)
        pts = self.alea.uniform(self.ecartmin, self.ecartmax, self.nreflexions)
        pts = np.add.accumulate(pts)
        for pt in pts:
            self.c.addT(pt, signal)
            signal = signal * self.coeff
        return self.c.a

    def change(self, dureeInitiale=None, premierecart=None,
               premiercoeff=None, duree=None, ecartmin=None,
               ecartmax=None, epsilon=None, alea=None):
        """ permet de changer les valeurs des attributs.
        """
        if dureeInitiale is not None:
            self.dureeInitiale = dureeInitiale
        elif premierecart is not None:
            self.premierecart = premierecart
        elif premiercoeff is not None:
            self.premiercoeff = premiercoeff
        elif duree is not None:
            self.duree = duree
        elif ecartmin is not None:
            self.ecartmin = ecartmin
        elif ecartmax is not None:
            self.ecartmax = ecartmax
        elif epsilon is not None:
            self.epsilon = epsilon
        elif alea is not None:
            self.alea = alea
        self.calcul()

class ReverberationCumulative(OrigineStr):
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
                 duree=1.,
                 ecartmin=0.04,
                 ecartmax=0.06,
                 epsilon=peps,
                 xx=96785, xa=56347):
        """
        installe une réverb ; les données initiales sont :
          premierecart = 0.050
          premiercoeff = 0.125
          duree = 4.
          ecartmin = 0.04
          ecartmax = 0.06
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
        self.epsilon = epsilon
        self.alea = Serie002(xx, xa)
        self.nreflexions, self.coeff = None, None
        self.calcul()
        self.c = CanalMono(self.dureeInitiale)

    def calcul(self):
        """
        calcule self.nreflexions et self.coeff à l'intialisation ou
        après un changement de valeurs.
        """
        ecartmoyen = (self.ecartmin + self.ecartmax) / 2.0
        self.coeff = np.exp((np.log(self.epsilon) - \
                             np.log(self.premiercoeff)) * \
                            ecartmoyen / self.duree)
        self.nreflexions = int(np.log(self.epsilon)/np.log(self.coeff)) + 1

    def evt(self, signal):
        """ retourne le signal réverbéré
        'signal' : le signal à réverbérer """
        signal *= self.premiercoeff
        self.c.addT(0.0, signal)
        Pts = self.alea.uniform(self.ecartmin, self.ecartmax, self.nreflexions)
        Pts = np.add.accumulate(Pts)
        for pt in Pts:
            self.c.addT(pt, signal)
            signal = signal * self.coeff
        return self.c.ex()

    def filtre(self, signal, filtre):
        """ EXISTENCE PROBLÉMATIQUE
        retourne le signal réverbéré
        'signal' : le signal à réverbérer
        """
        self.c = CanalMono(self.dureeInitiale)
        signal *= self.premiercoeff
        self.c.addT(0.0, signal)
        Pts = self.alea.uniform(self.ecartmin, self.ecartmax, self.nreflexions)
        Pts = np.add.accumulate(Pts)
        for pt in Pts:
            signal = filtre.filtrer(signal)
            self.c.addT(pt, signal)
            signal = signal * self.coeff
        return self.c.ex()

    def __call__(self, signal):
        " comme evt "
        return self.evt(signal)

    def change(self, premierecart=None, premiercoeff=None,
               duree=None, ecartmin=None, ecartmax=None,
               xx=None, xa=None):
        """ permet de changer les valeurs des attributs.
        dureeInitiale, epsilon sont inutiles"""
        if premierecart is not None:
            self.premierecart = premierecart
        elif premiercoeff is not None:
            self.premiercoeff = premiercoeff
        elif duree is not None:
            self.duree = duree
        elif ecartmin is not None:
            self.ecartmin = ecartmin
        elif ecartmax is not None:
            self.ecartmax = ecartmax
        elif xa is not None and xx is not None:
            self.alea = Serie002(xa, xx)
        self.calcul()

#    def change2(self, params):
#        """ permet de changer les valeurs des attributs.
#        Exemple: params = [None, None, valeur, None, ...]
#        dureeInitiale, epsilon sont inutiles"""
#        premierecart, premiercoeff, \
#        duree, ecartmin, ecartmax, xx, xa = params
#        if dureeInitiale is not None:
#            self.dureeInitiale = dureeInitiale
#        elif premierecart is not None:
#            self.premierecart = premierecart
#        elif premiercoeff is not None:
#            self.premiercoeff = premiercoeff
#        elif duree is not None:
#            self.duree = duree
#        elif ecartmin is not None:
#            self.ecartmin = ecartmin
#        elif ecartmax is not None:
#            self.ecartmax = ecartmax
#        elif epsilon is not None:
#            self.epsilon = epsilon
#        elif xa is not None and xx is not None:
#            self.alea = Serie002(xa, xx)
#        self.calcul()
#
#    def change3(self, params):
#        """ permet de changer les valeurs des attributs. """
#        for i, valeur in params:
#            if i == 0:
#                self.premierecart = valeur
#            elif i == 1:
#                self.premiercoeff = valeur
#            elif i == 2:
#                self.duree = valeur
#            elif i == 3:
#                self.ecartmin = valeur
#            elif i == 4:
#                self.ecartmax = valeur
#            elif i == 5:
#                xa, xx = valeur
#                self.alea = Serie002(xa, xx)
#        self.calcul()
