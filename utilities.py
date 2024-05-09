from queue import PriorityQueue
import math
import networkx as nx
import osmnx as ox
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def astar_search(graph, start, goal, heuristic):

    print("astar_search function has been called")
    print()

    path = nx.astar_path(graph, start, goal, weight= "length")

    # # Initialize data structures
    # frontier = PriorityQueue()
    # frontier.put(start, 0)
    # came_from = {}
    # cost_so_far = {}
    # came_from[start] = None
    # cost_so_far[start] = 0
    # iteration_number = 1

    # # A* search algorithm
    # while not frontier.empty():
    #     current = frontier.get()

    #     print(f"Iteration number {iteration_number}")
    #     print(f"The node with ID {current} is being proccessed.")
        
    #     if current == goal:
    #         break

    #     if graph.has_node(current):
    #         print(f"The node with ID {current} does exist in the graph.")
    #         neighbors = list(graph.neighbors(current))
    #         print(f"The neighbors {neighbors}")
            
    #         # Get the attributes of the node
    #         node_attributes = graph.nodes[current]
            
    #         # Print the node ID and its attributes
    #         print("Node ID:", current)
    #         print("Attributes:", node_attributes)

    #         for next_node in graph.neighbors(current):
    #             print(f"Calculating the new cost for The node with ID {current}.")
    #             new_cost = cost_so_far[current] + graph[current][next_node]['travel_times']
    #             if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
    #                 cost_so_far[next_node] = new_cost
    #                 priority = new_cost + heuristic(goal, next_node)
    #                 frontier.put(next_node, priority)
    #                 came_from[next_node] = current
    #     else:
    #         print(f"The node with ID {current} does not exist in the graph.")
    #     iteration_number =+ 1
    #     print()

    # Construct path
    # path = []
    # current = goal
    # while current != start:
    #     path.append(current)
    #     current = came_from[current]
    # path.append(start)
    # path.reverse()

    return path

def euclidean_distance(node1, node2):

    print("euclidean_distance function has been called")
    print()

    # Get the coordinates of the nodes
    x1, y1 = node1['lat'], node1['lon']
    x2, y2 = node2['lat'], node2['lon']
    
    # Calculate the Euclidean distance
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return distance

def parse_xml_file(filepath):

    print("parse_xml_file function has been called")
    
    # Parse the XML file
    tree = ET.parse(filepath)
    root = tree.getroot()

    # Construct a graph
    G = nx.Graph()

    # Iterate over XML elements and add nodes and edges to the graph
    for node in root.findall('.//node'):
        node_id = node.attrib['id']
        lat = float(node.attrib['lat'])
        lon = float(node.attrib['lon'])
        G.add_node(node_id, pos=(lon, lat))
        # Extract tags as attributes
        tags = {}
        for tag in node.findall('tag'):
            tags[tag.attrib['k']] = tag.attrib['v']
        G.add_node(node_id, pos=(lon, lat), tags=tags)

    for way in root.findall('.//way'):
        nodes = [nd.attrib['ref'] for nd in way.findall('.//nd')]
        G.add_edges_from(zip(nodes, nodes[1:]))

    # Assuming you want to filter out nodes with the tag "<tag k="place" v="town"/>"
    tag_key = "place"
    tag_value = ["city", "town", "village"]

    # Create a list to store nodes with the desired tag
    filtered_nodes = []

    n = 0
    m = 0
    # Iterate over the nodes of the graph
    for node, data in G.nodes(data=True):
        # Check if the node has the desired tag
        n += 1
        if "tags" in data and tag_key in data["tags"] and data["tags"][tag_key] in tag_value:
            m += 1
            # If the node has the desired tag, add it to the filtered list
            filtered_nodes.append(node)
            print("Node:", node)
            print("Attributes:", data)

    print(f"number of nodes checked is {n}")
    print(f"number of nodes with tags is {m}")

    # Create a new graph to contain only the filtered nodes and their edges
    H = nx.Graph()
    H.add_nodes_from(filtered_nodes)
    H.add_edges_from(G.subgraph(filtered_nodes).edges())

    # Filter edges from G to include only those connecting nodes within H
    filtered_edges = [(u, v) for (u, v) in G.edges() if u in filtered_nodes and v in filtered_nodes]

    # Get node names from the tags attribute
    node_names = {}
    for node, data in H.nodes(data=True):
        if 'tags' in data and 'name' in data['tags']:
            node_names[node] = data['tags']['name']

    print(node_names)
    
    # Draw the filtered subgraph including original edges
    pos = nx.get_node_attributes(G, 'pos')  # Get positions of all nodes in G
    pos_filtered = {node: pos[node] for node in H.nodes() if node in pos}  # Keep only positions of nodes in H
    nx.draw(H, pos_filtered, labels=node_names, with_labels=True, node_size=50)  # Draw nodes of H
    nx.draw_networkx_edges(G, pos_filtered, edgelist=filtered_edges)  # Draw filtered edges from G
    plt.show()


    print()
    
    return H