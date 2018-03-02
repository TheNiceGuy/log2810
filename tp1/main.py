#!/usr/bin/env python3

from enum import Enum
from pathlib import Path


villes = [
    None,
    "Montréal",      #  1
    "Québec",        #  2
    "Ottawa",        #  3
    "Toronto",       #  4
    "Halifax",       #  5
    "Sept-Îles",     #  6
    "Thunder Bay",   #  7
    "Sandy Lake",    #  8
    "Winnipeg",      #  9
    "Regina",        # 10
    "Saskatoon",     # 11
    "Calgary",       # 12
    "Vancouvert",    # 13
    "Edmonton",      # 14
    "Fort McMurray", # 15
    "Churchill",     # 16
    "Prince George", # 17
    "Fort Nelson",   # 18
    "Whitehorse",    # 19
    "Yellowknife",   # 20
]

class Sommet(object):
    def __init__(self, index, type_):
        self.__index = index
        self.__identifiant = villes[index]
        self.__type = type_

        self.__adjacents = set()
        self.__distances = {}

    def getIndex(self):
        return self.__index

    def getIdentifiant(self):
        return self.__identifiant

    def getAdjacents(self):
        return self.__adjacents

    def getDistance(self, sommet):
        return self.__distances[sommet.getIndex()]

    def hasGas(self):
        return (self.__type == 1)

    def appendAdjacent(self, sommet, distance):
        self.__adjacents.add(sommet)
        self.__distances[sommet.getIndex()] = distance

    def __repr__(self):
        return "{} ({})".format(self.__identifiant, self.__index)

    def __str__(self):
        string = "({}, {}, (\n".format(self.__identifiant, self.__index)
        for sommet in self.__adjacents:
            identifiant = sommet.getIdentifiant()
            distance = self.__distances[sommet.getIndex()]
            string += "\t({}, {}),\n".format(identifiant, distance)
        string = string[:-2]
        string += "\n))"
        return string

class Arc(object):
    def __init__(self, distance, sommet1, sommet2):
        self.__distance = distance
        self.__sommet1 = sommet1
        self.__sommet2 = sommet2

        sommet1.appendAdjacent(sommet2, distance)
        sommet2.appendAdjacent(sommet1, distance)

class Graphe(object):
    def __init__(self, chemin):
        self.__sommets = set()
        self.__arcs    = set()

        self.creerGraphe(chemin)

    def getSommets(self):
        return self.__sommets

    def getSommet(self, index):
        for sommet in self.__sommets:
            if sommet.getIndex() == index:
                return sommet
        return None

    def creerGraphe(self, chemin):
        with open(chemin) as fichier:
            self.creerSommets(fichier)
            self.creerArcs(fichier)

    def creerSommets(self, fichier):
        while True:
            # on lit les éléments d'une ligne
            ligne = fichier.readline().strip().split(',')

            # on regarde si on a atteint la ligne vide
            if len(ligne) == 1:
                return

            # on s'assure qu'il n'y a que deux nombres sur cette ligne
            if not len(ligne) == 2:
                print("Ligne de sommet mal formattée: {}".format(ligne))
                return

            # on crée le sommet
            self.__sommets.add(Sommet(int(ligne[0]), int(ligne[1])))

    def creerArcs(self, fichier):
        while True:
            # on lit les éléments d'une ligne
            ligne = fichier.readline().strip().split(',')

            # on regarde si on a atteint la ligne vide
            if len(ligne) == 1:
                return

            # on s'assure qu'il n'y a que deux nombres sur cette ligne
            if not len(ligne) == 3:
                print("Ligne de sommet mal formattée: {}".format(ligne))
                return

            # on obtient les sommets
            sommet1 = self.getSommet(int(ligne[0]))
            sommet2 = self.getSommet(int(ligne[1]))

            # on crée l'arc
            arc = Arc(int(ligne[2]), sommet1, sommet2)

            # on ajoute l'arc à la liste
            self.__arcs.add(arc)

    def lireGraphe(self):
        print(self)

    def plusCourtChemin(self, debut, fin, voiture):
        chemins = {}
        for sommet in self.__sommets:
            chemins[sommet.getIndex()] = None
        chemins[debut.getIndex()] = ExploreNode(voiture=voiture, sommet=debut)
        
        best = chemins[debut.getIndex()]
        visited = set()

        while not best.getSommet() is fin:
            smallest = None
            visited.add(best.getSommet())
            for sommet in best.getPossibles():
                #print(sommet)
                foward = best.avancer(sommet)

                if foward is None:
                    continue

                # on actualise les chemins si possible
                chemin = chemins[sommet.getIndex()]
                if chemin is None or chemin > foward:
                    chemins[sommet.getIndex()] = foward

                    chemin = chemins[sommet.getIndex()]
                    if smallest is None or smallest > foward:
                        smallest = chemin
 
            for sommet in self.__sommets.difference(visited):
                chemin = chemins[sommet.getIndex()]
                if chemin is None:
                    continue

                if smallest is None or smallest > chemin:
                    smallest = chemin

            if smallest is None:
                return None

            best = smallest
            #print(best)
            #print(visited)
            #print("")
            #self.debug(chemins, best)
        return best

    def debug(self, chemins, best):
        for sommet in self.__sommets:
            identifiant = sommet.getIdentifiant()
            index = sommet.getIndex()
            chemin = chemins[sommet.getIndex()]

            print("{} ({}):\n\t{}".format(identifiant, index, chemin))
        print("best:\n\t{}".format(best))
        print("-------------------------------------")

    def __str__(self):
        string = ""
        for sommet in self.__sommets:
            string += "{}\n".format(sommet)
        return string

class ExploreNode(object):
    def __init__(self, sommet, voiture, parent=None, essence=100, distance=0.0):
        self.__sommet   = sommet
        self.__voiture  = voiture
        self.__essence  = essence
        self.__distance = distance
        self.__parent   = parent

    def getVoiture(self):
        return self.__voiture

    def getSommet(self):
        return self.__sommet

    def getParent(self):
        return self.__parent

    def getDistance(self, sommet=None):
        if sommet is None:
            return self.__distance
        else:
            return self.__distance+self.__sommet.getDistance(sommet)

    def getEssence(self, sommet=None):
        if sommet is None:
            return self.__essence
        else:
            distance = self.__sommet.getDistance(sommet)
            cout = self.__voiture.getCout()
            return self.__essence-distance*cout

    def getPossibles(self):
        visited = set()

        node = self
        while not node is None:
            sommet = node.getSommet()
            visited.add(sommet)
            node = node.getParent()
        adjacents = self.getSommet().getAdjacents()

        return adjacents.difference(visited)

    def avancer(self, sommet):
        essence = self.getEssence(sommet=sommet)

        if essence < 12:
            return None
    
        distance = self.getDistance(sommet=sommet)

        if sommet.hasGas():
            essence = 100
            distance += 0.15

        voiture = self.getVoiture()
        return ExploreNode(sommet, voiture, parent=self, essence=essence, distance=distance)

    def foward(self, sommet):
        return ExploreNode(voiture=self.__voiture, sommet=sommet, parent=self)

    def __gt__(self, other):
        # TODO: ajouter la marque du véhicule dans la comparaison
        return self.getDistance() > other.getDistance()

    def __str__(self):
        stack = []

        node = self
        while not node is None:
            stack.append(node)
            node = node.getParent()

        string  = ""
        string += "Temps total: {} h\n".format(self.__distance)
        string += "Essence restant: {} %\n".format(self.__essence)
        string += "Transport: {}\n".format(self.__voiture)
        string += "Chemin: "

        while not len(stack) == 0:
            node = stack.pop()

            sommet = node.getSommet()
            identifiant = sommet.getIdentifiant()
            index = sommet.getIndex()

            string += "{} ({})".format(identifiant, index)

            if not len(stack) == 0:
                string += " -> "
        
        return string

class Marque(Enum):
    CHEAP = 0
    SUPER = 1

class Vehicule(object):
    def __init__(self, marque=Marque.SUPER):
        self._marque = marque

class Voiture(Vehicule):
    def getCout(self):
        if self._marque == Marque.CHEAP:
            return 5
        elif self._marque == Marque.SUPER:
            return 3

    def __str__(self):
        if self._marque == Marque.CHEAP:
            return "voiture cheap"
        elif self._marque == Marque.SUPER:
            return "voiture super"

class Pickup(Vehicule):
    def getCout(self):
        if self._marque == Marque.CHEAP:
            return 7
        elif self._marque == Marque.SUPER:
            return 4

    def __str__(self):
        if self._marque == Marque.CHEAP:
            return "pickup cheap"
        elif self._marque == Marque.SUPER:
            return "pickup super"

class Fourgon(Vehicule):
    def getCout(self):
        if self._marque == Marque.CHEAP:
            return 8
        elif self._marque == Marque.SUPER:
            return 6

    def __str__(self):
        if self._marque == Marque.CHEAP:
            return "fourgon cheap"
        elif self._marque == Marque.SUPER:
            return "fourgon super"

carte = None

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
    chemin = carte.plusCourtChemin(sommet1, sommet2, transport)
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
