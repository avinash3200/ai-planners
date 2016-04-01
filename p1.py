# Tushar Agarwal
# Shailesh Mani Pandey

# AI Lab 4

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

    def __init__(self, argType, argValue, isNegation):
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
        retStr = ""

        if self.isNegation:
            retStr += "-"

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

        return self.type == other.type and\
                self.value == other.value and\
                self.isNegation == other.isNegation
                
    def __ne__(self, other):
        """
        Checks the inequality of two `Arg` objects.
        """
        
        return not self.__eq__(other)


class PropositionTypes:
    """
    This class contains constants for different types of propositions.
    """

    ON = "on";
    ONTABLE = "ontable";
    CLEAR = "clear";
    HOLD = "hold";


class State:
    """
    This class represents the current state.
    This represents a conjuction of `TrueSentence` objects.
    """

    def __init__(self, trueSentenceList = [], groundTermList = []):
        """
        Initializes a `State` object.
        """

        self.trueSentenceList = trueSentenceList
        """
        A list of objects of class TrueSentence.
        """

        self.groundTermList = groundTermList
        """
        A list of ground `Arg` objects in sentences in the `trueSentenceList` list.
        """

        self.prevState = None
        """
        This variable is used to figure out a path after searching is done.
        """


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

        self.trueSentenceList = [trueSentence for trueSentence in self.trueSentenceList \
                if not (trueSentence == trueSentenceArg)]


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


    def isGoalState(state, goalState):
        """
        Checks if `state` is a goal state by comparing
        it to `goalState`. Returns `True` if it is, and `False` otherwise.
        Essentially compares two states.
        """

        return goalState == state



    def __str__(self):
        """
        Returns a human-friendly representation of
        the current state.
        """

        retStr = ""

        for trueSentence in self.trueSentenceList:
            retStr += str(trueSentence) + " \n"

        return retStr


    def getNextStates(self, actionList):
        """
        Applies each action in `actionList` to the `self` state
        and returns all the states generated.
        """

        retList = []

        for action in actionList:
            retList.extend(action.getStatesOnApplication(currentState))

        return retList

class TrueSentence:
    """
    This class represents a sentence whose truth value is "True".
    """

    def __init__(self, propositionType, argList, isNegation = False):
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
        "Adds" a negation sign before the statement.
        """


    def __eq__(self, other):
        """
        Check equality of `TrueSentence` objects.
        """

        return trueSentence.propositionType == trueSentenceArg.propositionType \
                    and self.isNegation == other.isNegation \
                    and cmp(trueSentence.argList, trueSentenceArg.argList) == 0
                    
    
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

        resultStr = ""

        if self.isNegation:
            resultStr += "~"

        resultStr = "("
        resultStr += self.propositionType

        for arg in self.argList:
            resultStr+=" "
            resultStr += str(arg)
        resultStr = resultStr.strip()
        resultStr += ")"

        return resultStr


class Action:
    """
    This class represents an action and applies, reverses, and
    manages all aspects of actions.
    """

    def __init__(self, preconditionList, effectList):
        """
        Initializes an Action object.
        """

        self.preconditionList = preconditionList
        """
        Preconditions: a list of TrueSentence objects
        """

        self.effectList = effectList
        """
        Effects: a list of TrueSentence objects
        """

        self.variableTermList = []
        """
        A list of `Arg` objects in sentences in the `preconditionList` list.
        """

        for arg in preconditionList.argList:
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

        retStr = ""
        retStr += "Pre: \n"
        for item in self.preconditionList:
            retStr += str(item)
        retStr += "\n"
        retStr += "Eff: \n"
        for item in self.effectList:
            retStr += str(item)
        retStr += "\n"

        return retStr


    def getStateOnActionUtil(self, stateObject, assignments):
        """
        Applies `this` Action to `stateObject` with given `assignments`.
        `assignments` Dictionary of assignments made.
        Returns a new `State` object.
        Does not modify `stateObject`.
        """

        retState = State(stateObject.trueSentenceList, stateObject.groundTermList)
        for trueSentence in self.effectList:
            newTrueSentence = TrueSentence(trueSentence.propositionType, [])
            for variable in trueSentence.argList:
                    savedArg = assignments[variable.value]
                    groundTermList.append(Arg(savedArg.argType, savedArg.argValue, savedArg.isNegation))

            newTrueSentence.argList = groundTermList
            if trueSentence.isNegation:
                retState.removeTrueSentence(newTrueSentence)
            else:
                retState.addTrueSentence(newTrueSentence)

        return retState


    def getStatesOnApplicationUtil(self, stateObject, unassignedVariableList, assignments, retList):
        """
        Assign groundterms to unassigned variables in `unassignedVariableList`.
        Returns a list of `State` objects possible after
        application of `this` Action to `stateObject`
        `assignments` Dictionary of assignments already made.
        Keys in this are `value` parameters of `Arg` objects.
        Values in this dictionary are `Arg` objects.
        `retList` List of `State` objects already generated.
        """

        if len(unassignedVariableList) == 0:
            groundTermTrueSentencesList = []
            for trueSentence in self.preconditionList:
                groundTermList = []
                for variable in trueSentence.argList:
                    groundTermList.append(assignments[variable.value])
                groundTermSentencesList.append(TrueSentence(trueSentence.propositionType, groundTermList))

            if stateObject.hasTrueSentences(groundTermTrueSentencesList):
                retList.append(self.getStateOnActionUtil(stateObject, assignments))

            return retList

        else:
            thisVariable = unassignedVariableList.pop()
            for groundTerm in stateObject.groundTermList:
                assignments[thisVariable.value] = groundTerm
                self.getStatesOnApplicationUtil(stateObject, unassignedVariableList, assignments, retList)
                assignments.pop(thisVariable.value)

            return retList


    def getStatesOnApplication(self, stateObject):
        """
        Generates states after unification to input `stateObject`.
        Returns a list of `State` objects.
        List may be empty.
        The argument `stateObject` is not modified.
        """

        assignments = {}
        retList = []
        return self.getStatesOnApplicationUtil(stateObject, self.variableTermList, assignments, retList)


def bfs(startState, goalState, actionList):
    """
    Performs a breadth-first search on states.
    Returns a `State` object which is equivalent
    to the goal state (`goalState`). A plan can be
    obtained by tracing the `prevState` pointers in states.
    """

    bfsQueue = []
    bfsQueue.append(startState)

    while len(bfsQueue) > 0:
        poppedState = bfsQueue.pop(0)

        if poppedState.isGoalState(goalState):
            return poppedState

        neighborList = currentState.getNextStates(actionList)

        for neighborState in neighborList:
            neighborState.prevState = poppedState

        bfsQueue.extend(neighborList)

    return None


def getActionsForBlocksWorld():
    """
    Hardcoded actions for the Blocks World.
    """

    pickBlock = Action([TrueSentence(PropositionTypes.ONTABLE,[Arg(ArgTypes.VARIABLE, 'block')]), \
                        TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'block')])], \
                        [ \
                        TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'block')]), \
                        TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'block')], True), \
                        TrueSentence(PropositionTypes.ONTABLE, [Arg(ArgTypes.VARIABLE, 'block'), True])])
                        
    unstackBlockAFromTopOfBlockB = Action([ \
            TrueSentence(PropositionTypes.ON, [Arg(ArgTypes.VARIABLE, 'blocka'), Arg(ArgTypes.VARIABLE, 'blockb')]), \
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blocka')])], \
            [ \
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'blocka')]), \
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blockb')]), \
            TrueSentence(PropositionTypes.ON, [Arg(ArgTypes.VARIABLE, 'blocka'), Arg(ArgTypes.VARIABLE, 'blockb')], True), \
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blocka')], True)])
    
    releaseBlock = Action([\
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'block')])], \
            [ \
            TrueSentence(PropositionTypes.ONTABLE, [Arg(ArgTypes.VARIABLE, 'block')]), \
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'block')]), \
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'block')], True)])
    
    stackBlockAOnTopOfBlockB = Action([ \
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blockb')]), \
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'blocka')])], \
            [ \
            TrueSentence(PropositionTypes.ON, [Arg(ArgTypes.VARIABLE, 'blocka'), Arg(ArgTypes.VARIABLE, 'blockb')], True), \
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blocka')]), \
            TrueSentence(PropositionTypes.HOLD, [Arg(ArgTypes.VARIABLE, 'blocka')], True), \
            TrueSentence(PropositionTypes.CLEAR, [Arg(ArgTypes.VARIABLE, 'blockb')], True)])
    
    return [pickBlock, unstackBlockAFromTopOfBlockB, releaseBlock, stackBlockAOnTopOfBlockB]


def readFile(fileName):
    """
    Returns a dictionary with initial state, final state and
    the "mode" of operation as read from the `fileName` file.
    Keys in dictionary are:
        planner, initState, goalState
    """

    retDict = {}

    with open(fileName) as inFile:
        readString = inFile.read()
        lines = readString.splitlines()

        try:
            numberBlocks = int(lines[0])
        except ValueError:
            print("Please tell me the number of blocks!")
            return None
        completeBlockList = []
        for i in range(1, numberBlocks+1):
            completeBlockList.append(Arg(ArgTypes.TERMINAL, i, False))

        validPlanners = ['f', 'a', 'g']
        if not lines[1] in validPlanners:
            print("Oh! Looks like you want a planner that we don't have!")
            return None
        retDict['planner'] = lines[1]

        if not lines[2] == 'initial':
            print("Don't know from where the initial state starts!")
            return None
        initState = State()
        words = lines[3].split()
        argList = []
        propositionType = None
        for word in words:
            if word == '(empty)':
                break
            if word[0] == '(':
                argList = []
                word = word.strip('(')
                propositionType = word
            else:
                try:
                    argList.append(completeBlockList[int(word.strip(')')) - 1])
                except:
                    print("Sorry! Can't read the file!")
                    return None
                if word[-1] == ')':
                    initState.addTrueSentence(TrueSentence(propositionType, argList))

        retDict['initState'] = initState

        if not lines[4] == 'goal':
            print("Don't know from where the goal state starts!")
            return None
        goalState = State()
        words = lines[5].split()
        argList = []
        propositionType = None
        isNegation = False
        for word in words:
            if word == '(empty)':
                break

            if word[0] == '~':
                isNegation = True
                word = word.strip('~')

            if word[0] == '(':
                argList = []
                propositionType = word.strip('(')
            else:
                try:
                    argList.append(completeBlockList[int(word.strip(')')) - 1])
                except:
                    print("Sorry! Can't read the file!")
                    return None
                if word[-1] == ')':
                    goalState.addTrueSentence(TrueSentence(propositionType, argList, isNegation))
                    isNegation = False

        retDict['goalState'] = goalState
        return retDict

