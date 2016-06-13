## Implementation of AI planners
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/tushar-agarwal/ai-planners/blob/master/LICENSE.md) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/479703ffd6ac4b53b8c377e16bcd6658)](https://www.codacy.com/app/tushar-agarwal/ai-planners?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tushar-agarwal/ai-planners&amp;utm_campaign=Badge_Grade) [![Category](https://img.shields.io/badge/Category-Coursework-ff69b4.svg)](https://github.com/tushar-agarwal/ai-planners)

Code documentation is available <a href="http://tushar-agarwal.github.io/ai-planners/" target="_blank">here</a>.

Sample test cases are present: `1.txt`, `2.txt`, `3.txt`, `4.txt`, `5.txt` and `6.txt`.

### Description

`p1.py` implements:

1. A forward (progression) planner using breadth first search
2. A forward (progression) planner using A* search
3. A goal stack planner

The are designed for the blocks world problem. The blocks world is described as follows.

> There are `N` blocks, table and a robotic arm. Blocks are identified by integers `1` to `N`. Each block can sit on top of another block or on the table. There can be a stack of blocks of arbitrary height. However only one block can be directly on another block. No two blocks can be sitting directly on the same block. The bottom most block of a stack must be on the table. The table can hold any number of blocks. If there is no block on top of a block, then the block is clear. The robotic arm can hold only one block. If the robotic arm does not hold any block, it is empty.

The propositions for this problem are as follows.

```
(on blocka blocka) – meaning "blocka" is stacked on "blockb" 
(ontable block)
(clear block)
(hold block)
(empty)
```

There are 4 actions specified using the following schemas.

```
action(pick block)
preconditions – (ontable block) (clear block) (empty)
effects – (hold block) ~(clear block) ~(empty) ~(ontable block)
```

```
action(unstack blocka blockb)
preconditions – (on blocka blockb) (clear blocka) (empty)
effects – (hold blocka) clear(blockb) ~(on blocka blockb) ~(empty) ~(clear blocka)
```

```
action(release block)
preconditions – (hold block)
effects – (ontable block) (clear block) (empty) ~(hold block)
```

```
action(stack blocka blockb)
preconditions – clear(blockb) (hold blocka)
effects – (on blocka blockb) (clear blocka) (empty) ~(hold blocka) ~(clear blockb)
```

In `p1.py`, actions are encoded in a way which makes modification easy.

A state will be specified as a list of propositions that hold good in that state separated by a space in a single line. For example, in a 3-blocks world, a state can be `(on 1 2) (clear 1) (ontable 3) (ontable 2) (clear 3) (empty)`.

Given a text file containing the initial and goal state description, and the choice of the planning approach, `p1.py` outputs a file containing the plan from the initial state to the goal state.

#### How to execute  
`python p1.py p.txt`

Here, the `p.txt` refers to a file with a blocks world problem instance as per the input format described below. The output will be written to `p_out.txt`. In general, for input filename `name.ext`, the output will be written to `name_out.ext`. A three-letter extension is assumed. 

#### Input  
The input argument is the name of the text file containing a blocks world problem instance. Specifically, the format of the input file is as follows.

```
N
planner
initial
State description
goal
State description
```

The first line is the number of blocks in the blocks world. The second line indicates the choice of the planner (`f`-forward planner with BFS, `a`-forward planner A* search and `g`- goal stack planner). The third line indicates that the line following it contains the complete description of the initial state. This is followed by the line containing the term goal. This is in turn followed by the line that completely describes the goal state.

#### Output
The code writes to a text file in the following format.

```
NA
Action 1
Action 2
...
Action NA
```

The first line indicates the number of actions in the plan. Each line then presents the action that has to be taken. 

#### A* heuristic

To calculate a heuristic value for a state, the heuristic computation algorithm relaxes the problem and solves an easier version of the problem. The heuristic computation algorithm performs a breadth-first forward search with relaxation in the following two ways:

1. Delete lists are ignored when a state is expanded. Hence, monotonic progress is made
towards the goal state.
2. When a state is expanded, all possible actions are applied at once, together. This helps to
control the branching factor which otherwise, if only technique `(1)` was used, may result in the creation of extremely large number of states.

##### A note on the Goal Stack planner

A problem specific heuristic is utilized to decide on relevant actions to insert onto the goal stack. The generalized goal stack planner is also implemented, but performs worse than the specialized version. 

*Some data for this readme is drawn from lab assignments present <a href="http://cse.iitrpr.ac.in/ckn/courses/s2016/csl452/csl452.html#labs" target="_blank">here</a>.*
