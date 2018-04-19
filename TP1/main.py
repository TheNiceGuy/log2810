#!/usr/bin/env python3

from pathlib import Path
from graphe import Graphe
from dijkstra import Dijkstra
from transport import Voiture,Pickup,Fourgon

carte = None

def lireGraphe():
    if carte is None:
        print("")
        print("Veuillez mettre à jour une carte.")
        print("")
        return

    print("")
    print(carte)

def creerGraphe(fichier):
    return Graphe(fichier)

def actualiserGraphe():
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
            print("Erreur: Le fichier n'existe pas.")
            continue
            
        if chemin.is_dir():
            print("Erreur: Veuillez spécifier un fichier.")
            continue

        break

    carte = creerGraphe(fichier)
    lireGraphe()

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
            print("Erreur: Le sommet doit être un nombre.")
            continue

        sommet1 = carte.getSommet(sommet1)
        if sommet1 is None:
            print("Le sommet n'est pas dans le graphe.")
            continue

        identifiant = sommet1.getIdentifiant()
        index = sommet1.getIndex()
        print("Vous avez choisie le sommet {} ({}).".format(identifiant, index))
        break

    while True:
        sommet2 = input("Index du sommet de fin: ")
        if len(sommet2) == 0:
            return

        try:
            sommet2 = int(sommet2)
        except ValueError:
            print("Erreur: Le sommet doit être un nombre.")
            continue

        sommet2 = carte.getSommet(sommet2)
        if sommet2 is None:
            print("Erreur: Le sommet n'est pas dans le graphe.")
            continue

        identifiant = sommet2.getIdentifiant()
        index = sommet2.getIndex()
        print("Vous avez choisie le sommet {} ({}).".format(identifiant, index))
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
            print("Erreur: Le choix est invalid.")
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
    print("(c) quitter")
    print("(d) afficher la carte")
    print("")

    while True:
        choix = input("Veuillez choisir votre action: ")

        if len(choix) != 1:
            print("Erreur: Veuillez spécifier une seule lettre.")
            continue

        if choix[0] == 'a':
            actualiserGraphe()
            return True
        elif choix[0] == 'b':
            plusCourtChemin()
            return True
        elif choix[0] == 'c':
            return False
        elif choix[0] == 'd':
            lireGraphe()
            return True
        else:
            print("Erreur: Le choix est invalid.")

if __name__ == "__main__":
    while menu():
        pass
