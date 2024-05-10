import tkinter as tk
from tkinter import ttk
import osmnx as ox
from utilities import astar_search, euclidean_distance

color1 = '#2a7fb8'
color2 = '#709bb8'

def get_state_id(state_name):

  state_ids = {
    "Amizeur": 4112937,
    "Béjaïa": 2094122,
    "Boulimat": 425040436,
    "Oum El Bouaghi": 4469695,
    "Souk Ahras": 6663208,
    "Batna": 4224144,
    "Djelfa": 7,
    "Illizi": 8,
    "Oran": 9,
    "Tamanrasset": 10,
    "Béchar": 11,
    "El Bayadh": 12,
    "Khenchela": 13,
    "Ouargla": 14,
    "Tindouf": 15,
    "Biskra": 16,
    "El Oued": 17,
    "Laghouat": 18,
    "Sétif": 19,
    "Tissemsilt": 20,
    "Bordj Bou Arreridj": 21,
    "Médéa": 22,
    "M'Sila": 23,
    "Tiaret": 24,
    "Tlemcen": 25,
    "Bouira": 26,
    "Mila": 27,
    "Naâma": 28,
    "Tizi Ouzou": 29,
    "Constantine": 30,
    "Mostaganem": 31,
    "Saïda": 32,
    "Skikda": 33,
    "Tébessa": 34
  }

  if state_name in state_ids:
    return state_ids[state_name]
  else:
    return None

def main_code(start, destination):
  ox.config(use_cache=True, log_console=True)

  place_name = "Béjaïa ,Algeria"

  G = ox.graph_from_place(place_name, network_type='all')
  G = ox.add_edge_speeds(G)
  G = ox.add_edge_travel_times(G)

  number_of_nodes = G.number_of_nodes()
  print(f"number of nodes is {number_of_nodes}")

  ox.plot_graph(G)

  start_node = get_state_id(start)
  goal_node = get_state_id(destination)

  print(start_node)
  print(goal_node)

  shortest_path = astar_search(G, start_node, goal_node, euclidean_distance)
  print(shortest_path)

def create_app_ui():

  states = [
      "Amizeur", "Béjaïa", "Boulimat", "Oum El Bouaghi", "Souk Ahras",
      "Batna", "Djelfa", "Illizi", "Oran", "Tamanrasset",
      "Béchar", "El Bayadh", "Khenchela", "Ouargla", "Tindouf",
      "Biskra", "El Oued", "Laghouat", "Sétif", "Tissemsilt",
      "Bordj Bou Arreridj", "Médéa", "M'Sila", "Tiaret", "Tlemcen",
      "Bouira", "Mila", "Naâma", "Tizi Ouzou", 
      "Constantine", "Mostaganem", "Saïda",
      "Djelfa", "Skikda", "Tébessa"
  ]

  root = tk.Tk()

  root.geometry("500x500")
  root.title("shortest-path")

  # Main frame
  main_frame = tk.Frame(root)
  main_frame.pack(fill=tk.BOTH, expand=True)

  # ComboBox Row
  combobox_row = tk.Frame(main_frame)

  start_var = tk.StringVar()
  destenation_var = tk.StringVar()

  # Create the combo box
  start_combo_box = ttk.Combobox(combobox_row, values=states, textvariable= start_var)
  start_combo_box.current(0)
  destenation_combo_box = ttk.Combobox(combobox_row, values=states, textvariable= destenation_var)
  destenation_combo_box.current(0)

  # Widgets
  label1 = tk.Label(main_frame, text= "Welcome shortest-path", font=('Roboto', 18))
  label2 = tk.Label(main_frame, text= "Please choose the starting city and the destination city", font=('Roboto', 12))
  button = tk.Button(
    main_frame,
    text="Generate", 
    font=('Roboto', 10), 
    command= lambda: main_code(start_var.get(), destenation_var.get()),
    background=color1,
    activebackground=color2,
    border= 0,
    )

  label1.pack(pady=20)
  label2.pack(pady=10)
  combobox_row.pack(fill=tk.X, pady=10)
  start_combo_box.pack(side= "left", padx=10)
  destenation_combo_box.pack(side= "right", padx=10)
  button.pack(pady=10)

  root.mainloop()

create_app_ui()