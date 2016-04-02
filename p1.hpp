#ifndef __P1_HPP
#define __P1_HPP

using namespace __shedskin__;
namespace __p1__ {

class ArgTypes;
class Arg;
class PropositionTypes;
class State;
class TrueSentence;
class Action;


extern str *__name__;


extern class_ *cl_ArgTypes;
class ArgTypes : public pyobj {
/**
This class contains constants for different types of arguments.
*/
public:
    static __ss_int VARIABLE;
    static __ss_int TERMINAL;

    ArgTypes() { this->__class__ = cl_ArgTypes; }
    static void __static__();
};

extern class_ *cl_Arg;
class Arg : public pyobj {
/**
This class represents an argument.
*/
public:
    __ss_int type;
    __ss_bool isNegation;
