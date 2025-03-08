import gradio as gr
import pandas as pd

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

with gr.Blocks(css=".gradio-container { max-width: 800px; margin: auto; }") as app:
    gr.Markdown("## 📂 Editable Excel Viewer")
    
    with gr.Row():
        file_upload = gr.File(label="📤 Upload Excel File", type="filepath")
        download_button = gr.Button("⬇️ Download Updated File")
    
    with gr.Row():
        sheet_dropdown = gr.Dropdown(choices=load_default_file(), label="📑 Select Sheet", interactive=True)
    
    dataframe = gr.Dataframe(label="📝 Edit Data", interactive=True, scale=1)
    
    with gr.Row():
        save_button = gr.Button("💾 Save Changes", variant="primary")
        message_output = gr.Textbox(label="📌 Status Message", interactive=False)
    
    file_upload.upload(upload_file, file_upload, sheet_dropdown)
    sheet_dropdown.change(load_sheet, sheet_dropdown, dataframe)
    save_button.click(save_changes, [sheet_dropdown, dataframe], message_output)
    download_button.click(download_file, inputs=[], outputs=gr.File(label="Download File"))
    
app.launch()
