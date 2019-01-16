import World.World
import Entities.Entities
import Animation.Animation

if __name__ == '__main__':
    w = World.World.World(20)
    pop = Entities.Entities.EntitiesPopulation(w.world_grid.matrix, 50)
    pop.population_init()
    w.population_position_insert(pop)
    a = Animation.Animation.Animation(w, pop)
    a.playing()
