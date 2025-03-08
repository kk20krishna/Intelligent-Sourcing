import pandas as pd

def load_excel_data(filepath):
    """
    Reads an Excel file and loads specific sheets into dataframes.
    Extracts a weightage dictionary from the 'Weightage' sheet.
    
    Parameters:
    filepath (str): Path to the Excel file.
    
    Returns:
    tuple: A dictionary containing weightages and individual dataframes.
    """
    # Define the sheet names to be read
    sheets = [
        'Weightage', 'Priority Data', 'Warehouse Data', 'Order Data',
        'Cost Data', 'Distance Data', 'Days Data'
    ]
    
    # Read the 'Weightage' sheet and create a dictionary
    weightage_df = pd.read_excel(filepath, sheet_name='Weightage')
    weightage_dict = dict(zip(weightage_df['Variable'], weightage_df['Weightage']))
    
    # Read all other sheets into separate dataframes
    priority_df = pd.read_excel(filepath, sheet_name='Priority Data')
    warehouse_df = pd.read_excel(filepath, sheet_name='Warehouse Data')
    order_df = pd.read_excel(filepath, sheet_name='Order Data')
    cost_df = pd.read_excel(filepath, sheet_name='Cost Data')
    distance_df = pd.read_excel(filepath, sheet_name='Distance Data')
    days_df = pd.read_excel(filepath, sheet_name='Days Data')
    
    return weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df

if __name__ == "__main__":
    filepath = 'Intelligent_Sourcing.xlsx'  # Example file path
    weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df = load_excel_data(filepath)
    
    # Print output for verification
    print("Weightage Dictionary:")
    print(weightage_dict)
    
    print("\nLoaded DataFrames:")
    print(f"\nPriority Data: {priority_df.shape} rows and columns")
    print(priority_df.head())
    print(f"\nWarehouse Data: {warehouse_df.shape} rows and columns")
    print(warehouse_df.head())
    print(f"\nOrder Data: {order_df.shape} rows and columns")
    print(order_df.head())
    print(f"\nCost Data: {cost_df.shape} rows and columns")
    print(cost_df.head())
    print(f"\nDistance Data: {distance_df.shape} rows and columns")
    print(distance_df.head())
    print(f"\nDays Data: {days_df.shape} rows and columns")
    print(days_df.head())
