# -*- coding: utf8 -*-

from typing import List, Dict, Tuple
from collections import defaultdict


class InfluenceGraph:
    def __init__(self):
        self._variables: Dict[str, Tuple[int]] = defaultdict(tuple)
        self._regulations = defaultdict(dict)

    def add_variable(self, name: str, *states: int):
        self._variables[name] = states

    def add_regulation(self, source: str, destination: str, expression: str):
        self._regulations[source][destination] = expression

    def __str__(self):
        string = '\nInfluenceGraph\n\tvariables:'
        for variable, states in self._variables.items():
            string += f'\n\t\t{variable} = {" ".join(map(str, states))}'
        string += '\n\tregulations'
        for source, d in self._regulations.items():
            for destination, expression in d.items():
                string += f'\n\t\t{source}: {expression} → {destination}'
        return string

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, InfluenceGraph):
            return False
        return (self._variables == other._variables
                and self._regulations == other._regulations)
