from exportfunctions import export_route_format
from functions import *
from visualize import *
from osm_json_parser import OsmJsonParser


target_distance = 10.0
formats_to_export = ['csv', 'gpx']
start_node_index = 120


def main():

    print(f"Starting Route Search - Wanted distance: {target_distance}\n")

    # Fetch JSON data
    parsed_json_data = fetch_json_data()
    if not parsed_json_data:
        print("No data")
        return

    # Create a JsonParser object
    parser = OsmJsonParser()

    # Build graph and get the start node
    graph, start_node_id = build_structure("graph", parser, parsed_json_data, start_node_index)

    # Search for path
    half_path, half_length, total_path, total_length = find_paths_full_nd_half(graph, start_node_id, target_distance)

    # Let the user choose between options
    selected_path = path_select(graph, total_path, total_length, half_path, half_length)

    # Export the path to selected formats
    export_route_format(formats_to_export, selected_path)

    print("Successfully Ended")


if __name__ == "__main__":
    main()
