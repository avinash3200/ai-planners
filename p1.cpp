#include "builtin.hpp"

namespace __p1__ {


str *__name__;


__ss_bool  default_0;

static inline list<TrueSentence *> *list_comp_0(State *self, TrueSentence *trueSentenceArg);
static inline list<str *> *list_comp_1(list<str *> *lines);

static inline list<TrueSentence *> *list_comp_0(State *self, TrueSentence *trueSentenceArg) {
    __ss_int __24;
    list<TrueSentence *> *__22;
    TrueSentence *trueSentence;
    list<TrueSentence *>::for_in_loop __25;
    __iter<TrueSentence *> *__23;

    list<TrueSentence *> *__ss_result = new list<TrueSentence *>();

    __22 = self->trueSentenceList;
    FOR_IN(trueSentence,__22,22,24,25)
        if (__NOT(__eq(trueSentence, trueSentenceArg))) {
            __ss_result->append(trueSentence);
        }
    END_FOR

    return __ss_result;
}

static inline list<str *> *list_comp_1(list<str *> *lines) {
    list<str *> *__111;
    list<str *>::for_in_loop __114;
    str *line;
    __ss_int __113;
    __iter<str *> *__112;

    list<str *> *__ss_result = new list<str *>();

    __ss_result->resize(len(lines));
    FOR_IN(line,lines,111,113,114)
        __ss_result->units[__113] = line->strip();
    END_FOR

    return __ss_result;
}

/**
class ArgTypes
*/

class_ *cl_ArgTypes;

__ss_int ArgTypes::VARIABLE;
__ss_int ArgTypes::TERMINAL;

void ArgTypes::__static__() {
    VARIABLE = 0;
    TERMINAL = 1;
}

/**
class Arg
*/

class_ *cl_Arg;

str *Arg::__str__() {
    /**
    Returns a human-friendly representation of
    the argument.
    */
    str *retStr;

    retStr = const_0;
    if (this->isNegation) {
        retStr = (retStr)->__iadd__(const_1);
    }
    if ((this->type==ArgTypes::TERMINAL)) {
        retStr = (retStr)->__iadd__((__str(this->value))->upper());
    }
    else {
        retStr = (retStr)->__iadd__((__str(this->value))->lower());
    }
    return retStr;
}

__ss_bool Arg::isVariable() {
    /**
    Returns true if 'Arg' object is a variable.
    */
    
    return ___bool((this->type==ArgTypes::VARIABLE));
}

__ss_bool Arg::__eq__(Arg *other) {
    /**
    Checks the equality of two `Arg` objects.
    */
    __ss_bool __3, __4, __5;

    return __AND(___bool((this->type==other->type)), __AND(___bool(__eq(this->value, other->value)), ___bool((this->isNegation==other->isNegation)), 4), 3);
}

void *Arg::__init__(__ss_int argType, str *argValue, __ss_bool isNegation) {
    /**
    Initializes the argument using `argType` and `argValue`.
    */
    
    this->type = argType;
    /**
    Type of the argument.
    */
    this->value = argValue;
    /**
    Value of the argument.
    */
    this->isNegation = isNegation;
    /**
    Helps in distinguishing between positive and negative literals.
    */
    return NULL;
}

/**
class PropositionTypes
*/

class_ *cl_PropositionTypes;

str *PropositionTypes::ON;
str *PropositionTypes::CLEAR;
str *PropositionTypes::HOLD;
str *PropositionTypes::EMPTY;
str *PropositionTypes::ONTABLE;

void PropositionTypes::__static__() {
    ON = const_2;
    ONTABLE = const_3;
    CLEAR = const_4;
    HOLD = const_5;
    EMPTY = const_6;
}

/**
class State
*/

class_ *cl_State;

void *State::addTrueSentence(TrueSentence *trueSentence) {
    /**
    Adds the `trueSentence` object to the state.
    */
    Arg *arg, *selfArg;
    __ss_bool alreadyPresent;
    list<Arg *> *__10, *__14, *__18;
    list<Arg *>::for_in_loop __13, __17, __21;
    __ss_int __12, __16, __20;
    __iter<Arg *> *__11, *__15, *__19;


    FOR_IN(arg,trueSentence->argList,10,12,13)
        if (arg->isVariable()) {
            return NULL;
        }
    END_FOR


    FOR_IN(arg,trueSentence->argList,14,16,17)
        alreadyPresent = False;

        FOR_IN(selfArg,this->groundTermList,18,20,21)
            if (__eq(arg, selfArg)) {
                alreadyPresent = True;
                break;
            }
        END_FOR

        if (__NOT(alreadyPresent)) {
            (this->groundTermList)->append(arg);
        }
    END_FOR

    (this->trueSentenceList)->append(trueSentence);
    return 0;
}

void *State::__init__(list<TrueSentence *> *trueSentenceList, list<Arg *> *groundTermList) {
    /**
    Initializes a `State` object.
    */
    
    this->trueSentenceList = (new list<TrueSentence *>(trueSentenceList));
    /**
    A list of objects of class TrueSentence.
    */
    this->groundTermList = (new list<Arg *>(groundTermList));
    /**
    A list of ground `Arg` objects in sentences in the `trueSentenceList` list.
    */
    this->prevState = NULL;
    /**
    This variable is used to figure out a path after searching is done.
    */
    this->prevAction = NULL;
    /**
    Stores the action taken to reach to this `State`.
    */
    this->prevAssignments = NULL;
    /**
    Stores the assignments made in the previous state to reach this state.
    */
    this->prevPrintData = const_0;
    /**
    Stores the string representing a combination of `self.prevAction` 
    and `self.prevAssignments`.
    */
    this->depth = 0;
    /**
    Housekeeping variable used to print progress.
    */
    return NULL;
}

list<State *> *State::getNextStates(list<Action *> *actionList) {
    /**
    Applies each action in `actionList` to the `self` state
    and returns all the states generated.
    */
    list<Action *>::for_in_loop __41;
    list<State *> *retList;
    Action *action;
    __iter<Action *> *__39;
    list<Action *> *__38;
    __ss_int __40;

    retList = (new list<State *>());

    FOR_IN(action,actionList,38,40,41)
        retList->extend(action->getStatesOnApplication(this));
    END_FOR

    return retList;
}

dict<str *, pyseq<str *> *> *State::tracePath() {
    /**
    Trace path from initial state to `self`.
    Returns a dictionary with:  
    (1) A string with actions (in order) in plan.
    (2) A list of states in the plan.
    */
    State *current, *state;
    dict<str *, pyseq<str *> *> *retDict;
    __iter<State *> *__7;
    list<State *> *__6, *pathList;
    str *retStr;
    list<State *>::for_in_loop __9;
    __ss_int __8;

    pathList = (new list<State *>());
    current = this;

    while (___bool(current)) {
        pathList->append(current);
        current = current->prevState;
    }
    pathList->reverse();
    retStr = const_0;

    FOR_IN(state,pathList,6,8,9)
        retStr = __add_strs(3, retStr, state->prevPrintData, const_7);
    END_FOR

    retDict = (new dict<str *, pyseq<***ERROR*** > *>());
    retDict->__setitem__(const_8, ((pyseq<***ERROR*** > *)retStr->strip()));
    retDict->__setitem__(const_9, ((pyseq<***ERROR*** > *)pathList));
    return retDict;
}

__ss_bool State::__eq__(str *other) {
    /**
    Checks equality of one `State` object with another.
    */
    
    return cmpList(((list<***ERROR*** > *)(this->trueSentenceList)), ((list<***ERROR*** > *)(other->trueSentenceList)));
}

void *State::removeTrueSentence(TrueSentence *trueSentenceArg) {
    /**
    Removes all objects "equal to" the `trueSentence` object from the state.
    */
    
    this->trueSentenceList = list_comp_0(this, trueSentenceArg);
    return NULL;
}

__ss_bool State::hasTrueSentences(list<TrueSentence *> *trueSentenceList) {
    /**
    Checks if all the sentences in `trueSentenceList` exist in the state.
    If they do not, returns `False`.
    */
    __ss_int __28, __32;
    list<TrueSentence *>::for_in_loop __29, __33;
    __iter<TrueSentence *> *__27, *__31;
    __ss_bool isPresent;
    list<TrueSentence *> *__26, *__30;
    TrueSentence *newSentence, *selfSentence;


    FOR_IN(newSentence,trueSentenceList,26,28,29)
        isPresent = False;

        FOR_IN(selfSentence,this->trueSentenceList,30,32,33)
            if (__eq(selfSentence, newSentence)) {
                isPresent = True;
                break;
            }
        END_FOR

        if (__NOT(isPresent)) {
            return False;
        }
    END_FOR

    return True;
}

__ss_bool State::isGoalState(str *goalState) {
    /**
    Checks if `state` is a goal state by comparing
    it to `goalState`. Returns `True` if it is, and `False` otherwise.
    Essentially compares two states.
    */
    
    return ___bool(__eq(goalState, ((***ERROR***)(this))));
}

/**
class TrueSentence
*/

class_ *cl_TrueSentence;

__ss_bool TrueSentence::__eq__(TrueSentence *other) {
    /**
    Check equality of `TrueSentence` objects.
    */
    __ss_bool __42, __43, __44;

    return __AND(___bool(__eq(this->propositionType, other->propositionType)), __AND(___bool((this->isNegation==other->isNegation)), cmpList(((list<***ERROR*** > *)(this->argList)), ((list<***ERROR*** > *)(other->argList))), 43), 42);
}

void *TrueSentence::__init__(str *propositionType, list<Arg *> *argList, __ss_bool isNegation) {
    /**
    Initializes a TrueSentence object.
    */
    
    this->propositionType = propositionType;
    /**
    Type of proposition.
    */
    this->argList = (new list<Arg *>(argList));
    /**
    List of Arg objects for the proposition.
    */
    this->isNegation = isNegation;
    /**
    "Adds" a negation sign before the statement.
    */
    return NULL;
}

/**
class Action
*/

class_ *cl_Action;

list<State *> *Action::getStatesOnApplicationUtil(State *stateObject, list<Arg *> *unassignedVariableList, dict<str *, Arg *> *assignments, list<State *> *retList) {
    /**
    Assign groundterms to unassigned variables in `unassignedVariableList`.
    Returns a list of `State` objects possible after
    application of `this` Action to `stateObject`
    `assignments` Dictionary of assignments already made.
    Keys in this are `value` parameters of `Arg` objects.
    Values in this dictionary are `Arg` objects.
    `retList` List of `State` objects already generated.
    */
    Arg *groundTerm, *thisVariable, *variable;
    list<TrueSentence *>::for_in_loop __84;
    __iter<TrueSentence *> *__82;
    list<Arg *> *__85, *__89, *groundTermList;
    TrueSentence *trueSentence;
    list<Arg *>::for_in_loop __88, __92;
    list<TrueSentence *> *__81, *groundTermTrueSentencesList;
    __ss_int __83, __87, __91;
    __iter<Arg *> *__86, *__90;

    if ((len(unassignedVariableList)==0)) {
        groundTermTrueSentencesList = (new list<TrueSentence *>());

        FOR_IN(trueSentence,this->preconditionList,81,83,84)
            groundTermList = (new list<Arg *>());

            FOR_IN(variable,trueSentence->argList,85,87,88)
                groundTermList->append(assignments->__getitem__(variable->value));
            END_FOR

            groundTermTrueSentencesList->append((new TrueSentence(trueSentence->propositionType, groundTermList, default_0)));
        END_FOR

        if (stateObject->hasTrueSentences(groundTermTrueSentencesList)) {
            retList->append(this->getStateOnActionUtil(stateObject, assignments));
        }
        return retList;
    }
    else {
        thisVariable = unassignedVariableList->pop();

        FOR_IN(groundTerm,stateObject->groundTermList,89,91,92)
            assignments->__setitem__(thisVariable->value, groundTerm);
            this->getStatesOnApplicationUtil(stateObject, unassignedVariableList, assignments, retList);
            assignments->pop(thisVariable->value);
        END_FOR

        unassignedVariableList->append(thisVariable);
        return retList;
    }
    return 0;
}

list<State *> *Action::getStatesOnApplication(State *stateObject) {
    /**
    Generates states after unification to input `stateObject`.
    Returns a list of `State` objects.
    List may be empty.
    The argument `stateObject` is not modified.
    */
    list<State *> *retList;
    dict<str *, Arg *> *assignments;

    assignments = (new dict<__ss_int, Arg *>());
    retList = (new list<State *>());
    return this->getStatesOnApplicationUtil(stateObject, this->variableTermList, assignments, retList);
}

State *Action::getStateOnActionUtil(State *stateObject, dict<str *, Arg *> *assignments) {
    /**
    Applies `this` Action to `stateObject` with given `assignments`.
    `assignments` Dictionary of assignments made.
    Returns a new `State` object.
    Does not modify `stateObject`.
    */
    list<str *> *__77;
    State *retState;
    Arg *savedArg, *variable;
    list<TrueSentence *>::for_in_loop __72;
    __iter<TrueSentence *> *__70;
    list<str *>::for_in_loop __80;
    __iter<str *> *__78;
    list<Arg *> *__73, *groundTermList;
    str *arg, *argListString;
    list<Arg *>::for_in_loop __76;
    __ss_int __71, __75, __79;
    list<TrueSentence *> *__69;
    TrueSentence *newTrueSentence, *trueSentence;
    __iter<Arg *> *__74;

    retState = (new State(stateObject->trueSentenceList, stateObject->groundTermList));

    FOR_IN(trueSentence,this->effectList,69,71,72)
        newTrueSentence = (new TrueSentence(trueSentence->propositionType, (new list<Arg *>()), default_0));
        groundTermList = (new list<Arg *>());

        FOR_IN(variable,trueSentence->argList,73,75,76)
            savedArg = assignments->__getitem__(variable->value);
            groundTermList->append((new Arg(savedArg->type, savedArg->value, savedArg->isNegation)));
        END_FOR

        newTrueSentence->argList = groundTermList;
        if (trueSentence->isNegation) {
            retState->removeTrueSentence(newTrueSentence);
        }
        else {
            retState->addTrueSentence(newTrueSentence);
        }
    END_FOR

    retState->prevAction = this;
    retState->prevAssignments = (new dict<__ss_int, Arg *>(assignments));
    argListString = const_0;

    FOR_IN(arg,this->argList,77,79,80)
        argListString = __add_strs(3, argListString, const_10, __str(assignments->__getitem__(arg)));
    END_FOR

    retState->prevPrintData = __add_strs(4, const_11, this->name, argListString, const_12);
    return retState;
}

void *Action::__init__(str *name, list<str *> *argList, list<TrueSentence *> *preconditionList, list<TrueSentence *> *effectList) {
    /**
    Initializes an Action object.
    */
    TrueSentence *precondition;
    list<TrueSentence *>::for_in_loop __52;
    __iter<TrueSentence *> *__50;
    __ss_bool alreadyPresent;
    list<Arg *> *__53, *__57;
    Arg *arg, *selfArg;
    list<Arg *>::for_in_loop __56, __60;
    list<TrueSentence *> *__49;
    __ss_int __51, __55, __59;
    __iter<Arg *> *__54, *__58;

    this->name = name;
    /**
    Name of the action.
    */
    this->argList = argList;
    /**
    List of entities on which the action is applied.
    */
    this->preconditionList = (new list<TrueSentence *>(preconditionList));
    /**
    Preconditions: a list of TrueSentence objects
    */
    this->effectList = (new list<TrueSentence *>(effectList));
    /**
    Effects: a list of TrueSentence objects
    */
    this->variableTermList = (new list<Arg *>());
    /**
    A list of `Arg` objects in sentences in the `preconditionList` list.
    */

    FOR_IN(precondition,preconditionList,49,51,52)

        FOR_IN(arg,precondition->argList,53,55,56)
            alreadyPresent = False;

            FOR_IN(selfArg,this->variableTermList,57,59,60)
                if (__eq(arg, selfArg)) {
                    alreadyPresent = True;
                    break;
                }
            END_FOR

            if (__NOT(alreadyPresent)) {
                (this->variableTermList)->append(arg);
            }
        END_FOR

    END_FOR

    return NULL;
}

str *bfs(str *startState, str *goalState, list<Action *> *actionList) {
    /**
    Performs a breadth-first search on states.
    Returns a `State` object which is equivalent
    to the goal state (`goalState`). A plan can be
    obtained by tracing the `prevState` pointers in states.
    */
    list<str *> *bfsQueue;
    State *neighborState;
    __iter<State *> *__94;
    list<State *> *__93, *neighborList;
    str *poppedState;
    list<State *>::for_in_loop __96;
    __ss_int __95;

    bfsQueue = (new list<***ERROR*** >());
    bfsQueue->append(startState);

    while ((len(bfsQueue)>0)) {
        poppedState = bfsQueue->pop(0);
        print(1, 0, const_13, 0, (const_14)->__add__(__str(poppedState->depth)));
        if (poppedState->isGoalState(goalState)) {
            return poppedState;
        }
        neighborList = poppedState->getNextStates(actionList);

        FOR_IN(neighborState,neighborList,93,95,96)
            neighborState->prevState = ((State *)(poppedState));
            neighborState->depth = (poppedState->depth+1);
        END_FOR

        bfsQueue->extend(neighborList);
    }
    return NULL;
}

__ss_bool cmpList(list<Arg *> *first, list<Arg *> *second) {
    /**
    "Deep" compares two lists. Returns `True` of they are equal, and
    `False` otherwise.
    */
    Arg *item, *itemInList, *other;
    __iter<TrueSentence *> *__102;
    __ss_bool exists;
    list<Arg *> *__101, *__97, *dupFirst, *dupSecond;
    list<Arg *>::for_in_loop __100, __104;
    __ss_int __103, __99;
    __iter<Arg *> *__98;

    if (__NOT((len(first)==len(second)))) {
        return False;
    }
    dupFirst = (new list<***ERROR*** >(first));
    dupSecond = (new list<***ERROR*** >(second));

    FOR_IN(item,dupFirst,97,99,100)
        exists = False;
        itemInList = NULL;

        FOR_IN(other,dupSecond,101,103,104)
            if (__eq(item, other)) {
                exists = True;
                itemInList = other;
                break;
            }
        END_FOR

        if (__NOT(exists)) {
            return False;
        }
        dupSecond->remove(itemInList);
    END_FOR

    return True;
}

list<Action *> *getActionsForBlocksWorld() {
    /**
    Hardcoded actions for the Blocks World.
    */
    Action *pickBlock, *releaseBlock, *stackBlockAOnTopOfBlockB, *unstackBlockAFromTopOfBlockB;

    pickBlock = (new Action(const_15, (new list<str *>(1,const_16)), (new list<TrueSentence *>(3,(new TrueSentence(PropositionTypes::ONTABLE, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_16, False)))), False)),(new TrueSentence(PropositionTypes::CLEAR, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_16, False)))), False)),(new TrueSentence(PropositionTypes::EMPTY, (new list<Arg *>()), False)))), (new list<TrueSentence *>(4,(new TrueSentence(PropositionTypes::HOLD, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_16, False)))), False)),(new TrueSentence(PropositionTypes::CLEAR, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_16, False)))), True)),(new TrueSentence(PropositionTypes::ONTABLE, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_16, False)))), True)),(new TrueSentence(PropositionTypes::EMPTY, (new list<Arg *>()), True))))));
    unstackBlockAFromTopOfBlockB = (new Action(const_17, (new list<str *>(2,const_18,const_19)), (new list<TrueSentence *>(3,(new TrueSentence(PropositionTypes::ON, (new list<Arg *>(2,(new Arg(ArgTypes::VARIABLE, const_18, False)),(new Arg(ArgTypes::VARIABLE, const_19, False)))), False)),(new TrueSentence(PropositionTypes::CLEAR, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_18, False)))), False)),(new TrueSentence(PropositionTypes::EMPTY, (new list<Arg *>()), False)))), (new list<TrueSentence *>(5,(new TrueSentence(PropositionTypes::HOLD, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_18, False)))), False)),(new TrueSentence(PropositionTypes::CLEAR, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_19, False)))), False)),(new TrueSentence(PropositionTypes::ON, (new list<Arg *>(2,(new Arg(ArgTypes::VARIABLE, const_18, False)),(new Arg(ArgTypes::VARIABLE, const_19, False)))), True)),(new TrueSentence(PropositionTypes::CLEAR, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_18, False)))), True)),(new TrueSentence(PropositionTypes::EMPTY, (new list<Arg *>()), True))))));
    releaseBlock = (new Action(const_20, (new list<str *>(1,const_16)), (new list<TrueSentence *>(1,(new TrueSentence(PropositionTypes::HOLD, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_16, False)))), False)))), (new list<TrueSentence *>(4,(new TrueSentence(PropositionTypes::ONTABLE, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_16, False)))), False)),(new TrueSentence(PropositionTypes::CLEAR, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_16, False)))), False)),(new TrueSentence(PropositionTypes::HOLD, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_16, False)))), True)),(new TrueSentence(PropositionTypes::EMPTY, (new list<Arg *>()), False))))));
    stackBlockAOnTopOfBlockB = (new Action(const_21, (new list<str *>(2,const_18,const_19)), (new list<TrueSentence *>(2,(new TrueSentence(PropositionTypes::CLEAR, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_19, False)))), False)),(new TrueSentence(PropositionTypes::HOLD, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_18, False)))), False)))), (new list<TrueSentence *>(5,(new TrueSentence(PropositionTypes::ON, (new list<Arg *>(2,(new Arg(ArgTypes::VARIABLE, const_18, False)),(new Arg(ArgTypes::VARIABLE, const_19, False)))), False)),(new TrueSentence(PropositionTypes::CLEAR, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_18, False)))), False)),(new TrueSentence(PropositionTypes::HOLD, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_18, False)))), True)),(new TrueSentence(PropositionTypes::CLEAR, (new list<Arg *>(1,(new Arg(ArgTypes::VARIABLE, const_19, False)))), True)),(new TrueSentence(PropositionTypes::EMPTY, (new list<Arg *>()), False))))));
    return (new list<Action *>(4,pickBlock,unstackBlockAFromTopOfBlockB,releaseBlock,stackBlockAOnTopOfBlockB));
}

dict<str *, str *> *readFile(str *fileName) {
    /**
    Returns a dictionary with initial state, final state and
    the "mode" of operation as read from the `fileName` file.
    Keys in dictionary are:
        planner, initState, goalState
    */
    list<str *> *__118, *__122, *lines, *validPlanners, *words;
    State *goalState, *initState;
    list<str *>::for_in_loop __121, __125;
    __ss_bool isNegation;
    str *propositionType, *word;
    file *inFile;
    list<Arg *> *argList, *completeBlockList;
    __iter<str *> *__119, *__123;
    dict<str *, str *> *retDict;
    __ss_int __116, __117, __120, __124, i, numberBlocks;

    retDict = (new dict<str *, ***ERROR*** >());
    WITH_VAR(open(fileName),inFile,0)
        lines = inFile->readlines();
        lines = list_comp_1(lines);
        try {
            numberBlocks = __int(lines->__getfast__(0));
        } catch (ValueError *) {
            print(1, 0, 0, 0, const_22);
            return NULL;
        }
        completeBlockList = (new list<Arg *>());

        FAST_FOR(i,1,(numberBlocks+1),1,116,117)
            completeBlockList->append((new Arg(ArgTypes::TERMINAL, i, False)));
        END_FOR

        validPlanners = (new list<str *>(3,const_23,const_24,const_25));
        if (__NOT((validPlanners)->__contains__(lines->__getfast__(1)))) {
            print(1, 0, 0, 0, const_26);
            return NULL;
        }
        retDict->__setitem__(const_27, ((***ERROR***  )lines->__getfast__(1)));
        if (__NOT(__eq(lines->__getfast__(2), const_28))) {
            print(1, 0, 0, 0, const_29);
            return NULL;
        }
        initState = (new State((new list<TrueSentence *>()), (new list<Arg *>())));
        words = (lines->__getfast__(3))->split();
        argList = (new list<Arg *>());
        propositionType = NULL;

        FOR_IN(word,words,118,120,121)
            if (__eq(word->__getfast__(0), const_11)) {
                argList = (new list<Arg *>());
                propositionType = word->strip(const_11);
            }
            else {
                try {
                    argList->append(completeBlockList->__getfast__((__int(word->strip(const_12))-1)));
                } catch (Exception *) {
                    print(1, 0, 0, 0, const_30);
                    return NULL;
                }
            }
            if (__eq(word->__getfast__((-1)), const_12)) {
                initState->addTrueSentence((new TrueSentence(propositionType->strip(const_12), argList, default_0)));
            }
        END_FOR

        retDict->__setitem__(const_31, ((***ERROR***  )initState));
        if (__NOT(__eq(lines->__getfast__(4), const_32))) {
            print(1, 0, 0, 0, const_33);
            return NULL;
        }
        goalState = (new State((new list<TrueSentence *>()), (new list<Arg *>())));
        words = (lines->__getfast__(5))->split();
        argList = (new list<Arg *>());
        propositionType = NULL;
        isNegation = False;

        FOR_IN(word,words,122,124,125)
            if (__eq(word->__getfast__(0), const_1)) {
                isNegation = True;
                word = word->strip(const_1);
            }
            if (__eq(word->__getfast__(0), const_11)) {
                argList = (new list<Arg *>());
                propositionType = word->strip(const_11);
            }
            else {
                try {
                    argList->append(completeBlockList->__getfast__((__int(word->strip(const_12))-1)));
                } catch (Exception *) {
                    print(1, 0, 0, 0, const_30);
                    return NULL;
                }
            }
            if (__eq(word->__getfast__((-1)), const_12)) {
                goalState->addTrueSentence((new TrueSentence(propositionType->strip(const_12), argList, isNegation)));
                isNegation = False;
            }
        END_FOR

        retDict->__setitem__(const_34, ((***ERROR***  )goalState));
        return retDict;
    END_WITH
    return 0;
}

void *writeFile(str *fileName, __ss_int numActions, pyseq<str *> *outputString) {
    /**
    Writes `outputString` to the given file. 
    `fileName` pathname of the file to write to.
    */
    file *f;

    f = open(fileName, const_35);
    f->write((__str(numActions))->__add__(const_7));
    f->write(outputString);
    f->close();
    return NULL;
}

void *__ss_main() {
    /**
    Take input argument (a file name), and write soduko solutions 
    to a file.
    */
    list<Action *> *actionList;
    dict<str *, pyseq<str *> *> *traceData;
    str *bfsData, *fileName;
    dict<str *, str *> *readData;
    __ss_int numActions;
    pyseq<str *> *outputString;

    if ((len(__sys__::argv)<2)) {
        print(1, 0, 0, 0, const_36);
    }
    else {
        actionList = getActionsForBlocksWorld();
        fileName = __str((__sys__::argv)->__getfast__(1));
        readData = readFile(fileName);
        traceData = NULL;
        outputString = const_0;
        numActions = 0;
        if (__eq(readData->__getitem__(const_27), const_23)) {
            bfsData = bfs(readData->__getitem__(const_31), readData->__getitem__(const_34), actionList);
            traceData = bfsData->tracePath();
            outputString = traceData->__getitem__(const_8);
            numActions = (len(traceData->__getitem__(const_9))-1);
        }
        else if (__eq(readData->__getitem__(const_27), const_24)) {
        }
        else if (__eq(readData->__getitem__(const_27), const_25)) {
        }
        else {
            print(1, 0, 0, 0, const_37);
        }
        if ((len(outputString)>0)) {
            writeFile((fileName->__slice__(2, 0, (-4), 0))->__add__(const_38), numActions, outputString);
        }
        else {
            print(1, 0, 0, 0, const_39);
        }
    }
    return NULL;
}

void __init() {
    __name__ = new str("__main__");

    cl_ArgTypes = new class_("ArgTypes");
    ArgTypes::__static__();
    cl_Arg = new class_("Arg");
    cl_PropositionTypes = new class_("PropositionTypes");
    PropositionTypes::__static__();
    cl_State = new class_("State");
    default_0 = False;
    cl_TrueSentence = new class_("TrueSentence");
    cl_Action = new class_("Action");
    __ss_main();
}

} // module namespace

int main(int __ss_argc, char **__ss_argv) {
    __shedskin__::__init();
    __sys__::__init(__ss_argc, __ss_argv);
    __shedskin__::__start(__p1__::__init);
}
