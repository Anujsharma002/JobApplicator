import gradio as gr
from services.generator import ResumeGenerator
from config import API_KEY
from services.file_handler import save_file, output_file

def process_input(job_url, resume_path):

    save_file(resume_path) # Save the uploaded resume file

    # Initialize the ResumeGenerator
    generator = ResumeGenerator(
        api_key=API_KEY,
        job_url=job_url,
        resume_path=resume_path
    )


    # Generate the cover letter
    cover_letter = generator.cover_letter()

    # Generate the updated resume PDF
    resume_content, output_path = generator.generate_resume()
    # generator.run()
    updated_resume_path = output_path  # Path to the generated PDF

    return cover_letter, updated_resume_path

# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Resume and Cover Letter Generator")
    with gr.Row():
        job_url_input = gr.Textbox(label="Job URL", placeholder="Enter the job URL")
        resume_file_input = gr.File(label="Upload Resume (PDF)", file_types=[".pdf"])
    with gr.Row():
        cover_letter_output = gr.Textbox(label="Generated Cover Letter", lines=10, interactive=False)
        updated_resume_output = gr.File(label="Download Updated Resume (PDF)")

    submit_button = gr.Button("Submit")

    # Link the button to the processing function
    submit_button.click(
        process_input,
        inputs=[job_url_input, resume_file_input],
        outputs=[cover_letter_output, updated_resume_output]
    )
