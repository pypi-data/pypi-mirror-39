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
# :~/pythoneon/Profils profils2.py

"""fournit quelques méthodes pour la mise en forme de profils
la fonction 'profilnormaliseN' est la même que celle de
profils4.py """

__author__ = "Copyright (c) René Bastian <rbastian@free.fr>"
__date__ = "2006.02.04, 08.01.19, 08.02.05, 2011.05.23, 2012.05.28"

def transtype(xp):
    """ transtype tous les tuples en listes """
    r = []
    for p in  xp:
        r.append(list(p))
    return r

def profilnormalise(profilP, somme=1.0):
    """un profil de durée quelconque est ramené à une duréé
    donnée par 'somme'.
    'profilP' : profil-liste avec des durées absolues;
    retourne un profil-liste.

    La présence de parties fixes m'& amené un temps à adopter le choix
    de laisser ces parties fixes en dehors du recalcul,
    mais il faut revenir à l'intégration sans cela on
    obtient des profils amputés.
    En passant à numpy, j'ai eu des ennuis.
    21.06.04, 12.07.05, 27.07.07, 7.01.08, 13.05.08., 9.02.09

    utilisé dans ProfilBase
    Le transtypage a été ajouté le 3.07.2012"""
    profilP = transtype(profilP)
    if somme <= 0.0:
        print("profils2.profilnormalise: somme <= 0:", somme)
        print(profilP)
        return None
    sm, sf = 0.0, 0.0
    for p in profilP:
        try:
            sm += p[1]
        except TypeError:
            raise SyntaxError("profilnormalise:erreur dans " + str(profilP))
        except IndexError:
            sf += p[1][0]

    rapport = (somme-sf)/sm
    #print(somme, sf, sm, rapport)
    R = []
    for a in profilP:
        if isinstance(a[1], (int, float)):
            #print("profils2.profilnormalise.valeur : duree", a[1])
            p = [a[0], a[1]*rapport] + a[2:]
            R.append(p)
        elif isinstance(a[1], tuple) and (len(a[1]) == 1):
            R.append([a[0], a[1][0]] + a[2:])
            #print("profils2.profilnormalise.tuple : duree", a[1])
        elif isinstance(a[1], tuple) and (len(a[1]) > 1):
            print("profilnormalise:", profilP, somme)
            print("profilP contient un tuple non normalisable.")
        else:
            print("profils2.profilnormalise:type(a[1])", type(a[1]))
    return R

