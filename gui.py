# gui.py
# Import necessary modules and packages
import logging
from log_config import configure_logging
import tkinter as tk
from tkinter import ttk, messagebox
from ping3 import ping
import database as db
import datetime
import time
import sqlite3

# Call the configure_logging function to set up logging
logger = configure_logging(log_file='ping.log', log_level=logging.DEBUG)

# Define functions related to GUI

def ping_target(target, count=10, interval=1):
    """
    Perform ping operations on a target IP address.

    Args:
        target (str): The IP address or hostname to ping.
        count (int): The number of ping attempts.
        interval (int): The time interval between ping attempts in seconds.

    Returns:
        Tuple[List[Tuple[datetime.datetime, str, float]], List[str]]:
            A tuple containing two lists:
                - A list of tuples with timestamp, target, and response time (in milliseconds).
                - A list of strings containing bad results (targets with no response).
    """
    results = []
    bad_results = []
    for i in range(count):
        response_time = ping(target)
        if response_time is not None:
            results.append((datetime.datetime.now(), target, response_time))
            logger.info(f'Response from {target}: time={response_time} MS')
        else:
            results.append((datetime.datetime.now(), target, None))
            logger.warning(f'No response from {target}')
            bad_results.append(f'No response from: {target} ')
        time.sleep(interval)
    return results, bad_results

def generate_report(results, filename):
    """
    Generate a ping report and save it to a file.

    Args:
        results (List[Tuple[datetime.datetime, str, float]]): A list of ping results.
        filename (str): The name of the file to save the report to.
    """
    with open(filename, "a") as file:
        file.write("Ping Report - {}\n".format(datetime.datetime.now()))
        for result in results:
            timestamp, target, response_time = result
            if response_time is not None:
                file.write("[{}] Response from {}: time={} MS\n".format(timestamp, target, response_time))
            else:
                file.write("[{}] No response from {}\n".format(timestamp, target))
        file.write("\n")

def on_generate_full_report():
    """
    Generate a full ping report for all devices and display it in the GUI.
    """
    ping_count = 4
    ping_interval = 1
    bad_results = []

    for value in db.fetch_devices():
        all_results = ping_target(value["IP"], ping_count, ping_interval)
        ping_results = all_results[0]
        if all_results[1]:
            bad_results.append(all_results[1][0])
        generate_report(ping_results, "report_full.txt")

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Full report generated.\n \n")

    if bad_results:
        output_text.insert(tk.END, "Pings without response: \n")
        for bad in bad_results:
            output_text.insert(tk.END, f"{bad}.\n")

def on_generate_selected_report():
    """
    Generate a ping report for the selected device and display it in the GUI.
    """
    selected_row = select_row_from_cb()
    if selected_row == None:
        return
    ping_count = 4
    ping_interval = 1

    ping_results = ping_target(selected_row[2], ping_count, ping_interval)[0]
    generate_report(ping_results, "report_selected_device.txt")

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Report generated for {selected_row[2]}.\n\n")
    for result in ping_results:
        output_text.insert(tk.END, f"IP: {result[1]}, Response: {result[2]}\n")

# Function to handle selection change
def on_combo_select(event):
    """
    Handle the event when a device is selected from the combo box.

    Args:
        event (tk.Event): The event object.
    """
    selected_name = ip_combobox.get()
    selected_row = db.find_row(selected_name)

    if selected_row:
        name_label.config(text=f"Name: {selected_row[1]}")
        ip_label.config(text=f"IP: {selected_row[2]}")

def add_device():
    """
    Add a new device to the database.
    """
    # Create a new window for adding a device
    add_window = tk.Toplevel(app)
    add_window.title("Add Device")

    # Create labels and entry widgets for name and IP
    name_label = tk.Label(add_window, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    ip_label = tk.Label(add_window, text="IP:")
    ip_label.pack()
    ip_entry = tk.Entry(add_window)
    ip_entry.pack()

    def save_device():
        # Get the values from the entry widgets
        device_name = name_entry.get()
        device_ip = ip_entry.get()

        if not device_name or not device_ip:
            # Check if either field is empty
            tk.messagebox.showerror("Error", "Both Name and IP are required")
            return

        db.add_device(device_name, device_ip)

        # Update the device list
        update_device_list()

        # Close the add window
        add_window.destroy()

    # Create a button to save the device
    save_button = tk.Button(add_window, text="Save", command=save_device)
    save_button.pack()

def update_device():
    """
    Update an existing device's name and IP in the database.
    """
    selected_row = select_row_from_cb()

    if selected_row == None:
        return

    # Create a new window for updating the device
    update_window = tk.Toplevel(app)
    update_window.title("Update Device")

    # Create labels and entry widgets for name and IP
    name_label = tk.Label(update_window, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(update_window)
    name_entry.pack()
    name_entry.insert(0, selected_row[1])

    ip_label = tk.Label(update_window, text="IP:")
    ip_label.pack()
    ip_entry = tk.Entry(update_window)
    ip_entry.pack()
    ip_entry.insert(0, selected_row[2])

    def save_updated_device():
        # Get the updated values from the entry widgets
        updated_name = name_entry.get()
        updated_ip = ip_entry.get()

        if not updated_name or not updated_ip:
            # Check if either field is empty
            tk.messagebox.showerror("Error", "Both Name and IP are required")
            return

        db.update_device(selected_row[0], updated_name, updated_ip)

        # Update the device list
        update_device_list()

        # Close the update window
        update_window.destroy()

    # Create a button to save the updated device
    save_button = tk.Button(update_window, text="Save", command=save_updated_device)
    save_button.pack()

def remove_device():
    """
    Remove an existing device from the database.
    """
    selected_name = ip_combobox.get()
    selected_row = db.find_row(selected_name)
    if selected_row == None:
        tk.messagebox.showerror("Error", "Please select a device")
        return

    # Ask for confirmation before removing the device
    confirmation = tk.messagebox.askyesno("Confirm Removal", f"Do you want to remove {selected_row[1]} ({selected_row[2]})?")

    if confirmation:
        # Remove the device from the database
        db.remove_device(selected_row[0])

        # Update the device list
        update_device_list()

def update_device_list():
    """
    Update the device list and combo box values.
    """
    devices_data = db.fetch_devices()

    # Empty the combo box values
    ip_combobox.set(' ')
    # Update the combo box values
    ip_combobox["values"] = [device["name"] for device in devices_data]

def show_table():
    """
    Display the SQLite database table in a new window.
    """
    # Create a new window for the table viewer
    table_viewer_window = tk.Toplevel(app)
    table_viewer_window.title("SQLite Table Viewer")

    # Create a Treeview widget to display the table
    tree = ttk.Treeview(table_viewer_window, columns=("Name", "IP"))
    tree.column("#0", width=0)
    tree.column("#1", width=150)
    tree.column("#2", width=110)
    tree.heading("#1", text="Name")
    tree.heading("#2", text="IP")

    # Define a function to populate the Treeview with data from the database
    def populate_tree():
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)

        [tree.insert("", "end", values=(item['name'], item['IP'])) for item in db.fetch_devices()]

    # Create a "Refresh" button to populate the Treeview
    refresh_button = tk.Button(table_viewer_window, text="Refresh", command=populate_tree)
    refresh_button.pack(pady=10)

    # Populate the Treeview initially
    populate_tree()

    # Pack the Treeview widget
    tree.pack()

def select_row_from_cb():
    """
    Retrieve the selected device's row from the combo box.

    Returns:
        Union[Tuple[int, str, str], None]: A tuple containing device ID, name, and IP if selected, or None if not selected.
    """
    selected_name = ip_combobox.get()
    selected_row = db.find_row(selected_name)
    if selected_row == None:
        tk.messagebox.showerror("Error", "Please select a device to update")
        return
    return selected_row

# Create the main application window
app = tk.Tk()
app.title("SCADA Ping Monitor")
app.geometry("600x400")  # Set the width and height of the window

# Create a menu bar
menu_bar = tk.Menu(app)
app.config(menu=menu_bar)

# Create a "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Generate Full Report", command=on_generate_full_report)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)

# Create a "Database" menu
db_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Database", menu=db_menu)
db_menu.add_command(label="Add Device", command=add_device)
db_menu.add_command(label="Update Device", command=update_device)
db_menu.add_command(label="Remove Device", command=remove_device)
db_menu.add_command(label="Show DB", command=show_table)

# Full Report Button
full_report_button = tk.Button(app, text="Generate Full Report", command=on_generate_full_report)
full_report_button.pack(pady=15)

# IP Selection Dropdown
ip_label = tk.Label(app, text="Or select device from the list:")
ip_label.pack(pady=5)
ip_combobox = ttk.Combobox(app, values=[device["name"] for device in db.fetch_devices()])
ip_combobox.pack(pady=5)

# Label to display selected name and IP
name_label = tk.Label(app, text="Name: ")
name_label.pack()
ip_label = tk.Label(app, text="IP: ")
ip_label.pack()

# Bind the selection event to the combo box
ip_combobox.bind("<<ComboboxSelected>>", on_combo_select)

# Selected Report Button
selected_report_button = tk.Button(app, text="Ping Selected Device", command=on_generate_selected_report)
selected_report_button.pack(pady=5)

# Output Text
output_text = tk.Text(app, height=15, width=60)
output_text.pack(pady=25)

app.mainloop()
