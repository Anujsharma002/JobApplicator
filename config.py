from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API","")
UPLOAD_DIR = "./Uploads"
OUTPUT_DIR = "./Output"
