class GinCalculator:

    def __init__(self):
        pass

    def calculate(self, entities_pool, world_grid_matrix, decimal=3):
        delta_income = 0
        income_pool = []
        delta_wealth = 0
        wealth_pool = []

        for _entity in entities_pool:
            if _entity.alive == 0:
                continue
            income = world_grid_matrix[_entity.position[0]][_entity.position[1]]['current_prod']
            income_pool.append(income)
            wealth_pool.append(_entity.wealth)

        total_num = len(income_pool)
        assert total_num == len(wealth_pool), 'Oops, something wrong happened.'
        if total_num == 0:
            return 0

        for i in range(total_num):
            for j in range(total_num):
                if i == j:
                    continue
                delta_income += abs(income_pool[i] - income_pool[j])
                delta_wealth += abs(wealth_pool[i] - wealth_pool[j])

        delta_income = delta_income / (total_num**2)
        delta_wealth = delta_wealth / (total_num**2)
        mean_of_income = sum(income_pool) / total_num
        mean_of_wealth = sum(wealth_pool) / total_num
        index_of_income = delta_income / (2 * mean_of_income)
        index_of_wealth = delta_wealth / (2 * mean_of_wealth)

        return round(index_of_income, decimal), round(index_of_wealth, decimal)
