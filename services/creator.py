from google import genai
from job_parser import parsed_data
from pypdf import PdfReader
from reportlab.pdfgen import canvas
import os
from dotenv import load_dotenv
class ResumeGenerator:
    def __init__(self, api_key, job_url, resume_path, output_path="output.pdf"):
        self.client = genai.Client(api_key=api_key)
        self.job_url = job_url
        self.resume_path = resume_path
        self.output_path = output_path
    
    def extract_resume_content(self):
        """Extracts text content from the first page of the resume PDF."""
        return PdfReader(self.resume_path).pages[0].extract_text()
    
    def generate_resume(self):
        job_content = parsed_data(self.job_url)
        resume_content = self.extract_resume_content()
        
        prompt = f'''
        {job_content}
        Resume content is below:
        {resume_content}
    - form a resume based on this job profile according to job description and job responsiblity 
    - dont give any other thing except resume content not any recommedation or any kind of thing
      and resume content is blend of resume content and what job is provided by the company
    -dont write any cover letter for it i need just resume and nothing more than this
    -dont write any note also
    -write things based on job description and resume content
    -placed name details according to resume
    -remove double stars or stars and arrange in proper formate
    -prefer resume for name and contact details
    -modify according to job description
    -add A brief 2–4 sentence summary highlighting your skills, experience, and career goals.
    -Tailored to the job  applying for
        '''
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        
        return response.candidates[0].content.parts[0].text
    
    def create_pdf(self, response_text):
        """Creates a formatted PDF from the generated resume text."""
        c = canvas.Canvas(self.output_path)
        x, y = 100, 750
        line_height = 15
        page_height = 800
        bottom_margin = 50

        text_obj = c.beginText(x, y)
        text_obj.setFont("Helvetica", 12)

        for line in response_text.split("\n"):
            if y <= bottom_margin:
                c.drawText(text_obj)
                c.showPage()
                text_obj = c.beginText(x, page_height - 50)
                text_obj.setFont("Helvetica", 12)
                y = page_height - 50

            text_obj.textLine(line)
            y -= line_height

        c.drawText(text_obj)
        c.save()
    
    def run(self):
        """Executes the complete resume generation process."""
        response_text = self.generate_resume()
        self.create_pdf(response_text)
        print("Resume PDF generated successfully.")
    def RUN(self):
        response_text = self.cover_letter()
        print(response_text)        
    def cover_letter(self):
        job_content = parsed_data(self.job_url)
        resume_content = self.extract_resume_content()
        
        prompt = f'''
        Using the provided job description and resume content, generate a professional and concise cover letter tailored to the job role.

Address the cover letter to the hiring manager if a name is available; otherwise, use a general greeting.

Begin with an engaging introduction that states the position being applied for and expresses enthusiasm for the role.

The body should highlight relevant skills, experience, and achievements that align with the job description.

Demonstrate how your expertise adds value to the company and how your background fits the role's responsibilities.

Include a closing paragraph that reiterates interest in the role, expresses willingness to discuss further in an interview, and thanks the reader for their time.

Keep the tone professional yet enthusiastic.

Ensure the cover letter is concise (around 250-350 words) and well-formatted.

Do not include any generic or unnecessary details—focus on relevant experiences and skills.

Job Description:
{job_content}

Original Resume Content:
{resume_content}
        '''
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        
        return response.candidates[0].content.parts[0].text
        

# Usage
if __name__ == "__main__":
    load_dotenv()
    generator = ResumeGenerator(
        api_key=os.getenv("GEMINI_API", "doesnt have any"),
        job_url="https://www.python.org/jobs/7834/",
        resume_path="C:/Users/anujs/Downloads/Blue Light Blue Color Blocks Flight Attendant CV (6).pdf"
    )

    # generator.run()
    generator.RUN()
