#-*-coding:utf-8-*-
# Profils/profilgeneral.py

"""
fournit rectag, cubicag, curvag, fluctuag,
nouveaux profils qui permettent une écriture étendue

rectag est écrit [rectag, y0, (dt, y)+]]
cubicag est écrit [cubicag, y0, p0, (dt, y, p)+]
fluctuag est écrit [fluctuag, y0, (dt, y)+]
constg est écrit [fluctuag, (dt, y)+]

rectap est écrit [rectag, y0, (dt, y)+]
cubicap est écrit [cubicag, y0, p0, (dt, y, p)+]
fluctuap est écrit [fluctuag, y0, (dt, y)+]
constp est écrit [constp, (dt, v)+]

Deux solutions possibles:
- soit reconstruire la suite habituelle: rectap, cubicap
- soit compiler immédiatement: rectag, cubicag,
La 2e solution est choisie car elle permet un calcul très rapide.
"""
import copy

import numpy as np
from samplerate import SR

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.04.01, 2013.08.08, 2014.09.27, 2015.01.23, 2018.08.30"

#class Cdroite():
#    def __init__(self)

def droite(duree, y0, y1, courbure, bdroit=True):
    """ une droite allant de (y0) à (y1) en duree sec avec
    la courbure donnée """
    n = int(duree * SR)
    dy = y1 - y0
    if bdroit:
        vy = np.linspace(0.0, 1.0, n)**courbure * dy + y0
    else:
        vy = (1.0 - np.linspace(0.0, 1.0, n))**courbure * dy + y0
    return vy

def consta(liste):
    """ construit une ligne horizontale
    syntaxe: [consta, d, y] """
    duree, y = liste
    n = int(duree * SR)
    return np.ones(n, np.float64) * y

def recta(liste):
    """ trace une droite; syntaxes de D:
        [duree, y_initial, y_final]
        [duree, y_initial, y_final, courbure] """
    try:
        duree, y0, y1, puiss = liste
    except ValueError:
        duree, y0, y1 = liste
        puiss = 1.0
    nd = int(duree * SR)
    if nd <= 1:
        return np.asarray([(y0 + y1)/2])
    if y0 == y1:
        return np.ones(nd, np.float64) * y0
    if puiss == 0.0:
        puiss = 1.0
    if puiss != 1.0: # CECI EST INCOHÉRENT; IL FAUT AUSSI 'try' ICI
        u = np.arange(0.0, 1.0, 1.0/nd)
        u **= puiss
        u *= y1 - y0
        return y0 + u
    else:
        try:
            return y0 + np.arange(0.0, 1.0, 1.0 / nd) * (y1 - y0)
        except MemoryError:
            print("recta:MemoryError", y0, y1, "duree*SR", nd, 1.0 / nd)
            return y0

def cubica(liste):
    """ trace une courbe que les mathématiciens désignent par 'cubique'.
    Syntaxe:
        liste = [dt, y0, p0, y1, p1 ]
    """
    def courbeCubique(x0, y0, p0, x1, y1, p1):
        """retourne une cubique
        'x0, y0: coordonnée du point initial
        'p0: tangente au point initial
        'x1, y1: coordonnée du point final
        'p1: tangente au point final
        """
        R = coeffscubiquex(x0, y0, p0, x1, y1, p1)
        vT = np.arange(x0, x1, 1.0/SR)
        S = valeurCubique(R, vT)
        return S

    def coeffscubiquex(x0, y0, p0, x1, y1, p1):
        """retourne les coeffs a, b, c, d
        tels que a * x**3 + b * x**2 + c * x + d
        passe par (x0, y0, p0, x1, y1, p1)
        """
        M = [[x0**3, x0**2, x0, 1],
             [x1**3, x1**2, x1, 1],
             [3 * x0**2, 2 * x0, 1, 0],
             [3 * x1**2, 2 * x1, 1, 0]]
        Y = [y0, y1, p0, p1]
        R = systemeCramer(M, Y)
        return R

    def valeurCubique(F, x):
        """ calcule la valeur de la cubique au point 'x'
        f_i étant les coefficients """
        return ((F[0] * x + F[1]) * x + F[2]) * x + F[3]

    def determinant(M):
        """retourne le déterminant du tableau M """
        return np.linalg.det(M)

    def systemeCramer(M, Y, baffiche=False):
        """ retourne R tel que M * R = Y """
        k = determinant(M)
        if k != 0:
            k = 1.0/k
        else:
            print("systemeCramer: Il n'y a pas de solution")
            return None
        R = []
        for i in range(len(M)):
            H = copy.deepcopy(M)
            for j in range(len(Y)):
                H[j][i] = Y[j]
            if baffiche:
                print(H)
            r = k * determinant(H)
            R.append(r)
        return R

    duree, y0, p0, y1, p1 = liste
    return courbeCubique(0.0, y0, p0, duree, y1, p1)

def fluctua(liste):
    """ 22.04.07, 2014.09.26, 2018.12.04
    cubica avec des pentes nulles aux extrémités
    puiss: possible """
    if len(liste) == 3:
        duree, y0, y1 = liste
        return cubica([duree, y0, 0.0, y1, 0.0])
    elif len(liste) == 4:
        duree, y0, y1, puiss = liste
        if y0 < y1:
            v0 = cubica([duree, 0.0, 0.0, 1.0, 0.0]) ** puiss
        else:
            v0 = cubica([duree, 1.0, 0.0, 0.0, 0.0]) ** puiss
        return v0 * (y1 - y0) + y0
    else:
        print("fluctua: avec 6 paramètres ?")

######################################################################
def rectag(yini, params):
    """ construit une suite de droites
    cette syntaxe facilite p-ê l'écriture des profils
    multiphoniques"""
    r = []
    y0 = yini
    for param in params:
        if len(param) == 3:
            dt, y, p = param
            v = recta([dt, y0, y, p])
        else:
            dt, y = param
            v = recta([dt, y0, y])
        r.append(v)
        y0 = y
    return np.concatenate(r)

def cubicag(yini, pini, params):
    """ construit une suite de cubiques """
    r = []
    y0, p0 = yini, pini
    for param in params:
        dt, y, p = param
        v = cubica([dt, y0, p0, y, p])
        r.append(v)
        y0, p0 = y, p
    return np.concatenate(r)

def fluctuag(yini, pini, params, dtfin, yfin, pfin):
    """ construit une suite de cubiques dont la pente est nulle,
    sauf la première et la dernière"""
    r = []
    y0, p0, p = yini, pini, 0.0
    for param in params:
        dt, y = param
        v = cubica([dt, y0, p0, y, p])
        r.append(v)
        y0, p0 = y, p
    dt, y1, p1 = dtfin, yfin, pfin
    v = cubica([dt, y0, p0, y1, p1])
    r.append(v)
    return np.concatenate(r)

def constag(params):
    """ construit une suite de droites horizontales
    Syntaxe: [(duree, v), (duree, v), (duree, v), ...])"""
    r = []
    for x in params:
        r.append(consta(x))
    return np.concatenate(r)

################################################################
 # <profil>p: p comme progressif

def rectap(yini, params):
    """ construit une suite de droites
    Syntaxe:
      [yini, (dt, y, [p]), (dt, y, [p]), (dt, y, [p]), ....]
    cette syntaxe facilite p-ê l'écriture des profils
    multiphoniques"""
    r = []
    y0 = yini
    for param in params:
        if len(param) == 3:
            dt, y, p = param
            v = [recta, dt, y0, y, p]
        else:
            dt, y = param
            v = [recta, dt, y0, y]
        r.append(v)
        y0 = y
    return r

def cubicap(yini, pini, params):
    """ construit une suite de cubiques
    Syntaxe:
      [yini, pini, (dt, y, p), (dt, y, p), (dt, y, p), ....]"""
    r = []
    y0, p0 = yini, pini
    for param in params:
        dt, y, p = param
        v = [cubica, dt, y0, p0, y, p]
        r.append(v)
        y0, p0 = y, p
    return r

def fluctuap(yini, pini, params, dtfin, yfin, pfin):
    """ construit une suite de cubiques dont la pente est nulle;
    retourne le profil-liste
    Syntaxe:
      [yini, pini, (dt, y), (dt, y), (dt, y), dtfin, yfin, pfin]"""

    r = []
    y0, p0, p = yini, pini, 0.0
    for param in params:
        dt, y = param
        v = [cubica, dt, y0, p0, y, p]
        r.append(v)
        y0, p0 = y, p
    dt, y1, p1 = dtfin, yfin, pfin
    v = [cubica, dt, y0, p0, y1, p1]
    r.append(v)
    return r

def constap(params):
    """ construit une suite de droites horizontales
    Syntaxe: [(duree, v), (duree, v), (duree, v), ...])"""
    r = []
    for x in params:
        duree, y = x
        r.append([recta, duree, y, y])
    return r

def point_cubique(y1, y2, y3, y4, t):
    """ calcule un point d'une cubique à la Bézier """
    return (1-t)**3*y1 + 3*t*(1-t)**2*y2 + 3*t**2*(1-t)*y3 + t**3*y4

def cubique_bezier(x0, x1, x2, x3, n):
    """  calcule n valeurs entre 0.0 et 1.0
    la fonction (1-t) * 3 * x0 + 3 * t* (1-t)2x1 + 3t2(1-t)x2 + t3x3
    """
    vpts = np.linspace(0.0, 1.0, n)
    return point_cubique(x0, x1, x2, x3, vpts)

def bezier(liste):
    """ profil pseudo-bezier: les lignes ne sont
    pas tangentes parce que les x sont alignés
    avec des pas égaux (linéairement) et non selon une autre cubique
    comme le veut la courbe de Bézier exacte."""
    duree, y0, y1, y2, y3 = liste
    n = int(duree * SR)
    return cubique_bezier(y0, y1, y2, y3, n)

