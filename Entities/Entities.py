import Entities.Entity
import random



class EntitiesPopulation:

    def __init__(self, world_grid, seed=None):
        self.__world_grid = world_grid
        self.__seed = seed

    @property
    def world_grid(self):
        return self.__world_grid

    @property
    def seed(self):
        return self.__seed

    def population_init(self):
        if not self.seed is None:
            random.seed(self.seed)

    def population_move(self):
        pass