# -*- coding: utf8 -*-

from collections import defaultdict
from itertools import product
from typing import Any, Dict, Iterable, List, Tuple
import re
import networkx as nx
from networkx.drawing.nx_pydot import to_pydot, write_dot
from discrete_model import DiscreteModel, Gene, InfluenceGraph

Variables = Dict[str, List[int]]
Relations = Dict[str, Dict[str, int]]
Mutliplex = Dict[str, Dict[str, str]]
State = Dict[Gene, int]
Level = Tuple[List[int]]
FP = Dict[str, int]
DFP = Dict[str, int]


class Graph(nx.DiGraph):
    def __eq__(self, other):
        return nx.is_isomorphic(self, other)


def _list_to_str(lst: Iterable[Any]) -> str:
    return ''.join(map(str, lst))


def _assign_k(model: DiscreteModel, state: State, var: str) -> str:
    k = "K_%s" % var
    if not var in model.multiplex:
        return k
    for multiplex, expression in sorted(model.multiplex[var].items()):
        if not expression or eval(expression, state.copy()):
            k = k + "+%s" % multiplex
    return k


def _fp(model: DiscreteModel, s: State) -> FP:
    return {var: model.relations[var][_assign_k(model, s, var)] for var in s}


def _dfp(model: DiscreteModel, s: State):
    fp = _fp(model, s)
    return [s[v] + (s[v] < fp[v]) - (s[v] > fp[v]) for v in model.influence_graph.genes]


def create_graph(model: DiscreteModel) -> Graph:
    genes = model.influence_graph.genes
    states = [gene.states for gene in genes]
    levels = product(*states)
    digraph = nx.DiGraph()
    for level in levels:
        if level:
            state = {v: level[i] for i, v in enumerate(genes)}
            next_states = [model.available_state(var, state) for var in genes]
            for nxt in product(*next_states):
                digraph.add_edge(_list_to_str(level), _list_to_str(nxt))
    return Graph(digraph)


def export_to_dot(filename: str, graph: Graph):
    write_dot(graph, filename + ".dot")


def show(graph: Graph):
    pos = nx.nx_agraph.graphviz_layout(graph)
    nx.draw_networkx_edges(graph, pos, alpha=0.3, edge_color='m')
    nx.draw_networkx_nodes(graph, pos,  node_color='w', alpha=0.4)
    nx.draw_networkx_edges(graph, pos, alpha=0.4,
                           node_size=0, width=1, edge_color='k')
    nx.draw_networkx_labels(graph, pos, fontsize=14)
