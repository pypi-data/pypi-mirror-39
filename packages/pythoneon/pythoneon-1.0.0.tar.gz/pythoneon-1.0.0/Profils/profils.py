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
# Profils/profils.py

"""fournit des profils

Constituants de base:
--df recta([duree, y0, y1[, puiss]]):
--df cubica([duree, y0, p0, y1, p1[, puissance]]): # puissance sans intérêt
--df fluctua([duree, y0, y1,[, puissance]]): # puissance sans intérêt
--df const([duree, v])

--df rectag(y0, (d, y), (d, y)) ds profilgeneral
--df fluctuag(y0, (d, y), (d, y)) ds profilgeneral
--df cubicag(y0, p0, (d, y, p), (d, y, p)) ds profilgeneral
--df constg([duree, v, (duree, v), (duree, v), ...]) ds profilgeneral

--df rectap(y0, (d, y), (d, y)) ds profilgeneral
--df fluctuap(y0, (d, y), (d, y)) ds profilgeneral
--df cubicap(y0, p0, (d, y, p), (d, y, p)) ds profilgeneral
--df constp([duree, v, (duree, v), (duree, v), ...]) ds profilgeneral

# syntaxe fausses :)
--df profil(liste de constituants):
--df fonction([duree, x0, x1, fct[, y0, y1]]):
--df goutte([duree1, penteini, duree2, pentefin]):
--df gutta([duree, ymax]):
--df frons([duree, y0, y1]):, def front([duree, y0, y1):
--df expt([duree, y0, limite=0.00001]):
--df expAD([duree, ratioattac]):
--df parab([y0, p0, (y1, d1), (y2, d2), ...]):
--df arcparabole(duree, h, bfinal=False):
--df jonction([duree])

Fonctions pour 'cubica'

--df courbeCubique(x0, y0, p0, x1, y1, p1):
--df coeffscubiquex(x0, y0, p0, x1, y1, p1):
--df valeurCubique(F, x):
--df determinant(M):
--df systemeCramer(M, Y, affiche = 0):

Dérivés:

--df fluctua(liste):
--df vrecta():
--df vcubica():
--df vcurva():
--df vfluctua():
--df vrectac():
--df rectac():
--df rectil(liste):
--df rectaf(duree, y0, y1, puiss = 1.0):
--df curvaf(duree, yi, yt, c, coeff=1.0):
--df cubicaf(D):
--df curva(D):

Transformations:

--df transposeliste(liste, dh):
--df prolon():
--df prolonbrut(p):

Afficheurs:

--df dureeEnv(E):
--df afficheprofil(P):
--df explicitafficheprofil(P):
--df affprofil(pListe, message=None):
--df printprofil(pListe): # très pratique

Obsolètes ou déplacées:

--df profil_2008(listeP):
--df transposeliste2(liste, dh):
--df pyxil(profilP, x0, y0, xcoeff, pas=1000):

La classe Guimbarde n'est pas adaptée à tous les cas souhaitables
d'où la création d'un constituant  'def j(duree)' insérant un
glissement entre les niveaux adjacents.
"""
#certaines fonctions ne sont pas sûres car pas
#suffisamment utilisées."""
#10.03.03-24.04.03-6.9.03-20.10.04, 8.08.06, 5.11.06
# anciennes scories dans v0-profils.py

#import copy
import numpy as np

from samplerate import SR

from Outils.ajuster import prolongerZ
from origine import OrigineStr
from Profils.profilgeneral import (recta, cubica, fluctua, consta)
                           #rectag, cubicag, fluctuag, constag,
                           #rectap, cubicap, fluctuap, constap)
from conversions import (extremum, exponen)
__all__ = [
    "profilj", #(listep):
    "profil", #(listeP):
    #"recta_fonction", #(liste, vt, tsomme=0.0):
    #"cubica_fonction", #(liste, vt, tsomme):
    #"profil_fonction", #(listeP, vt):
    "consta", #(liste):
    "recta", #(liste):
    "fonction", #(params): #duree, x0, x1, fct[, y0, y1]
    "goutte", #(duree1, penteini, duree2, pentefin):
    "gutta", #(duree):
    "front", #(duree, y0, y1):
    "frons", #(", #(duree, y0, y1)):
    "expADbrut", #(a, b, x):
    "expAD", #(params):
    "expt", #(params):
    "expT", #(duree, y0, limite=0.00001):
    "cubica", #(liste, bdernier=False):
    "jonction", #(listeP=None):
    #"courbeCubique", #(x0, y0, p0, x1, y1, p1):
    #"coeffscubiquex", #(x0, y0, p0, x1, y1, p1):
    #"valeurCubique", #(F, x):
    #"determinant", #(M):
    #"systemeCramer", #(M, Y, affiche = 0):
    "fluctua", #(liste): # inutilisé
    "vrecta", #():
    "vcubica", #():
    "vcurva", #():
    "vfluctua", #():
    "vrectac", #():
    "rectac", #():
    "rectil", #(liste):
    "rectaf", #(duree, y0, y1, puiss = 1.0):
    "curvaf", #(duree, yi, yt, c, coeff=1.0):
    "cubicaf", #(D):
    "curva", #(D):
    "arcparabole", #(duree, h, bfinal=False):
    "coeffsparabole", #(d, y0, y1, p0):
    "traceparabole", #(a, b, c, d):
    "rparabole", #(y0, p0, couples):
    "parab", #(p):
    "transpose23", #(p23, dh):
    "transpose24", #(p24, dh):
    "transposeliste", #(liste, dh):
    "modifprofil", #(p0, durees):
    "prolon", #(): # à remplacer par un booléen ?
    "prolonbrut", #(p):
    "profil_2008", #(listeP):
    "transposeliste2", #(liste, dh):
    "pyxprofil", #(profilP, x0, y0, xcoeff, pas=1000):
    "dureeEnv", #(E):
    "affprofil", #(pListe, message=None):
    "printprofil", #(pListe):
    "afficheprofil", #(listeP):
    "explicitafficheprofil", #(P):
    ]
__author__ = "Copyright (c) René Bastian <rbastian@free.fr>"
__date__ = """ 2003.03.03, 2006.02.10, 2007.02.11, 07.04.22, 09.09.20,
2012.08.08, 2012.10.14, 2015.05.08 """

########### Les constituants de base #######################

def normeProfil(pliste):
    """ réduit un profil de fréquences au niveau 1.0 """
    r = []
    v0 = pliste[0][2]
    for p in pliste:
        if p[0] == recta and len(p) == 4:
            x = [recta, p[1], p[2] / v0, p[3] / v0]
        elif p[0] == recta and len(p) == 5:
            x = [recta, p[1], p[2] / v0, p[3] / v0, p[4]]
        elif p[0] == cubica:
            x = [cubica, p[1], p[2] / v0, p[3], p[4] / v0, p[5]]
        elif p[0] == fluctua:
            x = [recta, p[1], p[2] / v0, p[3] / v0]
        else:
            print("normeProfil: pas encore fait")
        r.append(x)
    return r

def profilj(listep):
    """ profil comprenant des constituants de jonction """
    #r = []
    #prec = listep[0]
    n = len(listep)
    for i in range(1, n):
        if listep[i] == jonction:
            pass
        else:
            pass

def profil(xlisteP):
    """ calcule un vecteur-profil à partir de sa description.
    'xlisteP' : liste des composants du profil
    06.12.07 ; env. 12 % plus rapide que la précédente version.
    La version 'liste de listes' a l'avantage de pouvoir être
    utilisée par 'ProfilBase'.
    Le gain de temps de calcul est de 1.001 ! :-) """
    # inutile
#    if xlisteP == []:
#        print("profil(listeP) == []")
#        return np.zeros(1)
#    elif not isinstance(xlisteP, (list, tuple)):
#        print("profil:listeP", type(xlisteP))
#        return
# obsolète
#    listeP = xlisteP
#    for e in xlisteP:
#        if e[0] in [rectap, cubicap, fluctuap, constap]:
#            print("profil:[rectap, ...] reste à contrôler")
#            x = e[0](*e[1:])
#            listeP.append(x)
#        elif e[0] in [rectag, cubicag, fluctuag, constag]:
#            print("profil:[rectag, ...] reste à contrôler")
#            x = e[0](*e[1:])
#            listeP.append(x)
#        else:
#            listeP.append(e)
    listeR = []
    xprec = [0.0, 0.0]
    for e in xlisteP:
        if e[0] == prolon:
            x = prolonbrut((e[1], xprec[-2], xprec[-1]))
        elif isinstance(e, np.ndarray):
            x = e
        elif e[0] == rectaf:
            if len(e[1:]) == 3:
                duree, y0, y1 = e[1:]
                x = rectaf(duree, y0, y1)
            if len(e[1:]) == 4:
                duree, y0, y1, puiss = e[1:]
                x = rectaf(duree, y0, y1, puiss)
        else:
            try:
                x = e[0](e[1:])
            except TypeError:
                x = e[0](*e[1])
        listeR.append(x)
        xprec = x
    try:
        return np.concatenate(listeR)
    except ValueError:
        print("profils.profil:ValueError")
        print("listeP:", xlisteP)
        print("listeR:", listeR)
        for r in listeR:
            print(type(r),)
            try:
                print(r.size)
            except AttributeError:
                print(r)



#
#def const(liste):
#    """ construit une ligne horizontale
#    syntaxe: [const, d, y] """
#    duree, y = liste
#    n = int(duree * SR)
#    return np.ones(n, np.float64) * y
#
#def recta(liste):
#    """ trace une droite; syntaxes de D:
#        [duree, y_initial, y_final]
#        [duree, y_initial, y_final, courbure] """
##    12.08.04 : le chgt en n = int(duree*SR) en n+1 n'a qu'une
##                influence négligeable
##    11.02.07 : essai pour introduire des durées fonction du temps -->
##        --> collision avec les durées fixes
##    22.04.07 : révision complète, chgt de la 'courbure'
#
#    try:
#        duree, y0, y1, puiss = liste
#    except ValueError:
#        duree, y0, y1 = liste
#        puiss = 1.0
#    nd = int(duree * SR)
#    if nd <= 1:
#        return np.asarray([(y0 + y1)/2])
#    if y0 == y1:
#        return np.ones(nd, np.float64) * y0
#    if puiss == 0.0:
#        puiss = 1.0
#    if puiss != 1.0: # CECI EST INCOHÉRENT; IL FAUT AUSSI 'try' ICI
#        u = np.arange(0.0, 1.0, 1.0/nd)
#        u **= puiss
#        u *= y1 - y0
#        return y0 + u
#    else:
#        try:
#            return y0 + np.arange(0.0, 1.0, 1.0 / nd) * (y1 - y0)
#        except MemoryError:
#            print("recta:MemoryError", y0, y1, "duree*SR", nd, 1.0 / nd)
#            return y0

def fonction(params): #duree, x0, x1, fct[, y0, y1]
    """
    x0, x1 : valeurs intiale et finale des abscisses de fct(x)
    fct : fonction qui est à fournir
    y0, y1 : valeurs initiale et finale fct(x0) -> y0 et fct(x1) -> y1
   syntaxe possible:
      [fonction, duree, x0, x1, fct, y0=None, y1=None]
    """
    duree, x0, x1, fct = params[:4]
    n = int(duree * SR)
    vx = np.linspace(x0, x1, n)
    vy = fct(vx)
    if len(params) == 4:
        return vy
    else:
        y0, y1 = params[4:]
        m0, m1 = y0 / vy[0], y1 / vy[-1]
        v = np.linspace(m0, m1, n)
        return vy * v

def goutte(duree1, penteini, duree2, pentefin):
    """retourne un profil de goutte
    d'une durée env. 0.1 sec comprenant
        - une partie montante presque raide
        - et une partie descendante
        - bgoutte(0.03, 80.0, 0.07, -1.0) est une bonne solution
        - goutte(0.03, 100.0, 0.07, -10.0) aussi
    #20.06.05
    """
    P = [[cubica, duree1, 0.0, penteini, 1.0, 0.0],
         [cubica, duree2, 1.0, 0.0, 0.0, pentefin]]
    p = profil(P)
    p = p / extremum(p)
    return p

def gutta(duree):
    """ un profil approximativement en forme de goutte
    syntaxe pour 'profils' : [gutta, duree] REVOIR
    """
    #print(ymax, "n'est pas utile")
    n = int(duree * SR)
    x = np.linspace(0.0, duree, n)
    v = abs((x - duree) * x**0.5)
    return v / v.max()

def fimpulse(duree):
    """ une sorte d'impulsion molle; elle a bonne figure
    de 1. à 3."""
    def func(x):
        " le calcul ponctuel "
        return np.exp(-x**2) * np.log(x)

    n = int(duree * SR)
    vx = np.linspace(1.0, 3.0, n)
    vy = func(vx)
    dy = np.linspace(vy[0], vy[-1], vy.size)
    vy -= dy
    return vy / vy.max()

def front(duree, y0, y1):
    """ un profil partant avec une pente infinie de y0 pour
    arriver à y1 avec une pente nulle
    cf.Piskounov I p. 334 """
    return frons((duree, y0, y1))

def frons(p):
    """ un profil partant avec une pente infinie de y0 pour
    arriver à y1 avec une pente nulle
    cf.Piskounov I p. 334 """
    duree, y0, y1 = p
    n = int(duree * SR)
    x = np.linspace(0.0, duree / 3, n)
    v = abs((x - duree) * x**0.5)
    v /= v.max()
    d = y1 - y0
    return y0 + v * d

#-----------------------------------------------
def expADbrut(a, b, x):
    """ exponentielle 'attac-decay'
    le -= rmin n'est pas une bonne idée"""
    r = a * x * np.exp(-b * x)
    r /= extremum(r)
    return r

def expAD(params):
    """ exponentielle 'attac-decay' ramenée à zéro par une cubique
    duree : durée totale
    rattac : fraction de la durée de la montée < 1.0
    """
    duree, rattac = params
    vt = np.arange(0.0, duree, 1.0 / SR)
    b = 1.0 / (duree * rattac)
    v = expADbrut(1.0, b, vt)
    n, ix = v.size, v.argmax()
    reste = n - ix
    cub = profil([[cubica, float(reste) / SR, 1.0, 0.0, 0.0, 0.0]])
    vreste = v[ix:]
    cub, vreste = prolongerZ((cub, vreste))
    vreste *= cub
    if duree <= 0.01 and vreste.max() <= 1.0:
        vreste **= 2
    return np.concatenate((v[:ix], vreste))


#----------------------------------
def expt(params):
    """ mise en forme pour expT
    duree, y0, limite=0.00001 = params """
    if len(params) == 2:
        d, y = params
        return expT(d, y)
    elif len(params) == 3:
        d, y, limite = params
        return expT(d, y, limite)

def expT(duree, y0, limite=0.00001):
    """
    calcule un vecteur (dé)croissant exponentiellement de
    'y0' jusqu'à 'limite'
    >>> from profils import expT
    >>> w = expT(1.0, 0.1)
    >>> w
    array([  1.00000000e+00,   9.97392764e-01,   9.94792326e-01, ...,
             1.00786267e-05,   1.00523494e-05,   1.00261405e-05])
    >>> w * 32767
    array([  3.27670000e+04,   3.26815687e+04,   3.25963601e+04, ...,
         3.30246362e-01,   3.29385331e-01,   3.28526546e-01])
    """
    n = int(duree * SR)
    c = exponen(abs(y0), limite, n)
    e = np.zeros(n)
    y = abs(y0)
    for i in range(n):
        e[i] = y
        y = y * c
    if y0 > 0.0:
        return e
    else:
        return -e

def jonction(listeP=None):
    """ constituant faisant la jonction entre les
    valeurs adjacentes """
    print(listeP)
#
#def cubica(liste, bdernier=False):
#    """ trace une courbe que les mathématiciens désignent par 'cubique'.
#    Syntaxes:
#        liste = [dt, y0, p0, y1, p1 ]
#        liste = [dt, y0, p0, y1, p1, puissance]
#    L'usage de 'puissance' est malaisé car cela change les pentes p0 et p1.
#    """
#    if len(liste) == 5:
#        duree, y0, p0, y1, p1 = liste
#        return courbeCubique(0.0, y0, p0, duree, y1, p1)
#        #if bdernier: # aménagement éventuel pour conduire vers zéro
#        #    return courbeCubique(0.0, y0, p0, duree, y1, p1)
#        #else:
#
#        #    return courbeCubique(0.0, y0, p0, duree, y1, p1)
#    elif len(liste) == 6:
#        # cette forme est difficilement contrôlable
#        duree, y0, p0, y1, p1, puiss = liste
#        nd = int(duree * SR)
#        courbure = np.arange(0., 1., 1./nd) ** puiss
#        y = courbeCubique(0.0, 0.0, p0, duree, y1 - y0, p1)
#        y, courbure = prolongerZ((y, courbure))
#        return y * courbure + y0
#
#
## ---------------- début des méthodes pour cubique --------------
#
#def courbeCubique(x0, y0, p0, x1, y1, p1):
#    """retourne une cubique
#    'x0, y0 : coordonnée du point initial
#    'p0 : tangente au point initial
#    'x1, y1 : coordonnée du point final
#    'p1 : tangente au point final
#    """
#    R = coeffscubiquex(x0, y0, p0, x1, y1, p1)
#    vT = np.arange(x0, x1, 1.0/SR)
#    S = valeurCubique(R, vT)
#    return S
#
#def coeffscubiquex(x0, y0, p0, x1, y1, p1):
#    """retourne les coeffs a, b, c, d
#    tels que a * x**3 + b * x**2 + c * x + d
#    passe par (x0, y0, p0, x1, y1, p1)
#    """
#    M = [[x0**3,   x0**2, x0, 1],
#         [x1**3,   x1**2, x1, 1],
#         [3 * x0**2, 2 * x0,  1,  0],
#         [3 * x1**2, 2 * x1,  1,  0]]
#    Y = [y0, y1, p0, p1]
#    R = systemeCramer(M, Y)
#    return R
#
#def valeurCubique(F, x):
#    """ calcule la valeur de la cubique au point 'x'
#    f_i étant les coefficients """
#    return (((F[0] * x + F[1]) * x + F[2]) * x + F[3])
#
#def determinant(M):
#    """retourne le déterminant du tableau M """
#    return np.linalg.det(M)
#
#def systemeCramer(M, Y, affiche = 0):
#    """ retourne R tel que M * R = Y """
#    k = determinant(M)
#    if k != 0:
#        k = 1.0/k
#    else :
#        print("systemeCramer: Il n'y a pas de solution")
#        return None
#    R = []
#    for i in range(len(M)):
#        H = copy.deepcopy(M)
#        for j in range(len(Y)):
#            H[j][i] = Y[j]
#        if affiche:
#            print(H)
#        r = k * determinant(H)
#        R.append(r)
#    return R
#
########### Dérivés des constituants de base #######################
#
#def fluctua(liste): # inutilisé
#    """
#    fonction défecteuse (bidon utilisée dans profilvariant.py)
#    liste = [dt, y0, y1, courbure]  = > 0.0, y0, 0.0, dt, y1, 0.0, SR
#    22.04.07
#    """
#    try:
#        duree, y0, p1, puiss = liste
#    except StandardError:
#        duree, y0, p0, y1 = liste
#        puiss = 1.0
#    p0, p1 = 0.0, 0.0
#    if puiss == 1.0:
#        return courbeCubique(0.0, y0, p0, duree, y1, p1)
#    else:
#        nd = int(duree * SR)
#        courbure = np.arange(0., 1., 1./nd)**puiss
#        y = courbeCubique(0.0, 0.0, p0, duree, y1-y0, p1)
#        return y * courbure + y0

#def rectaff(d, y0, y1):
#    " à sortir dès que les essais sont clos"
#    return recta([d, y0, y1])

def vrecta():
    " est utilisé symboliquement dans ProfilVariant"
    pass

def vcubica():
    " est utilisé symboliquement dans ProfilVariant"
    pass

def vcurva():
    " est utilisé symboliquement dans ProfilVariant"
    pass

def vfluctua():
    " est utilisé symboliquement dans ProfilVariant"
    pass

def vrectac():
    " est utilisé symboliquement dans ProfilVariant"
    pass

def rectac():
    " rien mais ne pas effacer"
    pass

def rectil(liste):
    """ trace une ligne droite horizontale
    Syntaxe de la liste: (duree, valeur)
    """
    duree, y = liste
    n = int(duree * SR)
    return np.ones(n, np.float64) * y

def rectaf(duree, y0, y1, puiss=1.0):
    """ 2010.08.05 trace une droite
    """
    nd = int(duree * SR)
    if nd <= 1:
        return np.asarray([(y0 + y1)/2])
    if y0 == y1:
        return np.ones(nd, np.float64) * y0
    if puiss == 0.0:
        puiss = 1.0
    if puiss != 1.0:
        u = np.arange(0.0, 1.0, 1.0/nd)
        u **= puiss
        u *= y1 - y0
        return y0 + u
    else:
        return y0 + np.arange(0.0, 1.0, 1.0/nd) * (y1 - y0)

def curvaf(duree, yi, yt, c, coeff=1.0):
    """trace une courbe exponentielle
        - allant de yi à yt en une durée d
        - selon une courbure c
        - coeff peut accentuer la courbure """
    a = np.exp(np.log(np.abs(yt - yi)) - c * np.log(duree))
    if yt < yi:
        a = -a
    T = np.arange(0.0, duree, 1.0/SR)
    if coeff == 1.0:
        return a * (T**c) + yi
    else:
        y = a * (T**c) + yi
        return y**coeff

def cubicaf(D):
    "comme cubica - jamais utilisé donc disponible"
    return  cubica(D)

def curva(D):
    """trace une courbe exponentielle
        - allant de D[1] à D[2] en une durée D[0]
        - selon une courbure D[3]
        D[4] peut accentuer la courbure
    syntaxes:
           [duree, y_initial, y_final, courbure]
           [duree, y_initial, y_final, courbure, puissance]
    """
    duree = D[0]
    yi = D[1]
    yt = D[2]
    c = D[3] # courbure
    #duree, yi, yt, c = D
    try:
        coeff = D[4]
    except IndexError: #, ValueError:
        coeff = 1.0
    a = np.exp(np.log(np.abs(yt - yi)) - c * np.log(duree))
    if yt < yi:
        a = -a
    vT = np.arange(0.0, duree, 1.0/SR)
    if coeff == 1.0:
        return a * (vT**c) + yi
    else:
        y = a * (vT**c) + yi
        return y**coeff

#################### parabole

def arcparabole(duree, h, bfinal=False):
    """ le sommet de l'arc de parabole est à 'h' au-dessus de l'axe
    du temps et ce sommet est atteint au temps 'duree'/2
    La fonction: y(t) = x*(a*x+b)"""
    d2 = duree * duree
    a = - 4 * h / d2
    b = -a * duree
    if bfinal:
        n = int(duree * SR)
        vx = np.linspace(0.0, duree, n)
    else:
        vx = np.arange(0.0, duree, 1.0 / SR)
    return vx * (a * vx + b)

def coeffsparabole(d, y0, y1, p0):
    """ calcul des coefficients de la parabole """
    b, c = p0, y0
    a = (y1 - y0 - p0*d)/(d**2)
    p1 = 2*a*d + b
    return a, b, c, p1

def traceparabole(a, b, c, d):
    """ calcule le vecteur """
    vt = np.arange(0.0, d, 1.0/SR)
    return a*(vt**2) + b*vt + c

def rparabole(y0, p0, couples):
    " calcule les coeffs consécutifs des arcs de parabole """
    r = []
    for c in couples:
        y1, d = c
        a, b, c, p1 = coeffsparabole(d, y0, y1, p0)
        r.append((a, b, c, d))
        y0, p0 = y1, p1
    return r

def parab(p):
    """ forme listée; voir Parabole/a_parabole.py """
    y0, p0 = p[:2]
    couples = p[2:]
    z = rparabole(y0, p0, couples)
    r = []
    for yy in z:
        w = traceparabole(*yy)
        r.append(w)
    return np.concatenate(r)

########## Transformations de profils

def transpose23(p23, dh, bprony=True):
    " transpose un profil 'recta' de 'dh' "
    if bprony:
        p23[2] += dh
        p23[3] += dh
    else:
        p23[2] *= dh
        p23[3] *= dh
    return p23

def transpose24(p24, dh, bprony=True):
    " transpose un profil 'cubica' de 'dh' "
    if bprony:
        p24[2] += dh
        p24[4] += dh
    else:
        p24[2] *= dh
        p24[4] *= dh
    return p24

def transposeliste(liste, dh, bprony=True):
    """dans 'liste' change
    - les valeurs en [2] et [3] des rectas
    - les valeurs en [2] et [4] des cubicas
    Les curvas sont expulsés.
    La fonction retourne une nouvelle liste pour éviter les effets de bord.
    UNIQUEMENT ADDITIVE
    """
    message = "transposeliste(liste, dh): y n'est pas un profil connu"
    r = []
    for x in liste:
        y = x[:]
        if y[0] in [recta, frons, fluctua]:
            r.append(transpose23(y, dh, bprony))
        elif y[0] == cubica:
            r.append(transpose24(y, dh, bprony))
        elif y[0] == arcparabole:
            y[2] += dh
            r.append(y)
        else:
            print(message)
    return r

def modifprofil(p0, durees):
    """ remplacer les durées d'un profil par celles données
    par la liste 'durees'. """
    r = []
    for d, pp in zip(durees, p0):
        pp[1] = d
        r.append(pp)
    return r

def prolon(): # à remplacer par un booléen ?
    " est un indicateur utilisé dans 'profils'"
    pass

def prolonbrut(p):
    """ prolongation du profil précédent avec la même pente
    y0, y1 = v[-2], v[-1] valeurs du vecteur précédant.
    Voir aussi 'expt' """
    duree, y0, y1 = p
    dt, dy = 1.0 / SR, y1 - y0
    n = int(duree / dt) + 1
    yfin = y0 + n * dy
    return recta((duree, y1, yfin))

#------------------------------------

##DEBUT

##### Prototype pour une classe future :)
##### Essais abandonnés, fonctions déplacées

class Profil(OrigineStr):
    """ classe presque pour rien, sinon avoir une instance de Profil """
    def __init__(self, p):
        OrigineStr.__init__(self)
        self.p = p

    def pprint(self):
        "affiche "
        afficheprofil(self.p)

    def evt(self):
        " construit le vecteur "
        return profil(self.p)

    def change(self, p=None):
        "pour changer"
        if p is not None:
            self.p = p

def profil_2008(listeP):
    """
    calcule un vecteur-profil à partir de sa description.
    'P' : liste des composants du profil
    06.12.07 ; env. 12 % plus rapide que la précédente version.
    La version 'liste de listes' a l'avantage de pouvoir être
    utilisée par 'ProfilBase'.
    """
    if listeP == []:
        print("profil(listeP) == []")
        return np.zeros(1)
    listeR = []
    if not isinstance(listeP, list):
        print("profil:listeP", type(listeP))
        return
    for e in listeP:
        listeR.append(e[0](e[1:]))
    try:
        return np.concatenate(listeR)
    except ValueError:
        print("profils.profil:ValueError")
        print("listeP", listeP)
        print("listeR", listeR)
        for r in listeR:
            print(type(r))

def transposeliste2(liste, dh):
    " ancienne forme"
    print("transposeliste2", liste, dh)
    #raise StandardError("aulieu de transposeliste2 : appeler transposeliste")


def pyxprofil(profilP, x0, y0, xcoeff, pas=1000):
    " déplacé "
    print("voir pyxnotation.py", profilP, x0, y0, xcoeff, pas)

#------------------ AFFICHAGES
########## Afficheurs de profils

def dureeEnv(E):
    """additionne les durées du profil E"""
    t = 0.
    for p in E:
        t += p[1]
    return t

def profil2str(pListe):
    """ forme affichable et enregistrable de pListe """
    r = ["["]
    for p in pListe:
        rr = ["[", str(p[0]).split(" ")[1], ","]
        for x in p[1:]:
            try:
                rr.append(str(x))
            except TypeError:
                rr.append("%-9s" % str(x))
            rr.append(",")
        rr.append("]")
        xs = " ".join(rr)
        r.append(xs)
    s = " ".join(r)
    s = s.replace(" ,", ",")
    s = s.replace(", ]", "]")
    s = s.replace("[ ", "[")
    s = s.replace("] [", "], [")
    s += "]"
    return s

def affprofil(pListe, message=None):
    " affiche le profil - vient de 'infoprofils.py' "
    print("Utiliser de préférence profil2str(pListe)")
    if message is not None:
        print(message)

    for p in pListe:
        r = [str(p[0]).split(" ")[1]]
        for x in p[1:]:
            try:
                r.append("%9.3f" % (x))
            except TypeError:
                r.append("%-9s" % str(x))
        s = " ".join(r)
        print(s)
    print("-" * 12)
    return str(pListe)

def printprofil(pListe):
    " affiche un profil "
    print("Utiliser de préférence profil2str(pListe)")
    a = str(pListe).split(" ")
    r = ["["]
    for x in a:
        if x == "at":
            pass
        elif x[:2] == "[<":
            r.append("[")
        elif x == "[[<function":
            r.append("\n[")
        elif x[:2] == "0x":
            r.append(",")
        elif x[-2:] == "],":
            r.append(x + "\n")
        else:
            r.append(x)
    s = " ".join(r)
    s = s.replace(" ,", ",")
    s = s.replace("\n[ ", "\n [ ")
    return s

def afficheprofil(listeP):
    " fonction simplette pour afficher un profil """
    print("Utiliser de préférence profil2str(pListe)")
    if isinstance(listeP, list):
        for p in listeP:
            print("[", str(p[0])[10:16], end=", ")
            for x in p[1:]:
                if x:
                    print("%7.3f" % x, end=", ")
                else:
                    print("%7s" % str(x), end=", ")
                    #print("%7s" % "None",)
            print("]")
    else:
        for p in listeP:
            print(p)
    print(len(listeP))

def explicitafficheprofil(P):
    " f. simplet pour afficher un profil """
    print("Utiliser de préférence profil2str(pListe)")
    if isinstance(P, list):
    #type(P) == type([]):
        for p in P:
            if p[0] == recta:
                print("%-6s" % ("recta"),)
            elif p[0] == cubica:
                print("%-6s" % ("cubica"), )
            elif p[0] == curva:
                print("%-6s" % ("curva"), )
            for x in p[1:]:
                print("%7.3f" % (x),)
            print()
    else:
        for p in P:
            print(p)

