
import tkinter as tk
from tkinter import filedialog, messagebox

# Store the current file name.
current_file = None

def mark_saved():
    """Mark the current text as saved."""
    text_area.edit_modified(False)

def save_as():
    """Choose a file name and save the note."""
    global current_file

    file_path = filedialog.asksaveasfilename(
        title="Save note as",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not file_path:
        return False

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", "end-1c"))

        current_file = file_path
        mark_saved()
        messagebox.showinfo("Saved", "Your note was saved successfully.")
        return True

    except (OSError, UnicodeError) as error:
        messagebox.showerror("Save Error", f"Could not save the note:\n{error}")
        return False

def save_note():
    """Save to the current file or ask for a file name."""
    if current_file is None:
        return save_as()

    try:
        with open(current_file, "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", "end-1c"))

        mark_saved()
        messagebox.showinfo("Saved", "Your note was saved successfully.")
        return True

    except (OSError, UnicodeError) as error:
        messagebox.showerror("Save Error", f"Could not save the note:\n{error}")
        return False

def confirm_discard_or_save():
    """Ask before losing unsaved changes."""
    if not text_area.edit_modified():
        return True

    answer = messagebox.askyesnocancel(
        "Unsaved Changes",
        "Do you want to save your changes before continuing?"
    )

    if answer is None:
        return False

    if answer:
        return save_note()

    return True

def new_note():
    """Create a new blank note."""
    global current_file

    if not confirm_discard_or_save():
        return

    text_area.delete("1.0", tk.END)
    current_file = None
    mark_saved()

def open_note():
    """Open a text file."""
    global current_file

    if not confirm_discard_or_save():
        return

    file_path = filedialog.askopenfilename(
        title="Open note",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", content)
        current_file = file_path
        mark_saved()

    except (OSError, UnicodeError) as error:
        messagebox.showerror("Open Error", f"Could not open the note:\n{error}")

def exit_app():
    """Close only after handling unsaved changes."""
    if confirm_discard_or_save():
        window.destroy()

def select_all(event=None):
    """Select all text in the editor."""
    text_area.tag_add("sel", "1.0", "end-1c")
    text_area.mark_set(tk.INSERT, "1.0")
    text_area.focus_set()
    return "break"

def show_about():
    """Display information about the application."""
    messagebox.showinfo(
        "About My Notes",
        "My Notes - Text Editor\nA simple notes app made with Python and Tkinter."
    )

# Create the main window.
window = tk.Tk()
window.title("My Notes - Text Editor")
window.geometry("700x500")

# Create the text area and scrollbars.
editor_frame = tk.Frame(window)
editor_frame.pack(fill="both", expand=True)

vertical_scrollbar = tk.Scrollbar(editor_frame, orient="vertical")
vertical_scrollbar.pack(side="right", fill="y")

horizontal_scrollbar = tk.Scrollbar(editor_frame, orient="horizontal")
horizontal_scrollbar.pack(side="bottom", fill="x")

text_area = tk.Text(
    editor_frame,
    wrap="none",
    undo=True,
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set,
    font=("Arial", 12)
)
text_area.pack(side="left", fill="both", expand=True)

vertical_scrollbar.config(command=text_area.yview)
horizontal_scrollbar.config(command=text_area.xview)

# Track edits so the app can warn about unsaved changes.
text_area.edit_modified(False)
text_area.bind("<<Modified>>", lambda event: None)

# Create the File menu.
menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="New", command=new_note, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_note, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_note, accelerator="Ctrl+S")
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)
# Create the Edit menu.
edit_menu = tk.Menu(menu_bar, tearoff=False)
edit_menu.add_command(
    label="Cut",
    command=lambda: text_area.event_generate("<<Cut>>")
)
edit_menu.add_command(
    label="Copy",
    command=lambda: text_area.event_generate("<<Copy>>")
)
edit_menu.add_command(
    label="Paste",
    command=lambda: text_area.event_generate("<<Paste>>")
)
edit_menu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
menu_bar.add_cascade(label="Edit", menu=edit_menu)
# Create the Help menu.
help_menu = tk.Menu(menu_bar, tearoff=False)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)
window.config(menu=menu_bar)
# Keyboard shortcuts.
window.bind("<Control-n>", lambda event: new_note())
window.bind("<Control-o>", lambda event: open_note())
window.bind("<Control-s>", lambda event: save_note())
window.bind("<Control-a>", select_all)
window.protocol("WM_DELETE_WINDOW", exit_app)
window.mainloop()
