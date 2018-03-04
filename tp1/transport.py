from enum import Enum

class Marque(Enum):
    CHEAP = 0
    SUPER = 1

class Transport(object):
    def __init__(self, marque=Marque.CHEAP):
        self._marque = marque

    def getCout(self):
        return NotImplementedError

    def getWithMarque(self, marque):
        raise NotImplementedError

    def getMarque(self):
        return self._marque

class Voiture(Transport):
    def getCout(self):
        if self._marque == Marque.CHEAP:
            return 5
        elif self._marque == Marque.SUPER:
            return 3

    def getWithMarque(self, marque):
        return Voiture(marque=marque)

    def __str__(self):
        if self._marque == Marque.CHEAP:
            return "voiture cheap"
        elif self._marque == Marque.SUPER:
            return "voiture super"

class Pickup(Transport):
    def getCout(self):
        if self._marque == Marque.CHEAP:
            return 7
        elif self._marque == Marque.SUPER:
            return 4

    def getWithMarque(self, marque):
        return Pickup(marque=marque)

    def __str__(self):
        if self._marque == Marque.CHEAP:
            return "pickup cheap"
        elif self._marque == Marque.SUPER:
            return "pickup super"

class Fourgon(Transport):
    def getCout(self):
        if self._marque == Marque.CHEAP:
            return 8
        elif self._marque == Marque.SUPER:
            return 6

    def getWithMarque(self, marque):
        return Fourgon(marque=marque)

    def __str__(self):
        if self._marque == Marque.CHEAP:
            return "fourgon cheap"
        elif self._marque == Marque.SUPER:
            return "fourgon super"
