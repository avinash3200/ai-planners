#!/usr/bin/python
# -*- coding: utf-8 -*-

# Tushar Agarwal
# Shailesh Mani Pandey

# AI Lab 4

from __future__ import print_function
import sys
from heapq import *
import time
import random

# Globals:

bfsNumNodesExpanded = 0
"""
This variable keeps track of total number of nodes expanded in breadth-first search.
"""

aStarNumNodesExpanded = 0
"""
This variable keeps track of total number of nodes expanded in A-Star search.
"""

class ArgTypes:

    """
    This class contains constants for different types of arguments.
    """

    VARIABLE = 0
    TERMINAL = 1


class Arg:
    """
    This class represents an argument.
    """

    def __init__(
        self,
        argType,
        argValue,
        isNegation,
        ):
        """
        Initializes the argument using `argType` and `argValue`.
        """

        self.type = argType
        """
        Type of the argument.
        """

        self.value = argValue
        """
        Value of the argument.
        """

        self.isNegation = isNegation
        """
        Helps in distinguishing between positive and negative literals.
        """

    def __str__(self):
        """
        Returns a human-friendly representation of
        the argument.
        """

        retStr = ''

        if self.isNegation:
            retStr += '~'

        if self.type == ArgTypes.TERMINAL:
            retStr += str(self.value).upper()
        else:
            retStr += str(self.value).lower()

        return retStr

    def isVariable(self):
        """
        Returns true if 'Arg' object is a variable.
        """

        return self.type == ArgTypes.VARIABLE

    def __eq__(self, other):
        """
        Checks the equality of two `Arg` objects.
        """

        return self.type == other.type and self.value == other.value \
            and self.isNegation == other.isNegation

    def __ne__(self, other):
        """
        Checks the inequality of two `Arg` objects.
        """

        return not self.__eq__(other)


class PropositionTypes:
    """
    This class contains constants for different types of propositions.
    """

    ON = 'on'
    ONTABLE = 'ontable'
    CLEAR = 'clear'
    HOLD = 'hold'
    EMPTY = 'empty'


class State:
    """
    This class represents the current state.
    This represents a conjuction of `TrueSentence` objects.
    """

    def __init__(self, trueSentenceList, groundTermList):
        """
        Initializes a `State` object.
        """

        self.trueSentenceList = list(trueSentenceList)
        """
        A list of objects of class TrueSentence.
        """

        self.groundTermList = list(groundTermList)
        """
        A list of ground `Arg` objects in sentences in the `trueSentenceList` list.
        """

        self.prevState = None
        """
        This variable is used to figure out a path after searching is done.
        """

        self.prevAction = None
        """
        Stores the action taken to reach to this `State`.
        """

        self.prevAssignments = None
        """
        Stores the assignments made in the previous state to reach this state.
        """

        self.prevPrintData = ''
        """
        Stores the string representing a combination of `self.prevAction`
        and `self.prevAssignments`.
        """

        self.depth = 0
        """
        Housekeeping variable used to print progress.
        """

        self.heuristicValue = 0
        """
        Value used in A-Star search.
        """

    def tracePath(self):
        """
        Trace path from initial state to `self`.
        Returns a dictionary with:
        (1) A string with actions (in order) in plan.
        (2) A list of states in the plan.
        """

        pathList = []
        current = self

        while current:
            pathList.append(current)
            current = current.prevState

        pathList.reverse()

        retStr = ''
        for state in pathList:
            retStr += state.prevPrintData + '\n'

        retDict = dict()
        retDict['outputString'] = retStr.strip()
        retDict['stateList'] = pathList

        return retDict

    def addTrueSentence(self, trueSentence):
        """
        Adds the `trueSentence` object to the state.
        """

        for arg in trueSentence.argList:
            if arg.isVariable():
                return

        for arg in trueSentence.argList:
            alreadyPresent = False
            for selfArg in self.groundTermList:
                if arg == selfArg:
                    alreadyPresent = True
                    break
            if not alreadyPresent:
                self.groundTermList.append(arg)

        self.trueSentenceList.append(trueSentence)

    def removeTrueSentence(self, trueSentenceArg):
        """
        Removes all objects "equal to" the `trueSentence` object from the state.
        """

        self.trueSentenceList = [trueSentence for trueSentence in
                                 self.trueSentenceList
                                 if not trueSentence == trueSentenceArg]

    def hasTrueSentences(self, trueSentenceList):
        """
        Checks if all the sentences in `trueSentenceList` exist in the state.
        If they do not, returns `False`.
        """

        for newSentence in trueSentenceList:
            isPresent = False
            for selfSentence in self.trueSentenceList:
                if selfSentence == newSentence:
                    isPresent = True
                    break
            if not isPresent:
                return False

        return True

    def isGoalState(self, goalState, inHeuristicMode=False):
        """
        Checks if `state` is a goal state by comparing
        it to `goalState`. Returns `True` if it is, and `False` otherwise.
        Essentially compares two states.
        """

        if not inHeuristicMode:
            return goalState == self
        else:
            return self.hasTrueSentences(goalState.trueSentenceList)

    def __eq__(self, other):
        """
        Checks equality of one `State` object with another.
        """

        return cmpListNoOrder(self.trueSentenceList, other.trueSentenceList)

    def __ne__(self, other):
        """
        Checks the inequality of two `State` objects.
        """

        return not self.__eq__(other)

    def __str__(self):
        """
        Returns a human-friendly representation of
        the current state.
        """

        retStr = ''

        for trueSentence in self.trueSentenceList:
            retStr += str(trueSentence) + ' \n'

        retStr += 'Previous Action : ' + self.prevPrintData + '\n' \
            + str(self.prevAction)
        return retStr

    def setHeuristicValue(self, goalState, actionList):
        """
        Sets the heuristic value of this object.
        """

        # self.heuristicValue = bfs(self, goalState, actionList, True).depth

        currState = State(self.trueSentenceList, self.groundTermList)
        count = 0

        while True:
            for action in actionList:
                retList = action.getStatesOnApplication(currState, True)
                if len(retList) > 0:
                    currState = retList[0]
                count += 1
                if currState.hasTrueSentences(goalState.trueSentenceList):
                    self.heuristicValue = count
                    return

        # self.heuristicValue = currState.heuristicValue
        self.heuristicValue = count

    def getNextStates(self, actionList, inHeuristicMode=False):
        """
        Applies each action in `actionList` to the `self` state
        and returns all the states generated.
        """

        retList = []

        for action in actionList:
            retList.extend(action.getStatesOnApplication(self,
                           inHeuristicMode))

        return retList


class TrueSentence:
    """
    This class represents a sentence whose truth value is "True".
    """

    def __init__(
        self,
        propositionType,
        argList,
        isNegation=False,
        ):
        """
        Initializes a TrueSentence object.
        """

        self.propositionType = propositionType
        """
        Type of proposition.
        """

        self.argList = list(argList)
        """
        List of Arg objects for the proposition.
        """

        self.isNegation = isNegation
        """
        \"Adds\" a negation sign before the statement.
        """

        self.truthValue = False
        """
        Truth value of the statement for Goal Stack planner.
        """

    def __eq__(self, other):
        """
        Check equality of `TrueSentence` objects.
        """

        return self.propositionType == other.propositionType \
            and self.isNegation == other.isNegation \
            and cmpListWithOrder(self.argList, other.argList)

    def __ne__(self, other):
        """
        Checks the inequality of two `TrueSentence` objects.
        """

        return not self.__eq__(other)

    def __str__(self):
        """
        Returns a human-friendly representation of
        the TrueSentence object.
        """

        resultStr = ''

        if self.isNegation:
            resultStr += '~'

        resultStr += '('
        resultStr += self.propositionType

        for arg in self.argList:
            resultStr += ' '
            resultStr += str(arg)
        resultStr = resultStr.strip()
        resultStr += ') '

        return resultStr

    def getNewGoals(self, currState, actionList):
        """
        Returns a dictionary of data required for new goals of GSP.
        Format of returned dictionary is :
            `trueSentenceList` : list of new `TrueSentence` objects.
            `action` : element of `actionList` that has to be applied.
            `assignments` : assignments used for applying returned action.
        `currState` is the current `State`.
        `actionList` is the list of possible actions in given world.
        Returns `None` if the goal is not reachable.
        """

        pickAction = actionList[0]
        unstackAction = actionList[1]
        releaseAction = actionList[2]
        stackAction = actionList[3]

        retDict = {}
        possibleActions = []
        assignments = {}

        possibleAssignments = list(currState.groundTermList)
        if self.propositionType == PropositionTypes.ON:
            nextAction = stackAction
        elif self.propositionType == PropositionTypes.ONTABLE:
            nextAction = releaseAction
        elif self.propositionType == PropositionTypes.EMPTY:
            nextAction = releaseAction
        elif self.propositionType == PropositionTypes.HOLD:
            checkSentence = TrueSentence(PropositionTypes.ONTABLE, self.argList, False)
            if currState.hasTrueSentences([checkSentence]):
                nextAction = pickAction
            else:
                nextAction = unstackAction
        elif self.propositionType == PropositionTypes.CLEAR:
            checkSentence = TrueSentence(PropositionTypes.HOLD, self.argList, False)
            if currState.hasTrueSentences([checkSentence]):
                nextAction = releaseAction
            else:
                nextAction = unstackAction
        else:
            return None

        for trueSentence in nextAction.effectList:
            if trueSentence.propositionType == self.propositionType \
                    and self.isNegation == trueSentence.isNegation:
                for ii in range(len(self.argList)):
                    assignments[trueSentence.argList[ii].value] = \
                            self.argList[ii]
                if nextAction == unstackAction:
                    if self.propositionType == PropositionTypes.HOLD:
                        for terminal in possibleAssignments:
                            checkSentence = TrueSentence(PropositionTypes.ON, \
                                    [self.argList[0], terminal], False)
                            if currState.hasTrueSentences([checkSentence]):
                                possibleAssignments = [terminal]
                                break
                    elif self.propositionType == PropositionTypes.CLEAR:
                        for terminal in possibleAssignments:
                            checkSentence = TrueSentence(PropositionTypes.ON, \
                                    [terminal, self.argList[0]], False)
                            if currState.hasTrueSentences([checkSentence]):
                                possibleAssignments = [terminal]
                                break
                    else:
                        return None
                elif self.propositionType == PropositionTypes.EMPTY:
                    for terminal in possibleAssignments:
                            checkSentence = TrueSentence(PropositionTypes.HOLD, \
                                    [terminal], False)
                            if currState.hasTrueSentences([checkSentence]):
                                possibleAssignments = [terminal]
                                break

                break


#             for trueSentence in action.effectList:
#                 if trueSentence.propositionType == self.propositionType \
#                         and self.isNegation == trueSentence.isNegation:
#                     assignments = {}
#                     possibleAssignments = list(currState.groundTermList)
#                     for ii in range(len(trueSentence.argList)):
#                         assignments[trueSentence.argList[ii].value] = \
#                                 self.argList[ii]
#                         possibleAssignments.remove(self.argList[ii])
#                     possibleActions.append([action, assignments, possibleAssignments])

#         if len(possibleActions) == 0:
#             return None

#         random.shuffle(possibleActions)
#         nextAction = possibleActions[0][0]
#         assignments = possibleActions[0][1]
#         possibleAssignments = possibleActions[0][2]
        retDict['action'] = nextAction

        for arg in nextAction.variableTermList:
            if not assignments.has_key(arg.value):
                if len(possibleAssignments) == 0:
                    break
                randomIndex = random.randrange(0, len(possibleAssignments))
                assignments[arg.value] = possibleAssignments[randomIndex]
                possibleAssignments.pop(randomIndex)

        retDict['assignments'] = assignments

        retTrueList = []
        for trueSentence in nextAction.preconditionList:
            assignedSentence = TrueSentence(trueSentence.propositionType, \
                    trueSentence.argList, trueSentence.isNegation)
            newArgList = []
            for arg in assignedSentence.argList:
                if arg.isVariable():
                    newArgList.append(assignments[arg.value])
                else:
                    newArgList.append(arg)
            assignedSentence.argList = newArgList
            retTrueList.append(assignedSentence)

        retDict['trueSentenceList'] = retTrueList

        # print("***new***")
#         print("State:")
#         print(currState)
#         print("Input:")
#         print(self)
#         printDict(retDict)

        return retDict

class Action:

    """
    This class represents an action and applies, reverses, and
    manages all aspects of actions.
    """

    def __init__(
        self,
        name,
        argList,
        preconditionList,
        effectList,
        ):
        """
        Initializes an Action object.
        """

        self.name = name
        """
        Name of the action.
        """

        self.argList = argList
        """
        List of entities on which the action is applied.
        """

        self.preconditionList = list(preconditionList)
        """
        Preconditions: a list of TrueSentence objects
        """

        self.effectList = list(effectList)
        """
        Effects: a list of TrueSentence objects
        """

        self.variableTermList = []
        """
        A list of `Arg` objects in sentences in the `preconditionList` list.
        """

        for precondition in preconditionList:
            for arg in precondition.argList:
                alreadyPresent = False
                for selfArg in self.variableTermList:
                    if arg == selfArg:
                        alreadyPresent = True
                        break
                if not alreadyPresent:
                    self.variableTermList.append(arg)

    def __str__(self):
        """
        Returns a human-friendly representation of
        the Action object.
        """

        retStr = 'Action : ' + self.name + '\n'
        retStr += 'Pre: '
        for item in self.preconditionList:
            retStr += str(item)
        retStr += '\n'
        retStr += 'Eff: '
        for item in self.effectList:
            retStr += str(item)
        retStr += '\n'

        return retStr

    def getStateOnActionUtil(
        self,
        stateObject,
        assignments,
        inHeuristicMode=False,
        ):
        """
        Applies `this` Action to `stateObject` with given `assignments`.
        `assignments` is the dictionary of assignments made.
        `inHeuristicMode` is the mode identifier.
        Returns a new `State` object.
        Does not modify `stateObject`.
        """

        retState = State(stateObject.trueSentenceList,
                         stateObject.groundTermList)
        for trueSentence in self.effectList:
            newTrueSentence = \
                TrueSentence(trueSentence.propositionType, [])
            groundTermList = []
            for variable in trueSentence.argList:
                savedArg = assignments[variable.value]
                # groundTermList.append(Arg(savedArg.type,
                        # savedArg.value, savedArg.isNegation))
                groundTermList.append(savedArg)

            newTrueSentence.argList = groundTermList
            if trueSentence.isNegation:
                if not inHeuristicMode:
                    retState.removeTrueSentence(newTrueSentence)
            else:
                retState.addTrueSentence(newTrueSentence)

        retState.prevAction = self
        retState.prevAssignments = dict(assignments)
        argListString = ''
        for arg in self.argList:
            argListString += ' ' + str(assignments[arg])

        retState.prevPrintData = '(' + self.name + argListString + ')'
        if inHeuristicMode:
            retState.heuristicValue = stateObject.heuristicValue + 1
        return retState

    def getStatesOnApplicationUtil(
        self,
        stateObject,
        unassignedVariableList,
        assignments,
        retList,
        inHeuristicMode=False,
        ):
        """
        Assigns groundterms to unassigned variables in `unassignedVariableList`.
        Returns a list of `State` objects possible after
        application of `this` Action to `stateObject`.
        `assignments` is a dictionary of assignments already made.
        Keys in this are `value` parameters of `Arg` objects.
        Values in this dictionary are `Arg` objects.
        `retList` is a list of `State` objects already generated.
        """

        if len(unassignedVariableList) == 0:

            effectTrueSentencesList = []
            for trueSentence in self.effectList:
                positiveGroundTermList = []
                if trueSentence.isNegation:
                    continue
                for variable in trueSentence.argList:
                    positiveGroundTermList.append(assignments[variable.value])
                effectTrueSentencesList.append(TrueSentence(trueSentence.propositionType,
                        positiveGroundTermList))

            if stateObject.hasTrueSentences(effectTrueSentencesList):
                return retList

            groundTermTrueSentencesList = []
            for trueSentence in self.preconditionList:
                groundTermList = []
                for variable in trueSentence.argList:
                    groundTermList.append(assignments[variable.value])
                groundTermTrueSentencesList.append(TrueSentence(trueSentence.propositionType,
                        groundTermList))

            if stateObject.hasTrueSentences(groundTermTrueSentencesList):
                if not inHeuristicMode:
                    retList.append(self.getStateOnActionUtil(stateObject,
                                   assignments, inHeuristicMode))
                else:
                    stateObject = \
                        self.getStateOnActionUtil(stateObject,
                            assignments, inHeuristicMode)
                    retList = [stateObject]
            return retList

        else:
            thisVariable = unassignedVariableList.pop()
            for groundTerm in stateObject.groundTermList:
                assignments[thisVariable.value] = groundTerm
                retList = self.getStatesOnApplicationUtil(stateObject,
                        unassignedVariableList, assignments, retList,
                        inHeuristicMode)
                if inHeuristicMode and len(retList) > 0:
                    stateObject = retList[0]
                assignments.pop(thisVariable.value)

            unassignedVariableList.append(thisVariable)
            return retList

    def getStatesOnApplication(self, stateObject,
                               inHeuristicMode=False):
        """
        Generates states after unification to input `stateObject`.
        Returns a list of `State` objects.
        This list may be empty.
        The argument `stateObject` is not modified.
        """

        assignments = {}
        retList = []
        return self.getStatesOnApplicationUtil(stateObject,
                self.variableTermList, assignments, retList,
                inHeuristicMode)

def gsp(startState, goalState, actionList):
    """
    Does Goal Stack planning.
    Returns a plan in the form of a list of dictionaries, in
    their logical order in the plan.
    The format of returned dictionary is:
        (1) `action` : element of `actionList` that has to be applied.
        (2) `assignments` : assignments used for applying returned action.
    No parameters used to call this function are changed.
    This function may not terminate (semi-decidable).
    """

    stack = []
    currentState = State(startState.trueSentenceList, \
                        startState.groundTermList)
    planList = []
    nBlocks = len(currentState.groundTermList)

    stack.append(goalState.trueSentenceList)
    for trueSentence in goalState.trueSentenceList:
        stack.append([trueSentence])

    while len(stack) > 0:
        # print("***new***")
        # printList(stack)
        print(str(len(planList)).zfill(3), end = "\r")
        poppedElement = stack.pop()

        if type(poppedElement) is list:

            if not currentState.hasTrueSentences(poppedElement):

                if len(poppedElement) > 1:
                    stack.append(poppedElement)
                    random.shuffle(poppedElement)
                    for trueSentence in poppedElement:
                        stack.append([trueSentence])

                else:
                    newGoalsData = poppedElement[0].getNewGoals(currentState, actionList)

                    if newGoalsData == None:
                        stack = []
                        currentState = State(startState.trueSentenceList, \
                                startState.groundTermList)
                        planList = []
                        stack.append(goalState.trueSentenceList)
                        for trueSentence in goalState.trueSentenceList:
                            stack.append([trueSentence])
                        continue

                    actionDict = dict()
                    actionDict['action'] = newGoalsData['action']
                    actionDict['assignments'] = newGoalsData['assignments']
                    stack.append(actionDict)
                    stack.append(newGoalsData['trueSentenceList'])
                    for trueSentence in newGoalsData['trueSentenceList']:
                        stack.append([trueSentence])
        else:
            action = poppedElement['action']
            assignments = poppedElement['assignments']
            currentState = action.getStateOnActionUtil(currentState, assignments)
            planList.append(poppedElement)
            # printDict(poppedElement)

    return planList

def aStar(startState, goalState, actionList):
    """
    Performs a A-Star search on states.
    Returns a `State` object which is equivalent
    to the goal state (`goalState`). A plan can be
    obtained by tracing the `prevState` pointers in states.
    """

    # pdb.set_trace()

    global aStarNumNodesExpanded
    aStarNodesExpanded = 0
    aStarQueue = []

    # Update heuristic value
    # startState.setHeuristicValue(goalState, actionList)

    heappush(aStarQueue, (startState.heuristicValue + startState.depth,
             startState))

    while len(aStarQueue) > 0:
        poppedElement = heappop(aStarQueue)
        poppedState = poppedElement[1]

        print('Searching plans of depth: ' + str(poppedState.depth),
              end='\r')

        if poppedState.isGoalState(goalState):
            return poppedState

        aStarNumNodesExpanded += 1
        neighborList = poppedState.getNextStates(actionList)

        for neighborState in neighborList:
            neighborState.prevState = poppedState
            neighborState.depth = poppedState.depth + 1

            # Update heuristic value

            neighborState.setHeuristicValue(goalState, actionList)
            heappush(aStarQueue, (neighborState.heuristicValue
                     + neighborState.depth, neighborState))

    return None


def bfs(
    startState,
    goalState,
    actionList,
    inHeuristicMode=False,
    ):
    """
    Performs a breadth-first search on states.
    Returns a `State` object which is equivalent
    to the goal state (`goalState`). A plan can be
    obtained by tracing the `prevState` pointers in states.
    """

    # pdb.set_trace()

    global bfsNumNodesExpanded
    bfsNumNodesExpanded = 0
    bfsQueue = []
    bfsQueue.append(startState)

    while len(bfsQueue) > 0:
        poppedState = bfsQueue.pop(0)
        print('Searching plans of depth: ' + str(poppedState.depth),
              end='\r')

        if poppedState.isGoalState(goalState, inHeuristicMode):
            return poppedState

        bfsNumNodesExpanded += 1
        neighborList = poppedState.getNextStates(actionList,
                inHeuristicMode)

        for neighborState in neighborList:
            neighborState.prevState = poppedState
            neighborState.depth = poppedState.depth + 1

        bfsQueue.extend(neighborList)

    return None


def cmpListWithOrder(first, second):
    """
    "Deep" compares two lists. Returns `True` of they are equal, and
    `False` otherwise.
    Order of elements in the lists matters.
    """

    if not len(first) == len(second):
        return False

    dupFirst = list(first)
    dupSecond = list(second)

    for ii, item in enumerate(dupFirst):
        if item != dupSecond[ii]:
            return False

    return True


def cmpListNoOrder(first, second):
    """
    "Deep" compares two lists. Returns `True` of they are equal, and
    `False` otherwise.
    Order of elements in the lists does not matter.
    """

    if not len(first) == len(second):
        return False

    dupFirst = list(first)
    dupSecond = list(second)

    for item in dupFirst:
        exists = False
        itemInList = None
        for other in dupSecond:
            if item == other:
                exists = True
                itemInList = other
                break

        if not exists:
            return False

        dupSecond.remove(itemInList)

    return True


def printDict(currentDict):
    """
    Prints a dictionary properly.
    """

    for key in currentDict.keys():
        print(str(key) + ': ')
        if type(currentDict[key]) is list:
            printList(currentDict[key])
        elif type(currentDict[key]) is dict:
            printDict(currentDict[key])
        else:
            print(str(currentDict[key]))

        print("")


def printList(currentList):
    """
    Prints a list properly.
    """

    print("#####")
    for item in currentList:
        if type(item) is list:
            printList(item)
        elif type(item) is dict:
            printDict(item)
        else:
            print(item, end = ", ")

    print("")

def getActionsForBlocksWorld():
    """
    Hardcoded actions for the Blocks World.
    """

    pickBlock = Action('pick', ['block'],
                       [TrueSentence(PropositionTypes.ONTABLE,
                       [Arg(ArgTypes.VARIABLE, 'block', False)],
                       False), TrueSentence(PropositionTypes.CLEAR,
                       [Arg(ArgTypes.VARIABLE, 'block', False)],
                       False), TrueSentence(PropositionTypes.EMPTY, [],
                       False)], [TrueSentence(PropositionTypes.HOLD,
                       [Arg(ArgTypes.VARIABLE, 'block', False)],
                       False), TrueSentence(PropositionTypes.CLEAR,
                       [Arg(ArgTypes.VARIABLE, 'block', False)], True),
                       TrueSentence(PropositionTypes.ONTABLE,
                       [Arg(ArgTypes.VARIABLE, 'block', False)], True),
                       TrueSentence(PropositionTypes.EMPTY, [], True)])

    unstackBlockAFromTopOfBlockB = Action('unstack', ['blocka', 'blockb'
            ], [TrueSentence(PropositionTypes.ON,
            [Arg(ArgTypes.VARIABLE, 'blocka', False),
            Arg(ArgTypes.VARIABLE, 'blockb', False)], False),
            TrueSentence(PropositionTypes.CLEAR,
            [Arg(ArgTypes.VARIABLE, 'blocka', False)], False),
            TrueSentence(PropositionTypes.EMPTY, [], False)],
            [TrueSentence(PropositionTypes.HOLD,
            [Arg(ArgTypes.VARIABLE, 'blocka', False)], False),
            TrueSentence(PropositionTypes.CLEAR,
            [Arg(ArgTypes.VARIABLE, 'blockb', False)], False),
            TrueSentence(PropositionTypes.ON, [Arg(ArgTypes.VARIABLE,
            'blocka', False), Arg(ArgTypes.VARIABLE, 'blockb', False)],
            True), TrueSentence(PropositionTypes.CLEAR,
            [Arg(ArgTypes.VARIABLE, 'blocka', False)], True),
            TrueSentence(PropositionTypes.EMPTY, [], True)])

    releaseBlock = Action('release', ['block'],
                          [TrueSentence(PropositionTypes.HOLD,
                          [Arg(ArgTypes.VARIABLE, 'block', False)],
                          False)],
                          [TrueSentence(PropositionTypes.ONTABLE,
                          [Arg(ArgTypes.VARIABLE, 'block', False)],
                          False), TrueSentence(PropositionTypes.CLEAR,
                          [Arg(ArgTypes.VARIABLE, 'block', False)],
                          False), TrueSentence(PropositionTypes.HOLD,
                          [Arg(ArgTypes.VARIABLE, 'block', False)],
                          True), TrueSentence(PropositionTypes.EMPTY,
                          [], False)])

    stackBlockAOnTopOfBlockB = Action('stack', ['blocka', 'blockb'],
            [TrueSentence(PropositionTypes.CLEAR,
            [Arg(ArgTypes.VARIABLE, 'blockb', False)], False),
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE,
            'blocka', False)], False)],
            [TrueSentence(PropositionTypes.ON, [Arg(ArgTypes.VARIABLE,
            'blocka', False), Arg(ArgTypes.VARIABLE, 'blockb', False)],
            False), TrueSentence(PropositionTypes.CLEAR,
            [Arg(ArgTypes.VARIABLE, 'blocka', False)], False),
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE,
            'blocka', False)], True),
            TrueSentence(PropositionTypes.CLEAR,
            [Arg(ArgTypes.VARIABLE, 'blockb', False)], True),
            TrueSentence(PropositionTypes.EMPTY, [], False)])

    return [pickBlock, unstackBlockAFromTopOfBlockB, releaseBlock,
            stackBlockAOnTopOfBlockB]


def readFile(fileName):
    """
    Returns a dictionary with initial state, final state and
    the "mode" of operation as read from the `fileName` file.
    Keys in dictionary are:
    'planner', 'initState', 'goalState'.
    """

    retDict = {}

    with open(fileName) as inFile:

        # pdb.set_trace()

        lines = inFile.readlines()
        lines = [line.strip() for line in lines]

        try:
            numberBlocks = int(lines[0])
        except ValueError:
            print('Please tell me the number of blocks!')
            return None
        completeBlockList = []
        for i in range(1, numberBlocks + 1):
            completeBlockList.append(Arg(ArgTypes.TERMINAL, i, False))

        validPlanners = ['f', 'a', 'g']
        if not lines[1] in validPlanners:
            print("Oh! Looks like you want a planner that we don't have!"
                  )
            return None
        retDict['planner'] = lines[1]

        if not lines[2] == 'initial':
            print("Don't know from where the initial state starts!")
            return None
        initState = State([], [])
        words = lines[3].split()
        argList = []
        propositionType = None
        for word in words:
            if word[0] == '(':
                argList = []
                propositionType = word.strip('(')
            else:
                try:
                    argList.append(completeBlockList[int(word.strip(')'
                                   )) - 1])
                except:
                    print("Sorry! Can't read the file!")
                    return None
            if word[-1] == ')':
                initState.addTrueSentence(TrueSentence(propositionType.strip(')'
                        ), argList))

        retDict['initState'] = initState

        if not lines[4] == 'goal':
            print("Don't know from where the goal state starts!")
            return None

        goalState = State([], [])
        words = lines[5].split()
        argList = []
        propositionType = None
        isNegation = False
        for word in words:
            if word[0] == '~':
                isNegation = True
                word = word.strip('~')

            if word[0] == '(':
                argList = []
                propositionType = word.strip('(')
            else:
                try:
                    argList.append(completeBlockList[int(word.strip(')'
                                   )) - 1])
                except:
                    print("Sorry! Can't read the file!")
                    return None
            if word[-1] == ')':
                goalState.addTrueSentence(TrueSentence(propositionType.strip(')'
                        ), argList, isNegation))
                isNegation = False

        retDict['goalState'] = goalState
        return retDict


def writeFile(fileName, numActions, outputString):
    """
    Writes `outputString` to the given file.
    `fileName` is the pathname of the file to write to.
    """

    f = open(fileName, 'w')
    f.write(str(numActions) + '\n')
    f.write(outputString)
    f.close()


def main():
    """
    Take input argument (a file name), and write soduko solutions
    to a file.
    """

    if len(sys.argv) < 2:
        print('Invalid/insufficient arguments!')
    else:
        actionList = getActionsForBlocksWorld()
        fileName = str(sys.argv[1])
        readData = readFile(fileName)
        traceData = None
        outputString = ''
        numActions = 0
        numNodesExpanded = 0
        global bfsNumNodesExpanded
        global aStarNodesExpanded
        bfsNumNodesExpanded = 0
        aStarNodesExpanded = 0

        initTime = time.time()

        if readData['planner'] == 'f':
            bfsData = bfs(readData['initState'], readData['goalState'],
                          actionList)
            traceData = bfsData.tracePath()
            outputString = traceData['outputString']
            numActions = len(traceData['stateList']) - 1
            numNodesExpanded = bfsNumNodesExpanded
        elif readData['planner'] == 'a':
            aStarData = aStar(readData['initState'],
                              readData['goalState'], actionList)
            traceData = aStarData.tracePath()
            outputString = traceData['outputString']
            numActions = len(traceData['stateList']) - 1
            numNodesExpanded = aStarNumNodesExpanded
        elif readData['planner'] == 'g':
            gspPlanList = gsp(readData['initState'], readData['goalState'],
                          actionList)
            for stage in gspPlanList:
                action = stage['action']
                assignments = stage['assignments']
                argListString = ''
                for arg in action.argList:
                    argListString += ' ' + str(assignments[arg])
                outputString += '(' + action.name + argListString + ')' + '\n'
            numActions = len(gspPlanList)
            numNodesExpanded = -1

        else:
            print('Invalid planner choice!')

        duration = time.time() - initTime

        if len(outputString) > 0:
            writeFile(fileName[:-4] + '_out.txt', numActions,
                      outputString)
        else:
            print('Error in searching for a plan: no output from planner!'
                  )

        print('\r..........................................................'
              )
        print('Planner: ' + readData['planner'])
        print('Time: ' + str(duration))
        print('Plan length: ' + str(numActions))
        if numNodesExpanded >= 0:
            print('Nodes expanded: ' + str(numNodesExpanded))
        else:
            print('Nodes expanded: ' + 'N.A.')
        print('Output written to: "' + str(fileName[:-4] + '_out.txt"'))
        print('..........................................................'
              )

    return


def checkPlan(plan, startState, goalState):
    """
    Check the validity of a plan `plan`
    given `startState` and `goalState`.
    """

    # TODO: implementation

    pass

main()
