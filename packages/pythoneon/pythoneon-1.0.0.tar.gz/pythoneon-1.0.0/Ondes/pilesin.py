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
# pilesin.py
##DEBUT
"""
fournit des fonctions entassant des sinus (combinaisons
de fréquences fixes, fréquences, variables, enveloppes ou
sans enveloppes)
"""

import numpy as np
from profilbase import ProfilBase
from conversions import extremum
from samplerate import SR
from ajuster import prolongerN

__author__ = "Copyright (c) 2005 René Bastian (Wissembourg, FRANCE)"
__date__ = "2006.12.29, 07.07.19, 09.03.24"

def pilestatique(listeL, duree, ph = 0.0):
    """
    'L : liste de tuples (amplitude, fréquence)
    'duree : durée
    La fréquence est fixe.
    Le son devient récursivement de plus en plus complexe.
    """
    T = np.arange(0.0, duree, 1.0/SR)
    for ampli, freq in listeL:
        ph = ampli * np.sin(2 * np.pi * freq * T + ph)
    return ph / extremum(ph)

def pilevariante(listeL, duree, ph = 0.0):
    """
    'listeL' : liste de tuples (amplitude, profil de hauteurs)
    'duree : durée 
    La fréquence varie selon un profil.
    Le son devient récursivement de plus en plus complexe.
    """    
    T = np.arange(0.0, duree, 1.0/SR)
    n = len(T)
    for  ampli, profilMF in listeL:
        if isinstance(profilMF, list):
            mf = ProfilBase(profilMF).samples(n)
        else:
            mf = profilMF            
        ph = ampli * np.sin(2 * np.pi * mf * T + ph)  
    return ph / extremum(ph)

def pileprofil(listeL, duree, ph=0.0):
    """
    'listeL' : liste de tuples
       (ampli, enveloppe-profil, frequence-profil) 
    'duree : durée
    Le son devient progressivement de plus en plus complexe.

    Donner à 'duree' la valeur d'une période d'une
    des oscillations et fournir le résultat à un
    modèle physique (idem pour 'pilestatique' et 'pilevariante')
    """ 
    T = np.arange(0.0, duree, 1.0/SR)
    n = T.size
    for  ampli, pE, pF in listeL:
        e = ProfilBase(pE).samples(n)
        if isinstance(pF, (list, tuple)):
            f = ProfilBase(pF).samples(n)
        elif isinstance(pF, (float, int)):
            f = pF
        e, T, f = prolongerN((e, T, f))
        try:
            ph = ampli * e * np.sin(2 * np.pi * f * T + ph)  
        except ValueError:
            print(T.size, f.size, e.size)
    try:
        return ph / extremum(ph)
    except TypeError:
        print(type(ph))
        return ph

##FIN
