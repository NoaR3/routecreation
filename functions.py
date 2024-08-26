from datetime import datetime

import requests
import heapq
import random
from edge import euclidean_distance, Edge
from graph import Graph

############################################################################################################

                                          # Connection And Get Json#
############################################################################################################
OSM_API_KEY = "AIzaSyBvc7jvuzXVRc-ths372d0_CwrHRjHPTuk"

# overpass_url = ("http://overpass-api.de/api/interpreter?data=[out:json];"
#                 "(way(32.0651,34.8143,32.0776,34.8386);"
#                 "node(32.0651,34.8143,32.0776,34.8386);"
#                 "rel(32.0651,34.8143,32.0776,34.8386););"
#                 "out;")

overpass_url = ("http://overpass-api.de/api/interpreter?data=[out:json];"
                "(way(32.054627,34.765903,32.065583,34.780580);"
                "node(32.054627,34.765903,32.065583,34.780580);"
                "rel(32.054627,34.765903,32.065583,34.780580););"
                "out;")

def fetch_json_data():
    headers = {"Authorization": f"Bearer {OSM_API_KEY}"}
    response = requests.get(overpass_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


############################################################################################################

                                          # Build Graph From Nodes And Edges #
############################################################################################################

def build_graph(edges, nodes):
    graph = Graph()
    for node in nodes:
        graph.add_node(node)

    for edge in edges:
        graph.add_edge(edge)

    create_cliques_for_close_nodes(graph)
    return graph


def build_structure(type, parser, json, start_node_index):
    if type == "graph":
        # Parse JSON data and create nodes
        nodes = parser.create_nodes_from_json(json)

        # Create ways,
        filtered_ways, filtered_nodes = parser.create_ways_from_json(json, nodes)

        # Create edges
        edges = create_edges_from_ways(filtered_ways, filtered_nodes)

        # Create graph
        return build_graph(edges, filtered_nodes), filtered_nodes[start_node_index].id


############################################################################################################

                                          # Create Edges And Cliques #
############################################################################################################


def create_edges_from_ways(ways, nodes):
    edges = []
    node_dict = {node.id: node for node in nodes}  # Create a dictionary for faster lookup by ID
    for way in ways:
        nodes = way.nodes
        # Iterate through all nodes except the last one
        for i in range(len(nodes) - 1):
            start_node_id = nodes[i]
            end_node_id = nodes[i + 1]

            # Use the dictionary for efficient node lookup
            start_node = node_dict.get(start_node_id)
            end_node = node_dict.get(end_node_id)


            if start_node is None or end_node is None:
                continue

            # Calculate edge length using your Euclidean distance
            length = euclidean_distance(start_node, end_node)

            edge = Edge(start_node, end_node, weight=length, tags=way.tags)
            edges.append(edge)

    return edges


def create_cliques_for_close_nodes(graph, threshold=1):
    node_ids = list(graph.nodes.keys())

    for i in range(len(node_ids)):
        node_1 = graph.nodes[node_ids[i]]
        for j in range(len(node_ids)):
            node_2 = graph.nodes[node_ids[j]]
            distance = euclidean_distance(node_1, node_2)
            if distance < threshold / 1000.0:  # Convert threshold to km
                if node_1 is node_2:
                    continue
                edge_exists = any(
                    (edge.source.id == node_1.id and edge.target.id == node_2.id)
                    for edge in graph.get_neighbors(node_1.id)
                )
                if not edge_exists:
                    # Create a new edge to form a clique
                    new_edge = Edge(node_1, node_2, distance, tags={})
                    graph.add_edge(new_edge)


############################################################################################################

                                          # Routing Alghoritms #
############################################################################################################


def dijkstra(graph, start_node_id, goal_node_id):
    open_set = []
    heapq.heappush(open_set, (0, start_node_id))
    came_from = {}
    g_score = {node_id: float('inf') for node_id in graph.nodes}
    g_score[start_node_id] = 0
    while open_set:
        current_distance, current_node_id = heapq.heappop(open_set)
        if current_node_id == goal_node_id:
            path = []
            total_length = current_distance
            while current_node_id in came_from:
                path.append(graph.nodes[current_node_id])
                current_node_id = came_from[current_node_id]
            path.append(graph.nodes[start_node_id])
            path.reverse()
            return path, total_length
        for edge in graph.get_neighbors(current_node_id):
            neighbor = edge.target.id
            tentative_g_score = g_score[current_node_id] + edge.weight

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node_id
                g_score[neighbor] = tentative_g_score
                heapq.heappush(open_set, (tentative_g_score, neighbor))

    return None, None  # If no path is found


def mark_node_as_visited(node):
    # Update the node's data to mark it as visited and record the last visited timestamp
    if node.data is None:
        node.data = "visited = yes, visit_count=1, last_visited=" + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:

        data_parts = node.data.split(", ")
        visit_count_part = next((part for part in data_parts if part.startswith("visit_count=")), "visit_count=0")
        visit_count_value = int(visit_count_part.split("=")[1]) + 1
        new_data_parts = [part for part in data_parts if not part.startswith("visit_count=")]
        node.data = (", ".join(new_data_parts)
                     + f", visit_count={visit_count_value}, last_visited="
                     + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def find_paths_full_nd_half(graph, start_node_id, target_distance):

    # Calculate halfway route
    half_path, half_length, _ = find_half_path(graph, start_node_id, target_distance)

    # Calculate full route
    total_path, total_length = find_full_path(graph, start_node_id, target_distance)

    return half_path, half_length, total_path, total_length


def find_half_path(graph, start_node_id, target_distance):
    current_node_id = start_node_id
    current_distance = 0.0
    path = [graph.nodes[current_node_id]]
    mark_node_as_visited(graph.nodes[current_node_id])

    # Calculate halfway route
    while current_distance < target_distance / 2:
        neighbors = graph.get_neighbors(current_node_id)
        unvisited_neighbors = [edge for edge in neighbors if
                               (edge.target.data is None or "visited = yes" not in edge.target.data)]

        if not unvisited_neighbors:
            min_visit_count = min(int(edge.target.data.split("visit_count=")[-1].split(",")[0])
                                  for edge in neighbors if "visit_count=" in edge.target.data)
            lowest_visit_count_neighbors = [edge for edge in neighbors if
                                            "visit_count=" in edge.target.data and int(
                                                edge.target.data.split("visit_count=")[-1].split(",")[
                                                    0]) == min_visit_count]
            edge = min(lowest_visit_count_neighbors,
                       key=lambda edge: datetime.strptime(edge.target.data.split("last_visited=")[-1],
                                                          '%Y-%m-%d %H:%M:%S')
                       if "last_visited=" in edge.target.data else datetime.min)
        else:
            edge = random.choice(unvisited_neighbors)

        if current_distance + edge.weight > target_distance / 2:
            return path, current_distance,current_node_id
        else:
            path.append(graph.nodes[edge.target.id])
            mark_node_as_visited(graph.nodes[edge.target.id])
            current_distance += edge.weight
            current_node_id = edge.target.id


def find_full_path(graph, start_node_id, target_distance):
    target_distance *= 1.8

    # Calculate first half
    first_half_path, first_half_path_distance, current_node_id = find_half_path(graph, start_node_id, target_distance, tolerance=0.1)

    # Use Dijkstra to find the second half of the path after reaching the halfway
    second_half_path, second_half_path_distance = dijkstra(graph, current_node_id, start_node_id)

    if second_half_path:
        total_path = first_half_path + second_half_path
        total_length = first_half_path_distance + second_half_path_distance
        return total_path, total_length

    else:
        print("No valid path found in the second half.")
        return None

############################################################################################################


############################################################################################################
