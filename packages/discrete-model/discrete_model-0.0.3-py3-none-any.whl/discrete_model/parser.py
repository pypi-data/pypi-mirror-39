# -*- coding: utf8 -*-

from typing import List, Iterable, Tuple
import re

from .influence_graph import InfluenceGraph
from .discrete_model import DiscreteModel


def parse_smbionet_output_file(filename: str) -> Tuple[DiscreteModel]:
    with open(filename) as output:
        return parse_smbionet_output_string(output.read())


def parse_smbionet_output_string(string: str) -> Tuple[DiscreteModel]:
    graph = InfluenceGraph()
    match = _create_pattern().match(string)
    _parse_variables(match['variables'], graph)
    _parse_regulations(match['regulations'], graph)
    return tuple(_parse_models(match['models'], graph))


def _create_pattern() -> re.Pattern:
    read_variables = r'\s*VAR(?P<variables>(?:.|\s)*?)'
    read_regulations = r'REG(?P<regulations>(?:.|\s)*?)'
    read_parameters = r'PARA(?P<parameters>(?:.|\s)*?)'
    read_ctl = r'CTL(?P<ctl>(?:.|\s)*?)'
    read_models = r'(?P<models>#(?:.|\s)*?)'
    read_check = r'(?P<checks>#\s*SELECTED MODELS(?:.|\s)*?)'
    return re.compile(
        '^'
        + read_variables
        + read_regulations
        + read_parameters
        + read_ctl
        + read_models
        + read_check
        + '$'
    )


def _parse_variables(string: str, graph: InfluenceGraph):
    pattern = re.compile(
        r'\s*(?P<variable>\w+)\s*=\s*(?P<states>(?:\d+\s+)*?\d+)\s*;')
    for match in pattern.finditer(string):
        graph.add_variable(match['variable'], *
                           map(int, match['states'].split()))


def _parse_regulations(string: str, graph: InfluenceGraph):
    pattern = re.compile(
        r'(?P<from>\w+)\s+\[(?P<predicate>.*?)\]\s*=>\s*(?P<to>\w+)')
    for match in pattern.finditer(string):
        graph.add_regulation(match['from'], match['to'],
                             _transform_predicate_to_a_valid_python_expression(match['predicate']))


def _transform_predicate_to_a_valid_python_expression(predicate: str):
    predicate = re.sub(r'[^<>]=', '==', predicate)
    predicate = re.sub(r'!', 'not', predicate)
    predicate = re.sub(r'\|', 'or', predicate)
    predicate = re.sub(r'&', 'and', predicate)
    return predicate


def _parse_models(string: str, graph: InfluenceGraph) -> Iterable[DiscreteModel]:
    pattern = re.compile(
        r'#\s+MODEL\s+(?P<id>\d+)\s+(?P<k_assigments>(?:(?!\s*#\s*MODEL).*\s*)*)')
    for match in pattern.finditer(string):
        yield _parse_k_assigments(match['k_assigments'], graph)


def _parse_k_assigments(string: str, graph: InfluenceGraph) -> DiscreteModel:
    model = DiscreteModel(graph)
    pattern = re.compile(
        r'#\s*(?P<variable>[^\s=]+)\s*=\s*(?P<states>(?:\d+\s+)*?\d+)\s*$', flags=re.MULTILINE)
    for match in pattern.finditer(string):
        model.set_variable_state(
            match['variable'], *map(int, match['states'].split()))
    return model
