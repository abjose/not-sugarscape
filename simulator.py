
"""
Brings together other components into a single simulation.
"""

from environment import Environment
from agent import Agent
from logger import Logger


"""
Have a bag of agents, facilitate interactions...
"""

class Simulator:

    def __init__(self, num_agents):
        self.agents = [Agent() for _ in range(num_agents)]
        self.logger = Logger()

    def tick(self, ):
        # keep track of who's still living
        alive = self.agents

        # then iterate through and act
        for a in self.agents:
            a.act(alive)

            if a.food <= 0 or a.leisure <= 0:
                # kill a
                print 'WOE IS ME!'
                alive.remove(a)

            # log agent
            self.logger.log_agent(a)

        # remove dead agents from original list
        self.agents = alive
        # update logger
        self.logger.advance_round()

    def run(self, ):
        i = 0
        while len(self.agents):
            i += 1
            print 'round', i, '\nagents left:', len(self.agents)
            self.tick()

        # plot things
        self.logger.plot()

    # in whichever function makes agents act, make sure to remove
    # agent from list if it dies


if __name__=='__main__':
    # should initially populate environment with agents
    # to tick, select agents in random order to carry out its rules
    
    s = Simulator(10)
    s.run()
