import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict
import os
import gradio as gr
from create_optimization_problem import create_sourcing_problem
from solve_optimization_problem import solve_sourcing_problem
from read_data import load_excel_data

def create_sourcing_graph(fulfillment_solution, plot_folder="plots"):


    # Delete all files in the 'plots' folder
    for filename in os.listdir(plot_folder):
        file_path = os.path.join(plot_folder, filename)
        if os.path.isfile(file_path):  # Ensure it's a file, not a directory
            os.remove(file_path)
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Extract warehouses and orders from the DataFrame
    warehouses = fulfillment_solution["Warehouse"].unique()
    orders = fulfillment_solution["Order"].unique()
    
    # Add nodes for warehouses (green) and orders (red)
    G.add_nodes_from(warehouses, color='green')  # Warehouses
    G.add_nodes_from(orders, color='red')  # Orders

    # Group shipments by (warehouse, order) and store product & quantity information
    shipment_info = defaultdict(list)
    for _, row in fulfillment_solution.iterrows():
        w = row["Warehouse"]
        o = row["Order"]
        p = row["Product"]
        q = row["Supply Quantity"]
        shipment_info[(w, o)].append(f"{p} ({int(q)})")
    
    # Ensure the plot folder exists
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)

    # Iterate through each order and generate its graph
    for o in orders:
        order_graph = nx.DiGraph()  # Create a new graph for each order
        
        # Add only the relevant warehouses and the current order node
        relevant_warehouses = [w for w, ord in shipment_info if ord == o]
        order_graph.add_nodes_from(relevant_warehouses, color='green')
        order_graph.add_node(o, color='red')
        
        # Add edges and calculate edge properties (width and color)
        edge_labels = {}
        edge_widths = []
        edge_colors = []
        for (w, ord), products in shipment_info.items():
            if ord == o:
                label = "\n".join(products)  # Combine product info for the edge label
                order_graph.add_edge(w, o, label=label)
                edge_labels[(w, o)] = label
                
                # Sum quantities for edge width scaling
                total_qty = sum(int(float(p.split('(')[-1].strip(')'))) for p in products)
                edge_widths.append(total_qty / 10)  # Scale edge width by total quantity
                edge_colors.append("black")
        
        # Positioning the nodes using spring layout
        pos = nx.spring_layout(order_graph, k=400, scale=100, iterations=200)
        
        # Assign node colors based on type (warehouse or order)
        node_colors = ["green" if node in relevant_warehouses else "red" for node in order_graph.nodes]
        
        # Calculate dynamic figure size based on the number of nodes
        num_nodes = len(order_graph.nodes)
        side = num_nodes * 1.7

        # Draw the network with labels, node colors, edge widths, and labels
        plt.figure(figsize=(side, side))
        nx.draw(order_graph, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, 
                node_size=2000, font_size=10, width=edge_widths, arrows=True)
        nx.draw_networkx_edge_labels(order_graph, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5)
        
        # Add a legend for clarity
        warehouse_patch = mpatches.Patch(color="green", label="Warehouse")
        order_patch = mpatches.Patch(color="red", label="Order")
        plt.legend(handles=[warehouse_patch, order_patch], loc="upper right")
        
        # Add title and save the plot
        plt.title(f"Enhanced Sourcing Network Diagram for Order {o}")
        plt.savefig(f'{plot_folder}/order_{o}.png')
        plt.close()

def display_gallery():
    # Load all the images in the 'plots' folder for display
    plot_folder = "plots"
    image_paths = [os.path.join(plot_folder, f) for f in os.listdir(plot_folder) if f.endswith(".png")]
    return image_paths

if __name__ == "__main__":
    filepath = 'Intelligent_Sourcing.xlsx'  # Example file path
    weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df = load_excel_data(filepath)
    
    # Create LP Problem
    prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable = create_sourcing_problem(weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df)

    # Solve LP Problem
    status, fulfillment_solution, warehouse_stock_status = solve_sourcing_problem(prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable)

    print(fulfillment_solution)
    
    # Create the graphs for each order
    create_sourcing_graph(fulfillment_solution)

    # Gradio app to display the gallery of saved images
    gr.Interface(fn=lambda: display_gallery(), inputs=None, outputs=gr.Gallery()).launch()
