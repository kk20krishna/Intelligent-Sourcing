import gradio as gr
import pandas as pd
from generate_data import generate_intelligent_sourcing_excel
from read_data import load_excel_data
from create_optimization_problem import create_sourcing_problem
from solve_optimization_problem import solve_sourcing_problem
from network_diagram import create_sourcing_graph, display_gallery
import os
import requests

# Default file name
default_file = "Intelligent_Sourcing.xlsx"

# Dictionary to store sheet data
df_sheets = {}

# Function to read the Markdown file from GitHub
def read_markdown_file_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        readme_content = response.text
    else:
        readme_content = "Failed to load {url}"
    return readme_content[237:] # exclude first part of README.md file in GitHub

# Function to read the Markdown file
def read_markdown_file(file):
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

# Function to load the default Excel file
def load_default_file():
    global df_sheets
    try:
        df_sheets = pd.read_excel(default_file, sheet_name=None)
        return list(df_sheets.keys())
    except Exception as e:
        return ["Error loading default file: " + str(e)]

# Function to upload a new Excel file
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

# Function to load a selected sheet
def load_sheet(sheet_name):
    df_sheets = pd.read_excel(default_file, sheet_name=None)
    if sheet_name in df_sheets:
        return df_sheets[sheet_name]
    return pd.DataFrame()

# Function to save edited data back to the sheet
def save_changes(sheet_name, edited_df):
    global df_sheets
    # Write data to Excel
    with pd.ExcelWriter(default_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        edited_df.to_excel(writer, sheet_name=sheet_name, index=False)
    df_sheets = pd.read_excel(default_file, sheet_name=None)
    return "Changes saved!"

# Function to download the updated Excel file
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

# Function to save weightage values
def save_weightage(weightage_Cost, weightage_Priority, weightage_distance, weightage_days):
    # Create weightage DataFrame
    weightage_df = pd.DataFrame({
        'Variable': ['Cost', 'Priority', 'Distance', 'Days'],
        'Weightage': [weightage_Cost, weightage_Priority, weightage_distance, weightage_days]
    })
    # Write data to Excel
    with pd.ExcelWriter(default_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        weightage_df.to_excel(writer, sheet_name='Weightage', index=False)
    return "Weights saved successfully!"

# Run optimization problem
def run_optimization():
    # Read Data
    weightage_dict, priority_df, warehouse_df, order_df, cost_df, distance_df, days_df = load_excel_data(default_file)

    # Create LP Problem
    prob, Warehouses, Products, Stock, Priority, Orders, Quantity, Variable = create_sourcing_problem(weightage_dict, priority_df, 
                                                                                                      warehouse_df, order_df, cost_df, distance_df, days_df)
    #print(prob.objective)

    # Solve LP Problem
    status, fulfillment_solution, warehouse_stock_status = solve_sourcing_problem(prob, Warehouses, Products, Stock,
                                                                                   Priority, Orders, Quantity, Variable)

    if status == "Optimal":
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(default_file, engine='openpyxl',
                                mode='a', if_sheet_exists='replace')

        # Write each DataFrame to a different worksheet.
        fulfillment_solution.to_excel(writer, sheet_name='Fulfillment Solution', index=False)
        warehouse_stock_status.to_excel(writer, sheet_name='Warehouse Stock Status', index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.close()

        create_sourcing_graph(fulfillment_solution)
        # Get all image files in the '/tmp/plots' folder
        plot_images = [os.path.join("/tmp/plots", filename) for filename in os.listdir("/tmp/plots") if filename.endswith(('.png', '.jpg', '.jpeg'))]

        return f'Optimization Status: {status}', fulfillment_solution, warehouse_stock_status, plot_images
    else:
        return f'Solution not found!!!! - status is - {status}', gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

# Generate excel sheet on app startup
# Define parameters for execution
output_filename = "Intelligent_Sourcing.xlsx"
num_of_warehouses = 4
num_of_products = 10
num_of_orders = 4
weightage_Cost = 1
weightage_Priority = 0.75
weightage_distance = 0.5
weightage_days = 0.25
range_priority = (1, 10)
range_prod_stock = (1, 100)
range_order = (1, 10)
range_cost = (1, 300)
range_distance = (1, 200)
range_days = (1, 7)
# Run function
generate_intelligent_sourcing_excel(output_filename, num_of_warehouses, num_of_products, num_of_orders, weightage_Cost, weightage_Priority,
                                    weightage_distance, weightage_days, range_priority, range_prod_stock, range_order, range_cost, range_distance, range_days)

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("""# Intelligent Sourcing """)
    with gr.Tabs():

        with gr.TabItem("About this App"):
            gr.Markdown(read_markdown_file_github("https://raw.githubusercontent.com/kk20krishna/Intelligent-Sourcing/refs/heads/main/README.md"))
        
        with gr.TabItem("📖 How to use this App"):
            gr.Markdown(read_markdown_file("app_doc.md"))

        with gr.TabItem("Run Optimization"):
            gr.Markdown("""### Run Optimization\nAdjust weightage parameters and run optimization.""")
            run_weightage_Cost = gr.Slider(label="Weightage Cost", minimum=0, maximum=1, value=0.5, step=0.25, interactive=True)
            run_weightage_Priority = gr.Slider(label="Weightage Priority", minimum=0, maximum=1, value=0.5, step=0.25, interactive=True)
            run_weightage_distance = gr.Slider(label="Weightage Distance", minimum=0, maximum=1, value=0.5, step=0.25, interactive=True)
            run_weightage_days = gr.Slider(label="Weightage Days", minimum=0, maximum=1, value=0.25, step=0.5, interactive=True)
            save_Weightage_button = gr.Button("Save Weightage")
            weightage_message_output = gr.Textbox(label="Status", interactive=False)
            run_optimization_button = gr.Button("Run Optimization")
            run_optimization_message_output = gr.Textbox(label="Status", interactive=False)
            with gr.Tabs():
                with gr.TabItem("Results: Fulfillment Solution"):
                    fulfillment_dataframe = gr.Dataframe(label="Fulfillment Solution")
                with gr.TabItem("Results: Warehouse Stock Status"):
                    warehouse_stock_dataframe = gr.Dataframe(label="Warehouse Stock Status")
                with gr.TabItem("Results: Plots"):
                    gallery_output = gr.Gallery(label="Plots")

            # Button bindings
            run_optimization_button.click(run_optimization, inputs=[], 
                                          outputs=[run_optimization_message_output, 
                                                   fulfillment_dataframe, 
                                                   warehouse_stock_dataframe,
                                                   gallery_output])
            save_Weightage_button.click(save_weightage, 
                                        inputs=[run_weightage_Cost, run_weightage_Priority, 
                                                run_weightage_distance, run_weightage_days], 
                                        outputs=weightage_message_output)

        with gr.TabItem("View/Edit Data"):
            gr.Markdown("""### View/Edit Data\nSelect a sheet to view and edit data.""")
            sheet_dropdown = gr.Dropdown(choices=load_default_file(), label="Select Sheet", interactive=True)
            dataframe = gr.Dataframe(load_sheet('Weightage'), label="Edit Data", interactive=True)
            save_button = gr.Button("Save Changes", variant="primary")
            view_data_message_output = gr.Textbox(label="Status Message", interactive=False)

            # Button Bindings
            sheet_dropdown.change(load_sheet, sheet_dropdown, dataframe)
            save_button.click(save_changes, [sheet_dropdown, dataframe], view_data_message_output)
        
        with gr.TabItem("Generate Data"):
            gr.Markdown("""### Generate Data\nEnter parameters to generate new intelligent sourcing data.""")
            generate_button = gr.Button("Generate Data")
            generate_data_message_output = gr.Textbox(label="Status Message", interactive=False)
            num_of_warehouses = gr.Textbox(label="Number of Warehouses", value="4")
            num_of_products = gr.Textbox(label="Number of Products", value="10")
            num_of_orders = gr.Textbox(label="Number of Orders", value="2")
            weightage_Cost = gr.Slider(label="Weightage Cost", minimum=0, maximum=1, value=0.5, step=0.25, interactive=True)
            weightage_Priority = gr.Slider(label="Weightage Priority", minimum=0, maximum=1, value=0.5, step=0.25, interactive=True)
            weightage_distance = gr.Slider(label="Weightage Distance", minimum=0, maximum=1, value=0.5, step=0.25, interactive=True)
            weightage_days = gr.Slider(label="Weightage Days", minimum=0, maximum=1, value=0.5, interactive=True)
            range_priority = gr.Textbox(label="Range Priority", value="(1, 10)")
            range_prod_stock = gr.Textbox(label="Range Product Stock", value="(1, 100)")
            range_order = gr.Textbox(label="Range Order", value="(1, 10)")
            range_cost = gr.Textbox(label="Range Cost", value="(1, 500)")
            range_distance = gr.Textbox(label="Range Distance", value="(1, 300)")
            range_days = gr.Textbox(label="Range Days", value="(1, 14)")

            # Button Bindings
            generate_button.click(generate_data, 
                                  inputs=[num_of_warehouses, num_of_products, num_of_orders, 
                                          weightage_Cost, weightage_Priority, weightage_distance, weightage_days, 
                                          range_priority, range_prod_stock, range_order, range_cost, range_distance, range_days], 
            outputs=generate_data_message_output)
        
        with gr.TabItem("Upload/Download Data"):
            gr.Markdown("""### Upload file / download file""")
            file_upload = gr.File(label="Upload Excel File", type="filepath")
            download_button = gr.Button("Download Updated File")
            file_output = gr.File(label="Download Processed File", value=default_file)

            # Button Bindings
            file_upload.upload(upload_file, file_upload, sheet_dropdown)
            download_button.click(download_file, inputs=[], outputs=file_output)
        
app.launch()
