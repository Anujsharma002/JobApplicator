from google import genai
from services.job_parser import parsed_data
from services.resume_parser import extract_resume_content
from config import OUTPUT_DIR
import subprocess
from rendercv.data.models.curriculum_vitae import CurriculumVitae
import os

class ResumeGenerator:
    def __init__(self, api_key, job_url, resume_path, output_path=OUTPUT_DIR):
        self.client = genai.Client(api_key=api_key)
        self.job_url = job_url
        self.resume_path = resume_path
        self.output_path = output_path
    
    def generate_resume(self):
        job_content = parsed_data(self.job_url)
        resume_content = extract_resume_content(self, self.resume_path)

        cv_schema = CurriculumVitae.model_json_schema()
        prompt = f'''
        Job Description: {job_content}
        Candidate Resume: {resume_content}

        Write the content of a resume in YAML format. The YAML should:
        
        1. Include all the sections that are required by rendercv as specified in their docs.
        2. Format it in yaml format.
        3. Ensure it follows rendercv guidelines for creating the yaml.
        4. Format the content professionally and concisely.
        6. wrap each fields content in double quotes. so that its a valid yaml.
        7. Use proper YAML syntax for keys and values.
        8. Ensure the output is valid YAML that can be converted to a PDF using rendercv.
        9. Make the content suitable for the given job description.
        10. In the skills section, include the skills as a string of comma-separated values.
        11. Keep the content highly concise so that the rendered pdf has only 1 page.
        12. Make sure to include the all the details from candidates reusme correctly especially the education sections. 

        below is the schema of rendercv's requeired fields in the yaml file

        cv:
        ...
        YOUR CONTENT
        ...
        design:
            theme: classic 
            

        stricly use the following JSON schema for the cv section to generate the yaml:
        {cv_schema}

        for the social networks field only include from the below list exclude anything othere than these eg leetcode:
        - GitHub
        - LinkedIn
        - X
        - Instagram
        - Youtube
        - GitLab
        - Mastadon
        - StackOverflow
        - ResearchGate
        - Telegram


        consider the given example of the yaml file to generate the content:
        cv:
            name: John Doe
            location: Location
            email: john.doe@example.com
            phone: tel:+1-609-999-9995
            social_networks:
                - network: LinkedIn
                username: john.doe
                - network: GitHub
                username: john.doe
            sections:
                welcome_to_RenderCV!:
                - '[RenderCV](https://rendercv.com) is a Typst-based CV
                    framework designed for academics and engineers, with Markdown
                    syntax support.'
                - Each section title is arbitrary. Each section contains
                    a list of entries, and there are 7 different entry types
                    to choose from.
                education:
                - institution: Stanford University
                    area: Computer Science
                    degree: PhD
                    location: Stanford, CA, USA
                    start_date: 2023-09
                    end_date: present
                    highlights:
                    - Working on the optimization of autonomous vehicles
                        in urban environments
                ...
        '''


        response = self.client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt,
        )
        
        # typst_code = response.candidates[0].content.parts[0].text
        content = response.text

        # Remove the first and last lines if they contain '''typst and '''
        content = content.strip()
        lines = content.splitlines()
        lines = lines[1:]  # Remove the first line
        lines = lines[:-1]  # Remove the last line
        content = "\n".join(lines)

        yaml_file_path = os.path.join(OUTPUT_DIR, "generated_resume.yaml")
        with open(yaml_file_path, "w") as yaml_file:
            yaml_file.write(content)
        # try:
        #     yaml_data = yaml.safe_load(content)
        # except yaml.YAMLError as e:
        #     print(f"Error in YAML content: {e}")
        #     raise RuntimeError("Invalid YAML content generated.")

        # Save YAML content to a .yaml file

        # Use RenderCV or a similar tool to convert YAML to PDF
        pdf_output_path = os.path.join(OUTPUT_DIR)
        try:
            subprocess.run(
                ["rendercv", "render", yaml_file_path, "-o", pdf_output_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error during YAML to PDF conversion: {e.stderr.decode()}")
            raise RuntimeError("Failed to convert YAML to PDF.")
        
        # Find the generated PDF file in the OUTPUT_DIR
        pdf_file_name = None
        for file_name in os.listdir(OUTPUT_DIR):
            if file_name.endswith(".pdf"):
                pdf_file_name = file_name
                break

        if not pdf_file_name:
            raise RuntimeError("No PDF file was generated by RenderCV.")

        pdf_output_path = os.path.join(OUTPUT_DIR, pdf_file_name)

        return content, pdf_output_path

    



    def update_output_path(self, path):
        self.output_path = path
    
    def run(self):
        """Executes the complete resume generation process."""
        response_text = self.generate_resume()
        # self.create_pdf(response_text)
        print("Resume PDF generated successfully.")
        # print(response_text)
        return response_text

    def RUN(self):
        response_text = self.cover_letter()
        print(response_text)       

    def cover_letter(self):
        job_content = parsed_data(self.job_url)
        resume_content = extract_resume_content(self, resume_path=self.resume_path)
        
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
    