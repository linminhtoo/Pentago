# Pentago
The game of Pentago, for CM4043
- Developing the game is mostly manipulating numpy/python functions, which is a fun coding exercise,
- plus building test cases to ensure everything works before we make more complex functions.
- **The AI was the most challenging part** - see minimax.py
- a naive bruteforce search of all possible moves using the minimax algorithm is very computationally expensiv
- and actually an area of ongoing research. To speed up the process, we searched the literature and executed two ideas.
1. **alpha-beta pruning** to prune the recursive search tree. in simple terms, gamestates that we know will not be better than already-explored gamestates, so there is no point expanding & evaluating them.
2. building a **transposition table** to store board states whose 'values' have already been evaluated. This is just like the idea of memoization in recursive algorithms. This really speeds up the search.

# Instructions
To run the game, just do:
```
    python main.py
```
You may want to test all functions by running, which executes a suite of test cases
(although not using python's unittest module, which is a TODO)
```
    python test_all_funcs.py
```
# Requirements
Nothing fancy. This project uses numpy, typing, math, random & tqdm, all of which should already come with your Python installation.
Tested on Python 3.7