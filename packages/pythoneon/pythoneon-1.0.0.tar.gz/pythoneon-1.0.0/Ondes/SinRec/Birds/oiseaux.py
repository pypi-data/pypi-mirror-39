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
# Ondes/SinRec/Birds/oiseaux.py

"""
Les originaux se trouvent dans 'bird.ins'
et un test dans 'bird.clm' dans le CLM de Bill Schottstaedt.
"""
from samplerate import SR
from profilbase import ProfilBase
from sinusrecursif import sinrec
from canal import CanalMono

__author__ = "Copyright (c) 2012 René Bastian (Wissembourg, FRANCE)"
__date__ = "2012.03.26"

def bigbird(dur, frequency, freqSkew, amplitude, freqEnvelope, ampEnvelope,
            partials):
    """
    C'est la fonction 'bird' avec des harmoniques.
    'partials' : [(nharmonique, amplitude), (nharmonique, amplitude), ...]
    Le python a été transcrit à partir de 'bird.clm' de Bill Schottstaedt.
    'sinrec' est l'équivalent de 'oscil'.
    """
    c = CanalMono(dur)
    n = int(SR * dur)
    freqE = ProfilBase(freqEnvelope).samples(n) * freqSkew
    freqE += frequency
    for nharm, ampliharm in partials:
        rfreq = freqE * nharm
        w = sinrec(rfreq) * ampliharm
        c.addT(0.0, w)
    ampEnv = ProfilBase(ampEnvelope).samples(w.size)
    ampEnv *= amplitude
    c.a *= ampEnv
    return c.a

def bird(dur, frequency, freqSkew, amplitude, freqEnvelope, ampEnvelope):
    """
    'freqEnvelope' est le profil qui dessine l'évolution de la fréquence,
    'freqSkew' est le multiplicateur qui détermine le débattement
             de la variation de fréquence autour de la
             fréquence moyenne donnée par 'frequency'
    'ampEnvelope' est le profil d'amplitude multiplié par 'amplitude'
             pour obtenir l'enveloppe finale.
    Le python a été transcrit à partir de 'bird.clm' de Bill Schottstaedt.
    Par rapport à l'original, il manque encore le filtrage et
    la réverb, mais je préfère que ces traitements restent externes.
    """
    n = int(SR * dur)
    freqE = ProfilBase(freqEnvelope).samples(n) * freqSkew
    freqE += frequency
    w = sinrec(freqE)
    ampEnv = ProfilBase(ampEnvelope).samples(w.size)
    ampEnv *= amplitude
    w *= ampEnv
    return w

