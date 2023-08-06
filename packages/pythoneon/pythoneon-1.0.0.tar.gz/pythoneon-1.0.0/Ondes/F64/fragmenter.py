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
# ~/py../Ondes/fragmenter.py

""" dans une onde f64, on prlève des fragments
#import alsaaudio  """
import subprocess
import numpy as np
from samplerate import SR

__author__ = "Copyright (c) 2018 René Bastian (Wissembourg, FRANCE)"
__date__ = "2018.11.18"

class F64(object):
    """ d'une f64 on prélève un ou plusieurs fragments """
    def __init__(self, fnom):
        self.w = np.fromfile(fnom)
        self.frag = None

    def fragmentT(self, pt0=0.0, pt1=None):
        """ prélever un fragment """
        ix0 = int(pt0 * SR)
        if pt1 is None:
            self.frag = self.w[ix0:]
            return self.w[ix0:]
        else:
            ix1 = int(pt1 * SR)
            if ix1 > self.w.size:
                print("F64.fragmentT ix1", ix1, "> w.size", self.w.size)
            self.frag = self.w[ix0:ix1]
            return self.w[ix0:ix1]

    def fragmentD(self, duree, pt0=0.0, fnom=None):
        """ durée donnée """
        pt1 = pt0 + duree
        w = self.fragmentT(pt0, pt1)
        if isinstance(fnom, str):
            w.tofile(fnom)
        return w

    def stat(self):
        """ quelques infos """
        print(self.w.size, self.w.max(), self.w.min(),
              "durée", self.w.size / SR)

    def play64mono(self):
        " joue le fichier dans le buffer "
        nomraw = "/tmp/xxxxxx.raw"
        self.frag.tofile(nomraw)
        comm16 = " ".join(["play -c1 -r", str(SR), "-q",
                           "-e floating-point -b64", nomraw])
        subprocess.call(comm16, shell=True)
