from pulp import *
import pandas as pd
import numpy as np
import xlsxwriter

filepath = 'Intelligent_Sourcing.xlsx'

#print(excel_file.sheet_names)
sheets = ['Weightage', 'Priority Data', 'Warehouse Data', 'Order Data', 'Cost Data', 'Distance Data', 'Days Data']

weightage_df = pd.read_excel(filepath, sheet_name='Weightage')
weightage_dict = dict(zip(weightage_df['Variable'], weightage_df['Weightage']))
Weightage_Cost = weightage_dict["Cost"]
Weightage_Priority = weightage_dict["Priority"]
Weightage_distance = weightage_dict["Distance"]
Weightage_days = weightage_dict["Days"]

priority_df = pd.read_excel(filepath, sheet_name='Priority Data')
warehouse_df = pd.read_excel(filepath, sheet_name='Warehouse Data')

print(warehouse_df)