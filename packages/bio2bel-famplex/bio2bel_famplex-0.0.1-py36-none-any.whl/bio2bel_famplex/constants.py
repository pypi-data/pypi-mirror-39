# -*- coding: utf-8 -*-

"""Constants for Bio2BEL FamPlex."""

VERSION = '0.0.1'


def get_version() -> str:
    """Get the software version of Bio2BEL FamPlex."""
    return VERSION


#: The URL for the relations file
RELATIONS_URL = 'https://raw.githubusercontent.com/sorgerlab/famplex/master/relations.csv'

#: The URL for the equivalence file
EQUIVALENCES_URL = 'https://raw.githubusercontent.com/sorgerlab/famplex/master/equivalences.csv'
