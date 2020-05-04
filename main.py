import World.World
import Entities.Entities
import Animation.Animation


if __name__ == '__main__':
    w = World.World.World(num_mountain=1, random_seed=120, reproduce_num=3, dimension=50)
    pop = Entities.Entities.EntitiesPopulation(w, 200, rand_intel=True)
    pop.population_init()
    a = Animation.Animation.Animation(w, pop, file_name='', gini_cal=False)
    a.playing()
