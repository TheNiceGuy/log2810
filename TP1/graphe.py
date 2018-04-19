villes = [
    "Unknown",
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
        try:
            self.__identifiant = villes[index]
        except IndexError:
            self.__identifiant = villes[0]
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

    def __str__(self):
        string = ""
        for sommet in self.__sommets:
            string += "{}\n".format(sommet)
        return string
