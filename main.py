import World.World
import Entities.Entities
import Animation.Animation

if __name__ == '__main__':
    w = World.World.World(16, random_seed=1)
    pop = Entities.Entities.EntitiesPopulation(w, 5)
    pop.population_init()
    w.population_position_insert(pop)
    a = Animation.Animation.Animation(w, pop)
    a.playing()
