import gradio as gr
import requests


# Temporary storage for uploaded files
uploaded_files = []

# Function to process and store uploaded files

def process_file(file, file_label):
    # Define your API endpoint
    api_endpoint = 'http://127.0.0.1:8000'
    
    if file is not None:
        # Prepare the headers for the HTTP request, if needed (e.g., authentication)
        headers = {
            # 'Authorization': 'Bearer <your-token-here>',
            'Content-Type': 'application/octet-stream',
        }

        # Make the PUT request with the file
        response = requests.put(
            url=f"{api_endpoint}/upload_file",  # Assuming the file_label can be passed as part of URL
            headers=headers,
            files={'file': file},
            # data=file.read(),  # Use this if API expects raw file data
        )

        # Check if the request was successful
        if response.status_code == 200 or response.status_code == 201:
            return f"Successfully uploaded: {file_label}"
        else:
            # Log the error or handle it as needed
            return f"Failed to upload {file_label}, status code: {response.status_code}, response: {response.text}"
            
    return f"No file was added to upload for {file_label}."

# Function to be called when "Compare" button is pressed
def compare_files(column_to_join):
    global uploaded_files

    # Check if all files have been uploaded
    file1 = file2 = rules_file = None
    for label, file in uploaded_files:
        if label == "file1":
            file1 = file
        elif label == "file2":
            file2 = file
        elif label == "rules_file":
            rules_file = file
    
    if not (file1 and file2 and rules_file):
        return "Please make sure to upload all three files before comparison."

    # Placeholder for the comparison logic or API call
    api_call_result = "Comparison results would be displayed here."

    # Clear uploaded files after comparison
    uploaded_files.clear()

    return api_call_result

# UI Setup with Gradio
def setup_interface():
    with gr.Blocks() as app:
        
        gr.Markdown("## Upload Files for Comparison")

        with gr.Row():
            file_1_input = gr.File(label="File 1")
            file_2_input = gr.File(label="File 2")
            rules_file_input = gr.File(label="Rules File")
            upload_button = gr.Button("Upload Files")
        
        upload_status = gr.Label("")  # Label to show upload status

        # Bind the process_file function to the upload button click event
        def on_upload_click(file1, file2, rules):
            messages = []
            messages.append(process_file(file1, "file1")) if file1 else None
            messages.append(process_file(file2, "file2")) if file2 else None
            messages.append(process_file(rules, "rules_file")) if rules else None
            return "\\n".join(messages)

        upload_button.click(
            on_upload_click,
            inputs=[file_1_input, file_2_input, rules_file_input],
            outputs=upload_status
        )

        with gr.Row():
            column_to_join = gr.Textbox(label="Unique Column to Join On")
            compare_button = gr.Button("Compare Files")
        
        output = gr.Textbox(label="Comparison Result")

        # Bind the compare_files function to the compare button click event
        compare_button.click(
            compare_files,
            inputs=[column_to_join],
            outputs=output
        )

    return app

# Create and launch the application
app = setup_interface()
app.launch(debug=True)
