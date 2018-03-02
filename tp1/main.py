#!/usr/bin/env python3

from pathlib import Path
from graphe import Graphe
from dijkstra import Dijkstra
from transport import Voiture,Pickup,Fourgon

carte = None

def lireCarte():
    print(carte)

def actualiserCarte():
    print("")
    print("Veuillez entrer le nom du fichier contenant la carte.")
    print("Entrez une ligne vide pour retourner au menu principal.")
    print("")

    fichier = None
    global carte

    while True:
        fichier = input("Nom du fichier: ")

        if len(fichier) == 0:
            print("")
            return

        chemin = Path(fichier)
        if not chemin.exists():
            continue
            
        if chemin.is_dir():
            continue

        print("")
        break

    carte = Graphe(fichier)

def plusCourtChemin():
    if carte is None:
        print("")
        print("Veuillez mettre à jour une carte.")
        print("")
        return

    print("")   
    print("Veuillez entrer les sommets pour le chemin.")
    print("Entrez une ligne vide pour retourner au menu principal.")
    print("")

    sommet1 = None
    sommet2 = None
    transport = None

    while True:
        sommet1 = input("Index du sommet de départ: ")
        if len(sommet1) == 0:
            return

        try:
            sommet1 = int(sommet1)
        except ValueError:
            continue

        sommet1 = carte.getSommet(sommet1)
        if sommet1 is None:
            print("Le sommet n'est pas dans le graphe.")
            continue
        break

    while True:
        sommet2 = input("Index du sommet de fin: ")
        if len(sommet2) == 0:
            return

        try:
            sommet2 = int(sommet2)
        except ValueError:
            continue

        sommet2 = carte.getSommet(sommet2)
        if sommet2 is None:
            print("Le sommet n'est pas dans le graphe.")
            continue
        break
 
    print("")
    print("Veuillez entrer le transport à utiliser.")
    print("(a) voiture")
    print("(b) pickup")
    print("(c) fourgon")
    print("")

    transport = None

    while True:
        transport = input("Transport à utiliser: ")
        if len(transport) == 0:
            print("")
            return

        if len(transport) != 1:
            continue

        if transport[0] == 'a':
            transport = Voiture()
        elif transport[0] == 'b':
            transport = Pickup()
        elif transport[0] == 'c':
            transport = Fourgon()
        else:
            continue
        break

    print("")
    dijkstra = Dijkstra(carte)
    chemin = dijkstra.plusCourtChemin(sommet1, sommet2, transport)
    if chemin is None:
        print("Il n'existe aucun chemin sécuritaire.")
    else:
        print(chemin)
    print("")

def menu():
    print("Quelle action voulez-vous faire?")
    print("(a) mettre la carte à jour")
    print("(b) déterminer le plus court chemin sécuritaire")
    print("(q) quitter")
    print("")

    while True:
        choix = input("Veuillez choisir votre action: ")

        if len(choix) != 1:
            continue

        if choix[0] == 'a':
            actualiserCarte()
            return True
        elif choix[0] == 'b':
            plusCourtChemin()
            return True
        elif choix[0] == 'q':
            return False

if __name__ == "__main__":
    while menu():
        pass
