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
# Ondes/Tables/ondepartable.py
"""
ondepartable.py rassemble des fonctions
permettant de produire des ondes
par balayage de tables
"""

import numpy as np
#from profilbase import ProfilBase
from samplerate import SR

__date__ = "2006.02.07, 2009.01.19, 2015.10.19"
__author__ = "Copyright (c) René Bastian 2002-2015 <rbastian@free.fr>"
##FIN
#__all__ = ["ondeTable", "ondeTableN", "ondeTableMF", "ondeTablePMF",
#           "oscillateurMF", "oscillateurN", "oscillateur", "ondeTable0"
#           ]

def ondeTable(table, modfreq):
    """ retourne une onde de fréquence variable selon 'modfreq'
    par balayage de la 'table'.
    'table' : une forme d'onde (souvent SR échantillons)
    'modfreq' : un vecteur des fréquences
    En général, modfreq = profil(E) ou
       modfreq = ProfilBase(E).temps(duree)
    """
    k = float(table.size) / SR
    phases = np.cumsum(modfreq * k)
    phases = phases.astype(np.int32)
    indices = phases % table.size
    return table[indices]

def ondeTableAncienne(table, modfreq):
    """ retourne une onde de fréquence variable selon 'modfreq'
    par balayage de la 'table'.
    'table' : une forme d'onde (souvent SR échantillons)
    'modfreq' : un vecteur des fréquences
    En général, modfreq = profil(E) ou
       modfreq = ProfilBase(E).temps(duree)
    """
    phases = np.cumsum(modfreq)
    phases = phases.astype(np.int32)
    indices = phases % table.size
    return table[indices]

def ondeTableInterpol(table, modfreq):
    """ retourne une onde de fréquence variable selon 'modfreq'
    par balayage de la 'table' avec interpolation.
    'table' : une forme d'onde (souvent SR échantillons)
    'modfreq' : un vecteur des fréquences
    En général, modfreq = profil(E) ou
       modfreq = ProfilBase(E).temps(duree)
    """
    phases = np.cumsum(modfreq)
    vt = phases % table.size
    n = vt.size
    w = np.zeros(n)
    for i in range(0, n):
        try:
            i0 = int(vt[i])
            if i0 != n -1:
                dy = (table[i0+1] - table[i0]) * (vt[i] - i0)
            else:
                dy = (table[0] - table[i0]) * (vt[i] - i0)
        except IndexError:
            pass
        w[i] = dy + table[i0]
    return w

def ondeTableInterpol_1(table, modfreq):
    """ retourne une onde de fréquence variable selon 'modfreq'
    par balayage de la 'table' avec interpolation.
    'table' : une forme d'onde (souvent SR échantillons)
    'modfreq' : un vecteur des fréquences
    En général, modfreq = profil(E) ou
       modfreq = ProfilBase(E).temps(duree)
    """
    phases = np.cumsum(modfreq)
    vt = phases % table.size
    n = vt.size
    w = np.zeros(n)
    for i in range(0, n):
        try:
            i0 = int(vt[i])
            if i0 != vt[i]:
                dy = (table[i0+1] - table[i0]) * (vt[i] - i0)
            else:
                dy = 0.0
        except IndexError:
            break
        w[i] = dy + table[i0]
    return w

def ondeTableFreqFixe(table, freq, duree):
    " la fréquence est fixe "
    vmf = np.ones(int(duree * SR)) * freq
    return ondeTable(table, vmf)

def ondeTableT(table, freq, duree, ph=0.0):
    """retourne une onde de fréquence 'freq' de durée 'duree'
    par balayage de la 'table'.
    'table' : vecteur numarray
    'freq ' : float, fréquence
    'duree' : float, durée
    """
    table = np.array(table)
    n = (duree + ph) * SR
    phases = np.arange(ph, n * freq, freq) % len(table)
    iphases = phases.astype(np.int32)
    return table[iphases]

##FIN

if __name__ == "__main__":
    print("voir test/test_ondepartable")
