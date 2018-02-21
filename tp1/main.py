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

        self.__arcs = set()

    def getIndex(self):
        return self.__index

    def getIdentifiant(self):
        return self.__identifiant

    def getAdjacents(self):
        adjacents = set()
        for arc in self.__arcs:
            adjacents.add(arc.getOther(self))
        return adjacents

    def getDistance(sommet):
        for arc in self.__arcs:
            if arc.getOther(self) == sommet:
                return arc.getDistance()
        raise ValueError

    def appendArc(self, arc):
        self.__arcs.add(arc)

    def __str__(self):
        string = "({}, {}, (\n".format(self.__identifiant, self.__index)
        for arc in self.__arcs:
            sommet = arc.getOther(self)
            identifiant = sommet.getIdentifiant()
            distance = arc.getDistance()

            string += "\t({}, {}),\n".format(identifiant, distance)
        string = string[:-2]
        string += "\n))"
        return string

class Arc(object):
    def __init__(self, distance, sommet1, sommet2):
        self.__distance = distance
        self.__sommet1 = sommet1
        self.__sommet2 = sommet2

        sommet1.appendArc(self)
        sommet2.appendArc(self)

    def getDistance(self):
        return self.__distance

    def getOther(self, sommet):
        other = sommet

        if self.__sommet1 == sommet:
            other = self.__sommet2
        elif self.__sommet2 == sommet:
            other = self.__sommet1

        if other == sommet:
            raise ValueError

        return other

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
            self.__sommets.add(Sommet(int(ligne[0]), ligne[1]))

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

    def plusCourtChemin(debut, fin):
        pass   

    def __str__(self):
        string = ""
        for sommet in self.__sommets:
            string += "{}\n".format(sommet)
        return string

class Marque(Enum):
    CHEAP,
    SUPER

class Vehicule(object):
    def __init__(self, marque):
        self.__marque = marque

class Voiture(Vehicule):
    def getCout(self):
        if self.__marque == Marque.CHEAP:
            return 5
        elif self.__marque == Marque.SUPER:
            return 3

class Pickup(Vehicule):
    def getCout(self):
        if self.__marque == Marque.CHEAP:
            return 7
        elif self.__marque == Marque.SUPER:
            return 4

class Fourgon(Vehicule):
    def getCout(self):
        if self.__marque == Marque.CHEAP:
            return 8
        elif self.__marque == Marque.SUPER:
            return 6

class ExploreTree(object):
    def __init__(self, graph):
        self.__graph    = graph
        self.__root     = None
        self.__branches = set()

    def dijkstra(self, debut, fin, voiture):
        restants = self.__graph.getSommets().copy().remove(debut)

        root = ExploreNode(debut, restants, voiture, 100, 0)
        best = root

        branches = set([root])

        while True:
            # on trouve le prochain sommet à visiter
            minimumDistance = None
            minimumSommet = None
            for sommet in best.getPossibles():
                if minimumDistance is None:
                    minimumDistance = best.getDistance(sommet)
                    minimumSommet = sommet
                    continue

                if minimumDistance > best.getDistance(sommet):
                    minimumDistance = best.getDistance()
                    minimumSommet = sommet

            # on s'assure que l'essence n'est pas trop basse
            essence = best.getEssence()-best.getVoiture().getCout()*minimumDistance
            if essence < 12:
                # TODO
                pass

            # on détermine les sommets qui restent à visiter
            restants = best.getRestants().copy().remove(sommet)

            # on calcule la nouvelle distance en empruntant ce chemin
            current = best.getCurrent()+minimumDistance

            # on ajoute le noeud dans l'arbre
            node = ExploreNode(sommet, restants, voiture, essence, current)

            best.appendChild(node)
            best = node

            for branch in branches:
                if best.getCurrent() > branch.getCurrent():
                    best = branch
                    
class ExploreNode(object):
    def __init__(self, sommet, restants, voiture, essence, current):
        self.__sommet   = sommet
        self.__restants = restants
        self.__voiture  = voiture
        self.__essence  = essence
        self.__current = current

        self.__childs = set()

    def getDistance(self, sommet):
        return self.__sommet.getDistance(sommet)

    def getPossibles(self):
        adjacents = self.__sommet.getAdjacents()
        possibles = self.__restants.intersection(adjacents)
        return possibles

    def getRestants(self):
        return self.__restants

    def getCurrent(self):
        return self.__current

    def getEssence(self):
        return self.__essence

    def getVoiture(self):
        return self.__voiture

    def appendChild(self, node):
        self.__childs.add(node)

g = Graphe('villes.txt')
print(g)
