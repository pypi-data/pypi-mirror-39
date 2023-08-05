# -*- coding: utf8 -*-

from typing import List, Dict, Tuple
from collections import defaultdict


class InfluenceGraph:
    def __init__(self):
        self._variables: Dict[str, Tuple[int]] = defaultdict(tuple)
        self._regulations = defaultdict(dict)

    def add_variable(self, name: str, *states: int):
        self._variables[name] = states

    def list_variables(self) -> Tuple[Tuple[str, Tuple[int]]]:
        return tuple(self._variables.items())

    def add_regulation(self, source: str, destination: str, expression: str):
        self._regulations[source][destination] = expression

    def list_regulations(self) -> Tuple[Tuple[str, str, str]]:
        regulations = []
        for source, d in self._regulations.items():
            for destination, expression in d.items():
                regulations.append((source, destination, expression))
        return tuple(regulations)

    def __str__(self):
        string = '\nInfluenceGraph\n\tvariables:'
        for variable, states in self.list_variables():
            string += f'\n\t\t{variable} = {" ".join(map(str, states))}'
        string += '\n\tregulations'
        for source, destination, expression in self.list_regulations():
            string += f'\n\t\t{source}: {expression} → {destination}'
        return string

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, InfluenceGraph):
            return False
        return (self._variables == other._variables
                and self._regulations == other._regulations)
