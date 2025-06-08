import matplotlib.pyplot as plt
import numpy as np
import time
import os 

NB_BITS  = 2
NB_POS   = 2**NB_BITS
POS_BITS = range(NB_POS) # valeur de chaque position
TR       = 250  # ms, temps d'échantillonage de lecture
TS       = 1000 # ms, temps par symbole lors de l'émission
TE       = TS / NB_POS # temps par position

# Nombre d'acquisitions que le pico a effectué par position
NB_ECH_PAR_POS = int(TE/TR) 

# Convertit les NB_POS * NB_ECH_PAR_POS positions indiquées dans liste à partir de start
# en le nombre associé. Le résultat est multiplié par 2^(2i) dans notre cas, car
# la transmission se fait par groupe de 2 bits
def pos_vers_symbole(liste, i, start):
    res = 0
    for j in range(NB_POS):
        res += int(liste[start + j]) * POS_BITS[j]
    res <<= 2
    return res
    
# Ecrit la transmission dans le fichier fout, de longueur n octets, a partir de la 
# liste des positions lues
def pos_liste_vers_fichier(liste, fout, n):
    b = 0         # Bit actuellement en décodage
    i = 0         # Indice du groupe de 2 bits en décodage dans b
    count = 0     # Nombre d'octets jusqu'ici décodés
    bytelist = [] # Liste stockant tous les bits décodés

    while count < n:
        b += pos_vers_symbole(liste, i, count<<2)
        i += 1
        count += 1

        # Si le bit est comp, on l'ajoute à la liste puis le réinitialise
        if i == 4: 
            bytelist.append(b) 
            b = 0
            i = 0
    fout.write(bytes(bytelist))

# Recherche le signal de début de transmission dans l
# Ici, ce signal est consiste à mettre les 4 positions à haut pendant 
# un temps de symbole
def cherche_debut(l):
    n = NB_ECH_PAR_POS * 4
    nb_uns  = 0
    for i in range(n):
        if l[i] == 1:
            nb_uns += 1 
    if nb_uns == n:
        return n
    for i, item in enumerate(l[n::]):
        if l[i] == 1: # l[i] est en fait la n-ieme case avant celle de item
            nb_uns -=1
        i+=1

        if item == 1:
            nb_uns += 1
        
        if nb_uns == n:
            return i+n

# Recherche le signal de fin de transmission dans l
# Ici, il est similaire à celui de début
def cherche_fin(l):
    return cherche_debut(l)

# Lit le fichier fin pour en extraire la liste de positions, 
# puis enregister le résultat dans fout
def lire_fichier(fin, fout):
    n = NB_ECH_PAR_POS * 4
    l = fin.readlines()
    start = cherche_debut(l)
    end = cherche_fin(l[start::]) + start
    pos_list_ver_fichier(l[start:end:], fout, end - start)

def main():
    filename = "buffer"
    with open(filename, "r", 1) as fin: # 1: Line-buffered
        with open("output", "wb") as fout:
            lire_fichier(fin, fout)

main()

def test_recherche():
    NB_ECH_PAR_POS = 1
    n = 4 * NB_ECH_PAR_POS
    assert(cherche_debut([1, 1, 1, 1, 1]) == 4)
    assert(cherche_debut([0, 1, 1, 1, 1]) == 5)

    l = [0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]
    start = cherche_debut(l)
    end   = cherche_fin(l[start+4::]) + start
    assert(start == 17 and end == 37)
