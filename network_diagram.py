import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict
from create_optimization_problem import create_sourcing_problem
from solve_optimization_problem import solve_sourcing_problem
from read_data import load_excel_data


def create_sourcing_graph(fulfillment_solution):
    # Create a directed graph
    G = nx.DiGraph()
    
    # Extract warehouses and orders from the DataFrame
    warehouses = fulfillment_solution["Warehouse"].unique()
    orders = fulfillment_solution["Order"].unique()
    
    # Add nodes for warehouses (blue) and orders (red)
    G.add_nodes_from(warehouses, color='blue')  # Warehouses
    G.add_nodes_from(orders, color='red')  # Orders

    # Group shipments by (warehouse, order) and store product & quantity information
    shipment_info = defaultdict(list)
    print(fulfillment_solution.columns)
    for _, row in fulfillment_solution.iterrows():
        w = row["Warehouse"]
        o = row["Order"]
        p = row["Product"]
        q = row["Supply Quantity"]
        shipment_info[(w, o)].append(f"{p[7:]} ({int(q)})")
    
    # Add edges and calculate edge properties (width and color)
    edge_labels = {}
    edge_widths = []
    edge_colors = []
    for (w, o), products in shipment_info.items():
        label = "\n".join(products)  # Combine product info for the edge label
        G.add_edge(w, o, label=label)
        edge_labels[(w, o)] = label
        
        # Sum quantities for edge width scaling
        total_qty = sum(int(float(p.split('(')[-1].strip(')'))) for p in products)
        edge_widths.append(total_qty / 10)  # Scale edge width by total quantity
        edge_colors.append("black")
    
    # Positioning the nodes using spectral layout
    #pos = nx.spectral_layout(G)
    pos = nx.circular_layout(G)
    #pos = nx.spring_layout(G, k=200, scale=40) 

    # Assign node colors based on type (warehouse or order)
    node_colors = ["blue" if node in warehouses else "red" for node in G.nodes]
    
    # Draw the network with labels, node colors, edge widths, and labels
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, 
            node_size=2000, font_size=10, width=edge_widths, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5)
    
    # Add a legend for clarity
    warehouse_patch = mpatches.Patch(color="blue", label="Warehouse")
    order_patch = mpatches.Patch(color="red", label="Order")
    plt.legend(handles=[warehouse_patch, order_patch], loc="upper right")
    
    # Add title and show the plot
    plt.title("Enhanced Sourcing Network Diagram")
    plt.show()
    
    # Save the figure
    plt.savefig('sourcing_network.png')



if __name__ == "__main__":
    filepath = 'Intelligent_Sourcing.xlsx'  # Example file path
    weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df,  = load_excel_data(filepath)
    
    # Create LP Problem
    prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable = create_sourcing_problem(weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df)
    #print(prob.objective)

    # Solve LP Problem
    status, fulfillment_solution, warehouse_stock_status = solve_sourcing_problem(prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable)

    print(fulfillment_solution)
    
    create_sourcing_graph(fulfillment_solution)