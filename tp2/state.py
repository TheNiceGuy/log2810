class State(object):
    """ Constructeur.

        :param state: Le nom de l'état.
    """
    def __init__(self, name):
        self.__name = name
        self.__transitions = dict()

    """ Cette fonction ajoute une transition à l'état.

        :param symbol: L'entrée à la transition.
        :param nstate: Le prochain état.
    """
    def addTransition(self, symbol, nstate):
        # on s'assure que la transition n'existe pas déjà
        if symbol in self.__transitions:
            raise ValueError

        # on ajoute la transition à la table
        self.__transitions[symbol] = nstate

    """ Cette fonction obtient le prochain état selon une entrée.

        :param symbol: L'entrée pour la transition.

        :return: Le prochain état si la transition existe, sinon None.
    """
    def next(self, symbol):
        # on s'assure que la transition existe
        if not symbol in self.__transitions:
            return None

        # on retourne le prochain état
        return self.__transitions[symbol]

    """ Cette fonction détermine si un état est un état final.

        :return: True si c'est un état final, sinon False.
    """
    def isTerminal(self):
        # aucune transition implique que c'est un état final
        return (len(self.__transitions) == 0)
        

    """ Cette fonction retourne le nom de l'état.

        :return: Le nom de l'état.
    """
    def getName(self):
        return self.__name
