import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalyzer:
    """
    Analyzes Docs using a pretrained model and logs all actions and supports session based organization
    """
    def __init__(self, data_dir = None, session_id = None):
        pass

    def analyze_document(self):
        pass

    def analyze_metadata(self):
        pass
