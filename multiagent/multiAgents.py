# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
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
        # return successorGameState.getScore()
        # Get the current score as base
        score = successorGameState.getScore()
        
        # Get food positions as a list
        foodList = newFood.asList()
        
        # If there's food, find the closest food
        if foodList:
            # Calculate distances to all food and find the minimum
            foodDistances = [manhattanDistance(newPos, food) for food in foodList]
            closestFoodDistance = min(foodDistances)
            # Use reciprocal of distance (closer food = higher score)
            score += 1.0 / (closestFoodDistance + 1)  # Add 1 to avoid division by zero
        else:
            # No food left, this is good!
            score += 1000
        
        # Consider ghost positions and scared timers
        for i, ghostState in enumerate(newGhostStates):
            ghostPos = ghostState.getPosition()
            ghostDistance = manhattanDistance(newPos, ghostPos)
            scaredTime = newScaredTimes[i]
            
            if scaredTime > 0:
                # Ghost is scared - Pacman can eat it for points
                if ghostDistance <= 1:
                    score += 200  # Bonus for being close to scared ghost
                else:
                    # Encourage moving towards scared ghosts (but not too much)
                    score += 50.0 / (ghostDistance + 1)
            else:
                # Ghost is dangerous - avoid it
                if ghostDistance <= 1:
                    score -= 500  # Heavy penalty for being close to dangerous ghost
                elif ghostDistance <= 2:
                    score -= 100  # Moderate penalty for being near dangerous ghost
                else:
                    # Small penalty that decreases with distance
                    score -= 10.0 / (ghostDistance + 1)
        
        return score

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
        # util.raiseNotDefined()
        def minimax(state, depth, agentIndex):
            """
            Recursive minimax function.
            state: current game state
            depth: remaining depth to search
            agentIndex: current agent (0 for Pacman, 1+ for ghosts)
            """
            # Terminal states
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            # Leaf nodes (reached max depth)
            if depth == 0:
                return self.evaluationFunction(state)
            
            # Get legal actions for current agent
            legalActions = state.getLegalActions(agentIndex)
            
            # If no legal actions, evaluate current state
            if not legalActions:
                return self.evaluationFunction(state)
            
            # Determine next agent
            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            
            # If next agent is Pacman (agent 0), we've completed a full ply
            # and should decrease depth
            if nextAgentIndex == 0:
                nextDepth = depth - 1
            else:
                nextDepth = depth
            
            # Pacman's turn (MAX player)
            if agentIndex == 0:
                bestValue = float('-inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = minimax(successor, nextDepth, nextAgentIndex)
                    bestValue = max(bestValue, value)
                return bestValue
            
            # Ghost's turn (MIN player)
            else:
                worstValue = float('inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = minimax(successor, nextDepth, nextAgentIndex)
                    worstValue = min(worstValue, value)
                return worstValue
        
        # Get legal actions for Pacman
        legalActions = gameState.getLegalActions(0)
        
        # Find the best action by evaluating each successor
        bestAction = None
        bestValue = float('-inf')
        
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            # Start with agent 1 (first ghost) and full depth
            value = minimax(successor, self.depth, 1)
            
            if value > bestValue:
                bestValue = value
                bestAction = action
        
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        def maxValue(state, depth, agentIndex, alpha, beta):
            """
            MAX player (Pacman) - maximize value
            """
            # Terminal states
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            # Leaf nodes (reached max depth)
            if depth == 0:
                return self.evaluationFunction(state)
            
            # Get legal actions for current agent
            legalActions = state.getLegalActions(agentIndex)
            
            # If no legal actions, evaluate current state
            if not legalActions:
                return self.evaluationFunction(state)
            
            # Determine next agent
            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            
            # If next agent is Pacman (agent 0), we've completed a full ply
            # and should decrease depth
            if nextAgentIndex == 0:
                nextDepth = depth - 1
            else:
                nextDepth = depth
            
            v = float('-inf')
            
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                
                # Determine if next agent is MAX or MIN
                if nextAgentIndex == 0:  # Next is Pacman (MAX)
                    value = maxValue(successor, nextDepth, nextAgentIndex, alpha, beta)
                else:  # Next is ghost (MIN)
                    value = minValue(successor, nextDepth, nextAgentIndex, alpha, beta)
                
                v = max(v, value)
                
                # Alpha-beta pruning (don't prune on equality)
                if v > beta:
                    return v
                
                alpha = max(alpha, v)
            
            return v
        
        def minValue(state, depth, agentIndex, alpha, beta):
            """
            MIN player (Ghosts) - minimize value
            """
            # Terminal states
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            # Leaf nodes (reached max depth)
            if depth == 0:
                return self.evaluationFunction(state)
            
            # Get legal actions for current agent
            legalActions = state.getLegalActions(agentIndex)
            
            # If no legal actions, evaluate current state
            if not legalActions:
                return self.evaluationFunction(state)
            
            # Determine next agent
            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            
            # If next agent is Pacman (agent 0), we've completed a full ply
            # and should decrease depth
            if nextAgentIndex == 0:
                nextDepth = depth - 1
            else:
                nextDepth = depth
            
            v = float('inf')
            
            for action in legalActions:
                successor = state.generateSuccessor(agentIndex, action)
                
                # Determine if next agent is MAX or MIN
                if nextAgentIndex == 0:  # Next is Pacman (MAX)
                    value = maxValue(successor, nextDepth, nextAgentIndex, alpha, beta)
                else:  # Next is ghost (MIN)
                    value = minValue(successor, nextDepth, nextAgentIndex, alpha, beta)
                
                v = min(v, value)
                
                # Alpha-beta pruning (don't prune on equality)
                if v < alpha:
                    return v
                
                beta = min(beta, v)
            
            return v
        
        # Get legal actions for Pacman
        legalActions = gameState.getLegalActions(0)
        
        # Find the best action by evaluating each successor
        bestAction = None
        bestValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            # Start with agent 1 (first ghost) and full depth
            value = minValue(successor, self.depth, 1, alpha, beta)
            
            if value > bestValue:
                bestValue = value
                bestAction = action
            
            # Update alpha for the root level
            alpha = max(alpha, value)
        
        return bestAction

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
        # util.raiseNotDefined()
        def expectimax(state, depth, agentIndex):
            """
            Recursive expectimax function.
            state: current game state
            depth: remaining depth to search
            agentIndex: current agent (0 for Pacman, 1+ for ghosts)
            """
            # Terminal states
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            
            # Leaf nodes (reached max depth)
            if depth == 0:
                return self.evaluationFunction(state)
            
            # Get legal actions for current agent
            legalActions = state.getLegalActions(agentIndex)
            
            # If no legal actions, evaluate current state
            if not legalActions:
                return self.evaluationFunction(state)
            
            # Determine next agent
            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            
            # If next agent is Pacman (agent 0), we've completed a full ply
            # and should decrease depth
            if nextAgentIndex == 0:
                nextDepth = depth - 1
            else:
                nextDepth = depth
            
            # Pacman's turn (MAX player)
            if agentIndex == 0:
                bestValue = float('-inf')
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = expectimax(successor, nextDepth, nextAgentIndex)
                    bestValue = max(bestValue, value)
                return bestValue
            
            # Ghost's turn (EXPECTATION player - random choice)
            else:
                totalValue = 0
                numActions = len(legalActions)
                
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = expectimax(successor, nextDepth, nextAgentIndex)
                    totalValue += value
                
                # Return the average (expectation) of all possible ghost actions
                return totalValue / numActions
        
        # Get legal actions for Pacman
        legalActions = gameState.getLegalActions(0)
        
        # Find the best action by evaluating each successor
        bestAction = None
        bestValue = float('-inf')
        
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            # Start with agent 1 (first ghost) and full depth
            value = expectimax(successor, self.depth, 1)
            
            if value > bestValue:
                bestValue = value
                bestAction = action
        
        return bestAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    
    # Get current position and state information
    pacmanPos = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    
    # Start with the current score
    score = currentGameState.getScore()
    
    # Food evaluation
    foodList = foodGrid.asList()
    if foodList:
        # Find the closest food
        foodDistances = [manhattanDistance(pacmanPos, food) for food in foodList]
        closestFoodDistance = min(foodDistances)
        
        # Reward for being close to food (reciprocal of distance)
        score += 10.0 / (closestFoodDistance + 1)
        
        # Penalty for having too much food left (encourages eating)
        remainingFood = len(foodList)
        score -= remainingFood * 4
    else:
        # No food left - great!
        score += 1000
    
    # Ghost evaluation
    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        ghostDistance = manhattanDistance(pacmanPos, ghostPos)
        scaredTime = ghostState.scaredTimer
        
        if scaredTime > 0:
            # Ghost is scared - Pacman can eat it
            if ghostDistance <= 1:
                score += 200  # Big bonus for being close to scared ghost
            else:
                # Encourage moving towards scared ghosts
                score += 100.0 / (ghostDistance + 1)
        else:
            # Ghost is dangerous - avoid it
            if ghostDistance <= 1:
                score -= 1000  # Heavy penalty for being close to dangerous ghost
            elif ghostDistance <= 2:
                score -= 500   # Moderate penalty for being near dangerous ghost
            else:
                # Small penalty that decreases with distance
                score -= 20.0 / (ghostDistance + 1)
    
    # Capsule evaluation
    if capsules:
        capsuleDistances = [manhattanDistance(pacmanPos, capsule) for capsule in capsules]
        closestCapsuleDistance = min(capsuleDistances)
        
        # Reward for being close to power pellets
        score += 50.0 / (closestCapsuleDistance + 1)
    
    return score

# Abbreviation
better = betterEvaluationFunction
