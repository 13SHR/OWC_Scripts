import gpiozero
import time

PIN = 23

laser = gpiozero.LED(PIN)

NB_BITS  = 2
NB_POS   = NB_BITS * NB_BITS 
POS_BITS = {"0b0":0, 
            "0b1":1, 
            "0b10":2, 
            "0b11":3
           }

TS = 1 # secondes - durée d'un signal i.e. Temps par Symbole
TE = TS / NB_POS

# Convertit char en une liste de 2 bits qui, une fois mis ensemble en petit boutiste, reforment char
def hex_vers_chunks(char):
    return list(map(bin, [(char >> 2*x) & 3 for x in range(4)]))

# Convertit en liste de 2 bits le texte dans s
def texte_vers_chunks(s):
    res = []
    for char in s:
        res += hex_vers_chunks(char)

    return res

# Attend tau secondes
# tau est un flottant, avec au plus 9 décimales
def wait(tau): 
    chrono = time.perf_counter()
    t = time.perf_counter()
    while t - chrono < tau:
        t = time.perf_counter()

# Émet le signal de début de transmission
def sync_debut():
    laser.off()
    wait(TS)
    laser.on()
    wait(TS)

# Émet le signal de fin de transmission
def sync_fin():
    laser.on()
    wait(TS)
    laser.off()
    wait(TS)

# Émet les signaux associés à liste_2_bits
def emit(liste_2_bits): 
    sync_debut()
    for chunk in liste_2_bits:
        chrono = time.perf_counter()
        pos = POS_BITS[chunk]
        for i in range(NB_POS):
            if i == pos:
                laser.on()
            else:
                laser.off()
            t = time.perf_counter()
            while t - chrono < TE:
                t = time.perf_counter()
            chrono = t 
    sync_fin()

def main():
    with open("input.txt", "rb") as fin:
        texte = fin.read()
    chunk_list = texte_vers_chunks(texte)
    emit(chunk_list)
    laser.off()


main()

