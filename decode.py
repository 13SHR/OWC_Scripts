import matplotlib.pyplot as plt
import numpy as np
import time
import os 

NB_BITS  = 2
NB_POS   = 4
POS_BITS = [0, 1, 2, 3]


def symbole_vers_chunk(liste, i, start):
    res = 0
    for j in range(4):
        res += int(liste[start + j]) * POS_BITS[j] << 2*i
    return res
    

def pos_liste_vers_fichier(liste, fout, n):
    b = 0
    i = 0
    count = 0
    bytelist = []
    while count < n:
        b += symbole_vers_chunk(liste, i, count<<2)
        i += 1
        count += 1
        if i == 4:
            i = 0
            bytelist.append(b) 
            b = 0
            if count % 800 == 0:
                print(f"{count>>3} octets décodés")
    fout.write(bytes(bytelist))

def main():
    filename = "sample.txt"
    with open(filename, "r") as f:
        l = f.read().splitlines()
    length = os.path.getsize(filename)
    with open("output.png", "wb") as fout:
        pos_liste_vers_fichier(l, fout, length>>3)

main()
