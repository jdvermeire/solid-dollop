# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound


try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'solid-dollop'
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound

from .drugbank import DrugBank
# TODO bread model into its own branch
from .model import Actions, AltSources, Base, DrugAltIds, Drugs, DrugTargets, Genes
