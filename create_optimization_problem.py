from pulp import *
import pandas as pd
from read_data import load_excel_data

def create_sourcing_problem(weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df):
    """
    Creates and returns a linear programming problem for intelligent sourcing optimization.
    
    Parameters:
        weightage_dict (dict): Dictionary containing weightages for cost, priority, distance, and days.
        priority_df (DataFrame): DataFrame containing priority values for each warehouse.
        warehouse_df (DataFrame): DataFrame containing stock availability for each warehouse.
        order_df (DataFrame): DataFrame containing order quantities for each product.
        cost_df (DataFrame): DataFrame containing cost values.
        distance_df (DataFrame): DataFrame containing distance values.
        days_df (DataFrame): DataFrame containing expected delivery days.
    
    Returns:
        LpProblem: Linear programming problem formulated for sourcing optimization.
        Warehouses, Products, Stock, Priority, Orders, Quantity
    """
    def min_max_scale(df, column):
        min_val = df[column].min()
        max_val = df[column].max()
        df[column] = (df[column] - min_val) / (max_val - min_val)
        return df

    # Extract weightages
    weightage_Cost = weightage_dict["Cost"]
    weightage_Priority = weightage_dict["Priority"]
    weightage_distance = weightage_dict["Distance"]
    weightage_days = weightage_dict["Days"]

    # Normalize data
    priority_df = min_max_scale(priority_df, "Priority")
    cost_df = min_max_scale(cost_df, "Cost")
    distance_df = min_max_scale(distance_df, "Distance")
    days_df = min_max_scale(days_df, "Days")

    # Create dictionaries for optimization
    Warehouses = warehouse_df['Warehouse'].tolist()
    Products = warehouse_df.columns[1:]
    Stock = makeDict([Warehouses, Products], warehouse_df.drop('Warehouse', axis=1).values, default=0)
    Priority = makeDict([Warehouses], priority_df.drop('Warehouse', axis=1).values.reshape(len(Warehouses)), default=0)
    Orders = order_df['Order'].tolist()
    Quantity = makeDict([Orders, Products], order_df.drop('Order', axis=1).values, default=0)

    cost_values = cost_df["Cost"].values.reshape(len(Warehouses), len(Orders), len(Products))
    cost = makeDict([Warehouses, Orders, Products], cost_values, default=0)

    distance_values = distance_df["Distance"].values.reshape(len(Warehouses), len(Orders), len(Products))
    distance = makeDict([Warehouses, Orders, Products], distance_values, default=0)

    days_values = days_df["Days"].values.reshape(len(Warehouses), len(Orders), len(Products))
    days = makeDict([Warehouses, Orders, Products], days_values, default=0)

    # Define variables and routes
    routes = [(w, o, s) for w in Warehouses for o in Orders for s in Products]
    Variable = LpVariable.dicts("Route", (Warehouses, Orders, Products), 0, None, LpInteger)

    # Create optimization problem
    prob = LpProblem("Sourcing_Problem", LpMaximize)

    # Objective function
    prob += lpSum(
        Variable[w][o][p] * (
            (weightage_Cost * -cost[w][o][p]) +
            (weightage_Priority * -Priority[w]) +
            (weightage_distance * -distance[w][o][p]) +
            (weightage_days * -days[w][o][p])
        )
        for (w, o, p) in routes
    ), "Sum_of_Costs"

    # Stock Constraints
    for w in Warehouses:
        for p in Products:
            prob += lpSum([Variable[w][o][p] for o in Orders]) <= Stock[w][p], f"Stock_Constraint_{p}_in_{w}"

    # Order Constraints
    for o in Orders:
        for p in Products:
            prob += lpSum([Variable[w][o][p] for w in Warehouses]) <= Quantity[o][p], f"Order_Fulfillment_{p}_to_{o}"

    return prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable

if __name__ == "__main__":
    filepath = 'Intelligent_Sourcing.xlsx'  # Example file path
    weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df,  = load_excel_data(filepath)
    
    prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable = create_sourcing_problem(weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df)
    print(prob.objective)
