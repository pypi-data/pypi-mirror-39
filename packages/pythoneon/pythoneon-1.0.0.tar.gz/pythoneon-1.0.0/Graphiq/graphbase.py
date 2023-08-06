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
# Graphiq/graphbase.py

""" La classe GraphG avec les méthodes svg, pdf, eps, png, ..
Cette classe est héritée par ProfilBase, Recta, ... pour
permettre la représentation graphique des vecteurs.

Ces graphiques n'ont a priori ni axes ni libelles.
(tandis que matplotlib trace les axes par défaut)
"""

import numpy as np
import pyx
from origine import OrigineStr

__author__ = "Copyright (c) 2015 René Bastian (Wissembourg, FRANCE)"
__date__ = "2015.09.01, 2018.11.25"

class GraphG(OrigineStr):
    """ fournit les méthodes svg, pdf, eps, png, .. """
    def __init__(self, beps=True, bpdf=False, ndecim=1000):
        OrigineStr.__init__(self)
        self.beps = beps
        self.bpdf = bpdf
        self.vy = None
        self.svgparams = None
        self.pdfparams = None
        self.epsparams = None
        self.ndecim = ndecim

    def svg(self, vy):
        """ trace un graphique SVG """
        pass

    def pdf(self, vy):
        """ trace un graphique PDF """
        pass

    def png(self, vy):
        """ trace un graphique PNG """
        pass

    def setvy(self, vy):
        """ pour entrer le vecteur """
        self.vy = vy

    def setsvg(self):
        """ pour entrer les paramètres de SVG """
        pass

    def setpdf(self):
        """ pour entrer les paramètres de PDF """
        pass

    def setpng(self):
        """ pour entrer les paramètres de PNG """
        pass

    def pyxgraph(self, fnom, x0=0.0, y0=0.0, xcoeff=0.05, ycoeff=1.0):
        """ essai avec Pyx
         il y a encore des accrocs - mais pas d'axes !!"""
        c = pyx.canvas.canvas()
        vy = self.vy
        vix = np.arange(0, vy.size, self.ndecim)
        vy = vy[vix]
        vy *= ycoeff
        vy += y0
        print(vy.size)
        vx = np.arange(0, vy.size) * xcoeff
        #vx += x0
        x = x0
        pk = pyx.path.path(pyx.path.moveto(x0, y0 + vy[0]))

        for x, y in zip(vx[1:], vy[1:]):
            pk.append(pyx.path.lineto(x, y))
        c.stroke(pk, [pyx.style.linewidth(0.08)])
        if self.beps:
            c.writeEPSfile(fnom)
        if self.pdf:
            c.writePDFfile(fnom)
        # pdf2svg existe

if __name__ == "__main__":
    pass
