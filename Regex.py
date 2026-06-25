from typing import Any, List
from .NFA import NFA

EPSILON = ''

class Regex:

    def thompson(self) -> NFA[int]:
        pass
        
class Character(Regex):
    def __init__(self, char: str):
        self.char = char
    def thompson(self) -> NFA[int]:
        S = set()
        if (self.char != EPSILON):
            S.add(self.char)
        K = set()
        K.add(0)
        K.add(1)
        q0 = 0
        d: dict[tuple[STATE, str], set[STATE]] = {}
        s = set()
        s.add(1)
        d[(0, self.char)] = s
        F = set()
        F.add(1)
        nfa = NFA(S, K, q0, d, F)
        return nfa

class CharacterRangeLower(Regex):
    def thompson(self) -> NFA[int]:
        S = set()
        for i in range(0, 26):
             S.add(chr(ord('a') + i))
        K = set()
        K.add(0)
        K.add(1)
        q0 = 0
        d: dict[tuple[STATE, str], set[STATE]] = {}
        s = set()
        s.add(1)
        for i in range(0, 26):
            d[(0, chr(ord('a') + i))] = s
        F = set()
        F.add(1)
        nfa = NFA(S, K, q0, d, F)
        return nfa

class CharacterRangeUpper(Regex):
    def thompson(self) -> NFA[int]:
        S = set()
        for i in range(0, 26):
             S.add(chr(ord('A') + i))
        K = set()
        K.add(0)
        K.add(1)
        q0 = 0
        d: dict[tuple[STATE, str], set[STATE]] = {}
        s = set()
        s.add(1)
        for i in range(0, 26):
            d[(0, chr(ord('A') + i))] = s
        F = set()
        F.add(1)
        nfa = NFA(S, K, q0, d, F)
        return nfa

class DigitRange(Regex):
    def thompson(self) -> NFA[int]:
        S = set()
        for i in range(0, 10):
             S.add(str(i))
        K = set()
        K.add(0)
        K.add(1)
        q0 = 0
        d: dict[tuple[STATE, str], set[STATE]] = {}
        s = set()
        s.add(1)
        for i in range(0, 10):
            d[(0, (str(i)))] = s
        F = set()
        F.add(1)
        nfa = NFA(S, K, q0, d, F)
        return nfa

class Star(Regex):
    def __init__(self, regex: Regex):
        self.regex = regex
    def thompson(self) -> NFA[int]:
        original_nfa = self.regex.thompson()
        S = original_nfa.S
        K = set()
        Max = 0
        for i in original_nfa.K:
            K.add(i+1)
            Max = max(Max, i + 1)
        K.add(0)
        K.add(Max + 1)
        q0 = 0
        d: dict[tuple[STATE, str], set[STATE]] = {}
        for (qi, ch) in original_nfa.d:
            s = set()
            for i in original_nfa.d.get((qi, ch)):
                s.add(i + 1)
            d[(qi + 1, ch)] = s
        d[(0, EPSILON)] = {1}
        d[(0, EPSILON)].add(Max + 1)
        d[(Max, EPSILON)] = {1}
        d[(Max, EPSILON)].add(Max + 1)
        F = set()
        F.add(Max + 1)
        nfa = NFA(S, K, q0, d, F)
        return nfa

class Plus(Regex):
    def __init__(self, regex: Regex):
        self.regex = regex
    def thompson(self) -> NFA[int]:
        original_nfa = self.regex.thompson()
        S = original_nfa.S
        K = set()
        Max = 0
        for i in original_nfa.K:
            K.add(i+1)
            Max = max(Max, i + 1)
        K.add(0)
        K.add(Max + 1)
        q0 = 0
        d: dict[tuple[STATE, str], set[STATE]] = {}
        for (qi, ch) in original_nfa.d:
            s = set()
            for i in original_nfa.d.get((qi, ch)):
                s.add(i + 1)
            d[(qi + 1, ch)] = s
        d[(0, EPSILON)] = {1}
        d[(Max, EPSILON)] = {1}
        d[(Max, EPSILON)].add(Max + 1)
        F = set()
        F.add(Max + 1)
        nfa = NFA(S, K, q0, d, F)
        return nfa

class Question(Regex):
    def __init__(self, regex: Regex):
        self.regex = regex
    def thompson(self) -> NFA[int]:
        original_nfa = self.regex.thompson()
        S = original_nfa.S
        K = set()
        Max = 0
        for i in original_nfa.K:
            K.add(i+1)
            Max = max(Max, i + 1)
        K.add(0)
        K.add(Max + 1)
        q0 = 0
        d: dict[tuple[STATE, str], set[STATE]] = {}
        for (qi, ch) in original_nfa.d:
            s = set()
            for i in original_nfa.d.get((qi, ch)):
                s.add(i + 1)
            d[(qi + 1, ch)] = s
        d[(0, EPSILON)] = {1}
        d[(0, EPSILON)].add(Max + 1)
        d[(Max, EPSILON)] = {Max + 1}
        F = set()
        F.add(Max + 1)
        nfa = NFA(S, K, q0, d, F)
        return nfa

class Concat(Regex):
    def __init__(self, regex1: Regex, regex2: Regex):
        self.regex1 = regex1
        self.regex2 = regex2
    def thompson(self) -> NFA[int]:
        original_nfa1 = self.regex1.thompson()
        original_nfa2 = self.regex2.thompson()
        S = original_nfa1.S.union(original_nfa2.S)
        K = set()
        for i in original_nfa1.K:
            K.add(i)
        for i in original_nfa2.K:
            K.add(i+len(original_nfa1.K))
        q0 = 0
        d = original_nfa1.d
        for (qi, ch) in original_nfa2.d:
            s = set()
            for i in original_nfa2.d.get((qi, ch)):
                s.add(i + len(original_nfa1.K))
            d[(qi + len(original_nfa1.K), ch)] = s
        d[(len(original_nfa1.K)-1, EPSILON)] = {len(original_nfa1.K)}
        F = set()
        F.add(len(original_nfa2.K) + len(original_nfa1.K) - 1)
        nfa = NFA(S, K, q0, d, F)
        return nfa


class Union(Regex):
    def __init__(self, regex1: Regex, regex2: Regex):
        self.regex1 = regex1
        self.regex2 = regex2
    def thompson(self) -> NFA[int]:
        original_nfa1 = self.regex1.thompson()
        original_nfa2 = self.regex2.thompson()
        S = original_nfa1.S.union(original_nfa2.S)
        K = set()
        for i in original_nfa1.K:
            K.add(i+1)
        for i in original_nfa2.K:
            K.add(i+len(original_nfa1.K)+1)
        K.add(0)
        K.add(len(original_nfa2.K) + len(original_nfa1.K) + 1)
        q0 = 0
        d: dict[tuple[STATE, str], set[STATE]] = {}
        for (qi, ch) in original_nfa1.d:
            s = set()
            for i in original_nfa1.d.get((qi, ch)):
                s.add(i + 1)
            d[(qi + 1, ch)] = s
        
        for (qi, ch) in original_nfa2.d:
            s = set()
            for i in original_nfa2.d.get((qi, ch)):
                s.add(i + len(original_nfa1.K) + 1)
            d[(qi + len(original_nfa1.K) + 1, ch)] = s
        d[(0, EPSILON)] = {1}
        d[(0, EPSILON)].add(len(original_nfa1.K)+1)
        d[(len(original_nfa1.K), EPSILON)] = {len(original_nfa2.K) + len(original_nfa1.K) + 1}
        d[(len(original_nfa2.K) + len(original_nfa1.K), EPSILON)] = {len(original_nfa2.K) + len(original_nfa1.K) + 1}
        F = set()
        F.add(len(original_nfa2.K) + len(original_nfa1.K) + 1)
        nfa = NFA(S, K, q0, d, F)
        return nfa

def parse_regex(s: str) -> Regex:
    L1 = []
    L2 = []
    regex = Character(EPSILON)
    prev = None
    okRange = False
    prev2 = None
    prev3 = None
    for i in s:
        if (i == '['):
            prev2 = prev
            okRange = True
        if prev == '\\':
           L1.append(Character(i))
           if (prev3 != '|'):
              L2.append("Concat")
           if (i == ' '):
              prev3 = prev
              prev = ' ' 
            
        elif (i != ' ' and i != '*' and i != '+' and i != '?' and i != '|' and i != '(' and i != ')' and i != '\\'and okRange == False):
            L1.append(Character(i))
            if (prev != '|'):
                L2.append("Concat")
        elif (i == '*'):
            temp = L1[-1]
            L1.pop()
            L1.append(Star(temp))
        elif (i == '+'):
            temp = L1[-1]
            L1.pop()
            L1.append(Plus(temp))
        elif (i == '?'):
            temp = L1[-1]
            L1.pop()
            L1.append(Question(temp))
        elif (i == ']'):
            if (prev == '9'):
                L1.append(DigitRange())
            elif (prev == 'z'):
                L1.append(CharacterRangeLower())
            elif (prev == 'Z'):
                L1.append(CharacterRangeUpper())
            if (prev2 != '|'):
                L2.append("Concat")
            okRange = False
        elif (i == '|'):
            unify = Character(EPSILON)
            while (len(L2) and L2[-1] == 'Concat'):
                unify  = Concat(L1[-1], unify)
                L2.pop()
                L1.pop()
            L1.append(unify)
            L2.append("Concat")
            L2.append("Union")
        elif (i == '('):
            L2.append("(")
        elif (i == ')'):
            unify = Character(EPSILON)
            while (L2[-1] != '('):
                if (L2[-1] == 'Concat'):
                    unify = Concat(L1[-1], unify)
                else:
                    temp = L1[-1]
                    L2.pop()
                    L1.pop()
                    unify = Union(L1[-1], Concat(temp, unify))
                L2.pop()
                L1.pop()
            L2.pop()
            L1.append(unify)
            if (len(L2) == 0 or L2[-1] != 'Union'):
                L2.append("Concat")
        if (i != ' '):
            prev3 = prev
            prev = i

    k = 0
    for c in L1:
        if (L2[k] == "Concat"):
            regex = Concat(regex, c)
        else:
            regex = Union(regex, c)
        prev = c
        k += 1
    return regex


