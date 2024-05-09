import tkinter as tk
import osmnx as ox
from utilities import astar_search, euclidean_distance

def show_screen2(screen1, screen2):
  # Show screen2
  screen2.pack(fill=tk.BOTH, expand=True)
  # Hide current screen (screen1)
  screen1.pack_forget()

def show_screen3(screen2, screen3):
  screen2.pack_forget()
  # Show screen3
  screen3.pack(fill=tk.BOTH, expand=True)

def create_app_ui():
    root = tk.Tk()

    root.geometry("500x500")
    root.title("shortest-path")

    # Define frames for each screen
    screen1 = tk.Frame(root)
    screen2 = tk.Frame(root)
    screen3 = tk.Frame(root)

    # Screen 1
    # Outer frame (fills the window)
    outer_frame = tk.Frame(screen1)
    outer_frame.pack(fill=tk.BOTH, expand=True)

    # Inner frame (holds label and button)
    inner_frame = tk.Frame(outer_frame)
    inner_frame.pack()

    label = tk.Label(inner_frame, text= "Welcome shortest-path", font=('Arial', 18))
    label.pack()

    button = tk.Button(inner_frame, text="Next", font=('Arial', 10), command = show_screen2(screen1, screen2))
    button.pack()

    # Screen 2
    # Outer frame (fills the window)
    outer_frame = tk.Frame(screen2)
    outer_frame.pack(fill=tk.BOTH, expand=True)

    # Inner frame (holds label and button)
    inner_frame = tk.Frame(outer_frame)
    inner_frame.pack()

    label = tk.Label(inner_frame, text= "Choose the starting point", font=('Arial', 18))
    label.pack()

    button = tk.Button(inner_frame, text="Algiers", font=('Arial', 10), command = show_screen3(screen1, screen2, screen3))
    button.pack()

    # Screen 3
    # Outer frame (fills the window)
    outer_frame = tk.Frame(screen3)
    outer_frame.pack(fill=tk.BOTH, expand=True)

    # Inner frame (holds label and button)
    inner_frame = tk.Frame(outer_frame)
    inner_frame.pack()

    label = tk.Label(inner_frame, text= "Choose the goal point", font=('Arial', 18))
    label.pack()

    button = tk.Button(inner_frame, text="Algiers", font=('Arial', 10))
    button.pack()

    screen1.pack(fill=tk.BOTH, expand=True)
    screen2.pack_forget()
    screen3.pack_forget()

    root.mainloop()

create_app_ui()

ox.config(use_cache=True, log_console=True)

# Define the location (for example, a city name or address)
place_name = "New York City, USA"

# Download the street network for the specified location
G = ox.graph_from_place(place_name, network_type='drive')
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

number_of_nodes = G.number_of_nodes()
print(f"number of nodes is {number_of_nodes}")

# Plot the graph
ox.plot_graph(G)

start_node = 9498751775
goal_node = 11890331361

shortest_path = astar_search(G, start_node, goal_node, euclidean_distance)
print(shortest_path)