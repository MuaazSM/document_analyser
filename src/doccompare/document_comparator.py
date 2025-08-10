import sys
import pandas as pd
from logger.custom_logger import CustomLogger
from dotenv import load_dotenv
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_lib import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentComparatorLLM:
    def __init__(self):
        pass

    def compare_documents(self):
        pass

    def format_response(self):
        pass

    