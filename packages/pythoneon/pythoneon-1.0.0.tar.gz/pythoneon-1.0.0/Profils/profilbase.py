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
# Profils/profilbase.py

"""
fournit "ProfilBase", "somme_durees", "translateMul", "translateAdd",

La classe ProfilBase facilite l'utilisation des profils:
- adaptation d'un profil à une durée (ou n samples) donné
- transposition d'un profil.

résidus des anciennes versions: v0-profilbase.py
"""
import copy
import numpy as np

from samplerate import SR
from Canal.canal import CanalMono
from conversions import extremum
from Utiles.utiles11 import former
from Profils.profilgeneral import (recta, cubica, fluctua, consta,
                                   rectag, cubicag, fluctuag, constag,
                                   rectap, cubicap, fluctuap, constap)
from profils import (profil, transposeliste)
from Graphiq.graphbase import GraphG

__all__ = ["ProfilBase", "somme_durees", "translateMul", "translateAdd"]

transposelisteprofil = transposeliste
__author__ = "Copyright (c) 2005 René Bastian (Wissembourg, FRANCE)"
__date__ = """2005.01.07, 2005.10.24, 2006.01.26, 2006.02.04, 2007.05.23,
2008.01.08, 2008.04.23, 2008.05.26, 2009.01.11, 2009.08.14, 2010.10.11,
2012.05.28, 2012.10.03, 2013.04.08, 2013.05.28, 2013.08.02, 2013.10.02,
2015.07.12 """

def translateAdd(listep):
    " ramène le minimum de listep à zéro par soustraction "
    v = profil(listep)
    ymin = v.min()
    clistep = copy.deepcopy(listep)
    r = []
    for m in clistep:
        if m[0] == recta:
            m[2] -= ymin
            m[3] -= ymin
        elif m[0] in (cubica, fluctua):
            m[2] -= ymin
            m[4] -= ymin
        elif m[0] == consta:
            m[2] -= ymin
        r.append(m)
    return r

def translateMul(listep):
    " ramène le minimum de listep à 1.0 par division"
    v = profil(listep)
    ymin = v.min()
    clistep = copy.deepcopy(listep)
    r = []
    for m in clistep:
        if m[0] == recta:
            m[2] /= ymin
            m[3] /= ymin
        elif m[0] in (cubica, fluctua):
            m[2] /= ymin
            m[4] /= ymin
        elif m[0] == consta:
            m[2] /= ymin
        r.append(m)
    return r

def somme_durees(p):
    " calcule la somme des durées d'un profil "
    s = 0.0
    for d in p:
        s += d[1]
    return s

class ProfilBase(GraphG):
    """
    classe pour adapter un profil donné sous forme de liste
    à une durée ou une longueur souhaitée..
    """
    def __init__(self, listep=None, badditif=True,
                 nomstock=None, binfo=False):
        """
        'listep': profil-liste == profil donné sous forme de liste
                  explicite selon la syntaxe traditionnelle;
        'absolu': les valeurs y ne sont pas ramenées au niveau zéro;
        'badditif': les valeurs y sont ramenées au niveau zéro par
                    soustraction, sinon par division;
        mettre le 'nomstock' dans un fichier de configuration ??
        "/home/rbm/pythoneon/Dicos/dicoProfils.py"
        """
        GraphG.__init__(self)
        self.nomstock = nomstock
        self.listep = listep
        if listep is not None:
            #self.developper(listep)
            self.somme = somme_durees(self.listep)
            self.maxt = self.somme
            self.coefft = self.maxt / self.somme # :)
            self.kexplicite()
        else:
            self.somme = None
            self.maxt = None
            self.coefft = None
        self.badd = badditif
        self.stocke()
        self.binfo = binfo
        self.y = None
        self.souche = "P"
        self.cptfig = 0
        self.ndecim = 100

    def kexplicite(self): # ???? CALCUL TROP TÔT ??
        " réécrit les formes condensées "
        r = []
        for x in self.listep:
            if x[0] in (rectap, cubicap, fluctuap, constap):
                r.append(x[0](x[:1]))
            else:
                r.append(x)
        self.listep = r

    def change(self, listep, babsolu=True):
        """ pour changer de profil """
        if babsolu:
            self.listep = listep
        else:
            if self.badd:
                self.listep = self.translateAdd(listep)
            else:
                self.listep = self.translateMul(listep)
        #self.developper(listep)
        self.somme = somme_durees(self.listep)
        self.maxt = self.somme
        self.coefft = self.maxt / self.somme # :)
        self.kexplicite()

    @staticmethod
    def profilnormaliseN(lp, n0, bliste=False, binfo=False):
        """ le profil 'lp' est calculé de façon à obtenir
        un vecteur 'v' dont 'v.size == n0';
        lp : le profil liste
        n0 : le nombre de samples à obtenir;
        aucune différence n'est autorisée; l'ajustement est fait
        soit en retranchant quelques samples, soit en ajoutant
        quelques samples de la même valeur que le dernier.
        """
        vp = profil(lp)
        if vp.size == n0:
            return vp
        else:
            c = float(n0) / vp.size
            r = []
            for x in lp:
                x[1] *= c
                r.append(x)
        if bliste:
            return r
        vp = profil(r)
        diff = vp.size - n0
        if binfo:
            print("profilnormaliseN: n0", n0, "diff", diff)
        if diff == 0:
            return vp
        elif diff > 0:
            return vp[:n0]
        elif diff < 0:
            z = np.ones(abs(diff)) * vp[-1]
            vp = np.concatenate((vp, z))
            return vp

    def developper(self, xlistep):
        """ réécrit les profils condensés en profils traduisibles
        par 'profil'; comme les fonctions Xag construisent des
        vecteurs, on peut inclure des profils de durée fixe: la
        fonction 'profil' les accepte.
        FAUX !!! LES RECTAG,... NE SONT PAS ADAPTABLES.
        PAS ENCORE UTILISABLE AVEC LES rectap, ...
        J'AI DES DOUTES QUE CE SOIT NECESSAIRE """
        for e in xlistep:
            if e[0] in [rectap, cubicap, fluctuap, constap,
                        rectag, cubicag, fluctuag, constag]:
                if e[0] == rectag:
                    x = e[0](e[1], e[2:])
                elif e[0] == rectap:
                    x = [e[0], e[1], e[2:]] # FAUX
                elif e[0] in [cubicap, cubicag]:
                    x = e[0](e[1], e[2], e[3:])
                elif e[0] in [fluctuap, fluctuag]:
                    x = e[0](e[1], e[2:])
                elif e[0] in [constap, constag]:
                    x = e[0](e[1:])
                self.listep.append(x)
            else:
                self.listep.append(e)

    def fonction(self, vt):
        """ au lieu de calculer des interpolations, cette méthode
        considère les descriptions comme des fonctions définies par
        segments et retourne la ou les valeurs correspondant au
        param 'vt'; cette méthode implique que les valeurs de 'vt'
        se situent entre 0.0 et un maximum correspondant à la somme
        des durées de chaque segment.
        La méthode 'limite', permet de changer ce maximum.
        """
        pass

    def limite(self, maxt):
        " fixe la valeur maximum de t "
        self.maxt = maxt
        self.coefft = self.maxt / self.somme

    def temps(self, duree, liminf=None, limsup=None, bmin=True):
        """
        calcule le profil-vecteur à partir de 'self.listep'
        de telle façon que la dimension du vecteur corresponde
        à 'duree' en sec.
        """
        n = int(duree * SR)
        return self.samples(n, liminf, limsup, bmin)

    def tempsH(self, duree, hProny):
        """ transposition du profil de la hauteur transpoProny """
        n = int(duree * SR)
        return self.samplesH(n, hProny)

    def samplesH(self, n, hProny):
        """ transposition du profil de la hauteur transpoProny """
        y = self.profilnormaliseN(self.listep, n, self.binfo)
        return y + hProny - y[0]

    def samples(self, n, liminf=None, limsup=None, bmin=True):
        """
        calcule le profil-vecteur à partir de 'self.listep'
        de telle façon que la dimension du vecteur soit 'n'.
        """
        y = self.profilnormaliseN(self.listep, n, self.binfo)
        if bmin and isinstance(y, np.ndarray):
            try:
                ymin = y.min()
            except ValueError:
                print("ProfilBase.samples", y.min())
        else:
            bmin = y[0] # conflictuel
        if liminf is None and limsup is None:
            self.y = y
            return y
        elif liminf is not None and limsup is not None:
            if limsup < liminf:
                print("ProfilBase.samples: limsup < liminf !")
                print("Il faut inverser ...")
                return
            coeff = (limsup - liminf) / (y.max() - ymin)
            self.y = (y - ymin) * coeff + ymin
            return y

    def stockN(self, n, nomstock):
        """ stock les données dans le fichier 'nomstock """
        pass

    def samplesL(self, n, bafficherreur=False):
        """
        construit un profil liste dont la dimension du vecteur calculé
        serait 'n'
        bafficherreur: affiche l'erreur par rapport à 1.0"""
        self.y = self.profilnormaliseN(self.listep, n, bafficherreur)
        return self.y

    def tempsL(self, duree, bafficherreur=False):
        """
        construit un profil liste dont la durée du vecteur calculé
        serait 'duree'
        bafficherreur: affiche l'erreur par rapport à 1.0"""
        n = int(duree * SR)
        return self.samplesL(n, bafficherreur)

    def tempsP(self, duree, dy, coeff=1.):
        """
        calcule le profil-vecteur à partir de 'self.listep'
        de telle façon que la dimension du vecteur corresponde
        à 'duree' en sec;
        le vecteur calculé est multiplié par 'coeff'
        'dy' est ajouté aux valeurs du vecteur
        """
        n = int(duree * SR)
        return self.samples(n) * coeff + dy

    def samplesP(self, n, dy, coeff):
        """
        calcule le profil-vecteur à partir de 'self.listep'
        de telle façon que la dimension du vecteur soit 'n';
        le vecteur calculé est multiplié par 'coeff'
        'dy' est ajouté aux valeurs du vecteur
        """
        self.y = self.samples(n) * coeff + dy
        return self.y

    def stocke(self):
        """ pour stocker le profil dans un réservoir """
        if self.nomstock is None:
            return
        xliste = copy.deepcopy(self.listep)
        try:
            xlistep = self.translateAdd(xliste)
        except TypeError:
            print("ProfilBase.stocke - TypeError")
            xlistep = xliste
        f = open(self.nomstock, "a")
        pl = former(xlistep)
        s = "\n".join(pl)
        try:
            f.write(s+"\n\n")
        except IOError:
            print("IOError:ProfilBase.stocke, nomfichier:", s)
        f.close()

    @staticmethod
    def translateAdd(listep):
        " ramène le minimum de listep à zéro par soustraction "
        v = profil(listep)
        ymin = v.min()
        clistep = copy.deepcopy(listep)
        r = []
        for m in clistep:
            if m[0] == recta:
                m[2] -= ymin
                m[3] -= ymin
            elif m[0] in (cubica, fluctua):
                m[2] -= ymin
                m[4] -= ymin
            elif m[0] == consta:
                m[2] -= ymin
            r.append(m)
        return r

    @staticmethod
    def translateMul(listep):
        " ramène le minimum de listep à 1.0 par division"
        v = profil(listep)
        ymin = v.min()
        clistep = copy.deepcopy(listep)
        r = []
        for m in clistep:
            if m[0] == recta:
                m[2] /= ymin
                m[3] /= ymin
            elif m[0] in (cubica, fluctua):
                m[2] /= ymin
                m[4] /= ymin
            elif m[0] == consta:
                m[2] /= ymin
            r.append(m)
        return r

#    def graph(self, bhold=False):
#        """ retourne le vecteur sous forme graphique
#        si bhold==True, les courbes sont insérées dans
#            un même plan graphique;
#        si bhold==False, le plan graphique est vidé.
#        Reste le problème des axes - qui doivent disparaître"""
#        vy = self.y
#        #print("1 vy:", vy.size)
#        vix = np.arange(0, vy.size, self.ndecim)
#        vy = vy[vix]
#        #print("2 vy:", vy.size)
#        vx = np.arange(0, vy.size)
#        #print("3 vx:", vx.size))
#        # ici il faut vider pyplot
#        pyplot.axis('off')
#        pyplot.plot(vx, vy)
#        fnom = self.souche + str(self.cptfig).zfill(4)
#        self.cptfig += 1
#        pyplot.savefig(fnom)
#        pyplot.hold(bhold)

class ProfilMultip():
    """ superposition de profils
    Version simplifiée pour l'instant """
    def __init__(self, listeProfils):
        """ listeProfils : liste de profils indépendants avec un
              coeff de pondération:
              [(Lprofil, coeff), (Lprofil, coeff), (Lprofil, coeff), ...]
        """
        self.listep = listeProfils
        #self.pb = [ProfilBase(p) for p in listeProfils]

    def lin2db(self, duree, pt=0.0):
        """ conversion du profil de linéaire en db """
        pass

    def db2lin(self, duree, pt=0.0):
        """ conversion du profil de db en linéaire """
        pass

    def lin2prony(self, duree, pt=0.0):
        """ conversion du profil de linéaire en prony """
        pass

    def prony2lin(self, duree, pt=0.0):
        """ conversion du profil de prony en linéaire """
        pass

    def temps(self, duree, pt=0.0):
        """ adapte """
        c = CanalMono(duree)
        n = int(duree * SR)
        for p, coeff in self.listep:
            if isinstance(p, list):
                v = ProfilBase(p).samples(n)
            elif isinstance(p, np.ndarray):
                v = p
            else:
                print(type(p))
                print("Je ne sais pas quoi faire ...")
                continue
            v /= extremum(v)
            v *= coeff
            c.addT(pt, v)
        return c.a

    def samples(self, n, pt=0.0):
        """ adapte """
        c = CanalMono()
        npt = int(pt * SR)
        for p, coeff in self.listep:
            v = ProfilBase(p).samples(n)
            v /= extremum(v)
            v *= coeff
            c.addN(npt, v)
        return c.a

def listeouvaleur(p, n):
    " choisir entre liste et valeur "
    if isinstance(p, list):
        return ProfilBase(p).samples(n)
    if isinstance(p, (float, int)):
        return p
    else:
        print("listeouvaleur(p, n): p n'est ni liste ni valeur")
