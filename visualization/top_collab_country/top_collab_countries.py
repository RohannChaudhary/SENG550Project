import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "../../datasets/top_collab_countries.csv"
df = pd.read_csv(file_path)


# Filter edges with a minimum shared_titles_count (e.g., collaborations with >= 5 titles)
df_filtered = df[df['shared_titles_count'] >= 5]

# Create a graph
G = nx.Graph()

# Add edges with weights (shared_titles_count)
for _, row in df_filtered.iterrows():
    G.add_edge(row['country_1'], row['country_2'], weight=row['shared_titles_count'])


plt.style.use("dark_background")

# Plot the network
plt.figure(figsize=(15, 10))  

# Position nodes using the spring layout with adjustments
pos = nx.spring_layout(G, seed=42, k=0.5, iterations=50)  

# Draw nodes and labels
nx.draw_networkx_nodes(G, pos, node_size=700, node_color="#E50914", alpha=0.9)  
nx.draw_networkx_labels(G, pos, font_size=10, font_color="white")

# Draw edges with weights
edges = nx.draw_networkx_edges(
    G, pos,
    edge_color="lightgrey", 
    width=[G[u][v]['weight'] / 10 for u, v in G.edges()], 
)

# Add a title
plt.title("Country Collaboration Network (Filtered by >= 5 Shared Titles)", fontsize=14, color="white", weight="bold")


plt.gca().set_facecolor("black")
plt.axis("off")

# Save the plot
plt.savefig("collaboration_network_netflix.png", dpi=300, bbox_inches="tight")
plt.close()
