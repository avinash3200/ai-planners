# Tushar Agarwal
# Shailesh Mani Pandey

# AI Lab 4

class Propositions:
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
        List of arguments for the proposition.
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

    def __init__(self):
        """
        Initializes an Action object.
        """

        # Preconditions: a list of TrueSentence objects
        # Effects: same as above

        pass

    def __str__(self):
        """
        Returns a human-friendly representation of
        the Action object.
        """

        pass

    def applyAction(self, stateObject):
        """
        Applies an action after unification.
        """

        pass

    def checkApplicability(self, stateObject):
        """
        A boolean function to check if the `self` action can
        be applied to the `stateObject` state.
        """

        pass

