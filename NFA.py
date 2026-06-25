from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        s = set()
        s.add(state)
        ok = 1
        while (ok == 1):
            ok = 0
            for k in s:
                states = self.d.get((k, ''))
                if (states is not None) and ((len(s.union(states))) > len(s)):
                    s = s.union(states)
                    ok = 1 
        return s


    def subset_construction(self) -> DFA[frozenset[STATE]]:
        q0 = self.epsilon_closure(self.q0)
        qi = frozenset(q0)
        mark: dict[frozenset[STATE], int] = {}
        K = set()
        K.add(frozenset(q0))
        d: dict[tuple[frozenset[STATE], str], frozenset[STATE]] = {}
        F = set()
        for state in self.F:
            if state in qi:
                F.add(qi)
                break
        states = set()
        states.add(qi)
        ok = 1
        while(ok == 1):
            s = set()
            ok = 0
            for c in self.S:
                for state in states:
                    s_curr = set()
                    for statei in state:
                        if (self.d.get((statei, c)) is not None):
                            for sepsilon in self.d.get((statei, c)):
                                s_curr = s_curr.union(self.epsilon_closure(sepsilon))
                    if (mark.get(state) != 1):
                        for state2 in self.F:
                            if state2 in s_curr:
                                F.add(frozenset(s_curr))
                                break
                        d[(state, c)] = frozenset(s_curr)
                        K.add(frozenset(s_curr))
                        s.add(frozenset(s_curr))
            for state in states:
                if (mark.get(state) != 1):
                    ok = 1
                    mark[state] = 1
            states = s
        dfa = DFA(self.S, K, frozenset(q0), d, F)
        return dfa

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        return self
