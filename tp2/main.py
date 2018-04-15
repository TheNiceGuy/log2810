#!/usr/bin/env python3

from pathlib import Path
from automata import Automata

automates = dict()
valides = None

def traiterLesEntrees(filename):
    contents = None

    # on lit le fichier en entier
    with open(filename) as fd:
        contents = fd.read().splitlines()

    # on s'assure que quelque chose a été lu
    if contents is None:
        return (None, None)

    # la première ligne est le numéro de l'automate
    numero = int(contents[0])

    # on retourne le numéro de l'automate et une list des variantes
    return (numero, contents[1:])

def obtenirNomFichier():
    fichier = None

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

    return fichier

def lireFichier():
    global automates

    print("")
    print("Veuillez entrer le nom du fichier contenant les règles.")
    print("Entrez une ligne vide pour retourner au menu principal.")
    print("")

    fichier = obtenirNomFichier()
    if fichier is None:
        return

    automate = Automata.creerAutomate(fichier)
    automates[automate.getNumero()] = automate

def lireEntrees():
    global automates
    global valides

    if len(automates) == 0:
        print("Erreur: Veuillez lire un fichier de règles.")
        return

    print("")
    print("Veuillez entrer le nom du fichier contenant les entrées à tester.")
    print("Entrez une ligne vide pour retourner au menu principal.")
    print("")

    fichier = obtenirNomFichier()
    if fichier is None:
        return

    (numero, variantes) = traiterLesEntrees(fichier)

    if not numero in automates:
        print("Erreur: L'automate ayant le numéro {} n'est pas connue.".format(numero))
        return

    if valides is None:
        valides = (numero, automates[numero].trouverMotDePasse(variantes))
    else:
        (vnum, vpass) = valides

        if vnum == numero:
            vpass = vpass.union(automates[numero].trouverMotDePasse(variantes))
            valides = (vnum, vpass)
            return

        valides = (numero, automates[numero].trouverMotDePasse(variantes))


def afficherLesMotsDePasse():
    global valides
    if valides is None:
        print("Erreur: Veuillez traiter des requêtes.")
        return

    (numero, passwords) = valides

    print("Voici les mots de passe valides pour l'automate {}:".format(numero))
    print("")
    for password in passwords:
        print(password)

def menu():
    print("Quelle action voulez-vous faire?")
    print("(a) lire un fichier de règles")
    print("(b) lire un fichier d'entrées")
    print("(c) afficher les mots de passe valides")
    print("(d) quitter")
    print("")

    while True:
        choix = input("Veuillez choisir votre action: ")

        if len(choix) != 1:
            print("Erreur: veuillez spécifier une seule lettre.")
            continue

        if choix[0] == 'a':
            lireFichier()
            return True
        elif choix[0] == 'b':
            lireEntrees()
            return True
        elif choix[0] == 'c':
            afficherLesMotsDePasse()
            return True
        elif choix[0] == 'd':
            return False
        else:
            print("Erreur: Le choix est invalide.")

if __name__ == '__main__':
    while menu():
        print("")
