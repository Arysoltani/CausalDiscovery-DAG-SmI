import networkx as nx
import matplotlib.pyplot as plt

# Function to read the graph data from a file
def read_graph_data(filename):
  
  graph = nx.DiGraph()  

  with open(filename, 'r') as f:

    next(f)

    for line in f:
      source, targets = line.strip().split(':', 1)
      targets = targets.strip().split() 

      if source not in graph.nodes:
        graph.add_node(source)

      for target in targets:
        if target not in graph.nodes:
          graph.add_node(target)
        graph.add_edge(source, target)

  return graph

filename = input()
file_out = input()
graph = read_graph_data(filename)

pos = nx.spring_layout(graph, k=0.5) 

node_colors = ['lightblue' if node in ['Frequency', 'Pressure'] else 'lightgreen' for node in graph.nodes]
node_sizes = [1000 if node in ['Frequency', 'Pressure'] else 500 for node in graph.nodes]  

nx.draw_networkx(graph, pos, with_labels=True, font_weight='bold', font_size=12,
                 node_size=node_sizes, linewidths=2)

plt.title("Causality Graph with Usage of SmI")

plt.axis('off')  # Hide axes

plt.savefig(file_out, bbox_inches='tight')

# plt.show()