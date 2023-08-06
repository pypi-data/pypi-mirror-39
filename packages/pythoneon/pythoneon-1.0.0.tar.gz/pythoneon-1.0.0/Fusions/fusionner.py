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
# fusionner.py

""" fusionner 2 ou plusieurs fichier f64 en un fichier raw & wav """
import subprocess
import numpy as np
from conversions import extremum
from Outils.ajuster import prolongerZ
__author__ = "Copyright (c) 2013 René Bastian (Wissembourg, FRANCE)"
__date__ = "2013.11.10, 2017.11.24"

def fusionner(fnom, n=2, MAX=32768.0):
    """ fusionner les fichiers f64 en un fichier raw
    n = 2 : par défaut la stéréo habituelle
    MAX = 32768.0 : par défaut 16 bits """
    noms = ["".join([fnom, ".", str(i), "f64"]) for i in range(n)]
    V = [np.fromfile(nom, np.float64) for nom in noms]
    b = True
    for i in range(1, len(V)):
        if V[i].size != V[i-1].size:
            b = False
            break
    if not b:
        V = prolongerZ(V)
    amax = 0.0
    for v in V:
        amax = max(amax, extremum(v))
    for v in V: # des fois  RuntimeWarning: invalid value encountered in divide
        v /= amax
    for v in V:
        v *= MAX
    try:
        A = np.array(V, np.int16)
    except ValueError:
        # par ex. V = NaN
        return False
    A = np.transpose(A)
    A = np.ravel(A)
    A.tofile(fnom + ".raw")
    return True

def fusionnerQ(souche, n=2, bwav=True, MAX=2**31-1):
    """ fusionner les fichiers f64 en un fichier raw
    n = 4 : par défaut la quadro habituelle
    MAX = 2**31-1 : par défaut 32 bits """
    noms = ["".join([souche, ".", str(i), "f64"]) for i in range(n)]
    V = [np.fromfile(nom, np.float64) for nom in noms]
    b = True
    for i in range(1, len(V)):
        if V[i].size != V[i-1].size:
            b = False
            break
    if not b:
        V = prolongerZ(V)
    amax = 0.0
    for v in V:
        amax = max(amax, extremum(v))
    for v in V: # des fois  RuntimeWarning: invalid value encountered in divide
        v /= amax
    for v in V:
        v *= MAX
    try:
        A = np.array(V, np.int32)
    except ValueError:
        # par ex. V = NaN
        return False
    A = np.transpose(A)
    A = np.ravel(A)
    A.tofile(souche + ".raw")
    if bwav:
        comm = " ".join(["sox -c4 -r192000 -e signed-integer -b32",
                         "r" + souche +  ".raw", "w" + souche + ".wav"])
        try:
            subprocess.call(comm, shell=True)
        except OSError:
            print("record:conversion raw -> wav pas faite")
    return True

