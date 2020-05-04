from matplotlib import pyplot
# 中文输出
pyplot.rcParams['font.sans-serif'] = ['SimHei']
pyplot.rcParams['axes.unicode_minus'] = False


class DrawWealth:

    def __init__(self):
        pass

    def get_data(self, entities):
        data = []
        for ent in entities.pool:
            if ent.alive == 1:
                data.append(ent.wealth)
        return data

    def draw(self, entities, world_time=0):
        data = self.get_data(entities)
        # pyplot.figure("The Great Sugar Empire | Figure")
        pyplot.figure('大糖帝国')
        pyplot.ion()
        pyplot.cla()
        pyplot.hist(data, 10)
        # pyplot.xlabel('low <--- Wealth ---> high')
        # pyplot.ylabel('Num of Pop')
        # pyplot.title(f'Wealth Distribution | World Time: {world_time}')
        pyplot.xlabel('少 <--- 财富水平区间 ---> 多')
        pyplot.ylabel('人数')
        pyplot.title(f'财富分布状况 | 时间：{world_time}')
        pyplot.grid(True)
        pyplot.pause(0.03)


if __name__ == '__main__':
    d = []
    for i in range(0, 10):
        for j in range(0, 10):
            d.append(j)
    data = pandas.DataFrame({'x':d})
    p = (ggplot(data=data)+geom_bar(aes(x='x'))+xlab('Test'))