import time
import os 

NB_BITS  = 2
NB_POS   = 4
POS_BITS = [0, 1, 2, 3]

# Convertit les NB_POS positions à partir de start en un symbole
# En téhorie, cette fonction ne fait que rechercher le 1 parmi les positions
def positions_vers_chunk(liste, i, start):
    res = 0
    for j in range(NB_POS):
        res += int(liste[start + j]) * POS_BITS[j] << 2*i
    return res
    
# Parcourt la liste des positions, contenant nb_octets octets, pour
# écrire le résultat décdodé dans fout
def pos_liste_vers_fichier(liste, fout, nb_octets):
    b = 0         # Octet en cours de lecture
    i = 0         # Nombre de chunks ajoutés à b
    count = 0     # Nombre de chunks parcourus au total
    bytelist = [] # Liste des octets décodés

    while count < nb_octets:
        b += positions_vers_chunk(liste, i, count<<2)
        i += 1
        count += 1

        # Lorsque l'octet est complet, l'ajouter à la liste
        if i == 4: 
            i = 0
            bytelist.append(b) 
            b = 0
    fout.write(bytes(bytelist))

def main():
    debut = time.perf_counter()
    filename = "sample.txt"
    with open(filename, "r") as f:
        l = f.read().splitlines()
    taille = os.path.getsize(filename)
    taille_octets = int(taille / (2 * NB_POS))
    with open("output", "wb") as fout:
        pos_liste_vers_fichier(l, fout, taille_octets) # Le fichier a 2*NB_POS positions enregistrées
    DeltaT = time.perf_counter() - debut               # time.perf_counter() est en secondes
    print(f"Nombre d'octets : {taille_octets} octets\nTemps écoulé : {DeltaT} secondes\nVitesse : {taille_octets / DeltaT} o/s")

main()
