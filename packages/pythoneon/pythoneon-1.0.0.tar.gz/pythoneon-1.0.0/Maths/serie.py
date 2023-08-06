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
# serie.py

"""fournit les classes
- Serie: les méthodes principales du générateur sériel de
nombres (très pseudo-)aléatoires ;
- Serie002: un générateur sériel de nombres (très pseudo-)aléatoires ;
avantage sur random: ne sera pas « amélioré
donc les séries resteront identiques.

Rajouté le 28.04.2011
remplir, brouiller, brouillerV, sub
Changé le 15.09.2011
version simple de seq et renommage de l'ancienne en seq_experim
"""
#fournit la classe SerieVecteurProgressif:
#fournit à chaque appel un vecteur dont le
#premier (ou le dernier) nombre a changé.

import sys
import copy
import numpy as np
from origine import OrigineStr
from samplerate import SR
from conversions import prony2samples

__date__ = """2005.01.02, 2006.02.07, 2006.04.17, 2008.08.19,
              2009.01.12, 2012.11.06, 2013.08.29"""
__author__ = "Copyright (c) René Bastian 2005-2012 <rbastian@free.fr>"

class Serie(OrigineStr):
    """classe de série (presque) infinie de nombres entiers ;
    on peut en dériver des séries de nombres réels."""
    def __init__(self, x=98765, a=1234567, b=27, m=2**31-1, decalage=False):
        """ crée une instance de générateur sériel """
        OrigineStr.__init__(self)
        self.x, self.a, self.b, self.m = x, a, b, m
        self.i, self.xinit, self.ncycle = 0, x, 0
        self.decalage = decalage

    def seq(self):
        """ calcule et fournit l'entier suivant """
        self.x = (self.x * self.a + self.b) % self.m
        self.i += 1
        if self.x == self.xinit:
            self.ncycle = self.i
            print("Serie002: longueur du cycle", self.ncycle)
            self.i = 0
        return self.x

    def fseq(self):
        """retourne la prochaine valeur réelle."""
        return self.seq() / self.m

    def quartuple(self):
        "retourne le quatuor des valeurs"
        return self.x, self.a, self.m, self.b

    def randint(self, a0, a1, n=1):
        """retourne une valeur entière entre a0 et a1"""
        if a1 < a0:
            a1, a0 = a0, a1
        if a0 == a1:
            return a0
        if n == 1:
            if a0 == a1:
                return a0
            else:
                return (self.seq() % (abs(a1-a0))) + a0
        elif n > 1:
            if a0 == a1:
                return [a0 for _ in range(n)]
            else:
                return [(self.seq() % (abs(a1-a0))) + a0 for _ in range(n)]

    def uniform(self, a0, a1, n=1):
        """retourne les N prochaines valeurs réelles (float) entre a0 et a1."""
        #assert a0 != a1, "Serie.uniform: a0 == a1"
        if a0 == a1:
            return a0
        assert n >= 1, "Serie.uniform: N < 1"
        if a1 < a0:
            a1, a0 = a0, a1
        if n == 1:
            x = self.fseq()
            return (a1 - a0) * x + a0
        elif n > 1:
            z = np.zeros(n, np.float64)
            for i in range(n):
                x = self.fseq()
                z[i] = (a1 - a0) * x + a0
            return z

    def choix(self, E, n=1):
        """tire n éléments de la liste E """
        assert n >= 1, "<== Serie.choix"
        return [E[self.randint(0, len(E))] for _ in range(n)]

class Serie001(OrigineStr):
    """classe de série (presque) infinie de nombres entiers ;
    on peut en dériver des séries de nombres réels."""
    def __init__(self, x=9, a=11, m=2**31-1, b=0,
                 decalage=False, fnom=None):
        """pour créer une instance de
        générateur de nombres pseudo-aléatoires.
        """
        OrigineStr.__init__(self)
        self.x = x
        self.a = a
        self.b = b
        self.m = m
        self.i = 0
        self.imax = 0
        self.xinit = x
        self.ncycle = 0
        self.decalage = decalage
        self.fnom = fnom
        #self.ncycle = None
#
#    def __str__(self):
#        """ affiche presque tout."""
#        n = max([len(str(x)) for x in self.__dict__])
#        format = "%-" + str(n) + "s: %s \n"
#        r = [self.__class__.__name__+"\n"]
#        for x in self.__dict__:
#            s = format % (str(x), self.__dict__[x])
#            r.append(s)
#        return "".join(R)

    @staticmethod
    def sub(y):
        """ le contraire de add.accumulate """
        z = [y[0]]
        a = y[0]
        for x in y[1:]:
            z.append(x - a)
            a = x
        return np.array(z)

    def seq(self):
        """ calcule et fournit l'entier suivant """
        #print(self.x #, self.a, self.b, self.m)
        try:
            self.x = (self.x * self.a + self.b) % self.m
        except TypeError:
            print(self.x, self.a, self.b, self.m, self.i, "xinit", self.xinit)
        self.i += 1
        if self.x == self.xinit:
            self.ncycle += 1
            self.imax = self.i
            self.i = 0
        return self.x

    def seq_experimental(self):
        """
        calcule et fournit l'entier suivant.
        """
        #print(self.x, self.a, self.b, self.m)
        self.x = (self.x*self.a+self.b) % self.m
        self.i += 1
        try:
            if self.x == self.xinit:
                print("\nFin de cycle")
                self.ncycle = self.i
                #self.affiche()
                print(self)
                self.i = 0
                q = input("Continuer ? ")
                if q in ["n", "N"]:
                    sys.exit()
                if self.decalage:
                    self.a += 1
                    self.xinit = self.x
                    print("Serie001 (nouveaux params): ",)
                    self.affiche()
            return self.x
        except RuntimeError:
            print(self.x, self.xinit)

    def seq2(self):
        "retourne la valeur suivante de  'x'"
        self.x = (self.x*self.a + self.b)*self.x % self.m
        self.i += 1
        try:
            if self.x == self.xinit:
                print("\nFin de cycle")

                self.ncycle = self.i
                self.affiche()
                self.i = 0
                q = input("Continuer ? ")
                if q[0] in ["n", "N", "q", "Q"]:
                    sys.exit()
                if self.decalage:
                    self.a += 1
                    self.xinit = self.x
                    print("Serie001 (nouveaux params): ",)
                    self.affiche()
            return self.x
        except RuntimeError:
            print(self.x, self.xinit)

    def seed(self, x, a):
        "introduit d'autres valeurs initiales"
        self.x = x
        self.a = a
        self.xinit = x
        self.ncycle = 0

    def couple(self):
        "retourne 'x' et 'a'"
        return self.x, self.a

    def quartuple(self):
        "retourne le quatuor des valeurs"
        return self.x, self.a, self.m, self.b
#
#    def __str__(self, tout=True):
#        "affiche l'état actuel"
#        if tout:
#            return self.__class__.__name__  + str(self.__dict__)
#        else:
#            xformat = "x: %10i a: %10i m: %10i b: %10i"
#            return xformat % (self.x, self.a, self.m, self.b)

    def ensemble(self, n):
        """
        fournit n nombres distincts.
        """
        R = []
        for _ in range(n):
            R.append(self.seq())
        E = set(R)
        #print(len(E))
        return E

    def affiche(self):
        "affiche l'état actuel"
        forme = "a: %10i m: %10i i: %10i xinit: %10i ncycle: %10i x: %10i"
        print(forme % (self.a, self.m, self.i, self.xinit, self.ncycle, self.x))

    def courant(self):
        "affiche qqs attributs de l'état actuel"
        print("a: %i m: %i i: %i x: %i" % \
        (self.a, self.m, self.i, self.x))

class Serie002(Serie001):
    """fournit une série (presque) infinie de nombres réels ou entiers.
    Les méthodes les plus utilisées:
       noise(duree, xmin = -1.0, xmax = +1.0)
       bruit(nsamples, xmin = -1.0, xmax = +1.0)
       uniform(x0, x1, N=1)
       randint(a0, a1, N=1)
    L'initialisation selon 'Serie001' est obligatoire.
    """
    def __init__(self, x, a, m=2**31-1, b=0, decalage=False, fnom=None):
        """initialisation
        x: élément variable
        a: multiplicateur fixe
        b: additioné fixe
        m: valeur maximum
        fnom: nom de stockage PAS ENCORE UTILISÉ
        """
        Serie001.__init__(self, x, a, m, b, decalage, fnom=fnom)
        self.xT = None
        self.ergo = 1
        self.aM = float(2**31) #2147483648
        self.aM1 = 2**31 - 1

    def seed(self, x, a):
        """
        change les valeurs initiales.
        """
        self.x = x
        self.a = a
        self.xinit = x
        self.ncycle = 0

    def randint(self, a0, a1, N=1):
        """retourne 'N' valeurs entre a0 et a1"""
        if a1 < a0:
            a1, a0 = a0, a1
        if N == 1:
            return (self.seq() % (abs(a1-a0))) + a0
        elif N > 1:
            z = [(self.seq() % (abs(a1-a0))) + a0 for _ in range(N)]
            return z

    def entier(self, a0, a1, N=1):
        """retourne une valeur entre a0 et a1"""
        return self.randint(a0, a1, N)

    def choice(self, listeE):
        """choisit une valeur de la liste E

        Cette méthode permet de guider les choix (cf SoleilBlanc/melos_1):
        au lieu de calculer un longue série de valeurs on peut
        faire choisir soit dans une liste assez courte (donc un choix
        quasi modal) ou très longues (donc un choix quasi sériel.
        """
        p = self.entier(0, len(listeE))
        return listeE[p]

    def choix_sans_repets(self, E, n):
        """tire n éléments de la liste E

        Emploi: voir 'choice'
        """
        if n == len(E):
            return E
        elif n < len(E):
            R = []
            while len(R) < n:
                x = self.choice(E)
                if x not in R:
                    R.append(x)
            return R

    def choix(self, E, n):
        """tire n éléments de la liste E

        Emploi: voir 'choice'
        """
        return [self.choice(E) for _ in range(n)]

    def battre(self, E):
        " comme battre les cartes "
        r = []
        while len(E) > 0:
            ix = self.randint(0, len(E))
            if E[ix] not in r:
                r.append(E[ix])
                del E[ix]
        return r

    def fseq(self):
        """retourne la prochaine valeur réelle."""
        x = self.seq()
        return float(x)/self.m

    def uniform(self, a0, a1, N=1):
        """retourne les N prochaines valeurs réelles (float) entre a0 et a1."""
        #assert a0 != a1, "Serie.uniform: a0 == a1"
        if a0 == a1:
            return a0
        assert N >= 1, "Serie.uniform: N < 1"
        if a1 < a0:
            a1, a0 = a0, a1
        if N == 1:
            x = self.fseq()
            return (a1 - a0) * x + a0
        elif N > 1:
            z = np.zeros(N, np.float64)
            for i in range(N):
                x = self.fseq()
                z[i] = (a1 - a0) * x + a0
            return z

    def cumuluniform(self, a0, a1, somme):
        """
        tant que somme n'est pas atteint, cumuluniform
        ajoute x tel que a0 < x <= a1
        """
        d, r = 0.0, []
        while True:
            v = self.uniform(a0, a1)
            if d + v < somme:
                r.append(v)
                d += v
            elif (d + v) > somme:
                r.append(somme - d)
                break
            elif (d + v) == somme:
                r.append(v)
                break
        return np.array(r)

    def pt(self, a1):
        "multiplie le nombre suivant par 'a1' - boff..."
        x = self.fseq()
        return a1*x

    def vunique(self, n, duree=1.0):
        "retourne un vecteur de 'n' nombres dont la somme est 'duree'"
        V = []
        for _ in range(int(n)):
            V.append(self.pt(duree))
        s = np.sum(V)
        V = np.array(V)/s
        return V * duree

    def vecteur(self, n, duree):
        """produit un vecteur de n points temporels sur duree."""
        self.xT = []
        for _ in range(int(n)):
            self.xT.append(self.pt(duree))
        self.xT.sort()
        return self.xT

    def brouillerV(self, vliste, dab, dzu):
        """ varie les valeurs 'v' de vliste en les remplaçant
        par une valeur située entre 'v-dab' et 'v+dzu'
        C'est un brouillage brut, car en général
        la somme de 'vliste' change"""
        try:
            n = vliste.size
        except AttributeError:
            n = len(vliste)
        v = np.zeros(n)
        for i in range(n):
            v[i] = self.uniform(vliste[i] - dab, vliste[i] + dzu)
        return v

    def brouiller(self, vliste, dab, dzu, tri=False):
        """ varie les valeurs 'v' de vliste en les remplaçant
        par une valeur située entre 'v-dab' et 'v+dzu'
        C'est un brouillage qui garde la somme constante"""
        if not isinstance(vliste, np.ndarray):
            a = np.array(vliste)
        else:
            a = vliste.copy()
        a = np.add.accumulate(a)
        n = a.size
        for i in range(n-1):
            a[i] = self.uniform(a[i] - dab, a[i] + dzu)
        a = self.sub(a)
        if tri:
            a.sort()
        return a

    def remplir(self, duree, vliste, dab, dzu):
        """ remplit 'duree' avec des valeurs proportionnelles
        à celles de 'vliste' mais brouillées dans l'intervalle
        (x-dab, x+dzu) """
        x = self.brouiller(vliste, dab, dzu)
        x = np.array(x)
        somme = x.sum()
        return x * duree / somme

    def bruit(self, n, xmin=-1.0, xmax=+1.0):
        "presque comme 'noise' ;-)"
        return self.uniform(xmin, xmax, n)

    def evtN(self, n=1, xmin=-1.0, xmax=+1.0):
        """ pour normaliser la nomenclature """
        return self.uniform(xmin, xmax, n)

    def evtT(self, duree=1.0, xmin=-1.0, xmax=+1.0):
        """ pour normaliser la nomenclature """
        n = int(duree * SR)
        return self.uniform(xmin, xmax, n)

    def menge(self, n):
        """
        retourne une suite de nombres de 0 à n-1
        sans répétition.
        """
        R = []
        while len(R) < n:
            x = self.randint(0, n)
            if x not in R:
                R.append(int(x))
        return R

    def ordre(self, n):
        """
        retourne une suite de nombres de 0 à n-1
        sans répétition.
        mieux que 'menge'
        """
        if not isinstance(n, int):
            print("Serie002.ordre: float(n) devient int(n)")
        n = int(n)
        r = []
        s = list(range(n))
        while len(r) < n:
            a = self.choice(s)
            if a not in r:
                r.append(a)
                s.remove(a)
                #print(s)
        return r

    def repartir(self, n):
        """ calcule tous les nombres du range(2**n), puis
        construit les strings binaires, chaque string ayant
        n """
        N = 2**n
        a = self.ordre(N)
        return [bin(x)[2:].zfill(n) for x in a]

    def noise(self, duree, xmin=-1.0, xmax=+1.0):
        "du bruit entre -1 et +1"
        n = int(SR*duree)
        return self.uniform(xmin, xmax, n)

    def bruit_decroissant(self, n, amorti):
        "du bruit amorti"
        if amorti == 1.0:
            return self.bruit(n)
        elif amorti > 1.0:
            return None
        else:
            b = np.ones(n, np.float64)
            for i in range(1, n):
                b[i] = b[i-1]*amorti
            for i in range(n):
                b[i] *= self.uniform(-1., +1.)
        return b

    def suite(self, E):
        """
        produit une permutation aleatoire des elements de E
        """
        #if not type(E) == types.ListType:
        #    E = E.tolist()
        E = list(E)
        R = []
        for _ in range(len(E)):
            indice = self.entier(0, len(E))
            R.append(E[indice])
            del E[indice]
        return R

    def suiteI(self, n, nmin, nmax):
        """retourne une suite de n nombres entre nmin et nmax,
        nmax exclu."""
        R = []
        for _ in range(n):
            R.append(self.entier(nmin, nmax))
        return R

    def suiteE(self, n, E):
        """
        retourne une suite sérielle de 'n' éléments
        de la liste 'E'.
        """
        R = []
        p = len(E)
        for _ in range(n):
            ix = self.entier(0, p)
            R.append(E[ix])
        return R

class Serie003(Serie001):
    """ quelques méthodes déplacées """
    def __init__(self, x, a, m=2**31-1, b=0, decalage=False, fnom=None):
        """initialisation
        x: élément variable
        a: multiplicateur fixe
        b: additioné fixe
        m: valeur maximum
        fnom: nom de stockage PAS ENCORE UTILISÉ
         """
        Serie001.__init__(self, x, a, m, b, decalage, fnom=fnom)
        self.xT = None
        self.ergo = 1
        self.aM = float(2**31) #2147483648
        self.aM1 = 2**31 - 1

    def ergodic(self):
        """ ergodic selon Jerzy Karczmarczuk """
        x = (self.ergo << 13) ^ self.ergo
        self.ergo = (x * (x * x * 599479 + 649657) + 1376312589) % self.aM1
        return self.ergo / self.aM

    def ergodicA(self, n, barray=True):
        " retourne un array d'ergodic "
        if barray:
            r = np.zeros(n)
            for i in range(n):
                r[i] = self.ergodic()
        else:
            r = []
            for i in range(n):
                r.append(self.ergodic())
        return r

class Serie010(Serie002):
    """ refuge pour les méthodes pas utilisées """
    def __init__(self, x=9, a=11, m=2**31-1, b=0, decalage=False, fnom=None):
        Serie002.__init__(self, x, a, m, b, decalage, fnom=fnom)
        self.xT = None

    def fseq_20130804(self):
        """retourne la prochaine valeur réelle.
        JE TROUVE QUE _ NE SERT À RIEN; """
        _ = self.seq()
        print(self.x)
        return float(self.x)/self.m

    def __call__(self, a0, a1, N=1):
        """
        retourne les 'N' prochaines valeurs réelles (float) entre a0 et a1.
        (identique à 'uniform')
        """
        return self.uniform(a0, a1, N)

    def hmusic(self, hm):
        """
        fournit une séquence de bruit dont la longueur en samples
        correspond à 'hm'
        """
        n = prony2samples(hm)
        return self.bruit(n)

    def brouillerK(self, vliste, coeff, tri=False, brut=True):
        """ varie les valeurs 'v' de vliste en les remplaçant
        par une valeur située entre 'v-k*v' et 'v+k*v'
        C'est un brouillage qui garde la somme constante.
        IL FAUT TESTER CETTE FONCTION POUR SAVOIR CE QU'ELLE FAIT.
        """
        if coeff >= 1.0:
            print("brouillerK: coeff coeff >= 1.0")
            return
        if not isinstance(vliste, np.ndarray):
            a = np.array(vliste)
        else:
            a = vliste.copy()
        n = a.size
        k0 = 1.0 - coeff
        k1 = 1.0 + coeff
        for i in range(n-1):
            a[i] = self.uniform(a[i] * k0, a[i] * k1)
        if brut:
            return a
        a = np.add.accumulate(a)
        n = a.size
        k0 = 1.0 - coeff
        k1 = 1.0 + coeff
        for i in range(n-1):
            a[i] = self.uniform(a[i] * k0, a[i] * k1)
        a = self.sub(a)
        if tri:
            a.sort()
        return a

    def distribution(self, xmin, xmax, nn):
        """produit un vecteur de nn nombres réels entre xmin et xmax."""
        T = []
        for _ in range(nn):
            T.append(self.uniform(xmin, xmax))
        return np.asarray(T)

    def promenade(self, n, ixini, E):
        """
        le promeneur part de 'ixini' pour faire 'n' pas
        de grandeurs donnés de 'E'.
        'n: nombre de pas
        'iini: indice de départ
        """
        pass


    def impulsions(self, duree, densite):
        """ fournit une suite d'impulsions - METTRE DANS IMPULSIONS ? """
        n = int(duree*SR)
        p = int(n*densite)
        w = np.zeros(n, np.float64)

        for _ in range(p):
            ix = self.randint(0, n)
            w[ix] = 1.0
        return w

    def __ordre(self, n):
        "ordonne les nombres (0, ..., n-1) en une suite"
        # voir communs_ka
        pass

class SerieVecteurProgressif(Serie002):
    """fournit à chaque appel un vecteur V de p valeurs ;
    V[1:] = V[:p] et V[0] = nouveau
    ou
    V[:p] = V[1:] et V[-1] = nouveau"""

    def __init__(self, p, r, x=19, a=23, m=2**31-1, b=0, decalage=False):
        """crée un générateur sériel apte à fournir un 'vecteur progressif'
        de longueur 'p'.
        """
        Serie002.__init__(self, x, a, m, b, decalage)
        self.x = x
        self.a = a
        self.b = b
        self.m = m
        self.i = 0
        self.xinit = x
        self.ncycle = 0
        self.decalage = decalage
        self.p = p - 1
        self.v = self.uniform(-1.0, +1.0, p) * r
        #print(self.v)

    def pousseD(self):
        """
        pousse le vecteur d'une case vers la droite et ajoute
        une nouvelle valeur en tête.
        """
        self.v[1:] = copy.copy(self.v[:self.p])
        self.v[0] = self.uniform(-1., +1.)
        return self.v

    def shiftR(self, r=1.):
        """
        pousse le vecteur d'une case vers la droite et ajoute
        une nouvelle valeur 'y' en queue telle que '-r < y < +r'
        """
        self.v[1:] = copy.copy(self.v[:self.p])
        self.v[0] = self.uniform(-1., +1.) * r
        return self.v

    def pousseG(self):
        """
        pousse le vecteur d'une case vers la gauche et ajoute
        une nouvelle valeur en queue.
        """
        self.v[:self.p] = copy.copy(self.v[1:])
        self.v[-1] = self.uniform(-1., +1.)
        return self.v

    def shiftL(self, r=1.):
        """
        pousse le vecteur d'une case vers la gauche et ajoute
        une nouvelle valeur 'y' en queue telle que '-r < y < +r'
        """
        self.v[:self.p] = copy.copy(self.v[1:])
        self.v[-1] = self.uniform(-1., +1.) * r
        return self.v

class Serie005(OrigineStr):
    """ pour utiliser plusieurs versions différentes """
    def __init__(self, a0, a1, alea):
        OrigineStr.__init__(self)
        self.alea = alea
        self.a0, self.a1 = a0, a1
        self.i = -1
        self.x1 = self.alea.uniform(self.a0, self.a1)
        self.x0 = self.alea.uniform(self.a0, self.a1)

    def evt(self, borne):
        """
        if i % borne == 0:
            x_i = uniform(...)
        else:
            x_i = 0.5 * (x_i-1 + x_i-2
        """
        self.i += 1
        if self.i % borne == 0:
            x = self.alea.uniform(self.a0, self.a1)
            self.x0 = self.x1
            self.x1 = x
            return x
        else:
            x = (self.x0 + self.x1) * 0.5
            self.x0 = self.x1
            self.x1 = x
            return x

    def evtSinus(self, borne, k):
        """
        if i % borne == 0:
            x_i = uniform(...)
        else:
            x_i = 0.5 * (x_i-1 + x_i-2
        """
        self.i += 1
        if self.i % borne == 0:
            x = self.alea.uniform(self.a0, self.a1)
            self.x0 = self.x1
            self.x1 = x
            return x
        else:
            x = k * self.x1 - self.x0
            self.x0 = self.x1
            self.x1 = x
            return x

    def evtDecay(self, borne, ratio):
        """
        if i % borne == 0:
            x_i = uniform(...)
        else:
            x_i = 0.5 * (x_i-1 + x_i-2)
        """
        self.i += 1
        if self.i % borne == 0:
            x = self.alea.uniform(self.a0, self.a1)
            self.x0 = self.x1
            self.x1 = x
            return x
        else:
            x = self.x0 * ratio
            self.x0 = self.x1
            self.x1 = x
            return x
