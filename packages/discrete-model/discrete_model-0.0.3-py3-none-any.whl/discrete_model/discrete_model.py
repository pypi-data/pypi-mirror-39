# -*- coding: utf8 -*-

from collections import defaultdict
from typing import Tuple, Dict

from .influence_graph import InfluenceGraph


class DiscreteModel:
    def __init__(self, influence_graph: InfluenceGraph):
        self.influence_graph = influence_graph
        self._assignment: Dict[str, Tuple[int]] = defaultdict(tuple)

    def set_variable_state(self, variable: str, *states: int):
        self._assignment[variable] = states

    def list_assignments(self) -> Tuple[Tuple[str, Tuple[int]]]:
        return tuple(self._assignment.items())

    def __str__(self):
        string = str(self.influence_graph)
        string += '\n\tmodel'
        for variable, states in self.list_assignments():
            string += f'\n\t\t{variable} {" ".join(map(str, states))}'
        return string

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, DiscreteModel):
            return False
        return (self.influence_graph == other.influence_graph
                and self._assignment == other._assignment)
