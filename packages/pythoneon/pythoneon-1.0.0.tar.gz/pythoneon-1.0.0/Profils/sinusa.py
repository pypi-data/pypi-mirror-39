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
# sinusa.py

"""
des profils avec des bouts de cosinus
(utilise les fonctions circulaires de numpy)
"""

import numpy as np

from samplerate import SR

__all__ = [
    "demicosT", "demicosN", "arc", "quartcosDN", "quartcosAN",
    "quartcosDT", "quartcosAT", "demicosDN", "_demicosAN",
    "_demicosDT", "_demicosAT", "cosina", "cosinux", "cosinax"
    ]
__author__ = "Copyright (c) 2009 René Bastian (Wissembourg, FRANCE)"
__date__ = "2009.05.16, 2013.07.29"

def arc(n):
    """ dessine un demi-cercle de n samples
    RETROUVER L'ALGO RÉCURSIF """
    if n % 2 == 1: # impair
        m1 = n/2
        m2 = m1 +1
    else:
        m1 = m2 = n/2
    a1 = demicosN(m1, 0.0, 1.0, dernier=False)
    a2 = demicosN(m2, 1.0, 0.0)
    return np.concatenate((a1, a2))

def demicosT(duree, y0, y1, dernier=True):
    """
    dessine un demi-cosinus allant de 'y0' à 'y1' en une durée 'duree';
    remplace une 'cubica' quand les pentes sont 0.0
    """
    n = int(duree * SR)
    if not dernier:
        n += 1
    if y0 < y1:
        v = np.linspace(np.pi, 2 * np.pi, n)
    elif y0 > y1:
        v = np.linspace(0.0, np.pi, n)
    v = (np.cos(v) + 1.0) * 0.5
    v = v * abs(y1 - y0) + min(y1, y0)
    if dernier:
        return v
    else:
        return v[:-1]

def demicosN(n, y0, y1, dernier=True):
    """ dessine un demi-cosinus allant de y0 à y1 en n samples"""
    if not dernier:
        n += 1
    if y0 < y1:
        v = np.linspace(np.pi, 2 * np.pi, n)
    elif y0 > y1:
        v = np.linspace(0.0, np.pi, n)
    v = (np.cos(v) + 1.0) * 0.5
    v = v * abs(y1 - y0) + min(y1, y0)
    if dernier:
        return v
    else:
        return v[:-1]

def quartcosDN(n, y0=1.0, y1=0.0, dernier=True):
    """calcule 'n' valeurs cosinus descendant de 1. à 0.
    si 'dernier=False' on récolte n-1 valeurs d'où l'ajustement
    """
    if not dernier:
        n += 1
    if y0 < y1:
        y0, y1 = y1, y0
    v = np.linspace(0.0, np.pi/2, n)
    v = (np.cos(v) * (y0 - y1)) + y1
    if dernier:
        return v
    else:
        return v[:-1]

def quartcosAN(n, y0=0.0, y1=1.0, dernier=True):
    """calcule 'n' valeurs cosinus ascendant de 0. à 1.
    si 'dernier=False' on récolte n-1 valeurs d'où l'ajustement
    """
    if not dernier:
        n += 1
    if y0 > y1:
        y0, y1 = y1, y0
    v = np.linspace(np.pi/2, 0.0, n)
    v = (np.cos(v) * (y1 - y0)) + y0
    if dernier:
        return v
    else:
        return v[:-1]

def quartcosDT(d, y0=1.0, y1=0.0, dernier=True):
    "temps au lieu de nombre"
    n = int(d * SR)
    return quartcosDN(n, y0, y1, dernier)

def quartcosAT(d, y0=0.0, y1=1.0, dernier=True):
    "temps au lieu de nombre"
    n = int(d * SR)
    return quartcosAN(n, y0, y1, dernier)

def demicosDN(y0, y1, n, dernier=True):
    """calcule 'n' valeurs cosinus descendant de 1. à -1.
    si 'dernier=False' on récolte n-1 valeurs
    """
    if not dernier:
        n += 1
    v = np.linspace(0.0, np.pi, n)
    v = ((np.cos(v) + 1.) * 0.5 * (y1 - y0)) + y1
    if dernier:
        return v
    else:
        return v[:-1]

def _demicosAN(y0, y1, n, dernier=True):
    "calcule 'n' valeurs cosinus montant de -1. à 1."
    if not dernier:
        n += 1
    v = np.linspace(np.pi, 2 * np.pi, n)
    if dernier:
        return np.cos(v) * (y1 - y0) + y0
    else:
        return (np.cos(v) * (y1 - y0) + y0)[:-1]

def _demicosDT(y0, y1, d, dernier=True):
    "calcule les cosinus descendant de 1. à -1.en un temps 'd'"
    n = int(d * SR)
    return demicosDN(y0, y1, n, dernier)

def _demicosAT(y0, y1, d, dernier=True):
    "calcule les cosinus ascendant de -1. à 1.en un temps 'd'"
    n = int(d * SR)
    return _demicosAN(y0, y1, n, dernier)

def cosina(dt, y0, y1, term=False):
    """ au lieu de calculer une 'cubica' avec des pentes 0.0,
    ce qui est très fréquent
    on calcule le cosinus sur une moitié de période.
    si 'term', on finit sur la valeur finale exacte.
    """
    freq = 0.5 / dt
    if not term:
        T = np.arange(dt, 0.0, -1./SR) * freq
    else:
        n = int(dt * SR)
        T = np.linspace(dt, 0.0, n) * freq
    return (np.cos(2 * np.pi * T) + 1.) * 0.5 *(y1 - y0) + y0

def cosinux(dt, y0, a0, y1, a1, term=False):
    """
    y0, y1 : valeurs en y
    a0, a1 : angle initial et final exprimé en proportion de 2*pi
    peu intéressant
    """
    a0 = a0 / (2 * np.pi)
    a1 = a1 / (2 * np.pi)
    freq = 0.5 / dt
    if not term:
        T = np.arange(a0, a1, -1./SR) * freq
    else:
        n = int(dt * SR)
        T = np.linspace(a0, a1, n) * freq
    return (np.cos(2 * np.pi * T) + 1.) * 0.5 *(y1 - y0) + y0

def cosinax(dt, y0, p0, y1, p1, term=False):
    """
    p0, p1 : pentes en y0 et y1
    les 'p' ne sont pas univoques, donc pas une bonne solution.
    """
    if not -1. <= p0 <= 1.:
        print("cosinax: il faut -1. <= p0 <= 1.")
        return
    if not -1. <= p1 <= 1.:
        print("cosinax: il faut -1. <= p1 <= 1.")
        return
    a0 = np.arccos(p0) / np.pi
    a1 = np.arccos(p1) / np.pi
    freq = 0.5 / dt
    if not term:
        T = np.arange(a0, a1, -1./SR) * freq
    else:
        n = int(dt * SR)
        T = np.linspace(a0, a1, n) * freq
    return (np.cos(2 * np.pi * T) + 1.) * 0.5 *(y1 - y0) + y0
