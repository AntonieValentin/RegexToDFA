from collections.abc import Callable
from dataclasses import dataclass
from itertools import product
import pandas as pd
from typing import TypeVar
from functools import reduce
import numpy as np

STATE = TypeVar('STATE')

@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]
    

    def accept(self, word: str) -> bool:
        state = self.q0
        while (len(word)):
            state = self.d.get((state, word[0]))
            word = word[1:]
        if (state in self.F):
            return True
        else:
            return False

    def minimize(self) -> 'DFA[frozenset[STATE]]':
        mark: dict[tuple[STATE, STATE], int] = {}
        dinverse: dict[tuple[STATE, str], set[STATE]] = {}
        for ((state1, c)) in self.d:
            state2 = self.d.get((state1, c))
            if (state2, c) not in dinverse:
                dinverse[(state2, c)] = set()
            dinverse[(state2, c)].add(state1)
            
        for i in self.K:
            for j in self.F:
                if (i not in self.F):
                    mark[(i, j)] = 1
                    mark[(j, i)] = 1
        ok = 1
        while ok == 1:
            ok = 0
            for i in self.K:
                for j in self.K:
                    if mark.get((i, j)) == 1:
                        for c in self.S:
                            if dinverse.get((i, c)) and dinverse.get((j, c)):
                                for elem1 in dinverse.get((i, c)):
                                    for elem2 in dinverse.get((j, c)):
                                        if (mark.get((elem1, elem2)) != 1):
                                            mark[(elem1, elem2)] = 1
                                            mark[(elem2, elem1)] = 1
                                            ok = 1
        setList = []
        for i in self.K:
            for j in self.K:
                if mark.get((i, j)) == None and i != j:
                    okSet = 0
                    for k in setList:
                        if (i in k) or (j in k):
                            okSet = 1
                            k.add(i)
                            k.add(j)
                            break
                    if (okSet == 0):
                        setElem = set()
                        setElem.add(i)
                        setElem.add(j)
                        setList.append(setElem)
        for state in self.K:
            okSetFind = 0
            for s in setList:
                if state in s:
                    okSetFind = 1
                    break
            if okSetFind == 0:
                setElem = set()
                setElem.add(state)
                setList.append(setElem)
        S = self.S
        K = set()
        i = 0
        m: dict[STATE, STATE] = {}
        for s in setList:
            state = frozenset(s) 
            for j in s:
                m[j] = state
            K.add(state)
            i = i + 1
        q0 = m.get(self.q0)
        d: dict[tuple[STATE, str], STATE] = {}
        F = set()
        for statef in self.F:
            F.add(m[statef])
        for state in self.K:
            for c in self.S:
                if self.d.get((state, c)) is not None:
                    d[(m[state], c)] = m[self.d.get((state, c))]
        min_dfa = DFA(S, K, q0, d, F)
        return min_dfa
        
    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':
        K = set()
        for state in self.K:
            K.add(f(state))
        q0 = f(self.q0)

        d: dict[tuple[OTHER_STATE, str], STATE]= {}
        for state in self.K:
            for c in self.S:
                if self.d.get((state, c)) is not None:
                    d[(f(state), c)] = f(self.d.get((state, c)))
        F = set()
        for stateF in self.F:
            F.add(f(stateF))
        other_dfa = DFA(self.S, K, q0, d, F)
        return other_dfa
    
    

 