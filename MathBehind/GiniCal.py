class GinCalculator:

    def __init__(self):
        pass

    def calculate(self, entities_pool, world_grid_matrix):
        delta_income = 0
        income_pool = []
        delta_wealth = 0
        wealth_pool = []
        for _entity1 in entities_pool:
            if _entity1.alive == 0:
                continue
            income1 = world_grid_matrix[_entity1.position[0]][_entity1.position[1]][0]
            income_pool.append(income1)
            wealth_pool.append(_entity1.wealth)
            for _entity2 in entities_pool:
                if _entity2.alive == 0:
                    continue
                income2 = world_grid_matrix[_entity2.position[0]][_entity2.position[1]][0]
                delta_income += abs(income1 - income2)
                delta_wealth += abs(_entity1.wealth - _entity2.wealth)

        total_num = len(income_pool)
        assert total_num == len(wealth_pool), 'Oops, something happened.'
        delta_income = delta_income / (total_num**2)
        delta_wealth = delta_wealth / (total_num**2)
        mean_of_income = sum(income_pool) / total_num
        mean_of_wealth = sum(wealth_pool) / total_num
        index_of_income = delta_income / (2 * mean_of_income)
        index_of_wealth = delta_wealth / (2 * mean_of_wealth)
        print('Index income: {}'.format(str(index_of_income)))
        print('Index wealth: {}'.format(str(index_of_wealth)))
        print('=='*10)

        return index_of_income, index_of_wealth