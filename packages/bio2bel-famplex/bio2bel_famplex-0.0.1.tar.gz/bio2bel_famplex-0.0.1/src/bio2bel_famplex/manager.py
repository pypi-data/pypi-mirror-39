# -*- coding: utf-8 -*-

"""Manager for Bio2BEL FamPlex."""

from bio2bel.manager.bel_manager import BELManagerMixin
from pybel import BELGraph
from .equivalences import append_equivalences_graph, get_equivalences_df
from .relations import build_relations_graph, get_relations_df

__all__ = [
    'Manager',
]


class Manager(BELManagerMixin):
    """Manager for Bio2BEL FamPlex."""

    def __init__(self, *args, **kwargs):  # noqa:D107
        pass

    @classmethod
    def _get_connection(cls):
        pass

    def to_bel(self) -> BELGraph:
        """Generate a BEL graph."""
        relations_df = get_relations_df()
        graph = build_relations_graph(relations_df)
        equivalences_df = get_equivalences_df()
        append_equivalences_graph(equivalences_df, graph)
        return graph
