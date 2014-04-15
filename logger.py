
"""
For logging/plotting information about agents.
"""

class Logger:

    def __init__(self, ):
        self.rounds = [RoundLog()]

    def advance_round(self, ):
        # advance by one round
        self.rounds.append(RoundLog())

    def log_agent(self, agent,):
        # log agent in current round
        self.rounds[-1].log_agent(agent)

    def plot(self, ):
        # plot...
        # for each round...
        #  how many agents cooperated/defected
        #  resources
        #  actions
        #  (average?) expected utility of each action over time
        #  global utility (also be able to see highest/lowest utility...)
        #  number of agents
        pass


class RoundLog:
    
    def __init__(self, ):
        self.num_agents = 0
        self.cooperated = 0
        self.defected   = 0
        self.actions  = dict(mate=0, hunt=0, rest=0, punish=0, gather=0,)
        self.resource_sums = dict(food=0, leisure=0, reputation=0, children=0)
        self.utility_sum = 0
        self.largest_utility = -1
        self.smallest_utility = 99999

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
        if u > self.largest_utility:  self.largest_utility = u
        if u < self.smallest_utility: self.smallest_utility = u
        # sum resources
        self.resource_sums['food']     += agent.food
        self.resource_sums['leisure']  += agent.leisure
        self.resource_sums['children'] += agent.children
        self.resource_sums['reputation'] += agent.get_reputation(agent)

