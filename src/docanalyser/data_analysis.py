import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_lib import PROMPT_REGISTRY
class DocumentAnalyzer:
    """
    Analyzes Docs using a pretrained model and logs all actions and supports session based organization
    """
    def __init__(self, data_dir = None, session_id = None):
        self.log = CustomLogger().get_logger(__name__)
        try:
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()

            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(parser = self.parser, llm = self.llm)
            self.prompt = PROMPT_REGISTRY["document_analysis"]

            self.log.info("DocumentAnalyzer initialized successfully")


        except Exception as e:
            self.log.error(f"Error initializing document: {e}")
            raise DocumentPortalException("Error initializing document", e)


    def analyze_document(self, document_text:str)-> dict:
        try:
            chain = self.prompt | self.llm | self.fixing_parser

            self.log.info("Metadata analysis chain initialized")

            response = chain.invoke({
                "format_instructions" : self.parser.get_format_instructions(),
                "document_text": document_text
            })

            self.log.info("Metadata extraction successful", keys = list(response.keys()))

            return response

        except Exception as e:
            self.log.error(f"Metadata analysis failed: {e}")
            raise DocumentPortalException("Metadata extraction failed", e)

    
