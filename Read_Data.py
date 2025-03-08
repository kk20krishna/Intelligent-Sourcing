import pandas as pd

def load_excel_data(filepath):
    """
    Reads an Excel file and loads specific sheets into individual dataframes.
    Extracts a weightage dictionary from the 'Weightage' sheet.
    
    Parameters:
    filepath (str): Path to the Excel file.
    
    Returns:
    tuple:
        - weightage_dict (dict): A dictionary mapping variable names to their corresponding weightages.
        - priority_df (DataFrame): Data from the 'Priority Data' sheet.
        - warehouse_df (DataFrame): Data from the 'Warehouse Data' sheet.
        - order_df (DataFrame): Data from the 'Order Data' sheet.
        - cost_df (DataFrame): Data from the 'Cost Data' sheet.
        - distance_df (DataFrame): Data from the 'Distance Data' sheet.
        - days_df (DataFrame): Data from the 'Days Data' sheet.
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
    for name, df in zip([
        "Priority Data", "Warehouse Data", "Order Data", "Cost Data", "Distance Data", "Days Data"
    ], [priority_df, warehouse_df, order_df, cost_df, distance_df, days_df]):
        print(f"\n{name}: {df.shape} rows and columns")
        print(df.head())
