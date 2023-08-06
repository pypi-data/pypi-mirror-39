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
# ajuster.py
"""
Le problème de la correspondance temps/échantillons est insoluble.  Il
faut ajuster les longueurs des vecteurs par complétion ou amputation.
En cas de complétion on peut compléter avec des zéros ou la dernière
valeur.  Comme la différence ne joue en général que sur qqs
échantillons, je ne prévois pas d'extrapolation.  L'amputation n'a pas
été utilisée - donc j'expulse la fonction.
'amputer', 'entrelacer', 'prolongerV' sont transférés dans 'zajuster.py'
"""
import os
import numpy as np
from samplerate import SR

__author__ = "Copyright (c) 2010 René Bastian (Wissembourg, FRANCE)"
__date__ = """2006.07.07 Rochefort s/Loire, 2008.03.13 St-Mamert, 2010.06.17,
           2013.02.14, 2014.06.06"""

FLOAT64_ITEMSIZE = 8

__all__ = ["prolongerZ", "prolongerN"]

def prolongerV(vecteurs):
    """ajoute des zéros aux vecteurs dont la
    dimension est inférieure au plus grand vecteur.
    Est plus lent que prolongerZ"""
    binegal = False
    n = vecteurs[0].size
    for v in vecteurs[1:]:
        if v.size > n:
            n = v.size
            binegal = True
    if binegal:
        C = []
        for v in vecteurs:
            w = np.zeros(n)
            w[:v.size] = v
            C.append(w)
        return C
    else:
        return vecteurs

def prolongerZ(vecteurs):
    """vecteurs = liste ou tuple de vecteurs
    ajoute des zéros aux vecteurs dont la
    dimension est inférieure au plus grand vecteur."""
    n = vecteurs[0].size
    for v in vecteurs[1:]:
        if v.size > n:
            n = v.size
    r = []
    #print("prolongerZ(vecteurs)", n)
    for v in vecteurs:
        k = n - v.size
        if k > 0:
            z = np.zeros(k)
            v = np.concatenate((v, z))
            #print("après", v.size)
        r.append(v)
    #for x in C:
    #    print(x.size,)
    #print()
    return tuple(r)

def prolongerZ_ancien(vecteurs):
    """ajoute des zéros aux vecteurs dont la
    dimension est inférieure au plus grand vecteur."""
    n = len(vecteurs[0])
    for v in vecteurs[1:]:
        if len(v) > n:
            n = len(v)
    C = []
    for v in vecteurs:
        k = n - len(v)
        if k > 0:
            z = np.zeros(k)
            v = np.concatenate((v, z))
        C.append(v)
    return tuple(C)

def fprolongerZ(listef):
    """
    'listef' : liste de fichiers en format 'np.float64'
    ajoute des 0.0 aux fichiers dont la dimension est inférieure
    au fichier le plus long
    """
    nmax = 0
    for f in listef:
        nf = os.fstat(f.fileno()).st_size
        if nmax < nf:
            nmax = nf
    for f in listef:
        nf = os.fstat(f.fileno()).st_size
        r = nmax - nf
        if r > 0:
            x = np.zeros(r / FLOAT64_ITEMSIZE)
            f.seek(nf)
            x.tofile(f)

def prolongerN(vecteurs):
    """ajoute à chaque vecteur autant de fois sa
    dernière valeur pour que tous les vecteurs aient
    la dimension du plus grand vecteur."""
    n = len(vecteurs[0])
    for v in vecteurs[1:]:
        if len(v) > n:
            n = len(v)
    C = []
    for v in vecteurs:
        k = n - len(v)
        if k > 0:
            try:
                z = np.ones(k) * v[-1]
            except ValueError:
                print("prolongerN(vecteurs):")
                print("nombre de valeurs", k, "valeur", v[-1])
                if not isinstance(v[-1], float):
                    print("objet inconnu", v)
            v = np.concatenate((v, z))
        C.append(v)
    return tuple(C)

def cherchezeros(w, ndebut=0, ncombien=None):
    """ w : le son original,
    ndebut : premier sample à examiner
    ncombien : combien de samples sont à examiner
    Retours:
     s : tuples(index de passage, sens, nombre de samples),
         cette disposition est à aménager selon les besoins
     gecarts : liste des dimensions en samples entre deux passages,
     vi : liste des index de passage par zéro"""
    s, gecarts, vi = [], [], []
    if ncombien is None:
        nfin = w.size
    else:
        nfin = ndebut + ncombien
    bchange = False
    i0 = ndebut
    s.append((ndebut, "n", i0 - i0))
    gecarts.append(0)
    vi.append(0)
    for i in range(ndebut+1, nfin):
        if w[i-1] <= 0.0 and w[i] > 0.0:
            bchange = True
            s.append((i - i0, "a", i))
            gecarts.append(i - i0)
        elif w[i-1] > 0.0 and w[i] <= 0.0:
            bchange = True
            s.append((i - i0, "d", i))
            gecarts.append(i - i0)
        if bchange:
            i0 = i
            vi.append(i)
            bchange = False
    #s.sort()
    return s, gecarts, vi

def traque_onde(w, lim=SR-50):
    """ dans une onde w chercher une suite de passages par zéro
    telle que 1) le premier passage soit ascendant à partir de 0
    et le dernier ascendant vers 0
              2) que la suite soit la plus lo,ngue possible
    """
    ts, ecarts, vi = cherchezeros(w)
    del ecarts, vi
    cpt = 0
    ref = ts[1][1]
    coll = []
    for t in ts:
        cpt += t[0]
        if t[1] == ref and cpt >= lim:
            #print(cpt, t[2])
            coll.append((cpt, t[2]))
            cpt = 0
    return coll


