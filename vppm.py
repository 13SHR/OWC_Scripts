from math import *
from pylab import *
from scipy.integrate import quad
import matplotlib.pyplot as plt
import numpy as np

"""Idée,
    Découper l'espace en k et trouver toutes les valeurs possibles
#1 espace -> 0, 1 = 2 valeurs
#2 espaces -> 0 1 2 3 = 4 valeurs
#k espaces -> 2^k valeurs

objectifs : trouver la limite ! quel k convient (différence réception, émission, trajet max)


objectifs suppl : Trouver quels caractères sont les plus représentés et adapter les ratios
"""

#On se donne 16 valeurs -> Hexadécimal -> k = 4
k = 4
ratios = [1/2,1/4,1/8,1/8] #Quel ratio associer à chaque valeur (ici 1/4) la somme doit faire 1
temps = 0.1 #en secondes = combien de temps dure un signal
nb_lettres = 4 #modifiable
pas = temps/100 #pour pouvoir bien délimiter et approximer le signal carré
tab_temps = np.arange(0,temps*nb_lettres,pas) #tableau qui va de 0 à temps avec des intervalles de taille pas
taille = int(nb_lettres*temps/pas)
tab_emission = [0]*taille
decoupage = [0]*taille


def decimal_to_binaire(n:int):
    assert(n<= 2**k)
    t = [0]*k    
    m = n
    i = 0
    while(m>0):
        if m%2 == 0:
            t[i] = 0
            m = m/2
        else:
            t[i] = 1
            m = m//2
        i += 1
    return t

def binaire_to_decimal(t:list) :
    assert(k == len(t))
    n=0
    for i in range(k):
       n += t[i] * 2**i
    return n

#Renvoie dans quelle portion de 0,1 on se situe (le k-eme decoupage)
def k_decoup(v,ratios):
    assert(v<=1 and v>=0)
    somme = ratios[0]
    k = 1
    while(v>somme):
        somme = somme + ratios[k]
        k += 1
    return (k-1)

#Récupère un entier n qu'il encode en binaire puis qu'il transmet sous la forme d'un signal
#en l'intégrant dans le signal tab_emission
def un_signal(n:int,tab_emission,duree,entier,ratios):
    tableau_binaire = decimal_to_binaire(n)
    debut = entier*(duree/pas)
    fin = (entier+1)*(duree/pas)
    i = int(debut)
    while(i < fin):
        k = k_decoup((i - debut)/(fin-debut),ratios)
        if tableau_binaire[k] == True:
            tab_emission[i] = 1
        else:
            tab_emission[i] = 0
        i = i + 1
        
        
        
        
#utilisations
#On veut envoyer 1,3,5,1
donnees = [1,3,5,1] #taille donnees = nb_lettres
def cree_signal(donnes,tab_emission,ratios):
    for i in range(nb_lettres):
        un_signal(donnes[i],tab_emission,temps,i,ratios)


for j in range(nb_lettres):
    decoupage[j*int(taille/nb_lettres)] = 1


cree_signal(donnees,tab_emission,ratios)
plt.title("Test pour 1,3,5,1")
plt.plot(tab_temps,decoupage,color = 'k',ls = '--')
plt.plot(tab_temps,tab_emission,color = 'r')


#On s'occupe maintenant de décoder le signal reçu (pas de vérifier que c'est le bon)
#Il nous faut connaître le temps d'émissions, 
def decode_un_signal(tab_reception,duree,entier,ratios): 
    #entier = combien-eme de lettre on décode
    nb_binaire = [0]*k
    somme = 0
    t_lettre = taille/nb_lettres
    for i in range(k):
        nb_binaire[i] = tab_reception[int(ceil((t_lettre * entier + somme*t_lettre)))+1]
        
        plt.plot((ceil((t_lettre * entier + somme*t_lettre+1))*nb_lettres*temps/taille),nb_binaire[i],'bo')
        #print(t_lettre,t_lettre*entier,somme*t_lettre,ceil((t_lettre * entier + somme*t_lettre)),ceil((t_lettre * entier + somme*t_lettre+1))*nb_lettres*temps/taille)
        somme = somme + ratios[i]
    
    return nb_binaire

decode_un_signal(tab_emission,temps,0,ratios)
decode_un_signal(tab_emission,temps,1,ratios)
decode_un_signal(tab_emission,temps,2,ratios)
decode_un_signal(tab_emission,temps,3,ratios)
    

#On cherche alors la fonction qui prends pour un signal reçu, une durée donnée pour une lettre, des ratios donnés, lis les différents chiffres binaire
def decode_tout_signal(tab_reception,duree,ratios,pas):
    #pas = combien de de temps dure l'écart entre deux cases du tableau
    nb_lettres = int(len(tab_reception)*pas/duree)
    tab_entiers = [0]*nb_lettres
    for i in range(nb_lettres):
        tab_entiers[i] = binaire_to_decimal(decode_un_signal(tab_reception,duree,i,ratios))
    return tab_entiers
    
tab = decode_tout_signal(tab_emission,temps,ratios,pas)
    
print(f"Le signal envoyé était {donnees} et le signal reçu est {tab} !\n")
#on ne connaît pas le nombre de lettres c'est à cette
#fonction de le déterminer, on regarde le découpage et on détermine combien de valeurs + ce qu'lles vallent

#On prendra comme convention qu'on envoie 20 valeurs "Zéro" à la fin d'un message
    
    
        
    
    