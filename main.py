import World.World
import Entities.Entities
import Animation.Animation



if __name__ == '__main__':
    w = World.World.World(20)
    pop = Entities.Entities.EntitiesPopulation(w.world_grid.matrix, 20)
    pop.population_init()
    w.population_position_insert(pop)
    w.world_grid.print_matrix()
    w.world_grid_clean()
    w.world_grid.print_matrix()