# -*- coding: utf-8 -*-

"""Tests for Bio2BEL FamPlex."""

import unittest

from bio2bel_famplex import Manager
from pybel import BELGraph


class TestManager(unittest.TestCase):
    """Tests for Bio2BEL FamPlex's manager."""

    def test_bel_export(self):
        """Test the BEL export."""
        manager = Manager()
        graph = manager.to_bel()
        self.assertIsInstance(graph, BELGraph)
        self.assertGreater(graph.number_of_nodes(), 0)
        self.assertGreater(graph.number_of_edges(), 0)
