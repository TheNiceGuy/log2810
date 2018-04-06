#!/usr/bin/env python3

from pathlib import Path

class StateMachine(object):
    def __init__(self, numero, states):
        self.__numero = numero
        self.__states = states

    @staticmethod
    def creerAutomate(filename):
        contents = None

        # on lit le fichier en entier
        with open(filename) as fd:
            contents = fd.read().splitlines()

        # on s'assure que quelque chose ait été lu
        if contents is None:
            return None

        # la première ligne est le numéro de l'automate
        numero = int(contents[0])

        # la table des états
        nodes = dict()

        # les prochaines lignes sont les productions
        for line in contents[1:]:
            # on obtient l'état à gauche et à droite
            states = line.split('=')

            # on obtient le symbol de transition
            current = states[0]
            symbol = states[1][-1]
            nstate = states[1]

            # on crée l'état s'il n'existe pas
            if not current in nodes:
                nodes[current] = dict()

            # on ajoute la transition dans la machine à états
            nodes[current][symbol] = nstate

        nodes[""] = dict()
        nodes[""]["S"] = "S"

        return StateMachine(numero, nodes)

    def motDePasseValide(self, password):
        state = "S"

        for symbol in password:
            if not state in self.__states:
                return False

            if symbol in self.__states[state]:
                state = self.__states[state][symbol]
            else:
                return False

        if state in self.__states:
            return False

        return True

    def trouverMotDePasse(self, variantes):
        valides = set()

        for password in variantes:
            if self.motDePasseValide(password):
                valides.add(password)

        return valides

    def getNumero(self):
        return self.__numero

machines = dict()
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
    global machines

    print("")
    print("Veuillez entrer le nom du fichier contenant les règles.")
    print("Entrez une ligne vide pour retourner au menu principal.")
    print("")

    fichier = obtenirNomFichier()
    if fichier is None:
        return

    machine = StateMachine.creerAutomate(fichier)
    machines[machine.getNumero()] = machine

def lireEntrees():
    global machines
    global valides

    if len(machines) == 0:
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

    if not numero in machines:
        print("Erreur: L'automate ayant le numéro {} n'est pas connue.".format(numero))
        return

    if valides is None:
        valides = (numero, machines[numero].trouverMotDePasse(variantes))
    else:
        (vnum, vpass) = valides

        if vnum == numero:
            vpass = vpass.union(machines[numero].trouverMotDePasse(variantes))
            valides = (vnum, vpass)
            return

        valides = (numero, machines[numero].trouverMotDePasse(variantes))


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
