from node import Node
from way import Way

############################################################################################################

                         # Parser That Creates Nodes And Ways From JSON #
############################################################################################################

class OsmJsonParser:

    def create_nodes_from_json(self, json_data):
        nodes = []

        if "elements" in json_data:
            for element in json_data["elements"]:
                if element["type"] == "node":
                    id = element["id"]
                    latitude = element["lat"]
                    longitude = element["lon"]
                    data = element.get("tags", {}).get("name", None)
                    elevation = None
                    nodes.append(Node(id, data, latitude, longitude))

                elif "lat" in json_data and "lon" in json_data:
                    id = json_data["id"]
                    latitude = json_data["lat"]
                    longitude = json_data["lon"]
                    data = json_data.get("display_name", None)
                    elevation = None
                    nodes.append(Node(id, data, latitude, longitude))

        return nodes

    def create_ways_from_json(self, json_data, nodes):
        filtered_ways = []
        nodes_in_use = set()
        ways_in_relation = set()

        if "elements" in json_data:
            for element in json_data["elements"]:
                if element["type"] == "relation":
                    relation_ways = element.get("members", [])
                    for member in relation_ways:
                        if ((member.get("type") == "way" or member.get("type") == "node")
                                and member.get("role") == "outer"):
                            ways_in_relation.add(member["ref"])


        if "elements" in json_data:
            for element in json_data["elements"]:
                if element["type"] == "way":
                    way_id = element["id"]
                    # Skip ways that are part of a relation
                    if way_id in ways_in_relation:
                        continue
                    way_nodes = element.get("nodes")
                    tags = element.get("tags")

                    if (tags is not None) and tags.get("building") is not None:
                        continue

                    if (tags is not None) and tags.get("landuse") is not None:
                        if 'landuse' in tags and tags['landuse'] in ['farmland', 'residential', 'construction']:
                            continue

                    if (tags is not None) and tags.get("amenity") is not None:
                        if 'amenity' in tags and tags['amenity'] in ['parking', 'parking_space']:
                            continue

                    if (tags is not None) and tags.get("leisure") is not None:
                        if 'leisure' in tags and tags['leisure'] in ['swimming_pool', 'pitch', 'park', 'garden',
                                                                     'sports_centre']:
                            continue

                    if (tags is not None) and tags.get("aeroway") is not None:
                        continue

                    if (tags is not None) and tags.get("addr:interpolation") is not None:
                        continue

                    if (tags is not None) and tags.get("building:part") is not None:
                        continue

                    if (tags is not None) and tags.get("place") is not None:
                        if 'place' in tags and tags['place'] in ['suburb']:
                            continue

                    nodes_in_use.update(way_nodes)
                    filtered_ways.append(Way(way_id, way_nodes, tags))

        filtered_nodes = [node for node in nodes if node.id in nodes_in_use]

        return filtered_ways, filtered_nodes

############################################################################################################


############################################################################################################