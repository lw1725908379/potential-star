import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import filedialog, dialog


# Function to handle quitting the application
def _quit():
    win.quit()
    win.destroy()
    exit()

# Function to display an About message box
def _msgBox0():
    msg.showinfo('About', 'This is a potentiostat application.')

# Function to save file
def savefile():
    global file_path
    file_path = filedialog.asksaveasfilename(title='Save file')
    if file_path:
        msg.showinfo('File Saved', f'File saved as {file_path}')
        val = file_path
        val1.set(val)

# Main application window
win = tk.Tk()
win.title("Electrochemical Potentiostat")
win.geometry("450x650+350+50")
win.resizable(0, 0)

# Creating a Menu Bar
menu_bar = Menu(win)
win.config(menu=menu_bar)

# Add menu items
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=_quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add another Menu to the Menu Bar and an item
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=_msgBox0)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Create Notebook for tabs
tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Potentiostat')
tabControl.pack(side='top', fill='both', expand=1)

# Placeholder variable
val1 = tk.StringVar()

# Run the main event loop
win.mainloop()
