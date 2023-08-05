#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convert FamPlex relations to BEL Statements."""

import pandas as pd

from pybel import BELGraph, to_bel
from pybel.constants import NAME, NAMESPACE
from pybel.dsl import BaseEntity, named_complex_abundance, protein
from .constants import RELATIONS_URL

__all__ = [
    "enrich_graph",
    "build_relations_graph",
]

NAMESPACES = {
    "HGNC": "https://arty.scai.fraunhofer.de/artifactory/bel/namespace/hgnc/hgnc-20180215.belns",
    "FPLX": "https://raw.githubusercontent.com/sorgerlab/famplex/1b7e14ec0fd02ee7ed71514c6e267f57d5641a4b/export/famplex.belns"
}


def get_relations_df() -> pd.DataFrame:
    """Get FamPlex relations as a DataFrame."""
    return pd.read_csv(RELATIONS_URL, header=None)


def enrich_graph(graph: BELGraph):
    """Find FamPlexes and their members in the graph and enrich them."""
    df = get_relations_df()
    for _, node in list(graph.nodes(data=True)):
        if is_famplex_node(node):
            subdf = look_up(df, node)
            append_relations_graph(subdf, graph)


def is_famplex_node(node: BaseEntity) -> bool:
    """Check if this is a node that can be enriched with FamPlex relations.

    - Does this node have the FamPlex namespace?
    - Does this node have the HGNC namespace?
    """
    namespace = node.get(NAMESPACE)
    return namespace is not None and namespace.lower() in {'famplex', 'fplx', 'hgnc'}


def look_up(df: pd.DataFrame, node: BaseEntity):
    """Get a subset of a DataFrame relevant to this node."""
    name = node.get(NAME)
    return df[(df[1] == name) | (df[4] == name)]


def build_relations_graph(df: pd.DataFrame) -> BELGraph:
    """Build a BEL Graph from a FamPlex DataFrame.

    :param df: A DataFrame representing famplex relations
    """
    graph = BELGraph(
        name="FamPlex Relations",
        version="0.0.1",
        authors="Kristian Kolpeja and Charles Tapley Hoyt",
    )
    append_relations_graph(df, graph)
    return graph


def append_relations_graph(df: pd.DataFrame, graph: BELGraph):
    """Append FamPlex relations to the graph."""
    graph.namespace_url.update(NAMESPACES)

    for index, (ns1, n1, rel, ns2, n2) in df.iterrows():
        if ns1 == "UP":
            continue

        sub = protein(ns1, n1)

        if rel == 'isa':
            obj = protein(ns2, n2)
            graph.add_is_a(sub, obj)

        else:  # partof
            obj = named_complex_abundance(ns2, n2)
            graph.add_has_member(obj, sub)


def main():
    """Provide BEL Statements from BEL graph."""
    df = get_relations_df()
    graph = build_relations_graph(df)
    with open("famplex.bel", "w") as file:
        to_bel(graph, file)


if __name__ == '__main__':
    main()
