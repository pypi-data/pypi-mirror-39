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
# Profils/faireprofils.py

"""
module pour construire des profils,
devrait être généralisé, mais la rédaction simple a aussi des avantages.
"""
import numpy as np
from conversions import extremum
from profils import recta, cubica
from origine import OrigineStr
from samplerate import sr
from serie import Serie002
from profilbase import ProfilBase

__author__ = "Copyright (c) 2009 René Bastian (Wissembourg, FRANCE)"
__date__ = "2009.12.10, 2012.11.24"


class FaireTable(OrigineStr):
    """
    Principe : le profil donne l'allure sommaire
    ce profil est dentelé par le générateur sériel
    puis on passe des harmoniques à la forme d'onde.

On peut concevoir la procédure suivante:
- dessiner une table d'onde : profiltable0
- en faire la FFT.real : profilharmo = fft(profiltable0)
- imposer une variation sérielle : profilharmon += bruit
- faire la IFFT pour obtenir : profiltable = ifft(prfilharmo)

    """
    def __init__(self, pprofil, nombre, minimum=0.0,
                 xx=675431, xa=198342):
        """
        Profil donne l'allure générale de l'enveloppe des harmoniques ;
        le générateur sériel découpe ce profil.
        'Profil : un profil-liste
        'nombre : nombre d'harmoniques souhaité
        'couple : semence du générateur sériel
        'minim : valeur minimum des harmoniques
        """
        OrigineStr.__init__(self)
        self.harm = None # pour faire plaisir à pylint
        self.v = None # aussi
        self.profiltable = ProfilBase(pprofil)
        self.alea = Serie002(xx, xa)
        self.nombre = nombre
        self.minimum = minimum
        self.table = self._table()

    def _table(self):
        """
        calcule la table à partir des harmoniques
        """
        self.harm = self.profiltable.samples(self.nombre)
        print(self.minimum, 1.0, self.nombre)
        bruit = self.alea.uniform(self.minimum, 1.0, self.nombre)

        self.harm *= bruit
        t = np.fft.ifft(self.harm, 2*sr).real[:sr]
        return t / extremum(t)
        #print(self.table.size)

    def elastique(self, prop, rmin, rmax):
        """
        'p : proportion du nombre d'harmoniques qui vont être
        agrandis ou réduits
        """
        n = int(self.nombre) * prop
        self.v = np.ones(self.nombre, np.float64)
        for _ in range(n):
            p = self.alea.randint(0, self.nombre)
            self.v[p] = self.alea.uniform(rmin, rmax)
        self.harm *= self.v
        self.table = np.fft.ifft(self.harm, sr).real
        return self.table

    def evt(self):
        """
        retourne la table calculée
        """
        return self.table

    def __call__(self):
        """
        retourne la table calculée
        """
        return self.table

FaireTable09 = FaireTable

def faireTable(ng, nd, alea):
    """ construit une table de ng segments
    au-dessus de zéro et nd segments en-dessous
    voir tfaireprofils.py """
    if ng < 2:
        ng = 2
    if nd < 2:
        nd = 2
    r = faireProfilEnveloppe(ng, alea)
    r.extend(faireProfilEnveloppeNegatif(nd, alea))
    return r

def faireProfilSym(n, alea):
    "écrit un profil de variation d'enveloppe"
    r = []
    y0 = 0.0
    for _ in range(n-1):
        y1 = alea.uniform(0.0, 1.0)
        r.append([recta, alea.uniform(0.1, 0.9), y0, y1])
        y0 = y1
    r.append([recta, alea.uniform(0.1, 0.9), y0, 0.0])
    return r

def faireTableSym(n, alea):
    """ construit une table de ng segments
    au-dessus de zéro et nd segments en-dessous
    voir tfaireprofils.py """
    if n < 2:
        print("faireTable(ng, alea): ng < 2")
        return
    r, r2 = [], []
    y0 = 0.0
    for _ in range(n-1):
        y1 = alea.uniform(0.0, 1.0)
        d = alea.uniform(0.1, 0.9)
        r.append([recta, d, y0, y1])
        r2.append([recta, d, -y0, -y1])
        y0 = y1
    d = alea.uniform(0.1, 0.9)
    r.append([recta, d, y0, 0.0])
    r2.append([recta, d, -y0, 0.0])
    r.extend(r2)
    return r

def faireProfilHarmonique(duree, alea, dtmin, dtmax, ymin=0.0, ymax=1.0):
    """
    construit sériellement un profil de cubiques se raccordant par des
    pentes nulles, d'une durée totale 'duree'
    entre 'ymin' et 'ymax', chaque segment durant entre 'dtmin' et 'dtmax',
    les valeurs initiale et finale étant 'yini' et 'yfin'.
    adapté de la fonction Generateurs.faireprofils.faireProfil
    """
    y0, yfin = 0.0, 0.0
    t = 0.0
    r = []
    borne = duree - dtmax
    while t < duree:
        if t < borne:
            dt = alea.uniform(dtmin, dtmax)
            y1 = alea.uniform(ymin, ymax)
        else:
            dt = duree - t
            y1 = yfin
        t += dt
        r.append([cubica, dt, y0, 0.0, y1, 0.0])
        y0 = y1
    return r

def faireProfilHauteur(n, hautmin, hautmax, alea, dtmin=0.1, dtmax=0.9,
                       bdiscontinu=False):
    """écrit un profil de variation de la hauteur (p.ex. d'un filtre)
    composé de 'n' segments
    """
    r = []
    y0 = alea.uniform(hautmin, hautmax)
    for _ in range(n):
        y1 = alea.uniform(hautmin, hautmax)
        r.append([recta, alea.uniform(dtmin, dtmax), y0, y1])
        if bdiscontinu:
            y0 = alea.uniform(hautmin, hautmax)
        else:
            y0 = y1
    return r

def faireCRecurs(n, alea, cmin=0.85, cmax=0.999):
    "construit un profil pour CRecurs pour PercuEthnique3"
    r = []
    for _ in range(n):
        r.append([recta, alea.uniform(0.1, 4), alea.uniform(cmin, cmax),
                  alea.uniform(cmin, cmax)])
    return r

def faireProfilEnveloppe(n, alea):
    "écrit un profil de variation d'enveloppe"
    r = []
    y0 = 0.0
    for _ in range(n-1):
        y1 = alea.uniform(0.0, 1.0)
        r.append([recta, alea.uniform(0.1, 0.9), y0, y1])
        y0 = y1
    r.append([recta, alea.uniform(0.1, 0.9), y0, 0.0])
    return r

def faireProfilEnveloppeNegatif(n, alea):
    "écrit un profil de variation d'enveloppe"
    r = []
    y0 = 0.0
    for _ in range(n-1):
        y1 = alea.uniform(0.0, -1.0)
        r.append([recta, alea.uniform(0.1, 0.9), y0, y1])
        y0 = y1
    r.append([recta, alea.uniform(0.1, 0.9), y0, 0.0])
    return r

def faireProfilPano(n, alea):
    "écrit un profil de variation de panoramique"
    r = []
    y0 = alea.uniform(0.0, 1.0)
    for _ in range(n):
        y1 = alea.uniform(0.0, 1.0)
        r.append([recta, alea.uniform(0.1, 0.9), y0, y1])
        y0 = y1
    return r

def faireEcarts(n, alea, dtmin=1.0, dtmax=4.0, ecmin=0.1, ecmax=0.2):
    """produit un profil d'écarts pour Percu"""
    r = []
    for _ in range(n):
        r.append([recta, alea.uniform(dtmin, dtmax),
                  alea.uniform(ecmin, ecmax),
                  alea.uniform(ecmin, ecmax)])
    return r

def faireProfilN(n, alea, dtmin, dtmax, ymin, ymax,
                 yini=None, yfin=None):
    """
    construit sériellement un profil de 'n' cubiques se raccordant par des
    pentes nulles, entre 'ymin' et 'ymax', chaque segment durant
    entre 'dtmin' et 'dtmax',
    les valeurs initiale et finale étant 'yini' et 'yfin'.
    """
    if yini is None:
        y0 = alea.uniform(ymin, ymax)
    else:
        y0 = yini
    r = []
    for _ in range(n-1):
        dt = alea.uniform(dtmin, dtmax)
        y1 = alea.uniform(ymin, ymax)
        r.append([cubica, dt, y0, 0.0, y1, 0.0])
        y0 = y1
    dt = alea.uniform(dtmin, dtmax)
    if yfin:
        y1 = yfin
    else:
        y1 = alea.uniform(ymin, ymax)
    r.append([cubica, dt, y0, 0.0, y1, 0.0])
    return r

def faireProfilD(n, alea, ymin, ymax, yini=None, yfin=None):
    """
    construit sériellement un profil de 'n' cubiques se raccordant par des
    pentes nulles, entre 'ymin' et 'ymax';
    une durée arbitraire (1.0) est bombardée sériellement de
    telle façon à déterminer 'n' durées (le profil final est construit
    par ProfilBase);
    les valeurs initiale et finale sont 'yini' et 'yfin'.
    """
    if yini is None:
        y0 = alea.uniform(ymin, ymax)
    else:
        y0 = yini
    r = []
    #print("***", n)
    dts = alea.uniform(0.0, 1.0, n)
    for dt in dts[:-1]:
        y1 = alea.uniform(ymin, ymax)
        r.append([cubica, dt, y0, 0.0, y1, 0.0])
        y0 = y1
    dt = dts[-1]
    if yfin is None:
        y1 = alea.uniform(ymin, ymax)
    else:
        y1 = yfin
    r.append([cubica, dt, y0, 0.0, y1, 0.0])
    return r

def faireProfil(duree, alea, dtmin, dtmax, ymin, ymax,
                yini=None, yfin=None):
    """
    construit sériellement un profil de cubiques se raccordant par des
    pentes nulles, d'une durée totale 'duree'
    entre 'ymin' et 'ymax', chaque segment durant entre 'dtmin' et 'dtmax',
    les valeurs initiale et finale étant 'yini' et 'yfin'.
    """
    if yini is None:
        y0 = alea.uniform(ymin, ymax)
    else:
        y0 = yini
    t = 0.0
    r = []
    while t < duree:
        dt = alea.uniform(dtmin, dtmax)
        t += dt
        if t < duree:
            y1 = alea.uniform(ymin, ymax)
        else:
            if yfin is None:
                y1 = alea.uniform(ymin, ymax)
            else:
                y1 = yfin
        r.append([cubica, dt, y0, 0.0, y1, 0.0])
        y0 = y1
    return r
