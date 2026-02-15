import tkinter as tk
from app_gui import BillCreator

def main():
    root = tk.Tk()
    app = BillCreator(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()
# Run the application
if __name__ == "__main__":
    main()
