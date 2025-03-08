import pandas as pd
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt

def generate_intelligent_sourcing_excel(
    output_filename,
    num_of_warehouses,
    num_of_products,
    num_of_orders,
    weightage_Cost,
    weightage_Priority,
    weightage_distance,
    weightage_days,
    range_priority,
    range_prod_stock,
    range_order,
    range_cost,
    range_distance,
    range_days
):
    """
    Generates an Excel file containing warehouse, order, and shipping data.
    
    Parameters:
    output_filename (str): The name of the output Excel file.
    num_of_warehouses (int): Number of warehouses.
    num_of_products (int): Number of products.
    num_of_orders (int): Number of orders.
    weightage_Cost (float): Weightage for cost.
    weightage_Priority (float): Weightage for priority.
    weightage_distance (float): Weightage for distance.
    weightage_days (float): Weightage for days.
    range_priority (tuple): Range for priority values.
    range_prod_stock (tuple): Range for product stock values.
    range_order (tuple): Range for order quantities.
    range_cost (tuple): Range for cost values.
    range_distance (tuple): Range for distance values.
    range_days (tuple): Range for delivery days values.
    """
    rng = np.random.default_rng(seed=42)  # Random number generator

    # Create weightage DataFrame
    weightage_df = pd.DataFrame({
        'Variable': ['Cost', 'Priority', 'Distance', 'Days'],
        'Weightage': [weightage_Cost, weightage_Priority, weightage_distance, weightage_days]
    })

    # Generate priority data
    priority_df = pd.DataFrame({
        'Warehouse': [f'Warehouse#{w}' for w in range(1, num_of_warehouses + 1)],
        'Priority': rng.integers(*range_priority, size=num_of_warehouses)
    })

    # Generate warehouse stock data
    warehouse_df = pd.DataFrame({
        'Warehouse': [f'Warehouse#{w}' for w in range(1, num_of_warehouses + 1)]
    })
    for p in range(1, num_of_products + 1):
        warehouse_df[f'Product#{p}'] = rng.integers(*range_prod_stock, size=num_of_warehouses)

    # Generate order data
    order_df = pd.DataFrame({
        'Order': [f'Order#{o}' for o in range(1, num_of_orders + 1)]
    })
    for p in range(1, num_of_products + 1):
        order_df[f'Product#{p}'] = rng.integers(*range_order, size=num_of_orders)

    # Function to generate shipping data
    def generate_shipping_data(metric_name, value_range):
        return pd.DataFrame([
            (w, o, p, rng.integers(*value_range))
            for w in warehouse_df["Warehouse"]
            for o in order_df["Order"]
            for p in warehouse_df.columns[1:]
        ], columns=["Warehouse", "Order", "Product", metric_name])

    # Generate cost, distance, and days DataFrames
    cost_df = generate_shipping_data("Cost", range_cost)
    distance_df = generate_shipping_data("Distance", range_distance)
    days_df = generate_shipping_data("Days", range_days)

    # Write data to Excel
    with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
        weightage_df.to_excel(writer, sheet_name='Weightage', index=False)
        priority_df.to_excel(writer, sheet_name='Priority Data', index=False)
        warehouse_df.to_excel(writer, sheet_name='Stock Data', index=False)
        order_df.to_excel(writer, sheet_name='Order Data', index=False)
        cost_df.to_excel(writer, sheet_name='Cost Data', index=False)
        distance_df.to_excel(writer, sheet_name='Distance Data', index=False)
        days_df.to_excel(writer, sheet_name='Days Data', index=False)

    print(f"Excel file '{output_filename}' has been successfully created.")
    return 


def plot_histograms(excel_filename):
    """
    Reads the generated Excel file and plots separate histograms for relevant data columns.
    """
    xls = pd.ExcelFile(excel_filename)
    
    data_sheets = {
        "Priority": pd.read_excel(xls, "Priority Data")["Priority"],
        "Product Stock": pd.read_excel(xls, "Stock Data").iloc[:, 1:].values.flatten(),
        "Order Quantity": pd.read_excel(xls, "Order Data").iloc[:, 1:].values.flatten(),
        "Cost": pd.read_excel(xls, "Cost Data")["Cost"],
        "Distance": pd.read_excel(xls, "Distance Data")["Distance"],
        "Days": pd.read_excel(xls, "Days Data")["Days"]
    }

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, (label, data) in enumerate(data_sheets.items()):
        axes[i].hist(data, bins=20, alpha=0.7, color='blue', edgecolor='black')
        axes[i].set_title(label)
        axes[i].set_xlabel("Value")
        axes[i].set_ylabel("Frequency")
        axes[i].grid(True)
    
    plt.tight_layout()
    plt.savefig("histogram_ranges.png")
    plt.close()
    print("Histogram saved as 'histogram_ranges.png'")


if __name__ == "__main__":
    # Define parameters for execution
    output_filename = "Intelligent_Sourcing.xlsx"
    num_of_warehouses = 10
    num_of_products = 100
    num_of_orders = 200
    weightage_Cost = 1
    weightage_Priority = 0.8
    weightage_distance = 0.6
    weightage_days = 0.4
    range_priority = (1, 10)
    range_prod_stock = (1, 100)
    range_order = (1, 10)
    range_cost = (1, 300)
    range_distance = (1, 200)
    range_days = (1, 7)

    # Run function
    generate_intelligent_sourcing_excel(
        output_filename,
        num_of_warehouses,
        num_of_products,
        num_of_orders,
        weightage_Cost,
        weightage_Priority,
        weightage_distance,
        weightage_days,
        range_priority,
        range_prod_stock,
        range_order,
        range_cost,
        range_distance,
        range_days
    )

    plot_histograms(excel_filename=output_filename)
