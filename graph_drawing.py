import pickle
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import rcParams
import math

# Load the saved layout
with open("trained_pickle\\pos.pkl", "rb") as f:
    pos = pickle.load(f)

with open("trained_pickle\\G.pkl", "rb") as f:
    G = pickle.load(f)

with open("trained_pickle\\node_sizes.pkl", "rb") as f:
    node_sizes = pickle.load(f)

for i in range(len(node_sizes)):
    if node_sizes[i] < 10: 
        node_sizes[i] *= 0.1
    else:
        node_sizes[i] *= 0.5


node_colors = node_sizes.copy()

for i in range(len(node_colors)):
    node_colors[i] = math.log(node_colors[i]+1)/math.log(2)

max_color = max(node_colors)


rcParams['figure.figsize'] = (12, 8)
    
# Example of node drawing with the loaded layout

plt.figure(facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')

nx.draw_networkx_nodes(
    G, pos,
    node_size=node_sizes,
    node_color=node_colors,
    cmap=plt.cm.GnBu,
    vmin=-max_color*2,  # Ensure smallest nodes are white
    vmax=max_color*2,  # Largest nodes are vivid blue
    alpha=0.8
)

nx.draw_networkx_edges(G, pos, edge_color="#d3d3d3", alpha=0.00589, width=0.5)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # No margins
plt.margins(0)  # Removes extra space around the plot


plt.axis("off")

# plt.savefig("img\\follower_graph_heatmap_nodes.png", dpi=300, bbox_inches='tight', facecolor='black', pad_inches=0)

plt.show()
