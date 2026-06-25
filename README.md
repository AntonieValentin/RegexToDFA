# Regex to MinDFA

A Python project for working with regular languages and finite automata. It implements the full conversion pipeline from a regular expression to an NFA, then to a DFA, and finally to a minimized DFA.

The project is based on the classic algorithms used in formal languages: Thompson construction for regex-to-NFA conversion, subset construction for NFA-to-DFA conversion, and DFA minimization for reducing equivalent states.

## Overview

The implementation is organized around three main abstractions:

* `Regex` - represents regular expressions and converts them into NFAs;
* `NFA` - represents nondeterministic finite automata, including epsilon transitions;
* `DFA` - represents deterministic finite automata and supports word acceptance and minimization.

Together, these classes make it possible to start from a regex and end with a compact deterministic automaton that recognizes the same language.

## Supported Regex Features

The parser supports the usual regex operators:

* concatenation;
* union with `|`;
* Kleene star `*`;
* one-or-more repetition `+`;
* optional expression `?`;
* grouped expressions using parentheses;
* `eps` for the empty word.

It also handles a few useful shortcuts:

* `[a-z]` for lowercase letters;
* `[A-Z]` for uppercase letters;
* `[0-9]` for digits.

Escaped characters can be used when an operator should be treated as a normal character.

## Automata Operations

The NFA implementation includes epsilon-closure computation and subset construction. Subset construction creates DFA states as sets of NFA states, which makes the transformation clear and close to the theoretical algorithm.

The DFA implementation can run an input word and decide whether it is accepted. It also includes minimization, which merges equivalent states and produces a smaller DFA with the same behavior.

## Conversion Flow

The typical workflow is:

```text
regular expression -> NFA -> DFA -> minimized DFA
```

For example, a regex is first translated into an NFA using Thompson construction. The NFA is then determinized through subset construction, and the resulting DFA can be minimized.

## Notes

The goal of the project is to connect the theory of regular languages with a concrete implementation. The code keeps the main algorithms visible instead of hiding them behind library calls, which makes the project useful for understanding how regex engines and automata transformations work internally.
