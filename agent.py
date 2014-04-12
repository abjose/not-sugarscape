
"""
Agents for the (not)sugarscape.
"""

"""
TODO
- add way to construct new agent given parents
- WHERE TO USE LEISURE? EVERYWHERE FOOD IS???
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
        # food store / initial endowment
        self.food = np.random.randint(5,26)
        # rate of food store consumption
        self.food_metabolism = np.random.randint(1,Agent.max_food_met)
        # leisure store / initial endowment
        self.leisure = np.random.randint(5,26)
        # rate of leisure store consumption
        self.leisure_metabolism = np.random.randint(1,Agent.max_leisure_met)

        # number of other agents to interact with in a round
        self.sociability = 3

        # cultural marker - be lame and just use a string
        #self.culture = ...

        # dict of reputations
        self.reputations = dict()
        
        # preferences for utility
        self.food_pref    = self.food_metabolism   /float(self.max_food_met)
        self.leisure_pref = self.leisure_metabolism/float(self.max_leisure_met)

        # preferences for perception
        self.cooperation_pref = np.random.uniform(-1,1)
        self.success_pref     = np.random.uniform(-1,1)
        self.reputation_pref  = np.random.uniform(-1,1)
        #self.ingroup_pref     = np.random.uniform(-1,1)

        # dict of possible actions keyed on markers for action selection
        self.actions = dict()
        self.actions[np.random.uniform(-1,1)] = self.mate
        self.actions[np.random.uniform(-1,1)] = self.attack
        self.actions[np.random.uniform(-1,1)] = self.hunt
        self.actions[np.random.uniform(-1,1)] = self.gather
        self.actions[np.random.uniform(-1,1)] = self.rest
        
    def tick(self, agents):
        # given a list of agents composing the world, interact with some
        for _ in range(self.sociability):
            other = np.random.choice(agents)
            self.act(other)

    def perception(self, other):
        # get own perception of other agent
        return self.success_pref * self.utility(other) \
               + self.reputation_pref * self.reputations[other] \
               #+ self.ingroup_pref * self.cultural_distance(other)

    def cultural_distance(self, other):
        pass

    def utility(self, agent):
        return self.food_pref * agent.food \
               + self.leisure_pref * agent.leisure \
               + self.reputation_pref * self.reputations[agent] #\ 
               # + global stuff?

    def reputation(self, agent):
        return self.reputations.get(agent, 0.)

    def update_reputation(self, agent, other_choice):
        # update reputation dict
        # update perceived self reputation as well as other's reputation
        # if other cooperated, increase their reputation and increase self rep
        # else, decrease theirs and own
        pass

    def cooperates_with(self, other):
        # return true if cooperates, false otherwise
        return np.random.uniform(-1,1) < self.perception(other)

    def receive_meme(self, other):
        # maybe learn from other
        # should not consider their self reputation?
        pass

    def act(self, other):
        # select an action, carry out, update reputations, etc.
        # select action by finding closest marker to perception
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


if __name__=='__main__':
    a = Agent()
    b = Agent()
    b = Agent()
