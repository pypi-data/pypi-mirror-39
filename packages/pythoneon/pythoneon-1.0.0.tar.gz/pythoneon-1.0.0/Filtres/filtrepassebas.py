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

#import numarray as NA
import numpy as np
from conversions08 import extremum
#import utiles as _u

__all__ = ["filtrePB"]

def filtrePB(w):
    n = len(w)
    z = np.zeros(n+1, np.float64)
    z[0] = w[0]
    for i in range(1,n):
        z[i] = (w[i-1] + w[i])*0.5
    x = extremum(z)
    return z/x

