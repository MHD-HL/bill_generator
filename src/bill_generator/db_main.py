import tkinter as tk
from db_gui import DatabaseGUI

def main():
    root = tk.Tk()
    app = DatabaseGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()
    
# Main application
if __name__ == "__main__":
    main()
