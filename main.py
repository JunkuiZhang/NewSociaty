import World.World
import Entities.Entities
import Animation.Animation

if __name__ == '__main__':
    w = World.World.World(random_seed = 123, reproduce_num = 1, dimension = 50)
    pop = Entities.Entities.EntitiesPopulation(w, 500, rand_intel=True)
    pop.population_init()
    a = Animation.Animation.Animation(w, pop, file_name='', gini_cal=True)
    a.playing()