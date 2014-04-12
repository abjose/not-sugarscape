
"""
Simulated environment.
"""

import numpy as np
from random import shuffle

from agent import Agent



"""
TODO
- ADD SOME UTILITY GRAPHING FUNCTIONALITY
- COULD START WRITING PAPER - TALK ABOUT CURRENT STATE AS BASICALLY 
  WITHOUT MORAL CHOICE
- MAKE SURE ITS REALLY EASY TO LOAD UP THIS CURRENT STATE / I.E. MAKE THIS A 
  KIND OF AGENT THAT CAN JUST BE CHOSEN AND WILL BEHAVE LIKE THIS...
- add age....other stuff from sugarscape page
- make rules s.t. can even modify stuff like "eat sugar..."
-- have utility just be another rule?? but like a 'required' rule?
- modify sugar caps to have some kind of distribution...
- maybe have environment construct proper viewer...have get_viewer?
- Make 'sight' and 'stride' different variables? So can see/communicate with 
  stuff far away maybe, but maybe only move a little

"""



class Environment:
    
    def __init__(self, s):
        # use yaml or something to load configuration?
        # size
        self.side = s
        
        # for 'placing' agents
        self.field = np.chararray((s, s), itemsize=5)
        # a dictionary for associating strings with agent objects
        self.agents = dict()

        # keep track of resources as vectors of (current, rate, max)
        # consider enclosing this in a function
        self.sugar = np.zeros((s, s, 3))
        # set current sugar
        self.sugar[:,:,0] = 5#np.random.randint(0, 25, (s, s))
        # set grow-back rate
        self.sugar[:,:,1] = 0#np.random.randint(1, 5, (s, s))
        # set sugar max
        self.sugar[:,:,2] = 5 #500
        # add sugar growback interval? would need counter and actual interval...

    def tick_resources(self, ):
        # maybe keep a list of resources to make shorter if have lots?
        self.sugar[:,:,0] = np.minimum(self.sugar[:,:,0]+self.sugar[:,:,1],
                                       self.sugar[:,:,2])

    def tick(self, ):
        # tick everything
        self.tick_resources()
        # update agents in random order
        agents = [agent for name,agent in self.agents.items()]
        shuffle(agents)
        for agent in agents:
            agent.tick()

    def add_agent(self, ):
        # add an agent to a random location?
        r, c = np.random.randint(0, self.side, 2)
        a = Agent(self, r, c)
        self.agents[a.name] = a
        # VERIFY WON'T GET MODIFIED...

    def kill_agent(self, agent):
        # remove an agent from the simulation
        # remove from field
        self.field[agent.r, agent.c] = ""
        # remove dict entry
        del self.agents[agent.name]

if __name__=='__main__':
    
    from viewer import Viewer

    e = Environment(250)

    for _ in range(500):
        e.add_agent()

    t = 0
    while True:
        print 'tick', t
        t += 1
        e.tick()
        #raw_input()
    
