
"""
Agents for the (not)sugarscape.
"""

"""
TODO
- consider adding cultural stuff...
- every tick, have chance to change own stuff slightly (or completely) based
  on your utility
- add memetic communication stuff to act()
- add variable action costs back in?
- kinda weird that still calculate cooperation on non-social tasks
- MAKE PUNISHMENT BETTER
- add initial better guesses to rewards?
- verify that behavior is appropriate when only 1 agent left - shouldn't try
  to mate with self, etc... MAYBE THIS IS GOOD PLACE TO INSERT DISTINCTION
  BETWEEN SOCIAL AND NON-SOCIAL ACTIONS
"""

import numpy as np
import pprint

class Agent:
    max_food_met = 3
    max_leisure_met = 3

    # stag hunt or prisoner's dilemma
    game = {}
    # self, other for both choice and score
    big = max_food_met+10#+5
    lil = max_food_met+5#+10
    game[(True,True)]   = (big,big)
    game[(True,False)]  = (-17, lil+22)
    game[(False,True)]  = (lil+22, -17)
    game[(False,False)] = (lil,lil)

    def __init__(self, ):
        # food store and rate of consumption
        self.food = 20#np.random.randint(15,26)
        self.food_metabolism = np.random.randint(1,Agent.max_food_met)
        # leisure store and rate of consumption
        self.leisure = 20#np.random.randint(15,26)
        self.leisure_metabolism = np.random.randint(1,Agent.max_leisure_met)

        # number of children created
        self.children = 0

        # preferences for utility
        self.food_pref    = np.random.uniform()
        self.leisure_pref = np.random.uniform()
        self.rep_pref     = np.random.uniform()
        self.coop_pref    = np.random.uniform() # need?

        # dict of reputations
        self.reputation = dict()
       
        # dict of possible actions
        self.actions = dict(mate = self.mate,
                            hunt = self.hunt,
                            rest = self.rest,
                            punish = self.punish,
                            gather = self.gather,)

        # mapping from action to expected resource change
        d = dict(food=5, leisure=5, reputation=5, children=5)
        self.rewards = dict([(k, d.copy()) 
                             for k in self.actions.keys() + 
                             ['cooperate', 'defect']])

        # some logging stuff
        self.last_self_choice = None
        self.last_other_choice = None
        self.last_action = None

    def act(self, agents):
        """ Choose an action greedily based on perceived future utility. """
        # choose an agent to interact with (if necessary?)
        other = np.random.choice(agents)

        # select action by finding closest marker to perception
        best_action = None
        best_utility = -999
        res = self.get_resources(self)
        for action in self.actions.keys():
            # calculate potential utility
            pu = self.utility(self.add_resources(res, self.rewards[action]))
            # track if best action
            if pu > best_utility:
                best_utility = pu
                best_action  = action

        # one-liner...
        #action = self.actions[max(self.actions.keys(), key=lambda a: self.utility(self.add_resources(res,self.rewards[a])))]
 
        # decide if cooperating
        self_choice  = self.cooperates_with(other)
        #if self_choice: print 'COOPERATING!'
        #else: print 'DEFECTING!'
        other_choice = other.cooperates_with(self)

        # do action
        if best_action == 'mate':
            # add baby if had one
            baby = self.mate(other, self_choice, other_choice)
            if baby: agents.append(baby)
        else:
            self.actions[best_action](other, self_choice, other_choice)

        # update reputations
        if action in ['mate', 'hunt']:
            self.update_reputation(other, other_choice)
            other.update_reputation(self, self_choice)

        # update perception of rewards
        new_res = self.get_resources(self)
        self.update_rewards(best_action, res, new_res)
        if self_choice: self.update_rewards('cooperate', res, new_res)
        else:           self.update_rewards('defect', res, new_res)
        if other_choice: other.update_rewards('cooperate', res, new_res)
        else:            other.update_rewards('defect', res, new_res)
        
        # subtract metabolism from resource store
        self.food    -= self.food_metabolism
        self.leisure -= self.leisure_metabolism

        # update logging variables
        self.last_self_choice = self_choice
        self.last_other_choice = other_choice
        self.last_action = best_action

    def get_resources(self, agent):
        """ Return given agent's resources. """
        return dict(food       = agent.food,
                    leisure    = agent.leisure,
                    reputation = self.get_reputation(agent),
                    children   = agent.children)

    def add_resources(self, r1, r2):
        """ Add corresponding entries in two resources dicts. """
        return dict([(k, r1[k]+r2[k]) for k in r1.keys()])

    def update_rewards(self, action, r1, r2):
        # given two sets of resources, find difference and update rewards dict
        # assumes r1 is from before r2
        for k in r1.keys():
            self.rewards[action][k] += r2[k] - r1[k]
            self.rewards[action][k] /= 2.

    def utility(self, resources):
        # given an agent's resources, return that agent's (perceived) utility
        # calculate food well-being (# rounds unitl starvation)
        fwb = resources['food'] / float(self.food_metabolism)
        # calculate leisure well-being
        lwb = resources['leisure'] / float(self.leisure_metabolism)
        # number of children...
        c = 5*resources['children']
        # reputation...
        r = resources['reputation']
        # return sum
        # don't use preferences yet?
        return fwb + lwb + c + r

    def get_reputation(self, agent):
        """ Return reputation of agent or default of 0.5 """
        return self.reputation.get(agent, 0.5)

    def update_reputation(self, agent, other_choice):
        """ update reputation dict """
        # TODO: make updates nicer - specifically, if agent has high reputation,
        #       maybe make defection seem 'worse'
        # Basically want to modify rep more based on reputation of other
        # like if agent with high rep defects, want to lower own rep more...
        if other_choice:
            self.reputation[agent]=self.constrain(self.get_reputation(agent)+.1)
            self.reputation[self]=self.constrain(self.get_reputation(self)+.1)
        else:
            self.reputation[agent]=self.constrain(self.get_reputation(agent)-.1)
            self.reputation[self]=self.constrain(self.get_reputation(self) -.1)

    def cooperates_with(self, other):
        # return true if cooperates, false otherwise
        # TODO: INCLUDE UTILITY CALC
        # TODO: evolve weights to these too...
        #return np.random.uniform() < self.get_reputation(other)
        res = self.get_resources(self)
        cu = self.utility(self.add_resources(res, self.rewards['cooperate']))
        du = self.utility(self.add_resources(res, self.rewards['defect']))
        return (self.get_reputation(other)-.5)*5. + cu > du
        # STABLE-ISH AT *1.!

    def receive_meme(self, other):
        # maybe learn from other
        # should not consider their self reputation?
        pass

    def mate(self, other, self_choice, other_choice):
        # try to mate
        if self_choice and other_choice:
            # make a new Agent
            baby = Agent()
            # TODO: SHOULD INFLUENCE BASED ON PARENT'S ATTRIBUTES

            # set baby's reputation high
            baby.reputation[self]  = 1.
            baby.reputation[other] = 1.

            # costly!!
            self.food  -= 2
            other.food -= 2
            self.leisure  -= 2
            other.leisure -= 2

            # increase baby count
            self.children += 1

            return baby
        return None

    def punish(self, other, self_choice, other_choice):
        # punish the other agent - mostly affects reputation
        self.reputation[other] = self.constrain(self.get_reputation(other)-0.1)
        self.reputation[self]  = self.constrain(self.get_reputation(self) +0.1)
        # uhh, update other agent's reputation dict?

    def hunt(self, other, self_choice, other_choice):
        # play stag hunt game
        self_score, other_score = Agent.game[(self_choice, other_choice)]
        # update scores
        self.food  += self_score
        other.food += other_score

    def gather(self, other, self_choice, other_choice):
        # gain some food
        self.food += np.random.randint(1,5)
        
    def rest(self, other, self_choice, other_choice):
        # increases leisure
        self.leisure += np.random.randint(1,5)

    def constrain(self, v):
        # constrain v between -1 and 1
        return min(max(-1.,v),1.)


class Government:

    """
    Should just tax negative interactions, add extra reward to positive ones
    interesting to relate this to norm punishment vs. reward stuff
    add something evaluating future utility to decision to cooperate?
    just keep track of change in utility based on cooperation vs defection
    decisions...
    """


    def __init__(self, ):
        pass




if __name__=='__main__':
    a = Agent()
    b = Agent()
    b = Agent()
