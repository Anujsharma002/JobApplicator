import gradio as gr
from services.generator import ResumeGenerator
from config import API_KEY

def process_input(job_url, resume_file, option):
    # Save the uploaded resume file locally

    # Initialize the ResumeGenerator
    generator = ResumeGenerator(
        api_key=API_KEY,
        job_url=job_url,
        resume_path=resume_file
    )

    # Generate output based on the selected option
    if option == "Generate Cover Letter":
        cover_letter = generator.cover_letter()
        return cover_letter
    elif option == "Generate Updated Resume":
        generator.run()
        return "Updated resume PDF has been generated successfully. Check the output.pdf file."

# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Resume and Cover Letter Generator")
    with gr.Row():
        job_url_input = gr.Textbox(label="Job URL", placeholder="Enter the job URL")
        resume_file_input = gr.File(label="Upload Resume (PDF)", file_types=[".pdf"])
    option_input = gr.Radio(
        choices=["Generate Cover Letter", "Generate Updated Resume"],
        label="Select an Option"
    )
    output = gr.Textbox(label="Output", lines=10, interactive=False)
    submit_button = gr.Button("Submit")

    # Link the button to the processing function
    submit_button.click(
        process_input,
        inputs=[job_url_input, resume_file_input, option_input],
        outputs=output
    )

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()