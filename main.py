import World.World
import Entities.Entities
import Animation.Animation



if __name__ == '__main__':
    w = World.World.World(6, random_seed=1)
    pop = Entities.Entities.EntitiesPopulation(w.world_grid.matrix, 1, seed=1)
    pop.population_init()
    w.population_position_insert(pop)
    w.world_grid.print_matrix()
    print('=='*10)
    w.world_grid_clean()
    pop.population_move()
    w.population_position_insert(pop)
    w.world_grid.print_matrix()