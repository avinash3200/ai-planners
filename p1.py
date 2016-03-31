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

    def addTrueSentence(self, trueSentence):
        """
        Adds the `trueSentence` object to the state.
        """

        self.trueSentenceList.append(trueSentence)

    def removeTrueSentence(self, trueSentenceArg):
        """
        Removes all objects "equal to" the `trueSentence` object from the state.
        """

        self.trueSentenceList = [trueSentence for trueSentence in self.trueSentenceList \
                if trueSentence.propositionType != trueSentenceArg.propositionType \
                    or cmp(trueSentence.argList, trueSentenceArg.argList) != 0]

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

    def isApplicable(self, stateObject):
        """
        A boolean function to check if the `self` action can
        be applied to the `stateObject` state.
        """

        pass

