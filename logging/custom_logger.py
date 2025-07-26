import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self, log_dir = "logs"):
        logs_dir = os.path.join(os.getcwd(), "logs") # Log Directory available in the Root Directory
        os.makedirs(logs_dir, exist_ok=True) 

        # Create timestamped log file name
        LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # Creating a LOG FILE to capture logs
        LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)   

        # Configure Logging
        logging.basicConfig(
        filename=LOG_FILE_PATH,
        format="[ %(asctime)s ] %(levelname)s %(name)s (line:%(lineno)d) - %(message)s",
        level=logging.INFO,
        )

    def get_Logger(self, name = __file__):              
        return logging.getLogger(os.path.basename(name)) # name captures the Current File

if __name__ == "__main__":
    logger = CustomLogger()
    logger = logger.get_Logger(__file__)
    logger.info("Custom Logger is initialized")