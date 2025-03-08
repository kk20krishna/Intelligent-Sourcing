import gradio as gr
import pandas as pd
from generate_data import generate_intelligent_sourcing_excel

# Default file name
default_file = "Intelligent_Sourcing.xlsx"

# Dictionary to store sheet data
df_sheets = {}

def load_default_file():
    global df_sheets
    try:
        df_sheets = pd.read_excel(default_file, sheet_name=None)
        return list(df_sheets.keys())
    except Exception as e:
        return ["Error loading default file: " + str(e)]

def upload_file(file):
    global df_sheets
    if file is None:
        return {"message": "Please upload a file."}
    
    # Save uploaded file as default
    file_path = default_file
    with open(file_path, "wb") as f:
        f.write(file.read())
    
    df_sheets = pd.read_excel(file_path, sheet_name=None)
    return list(df_sheets.keys())

def load_sheet(sheet_name):
    if sheet_name in df_sheets:
        return df_sheets[sheet_name]
    return pd.DataFrame()

def save_changes(sheet_name, edited_df):
    global df_sheets
    df_sheets[sheet_name] = edited_df
    return "Changes saved!"

def download_file():
    output_path = default_file
    with pd.ExcelWriter(output_path) as writer:
        for sheet, df in df_sheets.items():
            df.to_excel(writer, sheet_name=sheet, index=False)
    return output_path

# Define parameters for data generation
def generate_data(num_of_warehouses, num_of_products, num_of_orders, weightage_Cost, weightage_Priority, weightage_distance, weightage_days, range_priority, range_prod_stock, range_order, range_cost, range_distance, range_days):
    output_filename = "Intelligent_Sourcing.xlsx"
    
    # Convert string inputs to appropriate types
    range_priority = eval(range_priority)
    range_prod_stock = eval(range_prod_stock)
    range_order = eval(range_order)
    range_cost = eval(range_cost)
    range_distance = eval(range_distance)
    range_days = eval(range_days)
    
    generate_intelligent_sourcing_excel(output_filename, int(num_of_warehouses), int(num_of_products), int(num_of_orders), 
                                        float(weightage_Cost), float(weightage_Priority), float(weightage_distance), float(weightage_days), 
                                        range_priority, range_prod_stock, range_order, range_cost, range_distance, range_days)
    return "New data generated successfully!"

def run_optimization():
    return "Running optimization goes here!!"

with gr.Blocks() as app:
    with gr.Tabs():
        with gr.TabItem("Run Optimization"):
            run_optimization_button = gr.Button("Run Optimization")
            run_optimization_message_output = gr.Textbox(label="Status", interactive=False)

        with gr.TabItem("View/Edit Data"):
            sheet_dropdown = gr.Dropdown(choices=load_default_file(), label="Select Sheet", interactive=True)
            dataframe = gr.Dataframe(label="Edit Data", interactive=True)
            save_button = gr.Button("Save Changes", variant="primary")
            view_data_message_output = gr.Textbox(label="Status Message", interactive=False)
        
        with gr.TabItem("Generate Data"):
            generate_button = gr.Button("Generate Data")
            generate_data_message_output = gr.Textbox(label="Status Message", interactive=False)
            num_of_warehouses = gr.Textbox(label="Number of Warehouses", value="4")
            num_of_products = gr.Textbox(label="Number of Products", value="10")
            num_of_orders = gr.Textbox(label="Number of Orders", value="2")
            weightage_Cost = gr.Slider(label="Weightage Cost", minimum=1, maximum=10, value=1)
            weightage_Priority = gr.Slider(label="Weightage Priority", minimum=1, maximum=10, value=0.8)
            weightage_distance = gr.Slider(label="Weightage Distance", minimum=1, maximum=10, value=0.6)
            weightage_days = gr.Slider(label="Weightage Days", minimum=1, maximum=10, value=0.4)
            range_priority = gr.Textbox(label="Range Priority", value="(1, 10)")
            range_prod_stock = gr.Textbox(label="Range Product Stock", value="(1, 100)")
            range_order = gr.Textbox(label="Range Order", value="(1, 10)")
            range_cost = gr.Textbox(label="Range Cost", value="(1, 300)")
            range_distance = gr.Textbox(label="Range Distance", value="(1, 200)")
            range_days = gr.Textbox(label="Range Days", value="(1, 7)")
        
        with gr.TabItem("Upload/Download Data"):
            file_upload = gr.File(label="Upload Excel File", type="filepath")
            download_button = gr.Button("Download Updated File")
            file_output = gr.File(label="Download Processed File", value=default_file)
    
    file_upload.upload(upload_file, file_upload, sheet_dropdown)
    sheet_dropdown.change(load_sheet, sheet_dropdown, dataframe)
    generate_button.click(generate_data, inputs=[num_of_warehouses, num_of_products, num_of_orders, weightage_Cost, weightage_Priority, weightage_distance, weightage_days, range_priority, range_prod_stock, range_order, range_cost, range_distance, range_days], 
                          outputs=generate_data_message_output)
    save_button.click(save_changes, [sheet_dropdown, dataframe], view_data_message_output)
    download_button.click(download_file, inputs=[], outputs=file_output)
    run_optimization_button.click(run_optimization, inputs=[], outputs=run_optimization_message_output)
    
app.launch()
