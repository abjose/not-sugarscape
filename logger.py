
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
        # number of agents
        plt.title('Number of agents over time')
        plt.xlabel('time')
        plt.ylabel('# agents')
        plt.plot([r.num_agents for r in self.rounds])
        plt.show()
        
        # average, max, and min utility over time
        plt.title('Average, Max, and Min utility over time')
        plt.xlabel('time')
        plt.ylabel('utility')
        plt.plot([r.utility_sum/float(r.num_agents) for r in self.rounds],
                 label='average')
        plt.plot([r.max_utility for r in self.rounds], label='max')
        plt.plot([r.min_utility for r in self.rounds], label='min')
        plt.legend()
        plt.show()

        # proportion of cooperations to defections over time
        plt.title('Proportion of cooperation over time')
        plt.xlabel('time')
        plt.ylabel('Cooperative interactions / all interactions')
        plt.plot([r.cooperated / float(r.cooperated+r.defected)
                  for r in self.rounds])
        #plt.plot([r.cooperated for r in self.rounds])
        #plt.plot([r.defected for r in self.rounds])
        plt.ylim((0,1))
        plt.show()

        # actions chosen over time
        # total number of actions is just number of agents
        plt.title('Actions chosen over time')
        plt.xlabel('time')
        plt.ylabel('# times action chosen')
        plt.plot([r.actions['mate']/float(r.num_agents) for r in self.rounds],
                 label='mate')
        plt.plot([r.actions['hunt']/float(r.num_agents) for r in self.rounds],
                 label='hunt')
        plt.plot([r.actions['rest']/float(r.num_agents) for r in self.rounds],
                 label='rest')
        plt.plot([r.actions['punish']/float(r.num_agents) for r in self.rounds],
                 label='punish')
        plt.plot([r.actions['gather']/float(r.num_agents) for r in self.rounds],
                 label='gather')
        plt.legend()
        plt.show()

        # possessed resources over time
        plt.title('Possessed resources over time')
        plt.xlabel('time')
        plt.ylabel('Amount possessed')
        plt.plot([r.resource_sums['food'] for r in self.rounds], 
                 label='food')
        plt.plot([r.resource_sums['leisure'] for r in self.rounds], 
                 label='leisure')
        plt.plot([r.resource_sums['children'] for r in self.rounds],
                 label='children')
        plt.plot([r.resource_sums['reputation'] for r in self.rounds],
                 label='reputation')
        plt.legend()
        plt.show()

        # expected rewards for each action over time
        plt.subplot(511)
        plt.title('Expected reward for action over time - mate')
        plt.ylabel('reward amount')        
        r0 = self.rounds[0]
        for rk in r0.resource_sums.keys():
            plt.plot([r.reward_sums['mate'][rk] / float(r.num_agents) 
                      for r in self.rounds], label=rk)
        plt.legend()
        plt.subplot(512)
        plt.title('hunt')
        plt.ylabel('reward amount')        
        for rk in r0.resource_sums.keys():
            plt.plot([r.reward_sums['hunt'][rk] / float(r.num_agents) 
                      for r in self.rounds], label=rk)
        plt.legend()
        plt.subplot(513)
        plt.title('rest')
        plt.ylabel('reward amount')        
        for rk in r0.resource_sums.keys():
            plt.plot([r.reward_sums['rest'][rk] / float(r.num_agents) 
                      for r in self.rounds], label=rk)
        plt.legend()
        plt.subplot(514)
        plt.title('punish')
        plt.ylabel('reward amount')        
        for rk in r0.resource_sums.keys():
            plt.plot([r.reward_sums['punish'][rk] / float(r.num_agents) 
                      for r in self.rounds], label=rk)
        plt.legend()
        plt.subplot(515)
        plt.title('gather')
        plt.ylabel('reward amount')        
        plt.xlabel('time')
        for rk in r0.resource_sums.keys():
            plt.plot([r.reward_sums['gather'][rk] / float(r.num_agents) 
                      for r in self.rounds], label=rk)
        plt.legend()
        plt.show()

        # plot reputations over time?


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
