import gradio as gr
import requests

# Function to upload a file and return a Markdown link and status message
def upload_file(file_info):
    if file_info is None:
        return "", "No file selected"
    files = {'file': open(file_info, 'rb')}
    api_endpoint = '192.2.4.177:8000/upload_file'
    headers = {
        'Content-Type': 'application/octet-stream',
    }
    response = requests.get("http://127.0.0.1:8000/health_check")
    response = requests.post(
        url=api_endpoint,
        headers=headers,
        files=files,
    )
    if response.status_code in (200, 201):
        purl = response.json().get('presigned_url')
        return f"[{file_info}]({purl})", f"Successfully uploaded: {file_info}"
    else:
        return "", f"Failed to upload {file_info}. Response: {response.text}"

# Function to compare files (placeholder)
def compare_files(file1, file2, rules_file, column_to_join):
    if not (file1 and file2 and rules_file):
        return "Please upload all files before comparison."
    # Placeholder for your comparison logic
    return "Comparison results would be displayed here."

# Set up Gradio Blocks Interface
with gr.Blocks() as app:

    gr.Markdown("## Upload Files for Comparison")
    uploaded_list = gr.Markdown()
    upload_status = gr.Markdown()

    with gr.Row():
        file_1_input = gr.File(label="File 1")
        file_2_input = gr.File(label="File 2")
        rules_file_input = gr.File(label="Rules File")

    column_to_join_input = gr.Textbox(label="Unique Column to Join On")
    compare_button = gr.Button("Compare Files")
    comparison_output = gr.Textbox(label="Comparison Result")

    # We'll use these functions to update the uploaded files list with correct labels
    def upload_file1(file_info):
        link_md, message = upload_file(file_info)
        uploaded_list.update(uploaded_list.value + "\\n" + link_md)
        upload_status.update(message)
        
    def upload_file2(file_info):
        link_md, message = upload_file(file_info)
        uploaded_list.update(uploaded_list.value + "\\n" + link_md)
        upload_status.update(message)

    def upload_rules_file(file_info):
        link_md, message = upload_file(file_info)
        uploaded_list.update(uploaded_list.value + "\\n" + link_md)
        upload_status.update(message)

    file_1_input.change(upload_file1, inputs=[file_1_input], outputs=[uploaded_list, upload_status])
    file_2_input.change(upload_file2, inputs=[file_2_input], outputs=[uploaded_list, upload_status])
    rules_file_input.change(upload_rules_file, inputs=[rules_file_input], outputs=[uploaded_list, upload_status])

    compare_button.click(
        compare_files,
        inputs=[file_1_input,
                file_2_input,
                rules_file_input,
                column_to_join_input],
        outputs=[comparison_output]
    )

# Running the Gradio app
app.launch()
