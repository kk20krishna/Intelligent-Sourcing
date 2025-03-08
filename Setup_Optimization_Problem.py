from pulp import *
import pandas as pd
from Read_Data import load_excel_data 

filepath = 'Intelligent_Sourcing.xlsx'  # Example file path
weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df = load_excel_data(filepath)