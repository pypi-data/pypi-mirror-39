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
# ~/pythoneon/Ondes/SinRec/plingsinrec.py

""" association d'un sinus par récurrence avec un pling
x_i = k * x_{i-1} - x_{i-2} + a * (x_m + x_{m+1}) * 0.5 """

import numpy as np

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.09.30"

def plingsinrec(k, n, m, a, alea):
    """
    x_i = k * x_{i-1} - x_{i-2} + a * (x_m + x_{m+1}) * 0.5
    """
    w = np.zeros(n+m)
    w[:m] = alea.bruit(m)
    print(w.max(), w.min())
    w[m] = 1.0
    for i in range(m, n+m):
        w[i] = (k * w[i-1] - w[i-2] - a * (w[i-m] + w[i-m+1])) % 2.0
        if w[i] > 100000000.0:
            print(i)
            return w
    return w
