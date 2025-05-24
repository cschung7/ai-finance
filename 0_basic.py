# /mnt/nas/gpt/class/networx_web/network_practice.py
import networkx as nx
import matplotlib.pyplot as plt

def simple_plot():
    print("--- Simple NetworkX Plot ---")
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)])
    
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray', font_size=10)
    plt.title("My First NetworkX Plot in 'nx' Env")
    
    # Save the plot to a file in the current directory
    plot_filename = "my_first_plot.png"
    plt.savefig(plot_filename)
    print(f"Plot saved to {plot_filename}")
    
    # To display the plot interactively (optional, may require GUI environment)
    # plt.show() 

def analyze_centrality_and_path():
    print("\\n--- Centrality and Shortest Path Example ---")
    G = nx.karate_club_graph() # A classic social network
    
    # Centrality: Degree (visualized by node size)
    degrees = dict(G.degree())
    node_sizes = [v * 100 for v in degrees.values()]
    
    # Shortest Path: Highlight path between node 0 and node 33 (last node)
    source_node = 0
    target_node = G.number_of_nodes() - 1
    
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(12, 9))
    nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    try:
        path = nx.shortest_path(G, source=source_node, target=target_node)
        path_edges = list(zip(path, path[1:]))
        
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='tomato', node_size=[node_sizes[i] for i in path])
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        print(f"Shortest path between {source_node} and {target_node}: {path}")
    except nx.NetworkXNoPath:
        print(f"No path between {source_node} and {target_node}.")
        
    plt.title(f"Karate Club: Degree Centrality (Size) & Shortest Path {source_node}-{target_node} (Red)")
    centrality_plot_filename = "karate_club_centrality_path.png"
    plt.savefig(centrality_plot_filename)
    print(f"Centrality and path plot saved to {centrality_plot_filename}")
    # plt.show()

if __name__ == "__main__":
    simple_plot()
    analyze_centrality_and_path()
