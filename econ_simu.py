import random
import numpy as np 


class Agent(object):
    def __repr__(self):
        return "{}: ${}".format(self.name, self.fund)

    def __init__(self, name, fund):
        self.name  = name
        self.fund = fund

    def transact(self, another_agent, winner_take=0.7):
        total_fund  = self.fund + another_agent.fund
        coin_flip = random.random() >= 0.5
        deal  = (total_fund * winner_take, total_fund * (1 - winner_take))
        self.fund, another_agent.fund = deal if coin_flip else deal[::-1]


class Agent2(Agent):
    #A bit more advance agent, where transaction create value for the economy
    #This is the idea behind VAT
    def transact(self, another_agent, winner_take=0.7):
        total_fund  = self.fund + another_agent.fund
        added_value = 0.01 # bucks

        coin_flip = random.random() >= 0.5
        deal  = (total_fund * winner_take , total_fund * (1 - winner_take))
        deal = (deal[0] + added_value/2, deal[1] + added_value/2)

        self.fund, another_agent.fund = deal if coin_flip else deal[::-1]



class Economy(object):
    #study of inequality as an inevitable consequence of free trade
    def __init__(self, num_agent=100, init_fund=10, winner_take=0.7):

        self.agents = [Agent(name="agent_{}".format(i), fund=init_fund) for i in range(num_agent)]
        self.winner_take = winner_take

    def exchange(self):
        indices = list(range(len(self.agents)))
        random.shuffle(indices)
        
        mid = int(len(indices) / 2)
        left, right = indices[:mid], indices[-mid:]

        for k in range(mid):
            self.agents[left[k]].transact(self.agents[right[k]], winner_take=self.winner_take)

        return self

    def report(self):
        self.agents = sorted(self.agents, key=lambda x: x.fund)[::-1]
        print ('\n'.join([str(x) for x in self.agents]))

    def __repr__(self):
        def gini(x):
            # https://www.statology.org/gini-coefficient-python/
            x = np.array(x)
            total = 0
            for i, xi in enumerate(x[:-1], 1):
                total += np.sum(np.abs(xi - x[i:]))
            return total / (len(x)**2 * np.mean(x))


        funds = [x.fund for x in self.agents]

        return 'Economy: {}, gini: {}'.format(sum(funds), gini(funds))


econ = Economy()

for i in range(1000):
    econ.exchange()



class EconomyWithAddedValue(Economy):
    def __init__(self, num_agent=100, init_fund=10, winner_take=0.7):
        self.agents = [Agent2(name="agent_{}".format(i), fund=init_fund) for i in range(num_agent)]
        self.winner_take = winner_take



econ = EconomyWithAddedValue()

for i in range(1000):
    econ.exchange()



