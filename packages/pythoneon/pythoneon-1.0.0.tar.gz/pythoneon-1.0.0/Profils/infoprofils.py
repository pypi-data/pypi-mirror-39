#-*-coding:utf-8-*-
# infoprofils.py

" module pour afficher des profils "

__author__ = "Copyright (c) 2010 René Bastian (Wissembourg, FRANCE)"
__date__ = "2010.09.18, 2013.07.15"
__all__ = ["affprofil", "codeprofil"]

def affprofil(pListe, message=None):
    " affiche le profil sous forme lisible"
    if message is not None:
        print(message)
    for p in pListe:
        r = [str(p[0]).split(" ")[1]]
        for x in p[1:]:
            try:
                r.append("%9.3f" % (x))
            except TypeError:
                r.append(str(x))
        s = " ".join(r)
        print(s)

def codeprofil(pListe, message=None):
    " le profil pListe est affiché en code Python réutilisable"
    if message is not None:
        print(message)
    rr = ["["]
    for p in pListe:
        r = [" [", str(p[0]).split(" ")[1] + ","]
        for x in p[1:]:
            try:
                r.append("%f," % (x))
            except TypeError:
                r.append("%-12s" % str(x))
        r.append("],")
        s = " ".join(r)
        s = s.replace(", ]", "]")
        s = s.replace("[ ", "[")
        rr.append(s)
    s = "\n".join(rr)
    s += "]"
    s = s.replace(",]", "]")
    return s
