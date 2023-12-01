import mdp
import util
import random
import collections
from learningAgents import ValueEstimationAgent

class PolicyIterationAgent(ValueEstimationAgent):
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount=0.9, iterations=100):
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.policy = util.Counter()
          # Initialize a policy as a Counter
        for s in self.mdp.getStates():
            policies = self.mdp.getPossibleActions(s)
            if policies:  # Check if there are possible actions for the state
                random_policy = random.choice(policies)
                self.policy[s] = random_policy
        self.values = util.Counter()
        self.counter =0
        self.runPolicyIteration()
        

    def runPolicyIteration(self):
        states = self.mdp.getStates()

        for i in range(self.iterations):
            # Policy Evaluation
            self.values = self.PolicyEvaluation(self.policy)

            # Policy Improvement
            flag = True
            for state in states:
                if not self.mdp.isTerminal(state):
                    old_action = self.policy[state]
                    actions = self.mdp.getPossibleActions(state)
                    max_action = None
                    max_value = -999999
                    for action in actions:
                        q_value = self.computeQValueFromValues(state, action)
                        if q_value > max_value:
                            max_value = q_value
                            max_action = action
                    self.policy[state] = max_action
                    if old_action != max_action:
                        flag = False

            #counter variable is used to count the number of iterations till convergence            
            self.counter+=1

            # if every policy converges then the flag value remains true then we break
            if flag:
                break

    def PolicyEvaluation(self, policy):
        values = util.Counter()
        states = self.mdp.getStates()
        while True:
            delta = 0
            for state in states:
                if not self.mdp.isTerminal(state):
                    # old value of the state
                    v = self.values[state]
                    q = self.computeQValueFromValues(state, policy[state])
                    values[state] = q
                    #delta is used to check convergence
                    delta = max(delta, abs(v - q))
            self.values = values.copy()
            if delta < 1e-6:
                break
        return values
    
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        trans = self.mdp.getTransitionStatesAndProbs(state, action)
        q_value = 0.0
        for trans_state, prob in trans:
            reward = self.mdp.getReward(state, action, trans_state)
            q_value += prob * (reward + self.discount * self.values[trans_state])
        return q_value

    def computeActionFromValues(self, state):
        return self.policy[state]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
