from pulp import *
import pandas as pd
from read_data import load_excel_data
from create_optimization_problem import create_sourcing_problem

def solve_sourcing_problem(prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable):
    """
    Solves the sourcing optimization problem using PuLP.

    Parameters:
    prob (LpProblem): The linear programming problem instance.
    Warehouses (list): List of warehouse names.
    Products (list): List of product names.
    Stock (dict): Dictionary containing initial stock levels for each warehouse and product.
    Priority (dict): Dictionary containing priority levels for each order.
    Orders (list): List of order identifiers.
    Quantity (dict): Dictionary of order quantities for each product.
    Variable (dict): Dictionary of PuLP variables representing the decision variables.

    Returns:
    tuple: A tuple containing a string and two DataFrames:
        - LpStatus[prob.status] (str): The status of the solution.
        - fulfillment_solution: Contains details of supply quantities for each order from each warehouse.
        - warehouse_stock_status: Contains initial stock, supplied stock, and remaining stock levels.
    """
    
    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print("***** Solution Status *****")
    print("Status:", LpStatus[prob.status])


    # Fulfillment Solution
    fulfillment_solution = []
    for w in Warehouses:
        for p in Products:
            for o in Orders:
                fulfillment_solution.append({
                    "Warehouse": w,
                    "Product": p,
                    "Order": o,
                    "Supply Quantity": Variable[w][o][p].varValue
                })
    fulfillment_solution = pd.DataFrame(fulfillment_solution)

    # Stock Status
    warehouse_stock_status = []

    for w in Warehouses:
        for p in Products:
            warehouse_stock_status.append({
                "Warehouse": w,
                "Product": p,
                "Initial Stock": Stock[w][p],
                "Supplied Stock": sum(Variable[w][o][p].varValue for o in Orders),
                "Remaining Stock": Stock[w][p] - sum(Variable[w][o][p].varValue for o in Orders)
            })
    warehouse_stock_status = pd.DataFrame(warehouse_stock_status)

    return LpStatus[prob.status], fulfillment_solution, warehouse_stock_status



if __name__ == "__main__":
    filepath = 'Intelligent_Sourcing.xlsx'  # Example file path
    weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df,  = load_excel_data(filepath)
    
    # Create LP Problem
    prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable = create_sourcing_problem(weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df)
    #print(prob.objective)

    # Solve LP Problem
    status, fulfillment_solution, warehouse_stock_status = solve_sourcing_problem(prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable)

    print(fulfillment_solution)
    print(warehouse_stock_status)
