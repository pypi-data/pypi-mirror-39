from swmmio.tests.data import (MODEL_FULL_FEATURES_PATH, MODEL_FULL_FEATURES__NET_PATH,
                               MODEL_BROWARD_COUNTY_PATH, MODEL_XSECTION_ALT_01)
from swmmio import swmmio


def test_conduits_dataframe():

    m = swmmio.Model(MODEL_FULL_FEATURES_PATH)
    conduits = m.conduits()
    assert(list(conduits.index) == ['C1:C2'])

def test_nodes_dataframe():

    m = swmmio.Model(MODEL_XSECTION_ALT_01)
    nodes = m.nodes()

    node_ids_01 = ['dummy_node1','dummy_node2','dummy_node3','dummy_node4',
                   'dummy_node5','dummy_node6','dummy_outfall']

    assert(list(nodes.index) == node_ids_01)
    assert(nodes.loc['dummy_node1', 'InvertElev'] == -10.99)
    assert(nodes.loc['dummy_node2', 'MaxDepth'] == 20)
    assert(nodes.loc['dummy_node3', 'X'] == -4205.457)
    assert(nodes.loc['dummy_node4', 'MaxDepth'] == 12.59314)
    assert(nodes.loc['dummy_node5', 'PondedArea'] == 73511)

def test_model_to_networkx():

    m = swmmio.Model(MODEL_FULL_FEATURES__NET_PATH)
    G = m.network

    assert(G['J2']['J3']['C2.1']['Length'] == 666)
    assert(G['J1']['J2']['C1:C2']['Length'] == 244.63)
    assert(round(G.node['J2']['InvertElev'], 3) == 13.392)
