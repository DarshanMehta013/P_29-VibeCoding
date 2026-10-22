
import tkinter as tk
from tkinter import filedialog, messagebox

# Clear the editor for a new document.
def new_document():
    text_area.delete("1.0", tk.END)
    messagebox.showinfo("New Document", "A new blank document is ready.")

# Open and read an existing text file.
def open_file():
    file_path = filedialog.askopenfilename(
        title="Open a text file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", content)
        messagebox.showinfo("File Opened", "The file was opened successfully.")

    except (OSError, UnicodeError) as error:
        messagebox.showerror("Open Failed", f"Could not open the file:\n{error}")

# Save the editor contents to a file.
def save_file():
    file_path = filedialog.asksaveasfilename(
        title="Save a text file",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not file_path:
        return

    try:
        content = text_area.get("1.0", "end-1c")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        messagebox.showinfo("File Saved", "The file was saved successfully.")

    except (OSError, UnicodeError) as error:
        messagebox.showerror("Save Failed", f"Could not save the file:\n{error}")

# Close the application.
def exit_editor():
    window.destroy()

# Create the main application window.
window = tk.Tk()
window.title("Simple Text Editor")
window.geometry("700x500")

# Add the action buttons at the top.
button_frame = tk.Frame(window)
button_frame.pack(fill="x", padx=8, pady=8)

tk.Button(button_frame, text="New", width=10,
          command=new_document).pack(side="left", padx=4)

tk.Button(button_frame, text="Open", width=10,
          command=open_file).pack(side="left", padx=4)

tk.Button(button_frame, text="Save", width=10,
          command=save_file).pack(side="left", padx=4)

tk.Button(button_frame, text="Exit", width=10,
          command=exit_editor).pack(side="left", padx=4)

# Add the text area with scrollbars.
editor_frame = tk.Frame(window)
editor_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

vertical_scrollbar = tk.Scrollbar(editor_frame, orient="vertical")
vertical_scrollbar.pack(side="right", fill="y")

horizontal_scrollbar = tk.Scrollbar(editor_frame, orient="horizontal")
horizontal_scrollbar.pack(side="bottom", fill="x")

text_area = tk.Text(
    editor_frame,
    wrap="none",
    font=("Arial", 12),
    undo=True,
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)
text_area.pack(side="left", fill="both", expand=True)

vertical_scrollbar.config(command=text_area.yview)
horizontal_scrollbar.config(command=text_area.xview)

# Keep the application open until the user exits.
window.mainloop()
