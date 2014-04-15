
"""
For logging/plotting information about agents.
"""

"""
TODO
- make plots plot in real time
- ADD LABELS AND STUFF
"""

import matplotlib.pyplot as plt

class Logger:

    def __init__(self, ):
        self.rounds = []

    def advance_round(self, ):
        # advance by one round
        self.rounds.append(RoundLog())

    def log_agent(self, agent,):
        # log agent in current round
        self.rounds[-1].log_agent(agent)

    def plot(self, ):
        # plot lots of things after simulation done
        # number of agents
        plt.plot([r.num_agents for r in self.rounds])
        plt.show()
        
        # average, max, and min utility over time
        plt.plot([r.utility_sum/float(r.num_agents) for r in self.rounds])
        plt.plot([r.max_utility for r in self.rounds])
        plt.plot([r.min_utility for r in self.rounds])
        plt.show()

        # proportion of cooperations to defections over time
        # TODO: SWITCH TO SHOW RELATIVE PROPORTION!
        #plt.plot([r.cooperated / float(r.cooperated+r.defected)
        #          for r in self.rounds])
        plt.plot([r.cooperated for r in self.rounds])
        plt.plot([r.defected for r in self.rounds])
        plt.show()

        # actions chosen over time
        # TODO: SWITCH TO SHOW RELATIVE PROPORTION!
        plt.plot([r.actions['mate'] for r in self.rounds])
        plt.plot([r.actions['hunt'] for r in self.rounds])
        plt.plot([r.actions['rest'] for r in self.rounds])
        plt.plot([r.actions['punish'] for r in self.rounds])
        plt.plot([r.actions['gather'] for r in self.rounds])
        plt.show()


        # expected rewards for each action over time

        # possessed resources over time


class RoundLog:
    
    def __init__(self, ):
        # number of agents
        self.num_agents = 0
        # number of cooperation or defection decisions
        self.cooperated = 0
        self.defected   = 0
        self.actions  = dict(mate=0, hunt=0, rest=0, punish=0, gather=0,)
        # amount of resource possessed by agents
        self.resource_sums = dict(food=0, leisure=0, reputation=0, children=0)
        # expected rewards for each resource
        d = dict(food=0, leisure=0, reputation=0, children=0)
        self.reward_sums = dict([(k, d.copy()) for k in self.actions.keys()])
        # utility of all agents
        self.utility_sum = 0
        # largest utility of any agent
        self.max_utility = -1
        # smallest utility of any agent
        self.min_utility = 99999

    def log_agent(self, agent):
        """ Store stats about passed agent """
        # count agents
        self.num_agents += 1
        # count cooperations/defections
        if agent.last_self_choice: self.cooperated += 1
        else: self.defected += 1
        if agent.last_other_choice: self.cooperated += 1
        else: self.defected += 1
        # count actions
        self.actions[agent.last_action] += 1
        # count utility
        u = agent.utility(agent.get_resources(agent))
        self.utility_sum += u
        if u > self.max_utility: self.max_utility = u
        if u < self.min_utility: self.min_utility = u
        # sum resources
        self.resource_sums['food']     += agent.food
        self.resource_sums['leisure']  += agent.leisure
        self.resource_sums['children'] += agent.children
        self.resource_sums['reputation'] += agent.get_reputation(agent)
        # sum rewards
        for ak in self.actions.keys():
            for rk in self.resource_sums.keys():
                self.reward_sums[ak][rk] += agent.rewards[ak][rk]
