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
# Tpythoneon/Reverb/traine.py

"""
détecter les fins de fichier inaudibles; la détection doit se faire
soit en parallèle avec des fichiers 'f64' ou en série pour les
fichiers 'raw'.

La fonction traine64 est à utiliser après une réverbération.
Les deux autres fonctions sont à développer pour un usage solo.
"""

import numpy as np
from conversions import extremum #, prony2freq

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.12.07"

def traine64(w, ratio=0.001, binfo=False):
    """  évalue la traîne de l'arroi 'w'
    à utiliser avant l'enregistrement """
    lim = extremum(w) * ratio
    debut = 0
    if binfo:
        print(w.size, w.max(), w.min(), lim)
    wr = w[::-1]
    for i in range(wr.size):
        if wr[i] == 0.0:
            pass
        elif wr[i] > lim:
            if binfo:
                print(i, float(i) / wr.size)
            debut = i
            break
    return w.size - debut

def coupetraine(w, ratio=0.001):
    """ coupe la traîne inutile; on implicite 'ratio' et 'binfo'
    ratio=0.001, binfo=False"""
    borne = traine64(w, ratio)
    return w[:borne]

def evaluertraine16(fnom, lim=30, binfo=False):
    """ charge le fichier 'fnom.raw' et évalue la traîne """
    f = np.fromfile(fnom, np.int16)
    print(f.size, f.max(), f.min(), f[-1])
    fr = f[::-1]
    for i in range(fr.size):
        if fr[i] >= lim:
            if binfo:
                print(i, float(i) / fr.size)
            debut = i
            break
    return f.size - debut

def evaluertrainef64(fnom, ratio=0.001, binfo=False):
    """ charge le fichier 'fnom.?f64'
    et évalue la traîne """
    f = np.fromfile(fnom)
    lim = extremum(f) * ratio
    print(f.size, f.max(), f.min(), f[-1], lim)
    fr = f[::-1]
    for i in range(fr.size):
        if fr[i] == 0.0:
            pass
        elif fr[i] > lim:
            if binfo:
                print(i, float(i) / fr.size)
            debut = i
            break
    return f.size - debut
