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
# Groupes/Plings/plingvar.py

"""Varier la hauteur d'un pling
Les 1ères versions (plingtract.*) sont dans Residus
"""

import numpy as np

from samplerate import sr
from conversions import (prony2samples, prony2periode, prony2freq, 
                         freq2periode, extremum)
from profilbase import ProfilBase
from profils import recta
from canal import CanalMono
from filtrefixe import filtreContinu #, CanalMulti, Reverberation
from serie import Serie002
from sinusa import arc
from origine import OrigineStr

__author__ = "Copyright (c) 2010 René Bastian (Wissembourg, FRANCE)"
__date__ = "2010.06.04, 2011.07.09, 2013.07.27, 2014.06.16"

def retuilage(phauteur, onde0, filtrer=True):
    """ 'phauteur' : profil d'évolution de hauteur
    'onde0' : liste ou array de grains de sons, en général un vecteur
    (les durées des grains ne sont pas nécessairement égales) """
    nonde0 = len(onde0)
    vperiodes = ProfilBase(phauteur).samples(nonde0)
    vperiodes = prony2periode(vperiodes)
    duree = vperiodes.sum()
    c = CanalMono(duree)
    pt = 0.0
    for periode, wa in zip(vperiodes, onde0):
        c.addT(pt, wa)
        pt += periode
    if filtrer:
        return filtreContinu(c.a)
    else:
        return c.a

class PlingVar0(OrigineStr):
    """Variation de la hauteur vers le bas en intercalant des zéros
    ou en tuilant pour tirer le son vers le haut."""
    def __init__(self, alea=None):
        """ installe un générateur sériel interne """
        OrigineStr.__init__(self)
        if alea is None:
            self.alea = Serie002(619, 1907, 2843)
        else:
            self.alea = alea

    def plingsimple(self, duree, nh, penv=None):
        """ construit un pling de hauteur fixe 
        qui sert dans les autres méthodes.
        Si penv n'est pas donné, on utilise on bruit sériel sans enveloppe.
        Pour équilibrer le signal dès le départ on effectue
           w -= abs(w.mean())"""
        n = int(duree * sr)
        w = np.zeros(n)
        if penv == None:
            w[0:nh] = self.alea.uniform(-1., +1., nh)
        else:
            a = self.alea.uniform(-1., +1., nh)
            env = ProfilBase(penv).samples(nh)
            a *= env
            w[0:nh] = a
        for i in range(nh, n):
            w[i] = (w[i - nh] + w[i - nh + 1]) * 0.5
        w -= abs(w.mean())
        return w

    def plinghauteur(self, duree, hauteur, penv=None):
        """ construit le pling de hauteur fixe """
        n = int(duree * sr)
        w = np.zeros(n)
        nh = prony2samples(hauteur)
        if penv == None:
            w[0:nh] = self.alea.uniform(-1., +1., nh)
        else:
            a = self.alea.uniform(-1., +1., nh)
            env = ProfilBase(penv).samples(nh)
            a *= env
            w[0:nh] = a
        for i in range(nh, n):
            w[i] = (w[i - nh] + w[i - nh + 1]) * 0.5
        return np.resize(w, (n / nh, nh)) 
            
    def evtprimaire(self, duree, h0, coeff):
        """ produit un son
        h0 : hauteur de départ
        coeff : coeff de variation de la hauteur
        la 'duree' est indicative """
        nh = prony2samples(h0)
        periode = 1./ prony2freq(h0)
        wa = self.plingsimple(duree, nh)
        #play(wa, wa)
        c = CanalMono()
        pt = 0.0
        wn = 0
        periodevar = periode
        while wn < wa.size:
            c.addT(pt, wa[wn:wn + nh])
            pt += periodevar
            periodevar *= coeff
            wn += nh
        w = filtreContinu(c.a)
        w = filtreContinu(w)
        return w

#    def evtprimaireV(self, duree, h0, pcoeff):
#        """ produit un son
#        h0 : hauteur de départ
#        coeff : coeff de variation de la hauteur
#        la 'duree' est indicative 
#        ???????????? """
#        nh = prony2samples(h0)
#        periode = 1./ prony2freq(h0)
#        wa = self.plingsimple(duree, nh)
#        #play(wa, wa)
#        c = CanalMono(duree)
#        pt = 0.0
#        wn = 0
#        n = int(duree * sr)
#        periodevar = periode
#        vcoeff = ProfilBase(pcoeff).samples(n)
#        while wn < len(wa):
#            c.addT(pt, wa[wn:wn + nh])
#            pt += periodevar
#            periodevar *= vcoeff[?]
#            wn += nh
#        return c.a

    def evtduree(self, h0, phauteur, duree, penvonde=None, pvibrato=None, 
                 debut=0):
        """ phauteur : profil de la variation de hauteur
        h0 : hauteur utilisée pour le pling fournissant la matière
        duree : la durée
        penvonde : profil de l'enveloppe donnée à l'onde initiale du pling
        debut : première onde (permet de couper la percussion) """
        vperiodes = ProfilBase(phauteur).temps(duree)
        vperiodes = prony2periode(vperiodes)
        nperiodes = len(vperiodes)
        if pvibrato:
            vvibrato = ProfilBase(pvibrato).samples(nperiodes)
            vvibrato = freq2periode(vvibrato)
            vvibrato += 1.0
            vperiodes *= vvibrato
        pt = 0.0
        c = CanalMono(duree)
        ondes = self.plinghauteur(duree, h0, penvonde)
        for periode, onde in zip(vperiodes, ondes[debut:]):
            c.addT(pt, onde)
            pt += periode
        return filtreContinu(c.a)
        
    def evtsamples(self, h0, phauteur, nformes):
        """ Le profil de la variation de hauteur 'phauteur' 
        et le nombre de formes d'ondes 'nformes'
        détermine la durée du son et son évolution de hauteur.
        'h0' donne la forme d'onde qui est découpée """
        vperiodes = ProfilBase(phauteur).samples(nformes)
        vperiodes = prony2periode(vperiodes)
        nh = prony2samples(h0)
        periode = 1./ prony2freq(h0)
        duree = periode * nformes
        wa = self.plingsimple(duree, nh)
        #play(wa, wa)
        nwa = len(wa)
        nsamples = prony2samples(h0)
        vformes = np.resize(wa, (nwa / nsamples, nsamples)) 
        c = CanalMono(duree)
        pt = 0.0
        for periode, forme in zip(vperiodes, vformes):
            #print(periode)
            c.addT(pt, forme)
            pt += periode
        
        return c.a

    def tuilage0(self, h0, phauteur, nformes):
        """ superposition en continu d'un pling  
        'phauteur' : profil de variation de la hauteur 
                     == espacement des plings
        'nformes' : nombre de samples
        'h0' : hauteur moyenne ??"""
        vperiodes = ProfilBase(phauteur).samples(nformes)
        vperiodes = prony2periode(vperiodes)
        nh = prony2samples(h0)
        periode = 1./ prony2freq(h0)
        duree = periode * nformes
        wa = self.plingsimple(duree, nh)
        c = CanalMono(duree)
        pt = 0.0
        wb = -wa
        for i, periode in enumerate(vperiodes):
            if i % 2 == 0:
                c.addT(pt, wa)
            else:
                c.addT(pt, wb)
            pt += periode
        w = filtreContinu(c.a)
        return w

    def tuilage1(self, h0, phauteur, nformes):
        """ h0 : hauteur du pling original
        phauteur : variation de hauteur des ondes
        nformes : nombre d'ondes à traiter
        Il faut trouver la relation entre période de h0 et nformes:
        ~ alpha * nformes * periode = durée ??

        On produit un pling de nformes ondes.
        Ce pling est découpé et les ondes sont replacés
        sur un axe de temps selon un espacement correspondant à phauteur. """
        ptriangle = [[recta, 1.0,  0.,  1.],
                     [recta, 2.0,  1., -1.],
                     [recta, 1.0, -1.,  0.]]
        
        vperiodes = ProfilBase(phauteur).samples(nformes)
        vperiodes = prony2periode(vperiodes)
        nh = prony2samples(h0)
        periode = 1./ prony2freq(h0)
        duree = periode * nformes
        wa = self.plingsimple(duree, nh, ptriangle)
        wb = -wa
        c = CanalMono(duree)
        pt = 0.0        
        for i, periode in enumerate(vperiodes):
            if i % 2 == 0:
                c.addT(pt, wa)
            else:
                c.addT(pt, wb)
            pt += periode
        return c.a

    def tuilage2(self, h0, phauteur, nformes):
        """ h0 : hauteur du pling original
        phauteur : variation de hauteur des ondes
        nformes : nombre d'ondes à traiter

        On produit un pling de nformes ondes.
        Ce pling est découpé et les ondes sont replacés
        sur un axe de temps selon un espacement correspondant à phauteur.
        Essais:
        --------------------
        c = CanalMono(duree)
        pt = 0.0
        i = 0
        for periode in vperiodes:
            c.addT(pt, wa[i:])
            pt += periode
            i += nh
        w = filtreContinu(c.a)
        return w
        se termine par une interruption brutale (front)
        -------------------- """
        ptriangle1 = [[recta, 1.0,  0.,  1.],
                     [recta, 2.0,  1., -1.],
                     [recta, 1.0, -1.,  0.]]

        ptriangle2 = [[recta, 1.0,  0.,  1., 0.5],
                     [recta, 2.0,  1., -1., 2.0],
                     [recta, 1.0, -1.,  0., 0.5]]
        print(ptriangle1, ptriangle2)
        psaegezahn = [[recta, 1.0,  1.,  -1.]]
        vperiodes = ProfilBase(phauteur).samples(nformes)
        vperiodes = prony2periode(vperiodes)
        nh = prony2samples(h0)
        periode = 1./ prony2freq(h0)
        duree = periode * nformes
        #wa = self.plingsimple(duree, nh, ptriangle)
        wa = self.plingsimple(duree, nh, psaegezahn)
        c = CanalMono(duree)
        pt = 0.0
        for periode in vperiodes:
            c.addT(pt, wa)
            pt += periode
        w = filtreContinu(c.a)
        return w

class PlingVar1(PlingVar0):
    """ rendre PlingVar0 plus logique d'emploi """
    def __init__(self, diviseur=2.0, alea=None):
        " installation d'un  générateur sériel "
        PlingVar0.__init__(self, alea)
        self.div = diviseur

    def evt(self, duree, generateur, phauteur, penveloppe,
            ppano=None):
        """ construire un PlingVar avec un générateur externe,
        une durée donnée et avec le profil de hauteur, d'enveloppe
        et de panorama donné.
        """
        # préparation du vecteur des points temporels
        n = sr # provisoire
        pts = ProfilBase(phauteur).samples(n)
        pts = prony2periode(pts)
        dureeprov = pts.sum()
        n = int(n * duree / dureeprov)
        pts = ProfilBase(phauteur).samples(n)
        pts = prony2periode(pts)
        pts = pts.cumsum()
        pts = pts - pts[0]
        # préparation des ondes
        generateur = np.array(generateur) # pure précaution
        n = pts.size
        ng = generateur.size
        nv = n * ng
        v = np.zeros(nv)
        v[:ng] = generateur[:]
        for i in range(ng, nv):
            v[i] = (v[i-ng+1] + v[i-ng+2]) / self.div
        #return v
        # découpage en paquets d'ondes
        v = v.reshape((nv/ng, ng))
        we = arc(ng)
        c = CanalMono()
        for i, pt in enumerate(pts):
            e = v[i] * we
            c.addT(pt, e)
        env = ProfilBase(penveloppe).samples(c.a.size)
        w = c.a * env
        print("max", w.max(), "min", w.min())
        w /= extremum(w)
        if ppano is None:
            return w
        else:
            pano = ProfilBase(ppano).samples(w.size)
            return w * pano, w * (1.0 - pano)
            
            
