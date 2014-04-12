
"""
Brings together other components into a single simulation.
"""

from environment import Environment
from agent import Agent


"""
Have a bag of agents, facilitate interactions...
"""

class Simulator:

    def __init__(self, ):
        self.agents = []

    def tick(self, ):
        # shuffle agents
        np.random.shuffle(self.agents)
        # keep track of who's still living
        alive = self.agents
        # then iterate through and act
        for a in self.agents:
            a.tick(alive)
            if a.food <= 0 or a.leisure <= 0:
                # kill a
                print 'WOE IS ME!'
                alive.remove(a)
        # remove dead agents from original list
        self.agents = alive

    def run(self, ):
        while True:
            self.tick()

    # in whichever function makes agents act, make sure to remove
    # agent from list if it dies


if __name__=='__main__':
    # should initially populate environment with agents
    # to tick, select agents in random order to carry out its rules
    
    pass
