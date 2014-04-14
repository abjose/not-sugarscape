
"""
Agents for the (not)sugarscape.
"""

"""
TODO
- consider adding cultural stuff...
- every tick, have chance to change own stuff slightly (or completely) based
  on your utility
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

        # preferences for utility
        self.food_pref    = self.food_metabolism   /float(Agent.max_food_met)
        self.leisure_pref = self.leisure_metabolism/float(Agent.max_leisure_met)
        self.rep_pref     = np.random.uniform(-1,1)
        self.coop_pref    = np.random.uniform(-1,1) # need?

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
        for :
            pass

        #HOW TO TEMP. CHANGE AGENTS STORES? JUST HAVE A GET_RESOURCES
        #FUNCTION THAT IS PASSED TO THE UTILITY FUNCTION?


        p = self.perception(other)
        action = self.actions[min(self.actions.keys(), key=lambda x:abs(x-p))]

        # IF LIKE, SHARE INFORMATION WITH THEM
        # choose if like based on cooperation? or ingroup/rep?

        # decide if cooperating
        self_choice  = self.cooperates_with(other)
        other_choice = other.cooperates_with(self)

        # do action
        action(other, self_choice, other_choice)

        # update reputations
        self.update_reputation(other, other_choice)
        other.update_reputation(self, self_choice)
        # TODO:  consider outcome rather than just whether they cooperated?

    def get_resources(self, agent):
        """ Return given agent's resources. """
        return dict(food       = agent.food,
                    leisure    = agent.leisure,
                    reputation = self.reputation[agent])

    def utility(self, resources):
        # given an agent's resources, return that agent's (perceived) utility
        return self.food_pref * resources['food'] \
               + self.leisure_pref * resources['leisure'] \
               + self.reputation_pref * resources['reputation']

    def update_reputation(self, agent, other_choice):
        # update reputation dict
        # update perceived self reputation as well as other's reputation
        # if other cooperated, increase their reputation and increase self rep
        # else, decrease theirs and own
        # perhaps change 'step' based on previous perception of them? Like
        # will lower perception of good more if they defect?
        pass

    def cooperates_with(self, other):
        # return true if cooperates, false otherwise
        return np.random.uniform(-1,1) < self.perception(other)

    def receive_meme(self, other):
        # maybe learn from other
        # should not consider their self reputation?
        pass

    def mate(self, other, self_choice, other_choice):
        # try to mate
        # what's the point of having a baby?
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
