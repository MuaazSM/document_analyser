import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentIngestion:
    def __init__(self, base_dir):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def delete_existing_file(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error deleting existing file: {e}")
            raise DocumentPortalException("")

    def save_uploaded_file(self):
        """
        Saves uploaded files to a specific directory.
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error uploading file: {e}")
            raise DocumentPortalException("An error occured while saving the uploaded files", sys)
    
    def read_pdf(self, pdf_path: Path) -> str:
        """
        Reads a PDF file and extracts text from each page.
        """
        try:
            with fitz.open(self,pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text() 
                    if text.strip():
                        all_text.append(f"\n --- Page {page_num + 1} --- \n{text}")
                    self.log.info("PDF read successfully", file = str(pdf_path), pages = len(all_text))
                    return "\n".join(all_text)

        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentPortalException("An error encountered while reading the PDF", sys)


