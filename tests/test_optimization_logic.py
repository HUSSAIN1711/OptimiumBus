import networkx as nx
from app.core.graph_utils import snap_to_nearest_node


def test_snap_to_nearest_node():
    # Arrange: small graph with known coordinates
    G = nx.Graph()
    G.add_node("A", y=33.6846, x=-117.8265)   # Irvine
    G.add_node("B", y=34.0522, x=-118.2437)   # Los Angeles
    G.add_node("C", y=32.7157, x=-117.1611)   # San Diego

    # A coordinate near Irvine
    query_lat, query_lng = 33.6850, -117.8260

    # Act
    nearest = snap_to_nearest_node(G, query_lat, query_lng)

    # Assert
    assert nearest == "A"
