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

    def __init__(self):
        """
        Initializes a `State` object.
        """

        trueSentenceList = []
        """
        A list of objects of class TrueSentence.
        """

        groundTermList = []
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

    def __init__(self, propositionType, argList):
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


    def __eq__(self, other):
        """
        Check equality of `TrueSentence` objects.
        """

        return trueSentence.propositionType == trueSentenceArg.propositionType \
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


    def getAssignmentsUtil(self, stateObject, unassignedVariableList, assignments):
        """
        Assign groundterms to unassigned variables in `unassignedVariableList`.
        Returns a dictionary of valid substitutions, if possible.
        Else, returns None.
        `assignments` Dictionary of assignments already done.
        """

        if len(unassignedVariableList) == 0:
            groundTermTrueSentencesList = []
            for trueSentence in self.preconditionList:
                groundTermList = []
                for variable in trueSentence.argList:
                    groundTermList.append(assignments[variable.value])
                groundTermSentencesList.append(TrueSentence(trueSentence.propositionType, groundTermList))

            if stateObject.hasTrueSentences(groundTermTrueSentencesList):
                return assignments
            else:
                return None

        else:
            thisVariable = unassignedVariableList.pop()
            for groundTerm in stateObject.groundTermList:
                assignments[thisVariable.value] = groundTerm
                if self.getAssignmentsUtil(stateObject, unassignedVariableList) == None:
                    assignments.pop(thisVariable.value)
                    continue
                else:
                    return assignments

            return None


    def applyAction(self, stateObject):
        """
        Applies an action after unification to input `stateObject`.
        Returns a new `State` object, if successful.
        The argument `stateObject` is not modified.
        Returns `False` otherwise.
        """

        if not self.isApplicable(stateObject):
            return False
        else:
            pass


    def getVariableAssignments(self, stateObject):
        """
        A function to get assignments for variables so that
        this action can be applied to `stateObject`.
        Returns None if no such assignment is possible.
        """

        assignments = {}
        return self.getAssignmentsUtil(stateObject, self.variableTermList, assignments)


def readFile(fileName):
    """
    Returns a dictionary with initial state, final state and
    the "mode" of operation as read from the `fileName` file.
    """

    pass
