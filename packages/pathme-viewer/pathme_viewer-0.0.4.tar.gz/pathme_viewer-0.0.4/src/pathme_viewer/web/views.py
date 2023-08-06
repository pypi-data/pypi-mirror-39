# -*- coding: utf-8 -*-

"""This module contains the PathMe views."""

import datetime
import logging
import sys
from operator import itemgetter

from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    render_template,
    request
)
from flask_admin.contrib.sqla import ModelView
from networkx import NetworkXNoPath, all_simple_paths, betweenness_centrality, shortest_path
from pkg_resources import resource_filename
from pybel.struct import get_random_path
from pybel.struct.mutation.collapse import collapse_to_genes
from pybel_tools.selection import get_subgraph_by_annotations

from pathme_viewer.constants import COLLAPSE_TO_GENES, PATHS_METHOD, RANDOM_PATH, UNDIRECTED
from pathme_viewer.graph_utils import (
    export_graph,
    get_annotations_from_request,
    get_tree_annotations,
    merge_pathways,
    process_request
)
from pathme_viewer.models import Pathway

log = logging.getLogger(__name__)
time_instantiated = str(datetime.datetime.now())

pathme = Blueprint(
    'pathme_viewer',
    __name__,
    template_folder=resource_filename('pathme_viewer', 'templates'),
    static_folder=resource_filename('pathme_viewer', 'templates')
)

redirect = Blueprint(
    '',
    __name__,
    template_folder=resource_filename('pathme_viewer', 'templates'),
    static_folder=resource_filename('pathme_viewer', 'templates')
)


class PathwayView(ModelView):
    """Pathway view in Flask-admin."""

    column_searchable_list = (
        Pathway.name,
        Pathway.resource_name,
        Pathway.pathway_id,
        Pathway.created,
        Pathway.number_of_nodes,
        Pathway.number_of_edges,
        Pathway.version,
        Pathway.pybel_version,
        Pathway.contact,
        Pathway.authors,
        Pathway.description,
    )
    column_list = (
        Pathway.name,
        Pathway.resource_name,
        Pathway.pathway_id,
        Pathway.created,
        Pathway.number_of_nodes,
        Pathway.number_of_edges,
        Pathway.version,
        Pathway.pybel_version,
        Pathway.contact,
        Pathway.authors,
        Pathway.description,
    )


"""Redirection to home page"""


@redirect.route('/')
def home():
    """Redirect to PathMe page. Only used when PathMe is run independent from ComPath."""
    return render_template('home.html')


"""Views"""


@pathme.route('/pathme')
def home():
    """PathMe home page."""
    return render_template('home.html')


@pathme.route('/pathme/about')
def about():
    """Render About page. Only when is run independent from ComPath"""
    metadata = [
        ('Python Version', sys.version),
        ('Deployed', time_instantiated),
        ('KEGG Version', current_app.pathme_manager.get_pathway_by_id('hsa00010', 'kegg').created),
        ('Reactome Version', current_app.pathme_manager.get_pathway_by_id('R-HSA-109581', 'reactome').created),
        ('WikiPathways Version', current_app.pathme_manager.get_pathway_by_id('WP100', 'wikipathways').created),
    ]

    return render_template('meta/pathme_about.html', metadata=metadata)


@pathme.route('/pathme/viewer')
def viewer():
    """PathMe page."""
    pathways = process_request(request)

    # List of all pathway names
    pathway_names = {}
    pathway_id_to_name = {}
    for pathway_id, resource in pathways.items():
        pathway = current_app.pathme_manager.get_pathway_by_id(pathway_id, resource)

        if not pathway:
            continue

        pathway_id_to_name[pathway_id] = pathway.display_name
        pathway_names[pathway.display_name] = pathway_id

    return render_template(
        'pathme_viewer.html',
        pathways=pathways,
        pathways_name='+'.join(
            '{}<div class="circle" id="{}"></div>'.format(pathway_name, pathway_id)
            for pathway_name, pathway_id in pathway_names.items()),
        pathway_ids=list(pathways.keys()),
    )


@pathme.route('/api/pathway/')
def get_network():
    """Builds a graph from request and sends it in the given format."""
    pathways = process_request(request)

    graph = merge_pathways(pathways)

    annotations = get_annotations_from_request(request)

    if annotations:
        graph = get_subgraph_by_annotations(graph, annotations)

    if COLLAPSE_TO_GENES in request.args:
        collapse_to_genes(graph)

    log.info(
        'Exporting merged graph with {} nodes and {} edges'.format(graph.number_of_nodes(), graph.number_of_edges())
    )

    graph.name = 'Merged graph from {}'.format([pathway_name for pathway_name in pathways])
    graph.version = '0.0.0'

    return export_graph(graph, request.args.get('format'))


@pathme.route('/api/tree/')
def get_network_tree():
    """Builds a graph and sends the annotation ready to be rendered in the tree."""
    pathways = process_request(request)

    graph = merge_pathways(pathways)

    annotations = get_annotations_from_request(request)

    if annotations:
        graph = get_subgraph_by_annotations(graph, annotations)

    if COLLAPSE_TO_GENES in request.args:
        collapse_to_genes(graph)

    # Returns annotation in graph
    return jsonify(get_tree_annotations(graph))


@pathme.route('/admin/delete/pathways')
def delete_pathways():
    """Delete all pathways."""
    current_app.pathme_manager.delete_all_pathways()

    return jsonify(
        status=200,
        message='All Pathways have been deleted',
    )


@pathme.route('/api/pathway/paths')
def get_paths():
    """Returns array of shortest/all paths given a source node and target node both belonging in the graph

    ---
    tags:
        - paths
        - pathway

    parameters:
      - name: pathways[]
        description: pathway resource/name pair
        required: true
        type: str

      - name: resources[]
        description: pathway resource/name pair
        required: true
        type: str

      - name: source_id
        description: The identifier of the source node
        required: true
        type: str

      - name: target_id
        description: The identifier of the target node
        required: true
        type: str

      - name: cutoff
        in: query
        description: The largest path length to keep
        required: true
        type: integer

      - name: undirected

      - name: paths_method
        in: path
        description: The method by which paths are generated - either just the shortest path, or all paths
        required: false
        default: shortest
        schema:
            type: string
            enum:
              - all
              - shortest
    """
    pathways = process_request(request)

    graph = merge_pathways(pathways)

    # Create hash to node info
    hash_to_node = {
        node.sha512: node
        for node in graph
    }

    source_id = request.args.get('source')
    if source_id is None:
        raise IndexError('Source missing from cache: %s', source_id)

    target_id = request.args.get('target')
    if target_id is None:
        raise IndexError('target is missing from cache: %s', target_id)

    method = request.args.get(PATHS_METHOD)
    undirected = UNDIRECTED in request.args
    cutoff = request.args.get('cutoff', default=7, type=int)

    source = hash_to_node.get(source_id)
    target = hash_to_node.get(target_id)

    if source not in graph or target not in graph:
        log.info('Source/target node not in network')
        log.info('Nodes in network: %s', graph.nodes())
        abort(500, 'Source/target node not in network')

    if undirected:
        graph = graph.to_undirected()

    if method == 'all':
        paths = all_simple_paths(graph, source=source, target=target, cutoff=cutoff)
        return jsonify([
            [
                node.sha512
                for node in path
            ]
            for path in paths
        ])

    try:
        paths = shortest_path(graph, source=source, target=target)
    except NetworkXNoPath:
        log.debug('No paths between: {} and {}'.format(source, target))

        # Returns normal message if it is not a random call from graph_controller.js
        if RANDOM_PATH not in request.args:
            return 'No paths between the selected nodes'

        # In case the random node is an isolated one, returns it alone
        if not graph.neighbors(source)[0]:
            return jsonify([source])

        paths = shortest_path(graph, source=source, target=graph.neighbors(source)[0])

    return jsonify([
        node.sha512
        for node in paths
    ])


@pathme.route('/api/pathway/paths/random')
def get_random_paths():
    """Gets random paths given the pathways in the graph

    ---
    tags:
        - paths
        - pathway

    parameters:
      - name: pathways[]
        description: pathway resource/name pair
        required: true
        type: str

      - name: resources[]
        description: pathway resource/name pair
        required: true
        type: str

    """
    pathways = process_request(request)

    graph = merge_pathways(pathways)

    path = get_random_path(graph)

    return jsonify([
        node.sha512
        for node in path
    ])


@pathme.route('/api/pathway/centrality')
def get_nodes_by_betweenness_centrality():
    """Gets a list of nodes with the top betweenness-centrality

    ---
    tags:
        - pathway


    parameters:
      - name: pathways[]
        description: pathway resource/name pair
        required: true
        type: str

      - name: resources[]
        description: pathway resource/name pair
        required: true
        type: str

      - name: node_number
        in: path
        description: The number of top between-nodes to return
        required: true
        type: integer
    """
    node_number = request.args.get('node_number')

    if not node_number:
        abort(500, 'Missing "node_number" argument')

    try:
        node_number = int(node_number)
    except:
        abort(500, '"node_number" could not be parsed {}'.format(node_number))

    pathways = process_request(request)

    graph = merge_pathways(pathways)

    if node_number > graph.number_of_nodes():
        node_number = graph.number_of_nodes()

    bw_dict = betweenness_centrality(graph)

    return jsonify([
        node.sha512
        for node, score in sorted(bw_dict.items(), key=itemgetter(1), reverse=True)[:node_number]
    ])


@pathme.route('/api/autocompletion/pathway_name')
def api_pathway_autocompletion_resource_specific():
    """Autocompletion for pathway name given a database.

    ---
    tags:
      - autocompletion
    responses:
      200:
        description: returns a list for the autocompletion of 10 pathway in JSON.
     """
    q = request.args.get('q')
    resource = request.args.get('resource')

    if not q or not resource:
        return jsonify([])

    query_results = current_app.pathme_manager.query_pathway_by_name_and_resource(q, resource, limit=10)

    if not query_results:
        return jsonify([])

    return jsonify([
        {'label': pathway.name, 'value': pathway.pathway_id}
        for pathway in query_results
    ])


@pathme.route('/api/database/pathways')
def api_pathways_in_database():
    """Return number of pathways in database."""
    return jsonify(current_app.pathme_manager.count_pathways())
