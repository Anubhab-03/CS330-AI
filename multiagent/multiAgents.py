# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://acls
# i.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

#--------------------------------------------------------------------
# Group Number - 8                                                  -
# Group Members - Anubhab Chakraborty(Roll No. - 2106306)           -
#               - Akhil Thirukonda Sivakumar (Roll No. - 2103106)   -
#--------------------------------------------------------------------

import math
from util import manhattanDistance
from game import Directions
import random, util
#import sys
from game import Agent,Actions
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        ghostPositions = []
        
        for i in newGhostStates:
            ghostPositions.append(i.configuration.pos)
        
        for i in ghostPositions:
            if (newScaredTimes[ghostPositions.index(i)]==0):
                if manhattanDistance(newPos, i) < 2: return -math.inf

        currFood = currentGameState.getNumFood()
        newFoodnum = len(newFood.asList())
        if newFoodnum<currFood: return math.inf

        min_distance = math.inf
        for food in newFood.asList():
            distance = manhattanDistance(newPos, food)
            min_distance = min(min_distance, distance)
        return 1.0 / min_distance 

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState, depth):
            # Check if we've reached the desired depth or if the game is in a terminal state 
            if depth+1 == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            #initialize the maximum value to negative infinity
            maxi = float("-inf")

            # Get legal actions for the current player
            actions = gameState.getLegalActions(0)
            for action in actions:
                # Generate the successor state after taking the current action
                successor_state = gameState.generateSuccessor(0, action)

                #call min value for the next player with index 1 and increased depth
                value = min_value(successor_state, depth + 1,1)

                #update the maximum value
                maxi = max(maxi, value)
            return maxi

        def min_value(gameState, depth, index):
            # Check if we've reached the desired depth or if the game is in a terminal state
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
             #initialize the minimum value to positive infinity
            mini = float("inf")
            actions = gameState.getLegalActions(index)
            for action in actions:
                # Generate the successor state after taking the current action
                successor_state = gameState.generateSuccessor(index, action)
                #value = max_value(successor_state,depth)

                #if its the last opponent player then next player is maximising agent thus max_value is called
                if index == gameState.getNumAgents() - 1:
                    value = max_value(successor_state, depth)

                    #if its not the last player then min value is called for the other opponents
                else:
                    value = min_value(successor_state, depth, index + 1)

                #update the minimum value
                mini = min(mini, value)

            # finally return the min value achieved after coming out from loop 
            return mini


        # Main function for choosing the best action
        actions = gameState.getLegalActions(0)
        curr_max = float("-inf")
        action_path = None

        # Iterate through possible actions for player 0
        for action in actions:
            successor = gameState.generateSuccessor(0, action)

            #find the min value for player 1
            value = min_value(successor, 0, 1)

            # update the max value and the action path to be taken
            if value > curr_max:
                curr_max = value
                action_path = action

        # return the final action path
        return action_path

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState, depth,alpha,beta):
            # Check if we've reached the desired depth or if the game is in a terminal state 
            if depth+1 == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            #initialize the maximum value to negative infinity
            maxi = float("-inf")
            actions = gameState.getLegalActions(0)
            for action in actions:
                # Call min_value for the next player with increased depth, alpha, and beta values
                successor_state = gameState.generateSuccessor(0, action)
                value = min_value(successor_state, depth + 1,1,alpha,beta)
                maxi = max(maxi, value)
                
                # Pruning: If the maximum value is greater than beta, return the current maximum
                if maxi>beta:
                    #beta = maxi
                    return maxi
                
                # Update alpha (the best value found so far for the maximizing player)
                alpha = max(alpha,maxi)
            return maxi

        def min_value(gameState, depth, index,alpha,beta):
            # Check if the game is in a terminal state (win or lose)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            mini = float("inf")
            actions = gameState.getLegalActions(index)
            for action in actions:
                successor_state = gameState.generateSuccessor(index, action)
                if index == gameState.getNumAgents() - 1:
                    value = max_value(successor_state, depth,alpha,beta)
                    mini = min(value,mini)

                    # Pruning: If the minimum value is less than alpha, return the current minimum
                    if mini<alpha:
                        return mini
                    
                    # Update beta (the best value found so far for the minimizing player)
                    beta = min(beta,mini)
                else:
                    value = min_value(successor_state, depth, index + 1,alpha,beta)
                    #mini = max(float("-inf"), value)
                    mini = min(value,mini)

                    # Pruning: If the minimum value is less than alpha, return the current minimum
                    if mini<alpha:
                        return mini
                    
                    # Update beta (the best value found so far for the minimizing player)
                    beta = min(beta,mini)

                    
                
            return mini

        # Main function for choosing the best action
        actions = gameState.getLegalActions(0)
        curr_max = float("-inf")
        action_path = None
        alpha = float("-inf")
        beta = float("inf")
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = min_value(successor, 0, 1,alpha,beta)

            # Update the maximum value and the best action
            if value > curr_max:
                curr_max = value
                action_path = action

            # Pruning: If the maximum value is greater than beta, return the current best action
            if value > beta:
                return action_path

            # Update alpha (the best value found so far for the maximizing player)
            alpha = max(value, alpha)


        return action_path

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def max_value(gameState, depth):
            if depth+1 == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            maxi = float("-inf")
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor_state = gameState.generateSuccessor(0, action)
                value = expecti_value(successor_state, depth + 1,1)
                maxi = max(maxi, value)
            return maxi

        def expecti_value(gameState, depth, index):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            #mini = float("inf")
            expectimax =0
            
            actions = gameState.getLegalActions(index)
            length = len(actions)
            for action in actions:
                successor_state = gameState.generateSuccessor(index, action)
                if index == gameState.getNumAgents() - 1:
                    value = max_value(successor_state, depth)
                else:
                    value = expecti_value(successor_state, depth, index + 1)

                expectimax = expectimax + value
                
                # mini = min(mini, value)
            return float(expectimax)/float(length)

        actions = gameState.getLegalActions(0)
        curr_max = float("-inf")
        action_path = None

        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = expecti_value(successor, 0, 1)
            if value > curr_max:
                curr_max = value
                action_path = action

        return action_path

        
        
        util.raiseNotDefined()

def closestItemDistance(currentGameState, items):
    """Returns the maze distance to the closest item present in items"""

    # BFS to find the maze distance from position to closest item
    walls = currentGameState.getWalls()

    start = currentGameState.getPacmanPosition()

    # Dictionary storing the maze distance from start to any given position
    distance = {start: 0}

    # Set of visited positions in order to avoid revisiting them again
    visited = {start}

    queue = util.Queue()
    queue.push(start)

    while not queue.isEmpty():

        position = x, y = queue.pop()

        if position in items: return distance[position]

        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:

            dx, dy = Actions.directionToVector(action)
            next_position = nextx, nexty = int(x + dx), int(y + dy)

            if not walls[nextx][nexty] and next_position not in visited:
                queue.push(next_position)
                visited.add(next_position)
                # A single action separates position from next_position, so the distance is 1
                distance[next_position] = distance[position] + 1

    return None

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    
      DESCRIPTION:
      The following features are considered and combined:
        - Compute the maze distance to the closest food dot
        - Compute the maze distance to the closest capsule
        - If the ghost is scared and close, eat it
        - If the ghost is not scared and close, run away
        - Take into account score (the longer the game is, the lower the score will be)    

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    infinity = float('inf')
    position = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    ghostStates = currentGameState.getGhostStates()
    foodList = currentGameState.getFood().asList()
    capsuleList = currentGameState.getCapsules()

    if currentGameState.isWin(): return math.inf
    if currentGameState.isLose(): return -math.inf
    
    #calculating ghost factor
    for ghost in ghostStates:
        d = manhattanDistance(position, ghost.getPosition())
        if ghost.scaredTimer > 6 and d < 2:
            return math.inf
    ghostFactor = 1.0/d
    
    
    # Calculating food factor
    foodFactor = 1.0/closestItemDistance(currentGameState, foodList)

    # Calculating capsule factor
    capsuleFactor = closestItemDistance(currentGameState, capsuleList)
    capsuleFactor = 0.0 if capsuleFactor is None else 1.0/capsuleFactor

    # coefficients are arbitrary 
    return 10.0*foodFactor + 5.0*score + 0.5*capsuleFactor - 0.1*ghostFactor

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
