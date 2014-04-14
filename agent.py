
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
"""

import numpy as np

class Agent:
    max_food_met = 5
    max_leisure_met = 5

    # stag hunt game
    game = {}
    # self, other for both choice and score
    big = max_food_met*3
    lil = max_food_met+5
    game[(True,True)]   = (big,big)
    game[(True,False)]  = (0,  lil)
    game[(False,True)]  = (lil,0)
    game[(False,False)] = (lil,lil)

    def __init__(self, ):
        # food store and rate of consumption
        self.food = np.random.randint(5,26)
        self.food_metabolism = np.random.randint(1,Agent.max_food_met)
        # leisure store and rate of consumption
        self.leisure = np.random.randint(5,26)
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
                            rest = self.rest
                            attack = self.attack,
                            gather = self.gather,)

        # mapping from action to expected resource change
        self.results = dict([(k, dict(food=0, leisure=0, reputation=0)) 
                             for k,v in self.actions.items()])

    def act(self, other):
        """ Choose an action greedily based on perceived future utility. """
        # select action by finding closest marker to perception
        best_action = None
        best_utility = -999
        res = self.get_resources(self)
        for action in self.actions.keys():
            # calculate potential utility
            pu = self.utility(self.add_resources(res, self.results[action]))
            # track if best action
            if pu > best_utility:
                best_utility = pu
                best_action  = action

        # one-liner...
        #action = self.actions[max(self.actions.keys(), key=lambda a: self.utility(self.add_resources(res,self.results[a])))]
 
        # decide if cooperating
        self_choice  = self.cooperates_with(other)
        other_choice = other.cooperates_with(self)

        # do action
        self.actions[action](other, self_choice, other_choice)

        # update reputations
        self.update_reputation(other, other_choice)
        other.update_reputation(self, self_choice)
        # TODO:  consider outcome rather than just whether they cooperated?

        # subtract metabolism from resource store - die if too low

    def get_resources(self, agent):
        """ Return given agent's resources. """
        return dict(food       = agent.food,
                    leisure    = agent.leisure,
                    reputation = self.reputation[agent])

    def add_resources(self, r1, r2):
        """ Add corresponding entries in two resources dicts. """
        return dict([(k, r1[k]+r2[k]) for k in r1.keys()])

    def utility(self, resources):
        # given an agent's resources, return that agent's (perceived) utility
        # calculate food well-being (# rounds unitl starvation)
        fwb = self.food / float(self.food_metabolism)
        # calculate leisure well-being
        lwb = self.leisure / float(self.leisure_metabolism)
        # number of children...
        c = self.children
        # reputation...
        r = self.reputation[self]
        # return sum
        return fwb + lwb + c + r
        # don't use preferences yet?
        #return self.food_pref * resources['food'] \
        #       + self.leisure_pref * resources['leisure'] \
        #       + self.reputation_pref * resources['reputation']

    def reputation(self, agent):
        """ Return reputation of agent or default of 0.5 """
        return self.reputation.get(agent, 0.5)

    def update_reputation(self, agent, other_choice):
        # update reputation dict
        # TODO: make updates nicer - specifically, if agent has high reputation,
        #       maybe make defection seem 'worse'
        # Basically want to modify rep more based on reputation of other
        # like if agent with high rep defects, want to lower own rep more...
        if other_choice:
            self.reputation[agent] = self.constrain(self.reputation[agent]+0.1)
            self.reputation[self]  = self.constrain(self.reputation[self] +0.1)
        else:
            self.reputation[agent] = self.constrain(self.reputation[agent]-0.1)
            self.reputation[self]  = self.constrain(self.reputation[self] -0.1)

    def cooperates_with(self, other):
        # return true if cooperates, false otherwise
        return np.random.uniform() < self.reputation(other)

    def receive_meme(self, other):
        # maybe learn from other
        # should not consider their self reputation?
        pass

    def mate(self, other, self_choice, other_choice):
        # try to mate
        self_food_cost, self_leisure_cost   = 0,0
        other_food_cost, other_leisure_cost = 0,0
        if self_choice:
            self_food_cost,  self_leisure_cost  = self.get_costs(.5) # medium
        if other_choice:
            other_food_cost, other_leisure_cost = other.get_costs(.5)
        # make baby if both cooperate
        if self_choice and other_choice:
            # TODO: ADD GENETIC STUFF
            pass
        # update scores
        self.food     -= self_food_cost
        other.food    -= other_food_cost
        self.leisure  -= self_leisure_cost
        other.leisure -= other_leisure_cost
        # TODO: kinda stupid to choose 'mate' if already decided not to?

    def attack(self, other, self_choice, other_choice):
        # fight!
        # maybe make metabolism correlate to strength?
        # just remove own costs from opponent?
        # also take into account stores of things?
        pass

    def hunt(self, other, self_choice, other_choice):
        # play stag hunt game
        self_food_cost,  self_leisure_cost  = self.get_costs(1.) # hard
        other_food_cost, other_leisure_cost = other.get_costs(1.)
        # calculate scores
        self_score, other_score = Agent.game[(self_choice, other_choice)]
        # update scores
        self.food     += self_score  - self_food_cost
        other.food    += other_score - other_food_cost
        self.leisure  -= self_leisure_cost
        other.leisure -= other_leisure_cost
        # different costs based on cooperate or defect? ehh

    def gather(self, other, self_choice, other_choice):
        # gain some food
        food_cost, leisure_cost = self.get_costs(0.25) # pretty easy
        self.food    += np.random.randint(1,4) - food_cost
        self.leisure -= leisure_cost
        
    def rest(self, other, self_choice, other_choice):
        # increases leisure
        food_cost, _ = self.get_costs(0.1) # easy
        self.food    -= food_cost
        self.leisure += np.random.randin(1,5)

    def get_costs(self, scale):
        # return (food_cost, leisure_cost) tuple based on 'scale' (difficulty)
        food_cost    = max(1, int(round(scale*self.food_metabolism)))
        leisure_cost = max(1, int(round(scale*self.leisure_metabolism)))
        return (food_cost, leisure_cost)

    def make_baby(self, other):
        # combine stuff...mutate...etc.
        # how to add agent to simulation list from here?
        # to combine, could...average parent's markers?
        # and parent's cultures?
        # and utility/percpetion preferences...
        # could add in some random variation

        # make a new Agent
        baby = Agent()

        # combine and mutate 

        pass

    def constrain(self, v):
        # constrain v between -1 and 1
        return min(max(-1.,v),1.)


if __name__=='__main__':
    a = Agent()
    b = Agent()
    b = Agent()
