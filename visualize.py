import networkx as nx
import matplotlib.pyplot as plt

############################################################################################################

                                          # Convert Graph To NX And Draw #
############################################################################################################


def convert_to_nx(graph):
    nx_graph = nx.Graph()
    for node_id, node in graph.nodes.items():
        nx_graph.add_node(node_id, data=node.data, latitude=node.latitude, longitude=node.longitude)
    for edge_list in graph.edges.values():
        for edge in edge_list:
            nx_graph.add_edge(edge.source.id, edge.target.id, weight=edge.weight, length=edge.length, tags=edge.tags)
    return nx_graph


def draw_graph_with_cycle(graph, path):
    nx_graph = convert_to_nx(graph)
    pos = {node_id: (node.latitude, node.longitude) for node_id, node in graph.nodes.items()}
    plt.figure(figsize=(24, 32))
    nx.draw_networkx(nx_graph, pos, with_labels=False, width=8, node_color='lightblue', node_size=4, edge_color='gray')
    if path:
        path_edges = [(path[i].id, path[i + 1].id) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(nx_graph, pos, edgelist=path_edges, edge_color='pink', width=8)
        path_labels = {node.id: str(index) for index, node in enumerate(path)}
        nx.draw_networkx_labels(nx_graph, pos, labels=path_labels, font_color='red', font_size=8)

    plt.show()

############################################################################################################

                                          # User Choice #
############################################################################################################


def path_select(graph, path, total_length, first_half_path, target_distance):
    print(f"These are the lengths of the routes - Full Circle Route: {total_length}, Half Route: {target_distance}")
    choice = input("\nWould you like to take the Full Circle Route Or the shortest path? (Full/Half) ").strip().lower()
    if choice == "full":
        print("Full")
        draw_graph_with_cycle(graph, path)
        return path
    elif choice == "half":
        print("Not Full")
        draw_graph_with_cycle(graph, first_half_path)
        return first_half_path
    else:
        print("Invalid choice. Please select 'Full' or 'Half'.")
        return None

############################################################################################################


############################################################################################################