import logging

def configure_logging(log_file='ping.log', log_level=logging.DEBUG):
    """
    Configure the logging settings for the application.

    Args:
        log_file (str): The path to the log file.
        log_level (int): The desired logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        logging.Logger: The root logger instance.
    """
    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Create a logger instance for the current module
    logger = logging.getLogger(__name__)

    return logger

# Example usage:
# root_logger = configure_logging()
# logger.debug("This is a debug message.")
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")

