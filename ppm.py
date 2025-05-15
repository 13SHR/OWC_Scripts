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
TS = 0.00001 # secondes - durée d'un signal i.e. Temps par Symbole
TE = TS / NB_POS

def hex_vers_chunks(char):
    return list(map(bin, [(char >> 2*x) & 3 for x in range(4)]))

def texte_vers_chunks(s):
    res = []
    for char in s:
        res += hex_vers_chunks(char)

    return res

def sync_debut():
    pass

def sync_fin():
    pass

def emit(liste_2_bits, fout): 
    sync_debut()
    for chunk in liste_2_bits:
        chrono = time.perf_counter()
        pos = POS_BITS[chunk]
        for i in range(NB_POS):
            if i == pos:
                fout.write("1\n")
            else:
                fout.write("0\n")
            t = time.perf_counter()
            while t - chrono < TE:
                t = time.perf_counter()
            chrono = t 
    sync_fin()

def main():
    with open("input.png", "rb") as fin:
        texte = fin.read()
    chunk_list = texte_vers_chunks(texte)
    with open("sample.txt", "w") as fout:
        emit(chunk_list, fout)


main()

