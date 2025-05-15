import matplotlib.pyplot as plt
import numpy as np
import time

NB_BITS  = 2
NB_POS   = NB_BITS * NB_BITS 
POS_BITS = {"0b0":0, 
            "0b1":1, 
            "0b10":2, 
            "0b11":3
           }
TS = 0.5 # secondes - durée d'un signal i.e. Temps par Symbole
TE = TS / NB_POS

liste_t = []
debut = 0

def lettre_vers_chunks(lettre):
    return list(map(bin, [(ord(lettre) >> 2*x) & 3 for x in range(4)]))

def texte_vers_chunks(s):
    res = []
    for char in s:
        res += lettre_vers_chunks(char)

    return res

def sync_debut():
    pass

def sync_fin():
    pass

def emit(dst, liste_2_bits): 
    debut = time.perf_counter()
    sync_debut()
    for chunk in liste_2_bits:
        chrono = time.perf_counter()
        pos = POS_BITS[chunk]
        for i in range(NB_POS):
            if i == pos:
                dst.append(1)
                liste_t.append(chrono - debut)
                print(1) 
            else:
                dst.append(0)
                liste_t.append(chrono - debut)
                print(0)
            t = time.perf_counter()
            while t - chrono < TE:
                t = time.perf_counter()
            chrono = t 
    sync_fin()

def main():
    texte = "abc"
    plotlist = []
    chunk_list = texte_vers_chunks(texte)
    emit(plotlist, chunk_list)
    #afficher(plotlist)
    afficher2(plotlist)

def afficher(src):
    fig, ax = plt.subplots()
    
    plt.plot([TE * x for x in range(len(src))], src)
    plt.draw()

    xmin, xmax = ax.get_xlim()

    major_ticks = [int(xmin - TS) + TS * x for x in range(int((xmax - xmin) / TS))]
    minor_ticks  = [int(xmin - TE) + TE * x for x in range(int((xmax - xmin) / TE))]

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)

    ax.grid(which='major', color='lightgrey', linestyle='-', linewidth=1)
    ax.grid(which='minor', color='lightgrey', linestyle=':', linewidth=0.5)

    
    plt.show()

def afficher2(src):
    fig, ax = plt.subplots()

    plt.plot(liste_t, src)
    plt.draw()

    xmin, xmax = ax.get_xlim()
    major_ticks = [int(xmin - TS) + TS * x for x in range(int((xmax - xmin) / TS) + 1)]
    minor_ticks  = [int(xmin - TE) + TE * x for x in range(int((xmax - xmin) / TE))]

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)

    ax.grid(which='major', color='lightgrey', linestyle='-', linewidth=1)
    ax.grid(which='minor', color='lightgrey', linestyle=':', linewidth=0.5)

    
    plt.show()


main()

