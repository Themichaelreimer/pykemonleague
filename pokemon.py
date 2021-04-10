
from transform import *


class Factory:

    this = None

    # For looking up dicts of pokemon, moves, etc from csv or json
    resources = {
        'pokemon': None  # pokemon.csv
    }

    @staticmethod
    def get_factory():
        if Factory.this is not None:
            return Factor.this

    def __init__(self):
        Factory.this = self


class Pokemon:

    def __init__(self, params:dict):
        self.sprite = None
        self.transform = Transform()

    def position(self):
        return self.transform.position

    def render(self):
        pass

    def update(self, keys, dt):
        pass


class Moves:
    pass
