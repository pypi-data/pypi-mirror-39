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
# Structures/Empilements/empiler.py

""" fournit des classes et fonctions pour empiler """
# deux fonctions sont en cours; les deux sont rassemblées ici
# sous de nouveaux noms
from profils import recta
#from Ondes.pilesin import pileprofil
# voir s'il faut placer pilesin ici

__author__ = "Copyright (c) 2018 René Bastian (Wissembourg, FRANCE)"
__date__ = "2018.11.27"

def constrLAFpile1(freq, n):
    """
    construit la liste des (ampli, env, freq) pour pilevariante
    """
    duree = 1.
    r = []
    y1, y2 = 1., 0.5
    puiss1 = 0.5
    puiss2 = 1.
    puiss3 = 2.
    n = int(n)
    penv = [[recta, duree, 0., y1, puiss1],
            [recta, duree, y1, y2, puiss2],
            [recta, duree, y2, 0., puiss3]]
    for i in range(n):
        ampli = 1./(i+1)
        xfreq = (i+1)*freq
        pfreq = [[recta, duree, xfreq, xfreq]]
        r.append((ampli, penv, pfreq))
    return r

def constrLAFpile2(freq, n):
    """
    construit une liste de 'n' tuples (ampli, env, freq)
    pour pilevariante ou pileprofil
    on pourrait classifier ...
    """
    duree = 1.
    r = []
    y1, y2 = 1., 0.5
    puiss1 = 0.5
    puiss2 = 1.
    puiss3 = 2.
    n = int(n)
    penv = [[recta, duree, 0., y1, puiss1],
            [recta, duree, y1, y2, puiss2],
            [recta, duree, y2, 0., puiss3]]
    for i in range(1, n+1):
        ampli = 1./i
        xfreq = i * freq
        pfreq = [[recta, duree, xfreq, xfreq]]
        r.append((ampli, penv, pfreq))
    return r
