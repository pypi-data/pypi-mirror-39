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
# Groupes/Flutes/cfloeten.py

"""timbres de flûte avec portamento, trilles et autres fariboles;
"""

import numpy as np
from samplerate import SR
from conversions import prony2freq
import serie
from ondepartable import ondeTable
from Outils.ajuster import prolongerN
from canal import CanalMono
from Structures.portamento import Portamento
from profilbase import ProfilBase
from profils import recta, cubica
from origine import OrigineStr


__author__ = "Copyright (c) 2005 René Bastian (Wissembourg, FRANCE)"
__date__ = "2006.08.17, 2013.08.03, 2015.07.01"

__all__ = ["FloeteMono", "FloeteStereo"]

class FloeteMono(OrigineStr):
    """
    semble correct de 36.0 à 100.0
    bien à partir de 55.0
    """
    def __init__(self, pflute=None, alea=None):
        """
        timbre de flûte sans panorama
        """
        OrigineStr.__init__(self)
        if pflute is None:
            pflute = [[cubica, 1./5, 0.0, 0.0, 1.0, 0.0],
                      [cubica, 1./4, 1.0, 0.0, -1.0, 0.0],
                      [cubica, 1./3, -1.0, 0.0, 0.0, 0.0]]
        self.g = Portamento(1./11)
        self.table_flute = ProfilBase(pflute).temps(1.0)
        if alea is None:
            self.alea = serie.Serie002(75663, 12983)
        else:
            self.alea = alea

    def evt(self, penveloppe, *listeParams):
        """
        'penveloppe : enveloppe finale du son
        'listeParams : duree, dt, listeTons
        'duree : durée d'une note
        'dt : durée de l'intervalle de temps entre deux notes
        'listeTons : liste de tons
        """
        env = ProfilBase(penveloppe)
        mf = np.array([])
        for params in listeParams:
            duree, dt, listeTons = params
            mf = np.concatenate((mf, self.g.traitL(duree, dt, listeTons)))
        w = ondeTable(self.table_flute, mf)
        n = w.size
        env = env.samples(n)
        w, env = prolongerN((w, env))
        w = w * env
        return w

    def __call__(self, penveloppe, *listeParams):
        " comme evt "
        return self.evt(penveloppe, *listeParams)

    def tonvibre(self, duree, varHauteur, Enveloppe,
                 ModFreqVib, ModAmpliFreqVib, rapport):
        """ ajoute un vibrato à la méthode 'ton'
        'ModFreqVib' : modulation de la fréquence du vibrato,
        'ModAmpliFreqVib' : modulation de l'amplitude
        'rapport' : rapport entre part vibrée/part non vibrée du son """
        #print(varHauteur)
        n = int(duree * SR)
        mf = self.vib.samplesH(n, varHauteur,
                               ModFreqVib, ModAmpliFreqVib, rapport)
        #prony2freq(ProfilBase(varHauteur).temps(duree))
        w = ondeTable(self.table_flute, mf)
        n = len(w)
        env = ProfilBase(Enveloppe).samples(n)
        w = w * env
        n = len(w)+1
        z = np.zeros(n, np.float64)
        for i in range(1, n):
            z[i] = (w[i-1] + w[i-2]) / 2
        return z

    def ton(self, duree, Pronyvar, penveloppe, panorama):
        """
        'penveloppe : enveloppe finale du son
        'panorama : panorama final du son
        'Pronyvar : profil de variation de la hauteur Prony
        """
        mf = prony2freq(ProfilBase(Pronyvar).temps(duree))
        w = ondeTable(self.table_flute, mf)
        n = w.size
        env = ProfilBase(penveloppe).samples(n)

        w = w * env
        n = w.size + 1
        z = np.zeros(n, np.float64)
        for i in range(1, n):
            z[i] = (w[i-1] + w[i-2]) / 2
        pano = ProfilBase(panorama).samples(n)
        z, pano = prolongerN((z, pano))
        wg = z * pano
        wd = z * (1.0 - pano)
        return wg, wd

    def multiple(self, nsons, epaisseur, penveloppe, *listeParams):
        """ nsons, dont la hauteur varie selon des profils aléatoires
        entre le max et le min déterminés par l'épaisseur,
        sont superposés"""
        c = CanalMono()
        env = ProfilBase(penveloppe)
        mf = np.array([])
        for params in listeParams:
            duree, dt, listeTons = params
            mf = np.concatenate((mf, self.g.traitL(duree, dt, listeTons)))
        nmf = mf.size
        for _ in range(nsons):
            t0 = self.alea.uniform(0., 1.)
            y0 = self.alea.uniform(0., epaisseur)
            y1 = self.alea.uniform(0., epaisseur)
            y2 = self.alea.uniform(0., epaisseur)
            p = [[recta, t0, y0, y1],
                 [recta, 1.-t0, y1, y2]]
            v = ProfilBase(p).samples(nmf)
            mfalea = mf * (1. + v)
            w = ondeTable(self.table_flute, mfalea)
            n = w.size
            env = env.samples(n)
            w, env = prolongerN((w, env))
            w = w * env
            c.addT(0.0, w)
        return c.ex()

    def grenu(self, nsons, epaisseur, penveloppe, *listeParams):
        """
        n'est pas satisfaisant car le bruit blanc est
        superposé - l'autre essai (multiplier la mf par
        un profil sériel) n'est pas fameux non plus
        """
        c = CanalMono()
        env = ProfilBase(penveloppe)
        mf = np.array([])
        for params in listeParams:
            duree, dt, listeTons = params
            mf = np.concatenate((mf, self.g.traitL(duree, dt, listeTons)))
        #nmf = mf.size
        w0 = ondeTable(self.table_flute, mf)
        for _ in range(nsons):
            #mfalea = mf * (1. + v)
            v = self.alea.uniform(0., epaisseur, w0.size)
            w = w0 * (1. + v)
            n = w.size
            env = env.samples(n)
            w, env = prolongerN((w, env))
            w = w * env
            c.addT(0.0, w)
        return c.ex()

class FloeteStereo(FloeteMono):
    """utilisé dans 'trilles'"""
    def __call__(self, penveloppe, panorama, *listeParams):
        " voir evt "
        return self.__call__(penveloppe, panorama, *listeParams)

    def evt(self, penveloppe, panorama, *listeParams):
        """
        'duree : durée d'une note
        'dt : durée de l'intervalle de temps entre deux notes
        !! Il vaut mieux ne pas réverbérer au niveau de la génération,
        car :
        -- cela empèche de s'en servir plus tard
        -- bouffe du temps
        -- peut amener de la distorsion cachée.
        """
        env = ProfilBase(penveloppe)
        pano = ProfilBase(panorama)
        mf = np.array([])
        for params in listeParams:
            duree, dt, listeTons = params
            mf = np.concatenate((mf, self.g.traitL(duree, dt, listeTons)))
        w = ondeTable(self.table_flute, mf)
        n = w.size
        env = env.samples(n)
        pano = pano.samples(n)
        w, env, pano = prolongerN((w, env, pano))
        w = w * env
        wg = w * pano
        wd = w * (1. - pano)
        return wg, wd, w

    def tonvibre(self, duree, varHauteur, Enveloppe, Panorama,
                 ModFreqVib, ModAmpliFreqVib, rapport):
        """ ajoute un vibrato à la méthode 'ton'
        'ModFreqVib' : modulation de la fréquence du vibrato,
        'ModAmpliFreqVib' : modulation de l'amplitude
        'rapport' : rapport entre part vibrée/part non vibrée du son """
        #print(varHauteur)
        n = int(duree * SR)
        mf = self.vib.samplesH(n, varHauteur,
                               ModFreqVib, ModAmpliFreqVib, rapport)
        #prony2freq(ProfilBase(varHauteur).temps(duree))
        w = ondeTable(self.table_flute, mf)
        n = len(w)
        env = ProfilBase(Enveloppe).samples(n)
        w = w * env
        n = len(w)+1
        z = np.zeros(n, np.float64)
        for i in range(1, n):
            z[i] = (w[i-1]+w[i-2])/2
        pano = ProfilBase(Panorama).samples(n)
        z, pano = prolongerN((z, pano))
        wg = z * pano
        wd = z * (1.0 - pano)
        return wg, wd

    def reverb(self, penveloppe, panorama, *listeParams):
        """INUTILE ?
        'duree : durée d'une note
        'dt : durée de l'intervalle de temps entre deux notes
        méthode avec réverb : avec des pincettes.
        """
        env = ProfilBase(penveloppe)
        pano = ProfilBase(panorama)
        mf = np.array([])
        for params in listeParams:
            duree, dt, listeTons = params
            mf = np.concatenate((mf, self.g.traitL(duree, dt, listeTons)))
        w = ondeTable(self.table_flute, mf)
        n = w.size
        env = env.samples(n)
        pano = pano.samples(n)

        w, env, pano = prolongerN((w, env, pano))
        w = w * env
        wg = w * pano
        wd = w * (1. - pano)
        cg = CanalMono()
        cd = CanalMono()
        cg.addT(0.0, wg)
        cd.addT(0.0, wd)
        #dureeRev = 2.0
        #dureeRev = 1.5
        #dtRev = dt*5 #2
        #cg.autoreverb(0.125, dureeRev, dtRev, 3*dtRev)
        #cd.autoreverb(0.125, dureeRev, dtRev, 3*dtRev)
        print("reverb: ajouter la reverb !!!!")
        return cg.a, cd.a
