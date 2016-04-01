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


class PropositionTypes:
    """
    This class contains constants for different types of propositions.
    """

    ON = "on";
    ONTABLE = "ontable";
    CLEAR = "clear";
    HOLD = "hold";
    EMPTY = "empty";


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
                if eq(arg, selfArg):
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
                if not eq(trueSentence, trueSentenceArg)]


    def hasTrueSentences(self, trueSentenceList):
        """
        Checks if all the sentences in `trueSentenceList` exist in the state.
        If they do not, returns `False`.
        """

        for newSentence in trueSentenceList:
            isPresent = False
            for selfSentence in self.trueSentenceList:
                if eq(selfSentence, newSentence):
                    isPresent = True
                    break
            if not isPresent:
                return False

        return True


    def __str__(self):
        """
        Returns a human-friendly representation of
        the current state.
        """

        retStr = ""

        for trueSentence in self.trueSentenceList:
            retStr += str(trueSentence) + " \n"

        return retStr


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
        
        self.prevState = None
        """
        This variable is used to figure out a path after searching is done.
        """

    def __eq__(self, other):
        """
        Check equality of `TrueSentence` objects.
        """

        return trueSentence.propositionType == trueSentenceArg.propositionType \
                    and self.isNegation == other.isNegation \
                    and cmp(trueSentence.argList, trueSentenceArg.argList) == 0


    def __str__(self):
        """
        Returns a human-friendly representation of
        the TrueSentence object.
        """

        resultStr = "("
        resultStr += self.propositionType

        # TODO
        # Add arguments separated by comma to the resultStr

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
                if eq(arg, selfArg):
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


    def getStateOnAction(self, stateObject, assignments):
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
                retList.append(self.getStateOnAction(stateObject, assignments))

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


def isGoalState(state, goalState):
    """
    Checks if `state` is a goal state by comparing
    it to `goalState`. Returns `True` if it is, and `False` otherwise.  
    Essentially compares two states.
    """

    return eq(goalState, state)

def bfs(startState, goalState):
    pass


def readFile(fileName):
    """
    Returns a dictionary with initial state, final state and
    the "mode" of operation as read from the `fileName` file.
    """

    pass

