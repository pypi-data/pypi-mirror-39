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
# pythoneon/Profils/Generateurs/geneprofils.py

"""
fournit des générateurs sériels de profils.
Meilleur choix:
#class GenerateurProfil
    fonction __init__(alea, dtmin, dtmax, vmin=0.0, vmax=1.0,
                 pmin=1.0, pmax=1.0):
    fonction evt(nsegments, vmin=None, vmax=None):
    fonction evtEnv(nsegments):
    fonction evtTable(nsegmentsG, nsegmentsD):

Autres générateurs:

fonction genereprofil(moule, f):
fonction profiltuple_ancien(listeP, alea, liste=True): # cf. rale.py
fonction profiltuple(listeP, alea, liste=True): # cf. rale.py
fonction suiteDurees(duree, dmin, dmax, alea):se):
faireProfil(duree, valeurmoyen, valeurvar,
                laps1, laps2, alea, yini = None, yfinal = None,
                retourliste=True, info=False, titre=None):
fonction construireProfilEnveloppe(alea, nsegments=5):
fonction construireProfilTable(alea, nsegments=5):
fonction construireProfilProny(alea, nsegments=30):
fonction construireProfilPano(alea, nsegments=10):

Il n'est pas opportun d'intégrer un filtre dans la classe
GenerateurProfil parce qu'il vaut mieux que cette classe
retourne un profil-liste ; or, un filtrage implique qu'on
passe un vecteur.
C'est pourquoi il y a une classe à part GenerateurProfilFiltre.

L'usage raisonnable:
 - pour des tables: mettre vmin à -1.0
 - pour d'autres profils: laisser tel quel
     et translater les vecteurs:
        v = vmin + v * (vmax - vmin)
"""
import numpy as np
from origine import OrigineStr
from serie import Serie002
from profilbase import ProfilBase
from filtrefixe import FiltreFixe
from samplerate import sr
from profils import (recta, cubica, profil)
__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.05.11, 2014.09.26"


########## Générateurs sériels de profils

def genereprofil(moule, f):
    """ construit un profil explicite à partir du 'moule'
    où tous les tuples (a, b) sont remplacés par f(a, b)
    f peut être Serie002(v1, v2).uniform(x, y)"""
    r = []
    if isinstance(f, Serie002):
        f = f.uniform
    for p in moule:
        rr = []
        for x in p:
            if isinstance(x, tuple):
                a, b = x
                rr.append(f(a, b))
            else:
                rr.append(x)
        r.append(rr)
    return r

def profiltuple_ancien(listeP, alea, liste=True): # cf. rale.py
    """
    La liste-profil listeP contient des données tels que (y0, y1) ou (dt0, dt1)
    La valeur effective y ou dt sera déterminée sériellement à l'aide
    de 'alea'.

    L'option 'liste' permet de choisir un retour en profil calculé
    ou en profil-liste.
    SIMPLIFIABLE ? car on peut écrire alea(a, b) ?
    """
    import types
    listeR = []
    for p in listeP:
        r = []
        for pp in p:
            if isinstance(pp, tuple) and (len(pp) == 2):
                r.append(alea.uniform(pp[0], pp[1]))
            elif isinstance(pp, tuple) \
                    and (isinstance(pp[0], tuple)) \
                     and (len(pp[0]) == 2):
                x = alea.uniform(pp[0][0], pp[0][1])
                r.append((x))
            else:
                r.append(pp)
        listeR.append(r)
    if liste:
        return listeR
    else:
        return profil(listeR)

def profiltuple(listeP, alea, liste=True): # cf. rale.py
    """
    La liste-profil listeP contient des données tels que (y0, y1) ou (dt0, dt1)
    La valeur effective y ou dt sera déterminée sériellement à l'aide
    de 'alea'.

    L'option 'liste' permet de choisir un retour en profil calculé
    ou en profil-liste.
    SIMPLIFIABLE ? car on peut écrire alea(a, b) ?
    """
    listeR = []
    for p in listeP:
        r = []
        for pp in p:
            if isinstance(pp, tuple) and (len(pp) == 2):
                r.append(alea.uniform(pp[0], pp[1]))
            elif isinstance(pp, tuple)  \
                     and isinstance(pp[0], tuple) \
                     and (len(pp[0]) == 2):
                x = alea.uniform(pp[0][0], pp[0][1])
                r.append((x))
            else:
                r.append(pp)
        listeR.append(r)
    if liste:
        return listeR
    else:
        return profil(listeR)

#"suiteDurees" et "faireProfil" viennent de vagues.py

def suiteDurees(duree, dmin, dmax, alea):
    """
    construit une suite aléatoire de durées
    'duree : somme des durées
    'dmin : valeur minimum des segments
    'dmax : valeur maximum des segments
    'alea : fonction de génération aléatoire p.ex. random
    """
    r = []
    d = 0.0
    while d < duree:
        if duree - d < dmax:
            dd = duree - d
        else:
            dd = alea.uniform(dmin, dmax)
        r.append(dd)
        d = d + dd
    return r

def faireProfil(duree, valeurmoyen, valeurvar,
                laps1, laps2, alea, yini=None, yfinal=None,
                retourliste=True, info=False, titre=None):
    """
    construit un profil
    'titre : titre affiché
    'duree : durée du profil
    'valeurmoyen : valeur moyenne des valeurs
    'valeurvar : variation autour de la valeur moyenne
    'laps1, laps2 : intervalle de choix des segments de durées
    'yini : valeur initiale optionnelle
    'yfinal : valeur finale optionnelle
    utilisé dans
      'Interludes/finacte1.py',
      'Zone/tiento03.py',
      'Interludes/2_Interlude/interl2-3.py'
    à ne plus utiliser
    """
    vecteurDurees = suiteDurees(duree, laps1, laps2, alea)
    xprofil = []
    if info and titre is not None:
        print(titre)
    sformat = "[cubica, %7.3f, %7.3f 0.0, %7.3f, 0.0]"
    if yini is None:
        yini = alea.uniform(valeurmoyen - valeurvar,
                            valeurmoyen + valeurvar)
    for d in vecteurDurees:
        if d == vecteurDurees[-1] and yfinal is not None:
            m1 = yfinal
        else:
            m1 = alea.uniform(valeurmoyen - valeurvar,
                              valeurmoyen + valeurvar)
        a = [cubica, d, yini, 0.0, m1, 0.0]

        xprofil.append(a)
        if info:
            print(sformat % (d, yini, m1))
        yini = m1
    if info:
        print(xprofil)
    if retourliste:
        return xprofil
    else:
        return profil(xprofil)

def construireProfilEnveloppe(alea, nsegments=5):
    """ construit un profil utilisable comme enveloppe
    solution particulière"""
    r = []
    h0 = 0.0
    c = 1.0
    coeff = 0.8
    for _ in range(nsegments):
        d = alea.uniform(1.0, 2.0)
        h1 = alea.uniform(1.5*c, 3.0*c)
        p = alea.uniform(0.001, 4.0)
        r.append([recta, d, h0, h1, p])
        h0 = h1
        c *= coeff
    d = alea.uniform(1.0, 2.0)
    p = alea.uniform(0.001, 4.0)
    r.append([recta, d, h1, 0.0, p])
    return r

def construireProfilTable(alea, nsegments=5):
    """ construit un profil utilisable comme table
    solution particulière"""
    r = []
    h0 = 0.0
    for _ in range(nsegments):
        d = alea.uniform(1.0, 2.0)
        h1 = alea.uniform(0.0, 3.0)
        p = alea.uniform(0.001, 4.0)
        r.append([recta, d, h0, h1, p])
        h0 = h1
    d = alea.uniform(1.0, 2.0)
    p = alea.uniform(0.001, 4.0)
    r.append([recta, d, h1, 0.0, p])
    h0 = 0.0
    for _ in range(nsegments):
        d = alea.uniform(1.0, 2.0)
        h1 = alea.uniform(0.0, -3.0)
        p = alea.uniform(0.001, 4.0)
        r.append([recta, d, h0, h1, p])
        h0 = h1
    d = alea.uniform(1.0, 2.0)
    p = alea.uniform(0.001, 4.0)
    r.append([recta, d, h1, 0.0, p])
    return r

def construireProfilProny0(alea, liminf=75.0, limsup=90.0, nsegments=30):
    """ construit un profil de variation de hauteur
    solution particulière"""
    r = []
    h0 = alea.uniform(liminf, limsup)
    for _ in range(nsegments):
        d = alea.uniform(0.2, 1.8)
        h1 = alea.uniform(liminf, limsup)
        p = alea.uniform(0.001, 4.0)
        r.append([recta, d, h0, h1, p])
        h0 = h1
    return r

def construireProfilProny(alea, delta, base=0.0, nsegments=30):
    """ construit un profil de variation de hauteur en utilsant
    des rectas avec puissance"""
    r = []
    h0 = base
    for _ in range(nsegments):
        d = alea.uniform(0.2, 1.8)
        h1 = alea.uniform(base-delta, base+delta)
        p = alea.uniform(0.001, 4.0)
        r.append([recta, d, h0, h1, p])
        h0 = h1
    return r

def construireProfilPano(alea, nsegments=10):
    """ construit un profil de variation stéréo
    solution particulière"""
    r = []
    h0 = alea.uniform(0.0, 1.0)
    for _ in range(nsegments):
        d = alea.uniform(0.2, 1.8)
        h1 = alea.uniform(0.0, 1.0)
        p = alea.uniform(0.001, 4.0)
        r.append([recta, d, h0, h1, p])
        h0 = h1
    return r

class GenerateurProfil(OrigineStr):
    """ générateur d'un profil d'enveloppe, de hauteur, de pano,
    de table utilisant des 'recta' """
    def __init__(self, alea, dtmin, dtmax, vmin=0.0, vmax=1.0,
                 pmin=1.0, pmax=1.0):
        """
        alea : générateur sériel
        dtmin, dtmax : durée min et max
        vmin=0.0, vmax=1.0 : valeur min et max
        pmin=0.0, pmax=0.0 : puissance min et max

        Comme les profils sont adaptés à la durée souhaitée, la donnée
        des dtmin et dtmax n'est pas importante dans l'absolu, mais
        relativement les unes aux autres.
        """
        OrigineStr.__init__(self)
        self.alea = alea
        self.dtmin, self.dtmax = dtmin, dtmax
        self.vmin, self.vmax = vmin, vmax
        self.pmin, self.pmax = pmin, pmax

    def changer(self, alea=None, dtmin=None, dtmax=None,
                vmin=None, vmax=None, pmin=None, pmax=None):
        """ pour changer """
        if alea is not None:
            self.alea = alea
        if dtmin is not None:
            self.dtmin = dtmin
        if dtmax is not None:
            self.dtmax = dtmax
        if vmin is not None:
            self.vmin = vmin
        if vmax is not None:
            self.vmax = vmax
        if pmin is not None:
            self.pmin = pmin
        if pmax is not None:
            self.pmax = pmax

    def evt(self, nsegments, vmin=None, vmax=None):
        """ construit un profil de variation de hauteur,
        de fréquence, de pano, etc.
        Les résultats peuvent être fantasques si
        vmin et vmax ne sont pas dans l'intervalle (0.0, 1.0)
        """
        r = []
        if vmin is None:
            vmin = self.vmin
        if vmax is None:
            vmax = self.vmax
        #print(vmin, vmax)
        h0 = self.alea.uniform(vmin, vmax)
        for _ in range(nsegments):
            d = self.alea.uniform(self.dtmin, self.dtmax)
            h1 = self.alea.uniform(vmin, vmax)
            if self.pmin != self.pmax:
                p = self.alea.uniform(self.pmin, self.pmax)
                r.append([recta, d, h0, h1, p])
            else:
                r.append([recta, d, h0, h1])

            h0 = h1
        return r

    def evtRatio(self, duree, nsegratio, vmin=None, vmax=None):
        """ profil dont le nombre de segments nesegratio est
        proportionnel à la durée;  """
        if vmin is None:
            vmin = self.vmin
        if vmax is None:
            vmax = self.vmax
        #print(vmin, vmax)
        r = []
        nsegments = int(duree * nsegratio)
        h0 = self.alea.uniform(vmin, vmax)
        for _ in range(nsegments):
            d = self.alea.uniform(self.dtmin, self.dtmax)
            h1 = self.alea.uniform(vmin, vmax)
            if self.pmin != self.pmax:
                p = self.alea.uniform(self.pmin, self.pmax)
                r.append([recta, d, h0, h1, p])
            else:
                r.append([recta, d, h0, h1])

            h0 = h1
        return r

    def evtEnv(self, nsegments):
        """ construit un profil d'enveloppe, les valeurs
        initiale et finale étant 0.0;
        retourne un profil-liste"""
        r = []
        h0 = 0.0
        for _ in range(nsegments - 1):
            d = self.alea.uniform(self.dtmin, self.dtmax)
            h1 = self.alea.uniform(self.vmin, self.vmax)
            p = self.alea.uniform(self.pmin, self.pmax)
            r.append([recta, d, h0, h1, p])
            h0 = h1
        r.append([recta, d, h0, 0.0, p])
        return r

    def evtAttaque(self, nsegs, duree=0.06,
                   amins=(0.05, 0.1), amaxs=(0.8, 1.0)):
        """ construit un profil d'attaque, les valeurs
        initiale et finale étant 0.0;
        retourne un profil-liste"""
        binfo = False
        amin0, amin1 = amins
        amax0, amax1 = amaxs
        r = []
        xvdt = self.alea.uniform(0.0, duree, nsegs)
        xvdt.sort()
        if binfo:
            print(xvdt.size)
        vdt = np.array([xvdt[i+1] - xvdt[i] for i in range(xvdt.size -1)])
        if binfo:
            print("evtAttaque", vdt.sum())
        niv0 = self.alea.uniform(amax0, amax1)
        p = [recta, vdt[0], 0.0, niv0]
        r.append(p)
        for i, dt in enumerate(vdt[1:-1]):
            if i % 2 == 0:
                niv1 = self.alea.uniform(amax0, amax1)
            else:
                niv1 = self.alea.uniform(amin0, amin1)
            p = [recta, dt, niv0, niv1]
            r.append(p)
            niv0 = niv1
        p = [recta, vdt[-1], niv0, 0.0]
        r.append(p)
        return r

    def evtEnvDuree(self, dureeT):
        """ construit un profil d'enveloppe, les valeurs
        initiale et finale étant 0.0;
        La durée est telle dureeT < duree <= duree + dtmax
        retourne un profil-liste"""
        r = []
        h0 = 0.0
        duree = 0.0

        while duree < dureeT:
            d = self.alea.uniform(self.dtmin, self.dtmax)
            duree += d
            h1 = self.alea.uniform(self.vmin, self.vmax)
            p = self.alea.uniform(self.pmin, self.pmax)
            r.append([recta, d, h0, h1, p])
            h0 = h1
        r.append([recta, d, h0, 0.0, p])
        return r

    def envTract(self, nsegments, dtini, dtfin):
        " enveloppe pour Tractus; rectas sans puissance "
        r = []
        h0 = self.alea.uniform(self.vmin, self.vmax)
        r.append([recta, dtini, 0.0, h0])
        for _ in range(nsegments - 2):
            d = self.alea.uniform(self.dtmin, self.dtmax)
            h1 = self.alea.uniform(self.vmin, self.vmax)
            r.append([recta, d, h0, h1])
            h0 = h1
        r.append([recta, dtfin, h0, 0.0])
        return r

    def evtProny(self, nsegments, deltah, h0=None):
        """ dans le cas général (hini=0.0) construit un profil de hauteur
        relative qu'il faut transposer à la hauteur d'utilisation
        en additionnant la hauteur finale;
        'deltah' peut être positif ou négatif."""
        r = []
        if h0 is None:
            h0 = self.alea.uniform(-deltah, deltah)
        for _ in range(nsegments):
            d = self.alea.uniform(self.dtmin, self.dtmax)
            h1 = self.alea.uniform(-deltah, deltah) + h0
            p = self.alea.uniform(self.pmin, self.pmax)
            r.append([recta, d, h0, h1, p])
            h0 = h1
        return r

    def evtPronyDuree(self, dureeT, deltah, h0=None):
        """ dans le cas général (hini=0.0) construit un profil de hauteur
        relative qu'il faut transposer à la hauteur d'utilisation
        en additionnant la hauteur finale;
        'deltah' peut être positif ou négatif."""
        r = []
        if h0 is None:
            h0 = self.alea.uniform(-deltah, deltah)
        duree = 0.0
        while duree < dureeT:
            d = self.alea.uniform(self.dtmin, self.dtmax)
            duree += d
            h1 = self.alea.uniform(-deltah, deltah) + h0
            p = self.alea.uniform(self.pmin, self.pmax)
            r.append([recta, d, h0, h1, p])
            h0 = h1
        return r

    def evtRectasDiscontinus(self, nsegments, ymin, ymax):
        """ construit un profil de rectas discontinus dans
        l'intervalle (ymin, ymax)"""
        r = []
        for _ in range(nsegments):
            d = self.alea.uniform(self.dtmin, self.dtmax)
            y0 = self.alea.uniform(ymin, ymax)
            y1 = self.alea.uniform(ymin, ymax)
            p = self.alea.uniform(self.pmin, self.pmax)
            r.append([recta, d, y0, y1, p])
        return r

    def evtTable(self, nsegmentsG, nsegmentsD):
        """ construit un profil de table d'onde;
        nsegmentsG : profil au-dessus de 0;
        nsegmentsD : profil en-dessous de 0;
        retourne un profil-liste
        """
        rG = GenerateurProfil(self.alea, self.dtmin, self.dtmax,
                              self.vmin, self.vmax,
                              self.pmin, self.pmax).evtEnv(nsegmentsG)
        rD = GenerateurProfil(self.alea, self.dtmin, self.dtmax,
                              -self.vmin, -self.vmax,
                              self.pmin, self.pmax).evtEnv(nsegmentsD)
        return rG + rD

    def evtTableAsym(self, nsegments):
        """ construit un profil de table d'onde où
        retourne un profil-liste
        """
        return GenerateurProfil(self.alea, self.dtmin, self.dtmax,
                                -1.0, +1.0,
                                self.pmin, self.pmax).evtEnv(nsegments)

    def evtProgressif(self, nsegments, limite):
        """ construit un profil de variation de hauteur,
        de fréquence, de pano, etc. mais sans variations brusques.
        """
        r = []
        vmin = self.vmin
        vmax = self.vmax
        h0 = self.alea.uniform(vmin, vmax)
        for _ in range(nsegments):
            d = self.alea.uniform(self.dtmin, self.dtmax)
            while True:
                h1 = self.alea.uniform(vmin, vmax)
                if abs(h1 - h0) <= limite:
                    break
            p = self.alea.uniform(self.pmin, self.pmax)
            r.append([recta, d, h0, h1, p])
            h0 = h1
        return r

class GenerateurProfilFiltre:
    """ générateur d'un profil d'enveloppe, de hauteur
    passant par un filtre """
    def __init__(self, alea, dtmin, dtmax, vmin=0.0, vmax=1.0,
                 pmin=1.0, pmax=1.0, ncoeffs=None):
        """
        alea : générateur sériel
        dtmin, dtmax : durée min et max
        vmin=0.0, vmax=1.0 : valeur min et max
        pmin=1.0, pmax=1.0 : puissance min et max
        """
        self.gp = GenerateurProfil(alea, dtmin, dtmax,
                                   vmin, vmax,
                                   pmin, pmax)
        self.filtre = FiltreFixe("pb", ncoeffs)

    def temps(self, duree, nsegments, hfiltre, ncoeffs=None):
        """ construit un profil filtré
        hfiltre : hauteur du filtre en prony"""
        n = int(duree * sr)
        return self.samples(n, nsegments, hfiltre, ncoeffs)

    def samples(self, nsamples, nsegments, hfiltre, ncoeffs=None):
        """ construit un profil filtré
        hfiltre : hauteur du filtre en prony"""
        p = self.gp.evt(nsegments)
        v = ProfilBase(p).samples(nsamples)
        if ncoeffs is None:
            return self.filtre(v, hfiltre)
        else:
            return self.filtre(v, hfiltre, ncoeffs)

