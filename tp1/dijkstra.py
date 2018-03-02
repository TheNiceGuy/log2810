from transport import Marque

class Dijkstra(object):
    def __init__(self, graphe):
        self.__graphe  = graphe
        self.__chemins = None
        self.__optimal = None
        self.__visited = None

    def initialisation(self, debut, fin, transport):
        self.__chemins = {s: None for s in self.__graphe.getSommets()}
        self.__chemins[debut] = ExploreNode(debut, transport)
        self.__optimal = self.__chemins[debut]
        self.__visited = set()

    def getPossibles(self, chemin):
        # on obtient les sommets adjacents de son sommet
        adjacents = chemin.getSommet().getAdjacents()

        # on obtient tout les sommets sur sa trajectoire actuelle
        visited = set()
        while not chemin is None:
            sommet = chemin.getSommet()
            visited.add(sommet)
            chemin = chemin.getParent()

        # on calcule la différence pour obtenir les sommets possibles
        return adjacents.difference(visited)

    def avancer(self, chemin, sommet):
        # on obtient l'essence si on avancait au prochain sommet
        essence = chemin.getEssence(sommet=sommet)

        # on s'assure que le niveau d'essence est sécuritaire
        if essence < 12:
            transport = chemin.gettransport()

            # si la marque est déjà super, on ne peut pas avoir mieux
            if transport.getMarque() == Marque.SUPER:
                return None

            # on essaie avec un véhicule super
            chemin = self.recalculer(chemin, transport.getWithMarque(Marque.SUPER))
            if chemin is None:
                return None

            # on s'assure à nouveau que l'essence est valide
            essence = chemin.getEssence(sommet=sommet)
            if essence < 12:
                return None
    
        # on obtient la distance si on se déplace au sommet
        distance = chemin.getDistance(sommet=sommet)

        # on regarde si le prochain sommet a une station service
        if sommet.hasGas():
            essence = 100
            distance += 15

        # on obtient le véhicule
        transport = chemin.gettransport()

        # on retourne le nouveau chemin
        return ExploreNode(
            sommet, transport,
            parent=chemin,
            essence=essence,
            distance=distance
        )

    def recalculer(self, chemin, transport):
        # on regarde trouve le trajet actuel
        trajet = []
        while not chemin is None:
            trajet.append(chemin.getSommet())
            chemin = chemin.getParent()

        # cas trivial
        if len(trajet) == 0:
            return None

        # on obtient le chemin de début avec la nouvelle transport
        nouveau = ExploreNode(trajet.pop(), transport)

        # on parcours à nouveau le trajet avec la nouvelle transport
        while not len(trajet) == 0:
            sommet = trajet.pop()
            nouveau = self.avancer(nouveau, sommet)

            # le véhicule a manqué d'essence
            if nouveau is None:
                return None

        # le nouveau véhicule peut parcourir le trajet
        return nouveau
        

    def actualiserChemin(self, nouveau, sommet):
        # on n'actualise pas le chemin s'il n'y a rien
        if nouveau is None:
            return False

        # on obtient l'ancien chemin se rendant au sommet
        ancien = self.__chemins[sommet]

        # on actualise le chemin si le nouveau est plus petit
        if ancien is None or ancien > nouveau:
            self.__chemins[sommet] = nouveau
            return True

        return False

    def minimiser(self, chemin1, chemin2):
        # les deux ne peuvent pas être nulle
        if chemin1 is None and chemin2 is None:
            raise ValueError

        # cas trivials
        if chemin1 is None:
            return chemin2
        if chemin2 is None:
            return chemin1

        # on trouve le plus petit chemin
        if chemin1 > chemin2:
            return chemin2
        else:
            return chemin1

    def plusCourtChemin(self, debut, fin, transport):
        self.initialisation(debut, fin, transport)

        while not self.__optimal.getSommet() == fin:
            meilleur = None
            self.__visited.add(self.__optimal.getSommet())

            # on regarde les sommets possibles autour du chemin optimal
            for sommet in self.getPossibles(self.__optimal):
                nouveau = self.avancer(self.__optimal, sommet)

                if self.actualiserChemin(nouveau, sommet):
                    meilleur = self.minimiser(meilleur, nouveau)

            # on regarde si un autre trajet est plus efficace
            for sommet in self.__graphe.getSommets().difference(self.__visited):
                if self.__chemins[sommet] is None:
                    continue
                meilleur = self.minimiser(meilleur, self.__chemins[sommet])

            # aucun chemin n'est assez sécuritaire
            if meilleur is None:
                return None

            self.__optimal = meilleur

        return self.__optimal

class ExploreNode(object):
    def __init__(self, sommet, transport, parent=None, essence=100, distance=0):
        self.__sommet   = sommet
        self.__transport  = transport
        self.__essence  = essence
        self.__distance = distance
        self.__parent   = parent

    def gettransport(self):
        return self.__transport

    def getSommet(self):
        return self.__sommet

    def getParent(self):
        return self.__parent

    def getDistance(self, sommet=None):
        if sommet is None:
            # la distance actuelle
            return self.__distance
        else:
            # on veut la distance si on avance au prochain sommet
            return self.__distance+self.__sommet.getDistance(sommet)*60

    def getEssence(self, sommet=None):
        if sommet is None:
            # l'essence actuel
            return self.__essence
        else:
            # on veut l'essence si on avance au prochain sommet
            distance = self.__sommet.getDistance(sommet)
            cout = self.__transport.getCout()
            return self.__essence-distance*cout

    def __gt__(self, other):
        # si les deux sont de mêmes marque, alors on compare la distance
        if self.gettransport().getMarque() == other.gettransport().getMarque():
            return self.getDistance() > other.getDistance()

        # on tente toujours de prendre un véhicule de marque cheap
        if self.gettransport().getMarque() == Marque.CHEAP:
            return False
        else:
            return True

    def __str__(self):
        stack = []

        # on obtient tout les sommets
        node = self
        while not node is None:
            stack.append(node)
            node = node.getParent()

        # on écrit l'information sur le chemin
        string  = ""
        string += "Temps total: {} min\n".format(self.__distance)
        string += "Essence restant: {} %\n".format(self.__essence)
        string += "Transport: {}\n".format(self.__transport)
        string += "Chemin: "

        # on écrit la trajectoire
        while not len(stack) == 0:
            node = stack.pop()

            sommet = node.getSommet()
            identifiant = sommet.getIdentifiant()
            index = sommet.getIndex()

            string += "{} ({})".format(identifiant, index)

            # on ne met pas de flèche au dernier sommet
            if not len(stack) == 0:
                string += " -> "
        
        return string

if __name__ == '__main__':
    from transport import Voiture

    # configuration pour les tests
    node1 = ExploreNode(None, Voiture(Marque.CHEAP), distance=30)
    node2 = ExploreNode(None, Voiture(Marque.CHEAP), distance=20)
    node3 = ExploreNode(None, Voiture(Marque.SUPER), distance=30)
    node4 = ExploreNode(None, Voiture(Marque.SUPER), distance=20)

    # tests unitaires
    assert(    node1 > node2)
    assert(not node1 < node2)

    assert(not node1 > node3)
    assert(    node1 < node3)

    assert(not node1 > node4)
    assert(    node1 < node4)

    assert(    node3 > node4)
    assert(not node3 < node4)
