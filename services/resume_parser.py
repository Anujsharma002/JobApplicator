from pypdf import PdfReader

def extract_resume_content(self, resume_path):
        """Extracts text content from the first page of the resume PDF."""
        return PdfReader(resume_path).pages[0].extract_text()