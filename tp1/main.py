#!/usr/bin/env python3

from copy import copy
from enum import Enum


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
                print(sommet)
                foward = best.foward(sommet)

                # on s'assure qu'essence reste assez haut
                if foward.getEssence() < 12:
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

            best = smallest
            #print(best)
            #print(visited)
            #print("")
            self.debug(chemins, best)

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
    def __init__(self, voiture=None, sommet=None, parent=None):
        self.__sommet = sommet
        self.__parent = parent

        if parent is None:
            self.__voiture = voiture
            self.__distance = 0.0
            self.__essence  = 100
        else:
            if sommet is None:
                raise ValueError

            self.__voiture  = parent.getVoiture()
            self.__distance = parent.getDistance(sommet)
            self.__essence  = parent.getEssence(sommet)

            if sommet.hasGas():
                self.__distance += 0.15
                self.__essence = 100

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

    def foward(self, sommet):
        return ExploreNode(voiture=self.__voiture, sommet=sommet, parent=self)

    def __gt__(self, other):
        # TODO: ajouter la marque du véhicule dans la comparaison
        return self.getDistance() > other.getDistance()

    def __str__(self):
        string = "({}, {})".format(self.__distance, self.__essence)

        node = self
        while not node is None:
            sommet = node.getSommet()
            identifiant = sommet.getIdentifiant()
            index = sommet.getIndex()
            string += " <- {} ({})".format(identifiant, index)
            node = node.getParent()

        return string

class Marque(Enum):
    CHEAP = 0
    SUPER = 1

class Vehicule(object):
    def __init__(self, marque=Marque.CHEAP):
        self._marque = marque

class Voiture(Vehicule):
    def getCout(self):
        if self._marque == Marque.CHEAP:
            return 5
        elif self._marque == Marque.SUPER:
            return 3

class Pickup(Vehicule):
    def getCout(self):
        if self._marque == Marque.CHEAP:
            return 7
        elif self._marque == Marque.SUPER:
            return 4

class Fourgon(Vehicule):
    def getCout(self):
        if self._marque == Marque.CHEAP:
            return 8
        elif self._marque == Marque.SUPER:
            return 6

g = Graphe('villes.txt')
g.plusCourtChemin(g.getSommet(2), g.getSommet(19), Voiture(marque=Marque.SUPER))
#print(g)
