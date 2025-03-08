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

    # Determine warehouses and orders from shipments
    warehouses = set(w for w, _, _, _ in fulfillment_solution)
    orders = set(o for _, _, o, _ in fulfillment_solution)

    print(orders)

    # Add nodes to graph
    G.add_nodes_from(warehouses, color='blue')  # Warehouses
    G.add_nodes_from(orders, color='red')  # Orders

    # Group shipments by (warehouse, order)
    shipment_info = defaultdict(list)
    for w, p, o, q in fulfillment_solution:
        shipment_info[(w, o)].append(f"{p} ({q})")

    # Add edges with combined product info as labels
    edge_labels = {}
    edge_widths = []
    edge_colors = []
    for (w, o), p in shipment_info.items():
        label = "\n".join(p)  # Combine all products for the edge
        G.add_edge(w, o, label=label)
        edge_labels[(w, o)] = label
        total_qty = sum(int(p.split('(')[-1].strip(')')) for p in p)  # Sum quantities
        edge_widths.append(total_qty / 10)  # Scale edge width by total quantity
        edge_colors.append("black")

    # Positioning the nodes
    pos = nx.spectral_layout(G)

    # Node colors
    node_colors = ["yellow" if node in warehouses else "red" for node in G.nodes]

    # Draw the network
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, 
            node_size=2000, font_size=10, width=edge_widths, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5)

    # Add legend
    warehouse_patch = mpatches.Patch(color="blue", label="Warehouse")
    order_patch = mpatches.Patch(color="red", label="Order")
    plt.legend(handles=[warehouse_patch, order_patch], loc="upper right")

    plt.title("Enhanced Sourcing Network Diagram")
    plt.show()

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
    
    create_sourcing_graph(fulfillment_solution.itertuples(index=False, name=None))