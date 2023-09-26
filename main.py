# main.py
# Import necessary modules and packages
import logging
from log_config import configure_logging
import tkinter as tk
from gui import create_gui, LoadingDialog
from database import initialize_database
import datetime
import time

# Call the configure_logging function to set up logging
logger = configure_logging(log_file='ping.log', log_level=logging.DEBUG)
logger.info("Starting the application")

# Initialize the database (Assuming this function sets up your database schema)
initialize_database()
logger.info("Initializing the database")

# Create the main application window using Tkinter
root = tk.Tk()

# Set the title of the application window
root.title("SCADA Ping Monitor")

# Create and display the graphical user interface by calling create_gui function
create_gui(root)

# Enter the Tkinter main event loop to start the application
root.mainloop()
