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
#Partition/partition.py
"""fournit la classe Partition qui a les avantages
de la partition traditionnelle : flexibilité du temps.

Les modules 'partition12.py' et 'v0-...'
comprennent quelques anciennes méthodes.
Voir aussi exppartition.py -- à développer ?

Les méthodes 'montageX' pourraient être remplacés par des méthodes de la
classe 'Enregistreur' ?
"""

import os
import subprocess
import numpy as np
from samplerate import SR
#from ajuster import
from origine import OrigineStr
from conversions import extremum
from Canal.canal import (CanalMono, record)
from enregistrer import Enregistreur
from fusionner import fusionner
from Profils.profilbase import ProfilBase
#from ajuster import (prolongerZ)
from profils import (affprofil)
#from raw2wav import raw2wav
#from ajuster import prolongerZ fprolongerZ

__author__ = "Copyright (c) 2006-2014 René Bastian (Wissembourg, FRANCE)"
__date__ = """2006.05.08, 07.08.24, 09.10.05, 2010.06.12, 2014.03.19,
           2014.12.10, 2017.02.08, 2018.10.12"""

def calculExtremum(*signals):
    """retourne l'extremum des signaux"""
    mx = 0.0
    for sig in signals:
        mx = max(mx, extremum(sig))
    return mx

def calculdurees(listefichiers, nomrec=None, btempsrelatif=True):
    """ évalue les durées des fichiers 'f64' de la liste
    listefichiers : liste des fichiers à évaluer
    nomrec : nom du fichier pour la sauverage de l'évaluation
    btempsrelatif=True : l'évaluation est destinée à
          un montage en temps relatif"""
    maxl = 0
    for nom in listefichiers:
        maxl = max(maxl, len(nom))
    #print(maxl)
    maxl += 2
    sformat = "(%-" + str(maxl) + "s, %8.3f,        %8.3f,   1.0),"
    #print(sformat)
    r = []
    dureeprec = 0.0
    for nom in listefichiers:
        nomr = nom + ".0f64"
        n = os.stat(nomr).st_size
        duree = float(n)/(SR * 8)
        nom = '"' + nom + '"'
        if btempsrelatif:
            r.append(sformat % (nom, duree, dureeprec))
            dureeprec = duree
        else:
            r.append(sformat % (nom, duree, dureeprec))
    if nomrec is None:
        print(r)
    else:
        s = "\n".join(r)
        f = open(nomrec, "w")
        f.write(s)
        f.close(amorti=1.0)

class Multi(OrigineStr):
    """ installe un enregistreur multipistes; chaque piste
    est une instance de 'Enregistreur'.
    Compile une séquence de 1200 sec en env 600 sec.
    """
    def __init__(self, nomsouche, npistes, dureeInitiale=1.0,
                 nouveau=True):
        """
        'nomsouche' : nom générique pour les fichiers
        'npistes' : nombre de pistes
        'nouveau' :
            si True, l'existant est effacé
            si False, les signaux sont ajoutés à l'existant
        """
        OrigineStr.__init__(self)
        self.pistes = []
        for i in range(npistes):
            fnom = "".join([nomsouche, ".", str(i), "f64"])
            f = Enregistreur(fnom, dureeInitiale, nouveau)
            self.pistes.append(f)
        self.ext = 0
        self.npistes = npistes
        self.nomsouche = nomsouche

    def ajouter(self, pt, ncanal, signal):
        """ ajoute le 'signal' au point temporel 'pt' dans le
        canal 'ncanal'.
        """
        try:
            self.pistes[ncanal].ajouter(signal, pt)
        except IndexError:
            print("Partition.ajouter", "canal", ncanal)

    def close(self):
        """
        clôt toutes les pistes ouvertes
        """
        for f in self.pistes:
            f.close()

    def fusion(self, amorti=1.0):
        """ lit les fichiers 'self.nomsouche'+".?f64" et les réunit en un
        fichier 'self.nomsouche'+".raw".
        'amorti' : prévu pour adapter le signal s'il y a des dépassements. """
        assert amorti == 1.0
        self.close()
        v = fusionner(self.nomsouche, self.npistes)
        return v

class Partition(OrigineStr):
    """classe permettant des opérations comparables à celles
    qui sont possibles avec une partition de musique habituelle."""
    def __init__(self, nomsouche, npistes, dureeInitiale=1.0, binformer=False,
                 nouveau=True, texte=None, titre=None):
        """
        'u' : unité (tempo)
        'tempo' : tempo (None si tempo fixe, fonction si tempovariable)
        'tempovar' : True si tempovariable
        't' : point temporel
        'npistes' : nombre de canaux
        'nomsouche' : nom des fichiers à réaliser
        'nouveau' :
            si True, l'existant est effacé
            si False, les signaux sont ajoutés à l'existant
        'texte' : destiné à être un nom de fichier-texte
          pour recueillir des données.
        """
        OrigineStr.__init__(self)
        self.u = 1.0
        self.tempo = None
        self.pt0 = 0.0
        self.nomsouche = nomsouche
        self.npistes = npistes
        self.converti = False
        self.collecteur = Multi(nomsouche, npistes, dureeInitiale, nouveau)
                                #binfo=binformer)
        self.t = 0.0
        # attributs obsolètes ou non utilisés
        self.informer = binformer
        self.titre = titre
        self.texte = texte
#        try:
#            self.texte = open(texte, "w")
#        except TypeError:


    def unit(self, u):
        """attribue la valeur u à l'unité de temps self.u."""
        self.u = u

    @staticmethod
    def chrono(M, isforme=0, rfile=None):
        """ établit la liste chronologique des ingrédients
        M = (fichier_64, ecart, ampli)
        R = (ampli, ecart, duree, pt, pthoraire, nomfichier)
        La liste 'sformes' peut être complétée par d'autres formes.
        """
        pt = 0.0
        R = []
        sformes = ["a %6.2f e %5.2f d %6.2f pt %8.3f %8.3f %3i:%5.2f %s"]
        sforme = sformes[isforme]
        print(sforme)
        for fnom, ecart, ampli in M:
            v = np.fromfile(fnom + ".0f64")
            duree = float(v.size) / SR
            rnom = fnom.split("/")[-1]
            pt += ecart
            minute = int(pt / 60.0)
            sec = pt - (minute * 60)
            r = sforme % (ampli, ecart, duree, pt, pt + duree,
                          minute, sec, rnom)
            #print(r)
            R.append(r)
        s = "\n".join(R)
        if rfile is None:
            print(s)
        else:
            open(rfile, "w").write(s)

    def pt(self, xt):
        "donne un nouveau point temporel absolu"
        if self.tempo != None:
            self.u = self.tempo(self.pt0 - self.t)
        self.t = xt * self.u

    def ptx(self):
        """
        retourne la valeur du point temporel
        """
        return self.t

    def dr(self, ecart):
        """fixe le prochain point temporel en additiont 'ecart'
        au point temporel actuel."""
        if self.tempo != None:
            self.u = self.tempo(self.pt0 - self.t)
        self.t += ecart * self.u

    def ecart(self, xecart):
        "comme 'dr'"
        if self.tempo != None:
            self.u = self.tempo(self.pt0 - self.t)
        self.t += xecart * self.u

    def ftempo(self, pt0, f):
        "attribue la fonction f au tempo pour calculer un tempo variable"
        self.pt0 = pt0
        self.tempo = f

    def vtempo(self, f):
        "attribue la fonction f au tempo pour calculer un tempo variable"
        self.tempo = f

    def dimension(self):
        "retourne la durée actuelle de la partition"
        nom = self.nomsouche + ".0f64"
        return os.stat(nom).st_size/8

    def evt(self, *signals):
        """placement des signaux : 'signals' est une liste de signaux,
        chaque 'signals' correspond à un haut-parleur.
        """
        forme = "%s : u %8.3f t %8.3f ampli %8.3f"
        try:
            for i, signal in enumerate(signals):
                #if not isinstance(signal, np.ndarray):
                #    print(len(signal))
                #else:
                #    print("signal", signal.size)
                if signal is None:
                    pass
                else:
                    self.collecteur.ajouter(self.t, i, signal)
            #for i in range(len(signals)):
             #   self.collecteur.ajouter(self.t, i, signals[i])
        except IOError:
            print("Partition.evt: pas de signal")
            return
        self.kt(*signals)
        if self.informer:
            mx = calculExtremum(signals)
            print(forme % (self.titre, self.u, self.t, mx))

    def insert(self, souche, ampli=1.0, info=True):
        """
        ajoute le son "fnom.Xf64" au point actuel
        """
        if info:
            print("%-15s %5.2f %11.3f" % (souche, ampli, self.t),)
        r = []
        for ncanal in range(self.npistes):
            nomf = "".join([souche, ".", str(ncanal), "f64"])
            w = np.fromfile(nomf, np.float64)
            w *= ampli
            r.append(w)
        self.evt(*r)

    def kt(self, *signals):
        """
        affiche unité et point temporel actuels
        """
        if not signals:
            print("u %8.3f t %8.3f" % (self.u, self.t))
        else:
            d = 0
            for sig in signals:
                if sig is None:
                    pass
                else:
                    d = max(d, sig.size)
            tz = float(d) / SR
            minutes = int(self.t / 60.)
            secondes = self.t - minutes * 60
            print("u %8.3f t %8.3f + %8.3f -> %8.3f" % \
                (self.u, self.t, tz, self.t+tz))
            print("pt %2i:%5.2f" % (minutes, secondes))

    def close(self, amorti=1.0, bwav=True):
        """
        écrit le fichier raw & le fichier wav ;
        efface (ad lib.) les f64
        """
        self.collecteur.fusion(amorti=amorti)
        if bwav:
            comm = " ".join(("sox", "-c"+str(self.npistes),
                             "-e signed-integer",
                             "-r"+str(SR), "-b16",
                             self.nomsouche+".raw",
                             "w"+self.nomsouche+".wav"))
            subprocess.call(comm, shell=True)
        #raw2wav(self.nomsouche + ".raw") # ne marche pas
        #if self.texte is not None:
        #    self.texte.close()

    def ajouter(self, sg, sd, xt):
        """
        ajouter 'sg, sd' au point temporel 't'
        """
        self.pt(xt)
        self.evt((sg, sd))

    def montage1to2sur4(self, instructions): #, binfo=False):
        """ un 'fichier f64' est lu, le segment allant de xt0 à
        xt1 est inséré au 'pt+decalage'
        pour aller du 'canalini' au 'canalfin' avec 'ampli',
        selon 'ppano' et 'pprofil'; instr =
        (fnom, xt0, xt1, pt, decalage, pprofil, cini, cfin, ampli, ppano)
        """
        for instr in instructions:
            fnom, xt0, xt1, pt0, decalage, pprofil, cini, cfin, ampli, \
                ppano = instr
            w0 = np.fromfile(fnom)
            pt = pt0 + decalage
            n0 = int(xt0 * SR)
            n1 = int(xt1 * SR)
            if n0 < n1:
                w = w0[n0:n1]
            else:
                w = w0[n0:n1][::-1]
            n = w.size
            profil = ProfilBase(pprofil).samples(n)
            w *= profil * ampli
            panoini = ProfilBase(ppano).samples(n)
            w1 = w * panoini
            w2 = w * (1.0 - panoini)
            self.collecteur.ajouter(pt, cini, w1)
            self.collecteur.ajouter(pt, cfin, w2)

    def montage1toN(self, instructions, binfo=False):
        """ insère les fichiers f64 aux points temporels donnés
        avec l'amplitude ou le profil donnée à partir d'un fichier
        mono.
        Syntaxe : (souche, ptref, decalage, ampli0, ampli1, ...)"""

        def affinstr(n, instr):
            " affiche l'instruction "
            nom, pt, decalage = instr[0:3]
            try:
                print("n", "%4i" % (n), nom,
                      "%8.3f %8.3f" % (pt, decalage))
            except TypeError:
                pass
            for x in instr[3:]:
                if isinstance(x, float):
                    print("%8.3f" % x, end=" ")
                else:
                    try:
                        affprofil(x)
                    except TypeError:
                        pass
        print("-" * 12)
        #(nomf, pt, 0.0, (0.0, []), (2.0, [[recta, 1.0, 1.0, 0.0]]),
        # (0.0, []), (0.0, []))
        for i, instr in enumerate(instructions):
            if binfo:
                affinstr(i, instr)
                print()
            #print(i, "**", instr)
            #print(nomf)
            r = []
            nomf = instr[0]
            w = np.fromfile(nomf, dtype=float)
            print("w.size", w.size)
            self.pt(instr[1] + instr[2])
            #print(self.pt, end = " *")

            #for ncanal, x in enumerate(instr[3:]):
            for x in instr[3:]:
                if len(instr[3:]) != self.npistes:
                    print("Partition:montage12N - nombre de pistes incohérent")
                    print("self.npistes", self.npistes, "!=", len(instr[3:]))
                    return
                if x == (0.0, []):
                    wx = None
                else:
                    ampli, relief = x
                    vrelief = ProfilBase(relief).samples(w.size)
                    wx = w * vrelief * ampli
                #        elif isinstance(relief, np.ndarray):
                #            # UNE ESQUISSE
                #            prolongerZ(relief, w)
                #            wx = relief * w
                #        else:
                #            print("Partition.montage1toN:")
                #            print("incohérence", ampli, relief)
                r.append(wx)
                self.evt(*r)

    def montageMonotoN(self, instructions):
        " doublon "
        return self.montage1toN(instructions)

    def montage2toN(self, instructions):
        """ insère les fichiers f64 aux points temporels donnés
        avec l'amplitude donnée; permet d'utiliser des fichiers
        stéréo.
        Syntaxe : (souche, ptref, decalage, ampli, canalini, canalfin)"""
        for instr in instructions:
            souche, ptref, decal, ampli, ncanal0, ncanal1 = instr
            nomf = "".join([souche, ".0f64"])
            w0 = np.fromfile(nomf, np.float64)
            w0 *= ampli
            nomf = "".join([souche, ".1f64"])
            w1 = np.fromfile(nomf, np.float64)
            w1 *= ampli
            self.pt(ptref + decal)
            self.collecteur.ajouter(self.t, ncanal0, w0)
            self.collecteur.ajouter(self.t, ncanal1, w1)

    def montage(self, instructions, deltapt=0.0):
        """ insère les fichiers f64 aux points temporels donnés
        avec l'amplitude donnée
        Syntaxe : (souche, pt, ampli)"""
        for instr in instructions:
            r = []
            souche, pt, ampli = instr
            for ncanal in range(self.npistes):
                nomf = "".join([souche, ".", str(ncanal), "f64"])
                w = np.fromfile(nomf, np.float64)
                w *= ampli
                print(nomf, w.max())
                #if ncanal == 0:
                #    print("%25s" % (souche))
                r.append(w)
            self.pt(pt + deltapt)
            self.evt(*r)

    def montageCanal(self, instructions):
        """ insère les fichiers f64 aux points temporels donnés
        avec l'amplitude donnée """
        cg, cd = CanalMono(), CanalMono()
        for instr in instructions:
            souche, pt, ampli = instr
            print(souche, pt, ampli)
            nomf = souche + ".0f64"
            wg = np.fromfile(nomf, np.float64)
            wg *= ampli
            nomf = souche + ".1f64"
            wd = np.fromfile(nomf, np.float64)
            wd *= ampli
            cg.addT(pt, wg)
            cd.addT(pt, wd)
        record(cg.a, cd.a, self.nomsouche)

    def montage_(self, instructions, binfo=False):
        """effectue les instructions
        version particulière pour stéréo
        """
        for instr in instructions:
            souche, pt, ampli = instr
            nomf = "".join([souche, ".", "0f64"])
            wg = np.fromfile(nomf, np.float64)
            wg *= ampli
            try:
                nomf = "".join([souche, ".", "1f64"])
                wd = np.fromfile(nomf, np.float64)
            except FileNotFoundError:
                nomf = "".join([souche, ".", "0f64"])
                wd = np.fromfile(nomf, np.float64)
            wd *= ampli
            if binfo:
                print("extremum", extremum(wg), extremum(wd))
            self.pt(pt)
            self.evt(wg, wd)

    def montage_ecart_simple(self, instructions, pt=0.0):
        " alias "
        return self.montage_ecarts(instructions, pt)

    def montage_ecarts(self, instructions, pt=0.0):
        """effectue le montage par écarts;
        Syntaxe:
            (souche, ecart, ampli)
            (souche, ecart, ampli, ptdebut, duree, penv)"""
        self.pt(pt)
        for instr in instructions:
            r = []
            if len(instr) == 3:
                for ncanal in range(self.npistes):
                    souche, ecart, ampli = instr
                    if ncanal == 0:
                        print("%25s" % (souche))
                    nomf = "".join([souche, ".", str(ncanal), "f64"])
                    w = np.fromfile(nomf, np.float64)
                    w *= ampli
                    r.append(w)
            elif len(instr) == 6:
                souche, ecart, ampli, ptdebut, duree, penv = instr
                npt = int(ptdebut * SR)
                empan = int(duree * SR)
                for ncanal in range(self.npistes):
                    if ncanal == 0:
                        print("%25s" % (souche))
                    nomf = "".join([souche, ".", str(ncanal), "f64"])
                    w0 = np.fromfile(nomf, np.float64)
                    if npt > w0.size or npt+empan > w0.size:
                        print("Partition.montage:", instr)
                        print("pt ou duree hors limites")
                        return
                    w = w0[npt : npt + empan]
                    env = ProfilBase(penv).samples(w.size)
                    env /= extremum(env)
                    w *= ampli * env
                    r.append(w)
            self.dr(ecart)
            self.evt(*r)

    def montage_duree_ecart(self, instructions, pt=0.0):
        """effectue le montage par écarts:
        (souche, duree, ecart, ampli)
        Les durées ne sont pas nécessaires à la compilation
        mais facilitent l'écriture (pas toujours:)"""
        self.pt(pt)
        for instr in instructions:
            r = []
            for ncanal in range(self.npistes):
                souche, duree, ecart, ampli = instr
                if ncanal == 0:
                    print("%25s %7.2f" % (souche, duree))
                nomf = "".join([souche, ".", str(ncanal), "f64"])
                w = np.fromfile(nomf, np.float64)
                w *= ampli
                r.append(w)
            self.dr(ecart)
            self.evt(*r)
