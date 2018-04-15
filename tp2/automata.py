from state import State

class Automata(object):
    """ Constructeur.

        :param numero:      Le numéro de l'automate.
        :param transitions: Une liste de transitions.
    """
    def __init__(self, numero, transitions):
        self.__numero = numero
        self.__states = dict()

        # on crée les états
        for (state, _, nstate) in transitions:
            self.addState(state)
            self.addState(nstate)

        # on ajoute les transitions
        for (state, symbol, nstate) in transitions:
            nstate = self.__states[nstate]
            self.__states[state].addTransition(symbol, nstate)

    """ Cette fonction retourne le numéro de l'automate.

        :return: Le numéro de l'automate.
    """
    def getNumero(self):
        return self.__numero

    """ Cette fonction ajoute un état à l'automate s'il n'existe pas.

        :param state: Le nom de l'état.
    """
    def addState(self, name):
        # on crée l'état seulement s'il n'existe pas
        if not name in self.__states:
            self.__states[name] = State(name)

    """ Cette fonction regarde si un mot de passe est valide.

        :param password: Le mot de passe à valider.

        :return: Si le mot de passe est valide ou non.
    """
    def motDePasseValide(self, password):
        # on commence à l'état initiale
        state = self.__states["S"]

        for symbol in password:
            # on avance au prochain état
            state = state.next(symbol)

            # on s'assure que la transition existait 
            if state is None:
                return False

        # l'automate doit finir à un état terminal
        return state.isTerminal()

    """ Cette fonction trouve les mots de passe valides dans une liste.

        :param variantes: La liste de mots de passe à tester.

        :return: Les mots de passe valides.
    """
    def trouverMotDePasse(self, variantes):
        # l'ensemble des mots de passe valides
        valides = set()

        # on trouve tout les mots de passe valides
        for password in variantes:
            if self.motDePasseValide(password):
                valides.add(password)

        return valides

    """ Cette fonction créer une automate à partir d'un fichier.

        :param filename: Le chemin vers le fichier.

        :return: Un automate si tout c'est bien passé, sinon rien.
    """
    @staticmethod
    def creerAutomate(filename):
        contents = None

        # on lit le fichier en entier
        with open(filename) as fd:
            contents = fd.read().splitlines()

        # on s'assure que quelque chose ait été lu
        if contents is None:
            print("Le fichier n'a pas pu être lu.")
            return None

        # la première ligne est le numéro de l'automate
        try:
            numero = int(contents[0])
        except ValueError:
            print("Le numéro de l'automate n'a pas pu être lu.")
            return None

        # les prochaines lignes sont les transitions
        transitions = []
        for line in contents[1:]:
            # on obtient l'état à gauche et à droite
            states = line.split('=')

            # on obtient le symbol de transition
            state  = states[0]
            symbol = states[1][-1]
            nstate = states[1]

            # on garde en mémoire les transitions
            transitions.append((state, symbol, nstate))

        return Automata(numero, transitions)
