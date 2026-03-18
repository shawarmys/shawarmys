import pdfplumber
import os


class TextExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        with pdfplumber.open(self.file_path) as pdf:
            # Extract text from the first page
            first_page = pdf.pages[0]
            return first_page.extract_text()

    def extract_table(self):
        with pdfplumber.open(self.file_path) as pdf:
            # Extract table from the first page
            first_page = pdf.pages[0]
            return first_page.extract_table()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "clinic_4_nursing.pdf")

    print("Extracted Text:")
    text_extractor = TextExtractor(file_path)
    text = text_extractor.extract_text()
    print(text)

