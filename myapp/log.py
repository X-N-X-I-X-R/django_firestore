import logging
import os
from datetime import datetime

def setup_logger(file_name):
    """
    Sets up a logger for a specific file with its own log file.
    
    Args:
        file_name (str): The name of the file requesting the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logger_output')
    os.makedirs(log_dir, exist_ok=True)
    
    # Create file handler with current date in filename
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(
        os.path.join(log_dir, f'{file_name}_{current_date}.log')
    )
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Example usage:
'''
1 -> add this to the top of the file:

from log import setup_logger
logger = setup_logger(__name__)


2 -> then you can use the logger in the file like this:

logger.info("This is an info message")
logger.error("This is an error message")



'''


