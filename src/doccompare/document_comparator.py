import sys
import pandas as pd #type:ignore
from logger.custom_logger import CustomLogger
from dotenv import load_dotenv              #type:ignore
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_lib import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser  #type:ignore
from langchain.output_parsers import OutputFixingParser #type:ignore


class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv()
        self.log = CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser = OutputFixingParser.from_llm(parser = self.parser, llm = self.llm)
        self.prompt = PROMPT_REGISTRY["document_comparison"]
        self.chain = self.prompt | self.llm | self.parser | self.fixing_parser
        self.log.info("DocumentComparatorLLM initialized with model and parser.")
    
    def compare_documents(self, combined_docs):
        """
        Compares two docs and then returns a structured response
        """
        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instruction": self.parser.get_format_instructions()
            }
            self.log.info("Starting ddocument comparison", input = inputs)
            response = self.chain.invoke(inputs)
            self.log.info("Document comparison completed", response = response)
            return self._format_response(response)
        

        except Exception as e:
            self.log.error(f"Error formatting response into DataFrame: {e}")
            raise DocumentPortalException("Error formatting response", sys) from e

    def _format_response(self, response_parsed: list[dict]) -> pd.DataFrame:
        """
        Format the response from the LLM into a structured format.
        """
        try:
            df = pd.DataFrame(response_parsed)
            self.log.info("Response formatted into DataFrame", dataframe = df)
            return df
        except Exception as e:
            self.log.error("Error formatting response into DataFrame", error = str(e))
            raise DocumentPortalException("Error formatting response", sys)
    def combine_documents(self) -> str:
        try:
            content_dict = {}
            doc_parts = []

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    content_dict[filename.name] = self.read_pdf(filename)

            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename}\n{content}")

            combined_text = "\n\n".join(doc_parts)
            self.log.info("Documents combined", count = len(doc_parts))
            return combined_text


        except Exception as e:
            self.log.error(f"Error combining docs")