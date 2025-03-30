from services.generator import ResumeGenerator
import os
from dotenv import load_dotenv
from config import API_KEY
from app.ui import demo

if __name__ == "__main__":
    # load_dotenv()
    # generator = ResumeGenerator(
    #     api_key=API_KEY,
    #     job_url="https://www.python.org/jobs/7834/",
    #     resume_path="/home/priyanshu/Documents/my_docs/priyanshu_resume_2025.pdf"
    # )

    # # generator.run()
    # generator.RUN()

    demo.launch()