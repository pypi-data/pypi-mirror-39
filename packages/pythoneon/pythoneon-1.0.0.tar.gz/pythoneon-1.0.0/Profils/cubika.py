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
# Profils/cubika.py
# INTÉGRÉ DANS PROFILS

""" les fonctions n'ont été utilisées nulle part, donc je
les mets dans cubika """

import copy
import numpy as np
from samplerate import SR

def cubika(liste):
    """ trace une courbe que les mathématiciens désignent par 'cubique'.
    Syntaxe:
        liste = [dt, y0, p0, y1, p1 ]
    """
    def courbeCubique(x0, y0, p0, x1, y1, p1):
        """retourne une cubique
        'x0, y0: coordonnée du point initial
        'p0: tangente au point initial
        'x1, y1: coordonnée du point final
        'p1: tangente au point final
        """
        R = coeffscubiquex(x0, y0, p0, x1, y1, p1)
        vT = np.arange(x0, x1, 1.0/SR)
        S = valeurCubique(R, vT)
        return S

    def coeffscubiquex(x0, y0, p0, x1, y1, p1):
        """retourne les coeffs a, b, c, d
        tels que a * x**3 + b * x**2 + c * x + d
        passe par (x0, y0, p0, x1, y1, p1)
        """
        M = [[x0**3, x0**2, x0, 1],
             [x1**3, x1**2, x1, 1],
             [3 * x0**2, 2 * x0, 1, 0],
             [3 * x1**2, 2 * x1, 1, 0]]
        Y = [y0, y1, p0, p1]
        R = systemeCramer(M, Y)
        return R

    def valeurCubique(F, x):
        """ calcule la valeur de la cubique au point 'x'
        f_i étant les coefficients """
        return ((F[0] * x + F[1]) * x + F[2]) * x + F[3]

    def determinant(M):
        """retourne le déterminant du tableau M """
        return np.linalg.det(M)

    def systemeCramer(M, Y, affiche=0):
        """ retourne R tel que M * R = Y """
        k = determinant(M)
        if k != 0:
            k = 1.0/k
        else:
            print("systemeCramer: Il n'y a pas de solution")
            return None
        R = []
        for i in range(len(M)):
            H = copy.deepcopy(M)
            for _, j in enumerate(Y):
                H[j][i] = Y[j]
            if affiche:
                print(H)
            r = k * determinant(H)
            R.append(r)
        return R

    duree, y0, p0, y1, p1 = liste
    return courbeCubique(0.0, y0, p0, duree, y1, p1)
