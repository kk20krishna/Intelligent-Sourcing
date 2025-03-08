from generate_data import generate_intelligent_sourcing_excel, plot_histograms
from read_data import load_excel_data
from create_optimization_problem import create_sourcing_problem
from solve_optimization_problem import solve_sourcing_problem
from pulp import *
import pandas as pd
import xlsxwriter

filepath = 'Intelligent_Sourcing.xlsx'

# Define parameters for execution
output_filename = "Intelligent_Sourcing.xlsx"
num_of_warehouses = 4
num_of_products = 10
num_of_orders = 2
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

# Generate Data
generate_intelligent_sourcing_excel(output_filename, num_of_warehouses, num_of_products, num_of_orders, 
                                    weightage_Cost, weightage_Priority, weightage_distance, weightage_days, 
                                    range_priority, range_prod_stock, range_order, range_cost, range_distance, range_days)

plot_histograms(excel_filename=output_filename)


# Read Data
weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df = load_excel_data(filepath)

# Create LP Problem
prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable = create_sourcing_problem(weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df)
#print(prob.objective)

# Solve LP Problem
status, fulfillment_solution, warehouse_stock_status = solve_sourcing_problem(prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable)

if status == "Optimal":
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(filepath, engine='openpyxl',
                            mode='a', if_sheet_exists='replace')

    # Write each DataFrame to a different worksheet.
    fulfillment_solution.to_excel(writer, sheet_name='Fulfillment Solution', index=False)
    warehouse_stock_status.to_excel(writer, sheet_name='Warehouse Stock Status', index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.close()
else:
    print("Solution not found - status is - ", status)




