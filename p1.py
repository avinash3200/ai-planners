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

        # List of TrueSentence objects.
        # Only has "True" sentences. Rest is assumed False.

        pass

    def __str__(self):
        """
        Returns a human-friendly representation of
        the current state.
        """

        pass

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

