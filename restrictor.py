import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import sys
import os
import subprocess
import threading

global pathways, measures, templates
templates = os.environ.get("templates")
pathways =  os.environ.get("pathways")
measures =  os.environ.get("measures")

## Pathing Setup
this_dir = os.path.dirname(__file__)
display_lab_dir = os.path.abspath(os.path.join(this_dir, os.pardir))

# Function to report current environmental variable settings
def report_vars():
    print(f'Templates:',    os.environ.get('templates'))
    print(f'Pathways:',     os.environ.get('pathways'))
    print(f'Measures:',     os.environ.get('measures'))
    print('')

# Main UI window
def create_main_window():
    root = tk.Tk()
    root.title("Knowledge Restrictor GUI")
    root.geometry("1240x800")
    
    ## Widget styling global options
    style = ttk.Style()
    style.configure("main.TLabel",
        foreground = "#9b9a9c",
        background = "#480e7b",
        font=("Helvetica", 16)
    )
    style.configure("main.TButton",
        relief=     'raised'
    )
    style.configure('main.TCheckbutton',
        font=('Helvetica', 14)
    )

    # OS based behavior logic
    if sys.platform == 'darwin':
        print("User platform identified as MacOS")
    elif sys.platform == 'linux':
        print("User platform identified as Linux")
    elif sys.platform == 'windows':
        print("User platform identified as Windows")

    # UI elements
    ttk.Label(root, text="Report current environmental variable settings").pack(pady=5)
    readback_button = ttk.Button(root,
        text="Readback Vars",
        command=report_vars,
        style='main.TButton'
    )
    readback_button.pack(pady=5)

    ttk.Label(root, text="Enter message template file to restrict to:", style='main.TLabel').pack(pady=10)
    message_temp_entry = ttk.Entry(root)
    # INSERT A DEFAULT VALUE BELOW
    message_temp_entry.insert(0, "/Users/mack/Code/Display-Lab/knowledge-base/message_templates")  # Default value
    message_temp_entry.pack(pady=10)

    ttk.Label(root, text="Enter causal pathway file to restrict to:", style='main.TLabel').pack(pady=10)
    causal_path_entry = ttk.Entry(root)
    causal_path_entry.insert(0, "/Users/mack/Code/Display-Lab/knowledge-base/causal_pathways")  # Default value
    causal_path_entry.pack(pady=10)

    ttk.Label(root, text="Enter measures file to restrict to:", style='main.TLabel').pack(pady=10)
    measure_entry = ttk.Entry(root)
    measure_entry.insert(0, "/Users/mack/Code/Display-Lab/knowledge-base/measures.json")  # Default value
    measure_entry.pack(pady=10)

    # Entry fields for virtual environment and FastAPI app location
    ttk.Label(root, text="Virtual Environment Path:").pack()
    venv_entry = ttk.Entry(root)
    venv_entry.insert(0, "/Users/mack/Code/Display-Lab/precision-feedback-pipeline/PFPenv")  # Default value
    venv_entry.pack()

    ttk.Label(root, text="FastAPI App Location:").pack()
    app_entry = ttk.Entry(root)
    app_entry.insert(0, "/Users/mack/Code/Display-Lab/precision-feedback-pipeline")  # Default value    
    app_entry.pack()
    
    # Function to set environmental variables
    def set_env_vars():
        global measures, pathways, templates
        templates = message_temp_entry.get()
        pathways = causal_path_entry.get()
        measures = measure_entry.get()

        os.environ['templates'] = templates
        os.environ['pathways'] = pathways
        os.environ['measures'] = measures
        report_vars()

    ttk.Button(root, text="Save Configuration", command=set_env_vars).pack(anchor=tk.S, pady=20)
    

    # Function to deploy a PFP API instance as a subprocess
    def deploy_pfp():
        venv_path = venv_entry.get()
        app_location = app_entry.get()

        if venv_path and app_location:
            try:
                # Activate the virtual environment and run the FastAPI app
                activate_cmd = f"source {venv_path}/bin/activate && poetry run uvicorn main311:app --host 0.0.0.0 --port 8000"

                subprocess.Popen(activate_cmd, shell=True, executable="/bin/bash")  # Use /bin/bash as the shell

            except Exception as e:
                print(f"Error: {e}")


    # Deploy PFP button
    ttk.Button(root, text="Deploy PFP", command=deploy_pfp).pack(pady=10)

    # Log display section
    log_text = tk.Text(root, wrap=tk.WORD)
    log_text.pack(fill=tk.BOTH, expand=True)

    # Redirect print and log statements (stdout, stderr) to log_text widget
    def redirect_output(output_widget):
        class StdoutRedirector:
            def __init__(self, widget):
                self.widget = widget

            def write(self, text):
                self.widget.insert(tk.END, text)

        sys.stdout = StdoutRedirector(log_text)     # redirect output
        sys.stderr = StdoutRedirector(log_text)     # redirect errors
    redirect_output(log_text)

    # Confirm when user attempts to close the program
    def on_closing():
        if messagebox.askokcancel("Quit", "Close the GUI?"):
            root.destroy()
            sys.exit(0)
    root.protocol("WM_DELETE_WINDOW", on_closing)  # Set the close button event handler
    
    # Start Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    create_main_window()
    exit(0)
