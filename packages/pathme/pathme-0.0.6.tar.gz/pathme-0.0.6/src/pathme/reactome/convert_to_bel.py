# -*- coding: utf-8 -*-

"""This module contains the methods to convert a Reactome RDF network into a BELGraph."""
import logging
from typing import Dict, Iterable, List, Tuple

from bio2bel_hgnc import Manager as HgncManager
from pybel import BELGraph
from pybel.dsl import (
    abundance, activity, BaseEntity, composite_abundance, complex_abundance, gene, rna, protein, reaction, bioprocess,
    CompositeAbundance)

from pathme.constants import UNKNOWN
from pathme.reactome.utils import get_valid_node_parameters, process_multiple_proteins
from pathme.utils import parse_id_uri

log = logging.getLogger(__name__)

__all__ = [
    'convert_to_bel',
]


def convert_to_bel(nodes: Dict[str, Dict], interactions: List[Tuple[str, str, Dict]], pathway_info: Dict,
                    hgnc_manager) -> BELGraph:
    uri_id = pathway_info['uri_reactome_id']

    if uri_id != UNKNOWN:
        _, _, namespace, identifier = parse_id_uri(uri_id)
    else:
        identifier = UNKNOWN

    """Convert graph-like dictionaries to BELGraph."""
    graph = BELGraph(
        name=pathway_info['display_name'],
        version='1.0.0',
        description=pathway_info['comment'],
        pathway_id=identifier,
        authors="Josep Marín-Llaó, Daniel Domingo-Fernández & Sarah Mubeen",
        contact='daniel.domingo.fernandez@scai.fraunhofer.de',
    )

    nodes = nodes_to_bel(nodes, graph, hgnc_manager)

    for interaction in interactions:
        participants = interaction['participants']
        interaction_metadata = interaction['metadata']

        add_edges(graph, participants, nodes, interaction_metadata)

    return graph


def create_composite(members: Iterable) -> CompositeAbundance:
    composite_members = []
    for node_member in members:
        composite_members.append(node_member)

    return composite_abundance(composite_members)


def nodes_to_bel(nodes: Dict[str, Dict], graph, hgnc_manager: HgncManager) -> Dict[str, BaseEntity]:
    """Convert dictionary values to BEL nodes."""
    return {
        node_id: node_to_bel(node_att, graph, hgnc_manager)
        for node_id, node_att in nodes.items()
    }


def node_to_bel(node: Dict, graph, hgnc_manager: HgncManager) -> BaseEntity:
    """Convert node dictionary to BEL node object."""
    node_types = node['entity_type']

    identifier, name, namespace = get_valid_node_parameters(node, hgnc_manager)
    members = set()

    if namespace == 'hgnc_multiple_entry':
        return composite_abundance(process_multiple_proteins(identifier))

    elif 'Protein' in node_types:
        return protein(namespace=namespace.upper(), name=name, identifier=identifier)

    elif 'Dna' in node_types:
        return gene(namespace=namespace.upper(), name=name, identifier=identifier)

    elif 'Rna' in node_types:
        return rna(namespace=namespace.upper(), name=name, identifier=identifier)

    elif 'SmallMolecule' in node_types:
        return abundance(namespace=namespace.upper(), name=name, identifier=identifier)

    elif 'PhysicalEntity' in node_types:
        return abundance(namespace=namespace.upper(), name=name, identifier=identifier)

    elif 'Complex' in node_types:
        complex_components = node.get('complex_components')

        if complex_components:
            for component in complex_components:
                bel_node = node_to_bel(component, graph, hgnc_manager)

                members.add(bel_node)

        return complex_abundance(members=members, identifier=identifier, namespace=namespace.upper())

    elif 'Pathway' in node_types:
        bioprocess_node = bioprocess(identifier=identifier, name=name, namespace=namespace.upper())
        graph.add_node_from_data(bioprocess_node)
        return bioprocess_node

    else:
        log.warning('Entity type not recognized', node_types)


def add_edges(graph: BELGraph, participants, nodes, att: Dict):
    uri_id = att['uri_id']
    edge_types = att['interaction_type']

    if isinstance(participants, dict):

        reactants = {
            nodes[source_id]
            for source_id in participants['reactants']
        }

        products = {
            nodes[product_id]
            for product_id in participants['products']
        }

        reaction_node = reaction(reactants=reactants, products=products)
        graph.add_node_from_data(reaction_node)

    elif isinstance(participants, tuple):
        u = nodes[participants[0]]
        v = nodes[participants[1]]
        add_simple_edge(graph, u, v, edge_types, uri_id)


def add_simple_edge(graph: BELGraph, u, v, edge_types, uri_id):
    if 'ACTIVATION' in edge_types:
        # TODO anadir pubmed y descripcion
        graph.add_increases(u, v, citation=uri_id, evidence='', object_modifier=activity(), annotations={})

    elif 'INHIBITION' in edge_types:
        # TODO anadir pubmed y descripcion
        graph.add_decreases(u, v, citation=uri_id, evidence='', object_modifier=activity(), annotations={})

    else:
        log.warning('edge type %s', edge_types)
