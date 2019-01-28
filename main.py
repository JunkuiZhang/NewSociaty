import World.World
import Entities.Entities
import Animation.Animation

if __name__ == '__main__':
    w = World.World.World(36, random_seed=1, inflation=.03)
    pop = Entities.Entities.EntitiesPopulation(w, 200)
    pop.population_init()
    w.population_position_insert(pop)
    a = Animation.Animation.Animation(w, pop, file_name='test')
    a.playing()
