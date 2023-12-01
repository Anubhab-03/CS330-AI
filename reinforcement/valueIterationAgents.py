# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections
import copy

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.counter = 0 # for counting the number of iterations taken to converge
        self.runValueIteration()


    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        
        "*** YOUR CODE HERE ***"
        #getting all possible states
        states = self.mdp.getStates()
        
        for i in range(self.iterations):
            curr_value = util.Counter()
            flag = True
            
            for j in states:
                # if state is terminal then no legal actions are possible
                if self.mdp.isTerminal(j):
                    curr_value[j] = self.mdp.getReward(j,'exit','')
                else:
                    # all possible actions are listed
                    actions = self.mdp.getPossibleActions(j)
                    max_value = -999999
                    for k in actions:
                        #for a particular action the transition state and probability is stored
                        trans = self.mdp.getTransitionStatesAndProbs(j,k)
                        new_v =0.0
                        for iter in trans:
                            new_v+=iter[1]*(self.mdp.getReward(j,k,iter[0])+ self.discount*self.values[iter[0]])

                        #finding the maximum value over all actions
                        max_value = max(new_v,max_value)
                    if(max_value!=-999999):
                       #updating the current value array
                       curr_value[j] = max_value
                        

            self.counter+=1
        
            for it in states:
                if curr_value[it]!=self.values[it]:
                    # if any of the previous value mismatches with the upadated value
                    # then algorithm has yet not converged
                    flag = False

            # if converged then break
            if(flag): 
                
                break
            # updating the values array
            for it in states:
                self.values[it] = curr_value[it] 
            
            
           
            




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # Q(s,a) = sum over all s' (T(s,a,s')*(R(s,a,s')+ gamma*Q(s',a')))
        trans = self.mdp.getTransitionStatesAndProbs(state,action)
        q_value=0.0
        for i in trans:
            q_value+=i[1]*(self.mdp.getReward(state,action,i[0])+self.discount*self.values[i[0]])

        return q_value
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        # if the state is termianl then there are no possible actions
        if self.mdp.isTerminal(state):
            return None
        
        action_list = self.mdp.getPossibleActions(state)
        action=""
        max_value = -999999
        for i in action_list:
            q = self.computeQValueFromValues(state,i)
            if(q>max_value):
                max_value = q
                action = i
        # returning the action which gives the maximum value 
        return action
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
