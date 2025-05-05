# Python code creates a GUI-based Document Management System that allows users to write, format, save, preview, and generate PDFs of text documents, 
# with features like font styling, word count, and print preview using Tkinter and FPDF.


import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font, ttk
from fpdf import FPDF
import os
class DocumentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Management System")
        self.root.geometry("800x600")

        self.setup_widgets()
        self.setup_menu()
        self.update_word_count()

    def setup_widgets(self):
        toolbar = tk.Frame(self.root, bg="lightgray")
        toolbar.pack(fill='x')
        self.font_family = tk.StringVar(value="Arial")
        self.font_size = tk.IntVar(value=12)
        tk.Label(toolbar, text="Font:").pack(side="left")
        font_box = ttk.Combobox(toolbar, textvariable=self.font_family, values=font.families(), width=15)
        font_box.pack(side="left")
        tk.Label(toolbar, text="Size:").pack(side="left")
        size_box = ttk.Combobox(toolbar, textvariable=self.font_size, values=list(range(8, 40)), width=3)
        size_box.pack(side="left")
        tk.Button(toolbar, text="Bold", command=self.make_bold).pack(side="left")
        tk.Button(toolbar, text="Italic", command=self.make_italic).pack(side="left")
        tk.Button(toolbar, text="Underline", command=self.make_underline).pack(side="left")
        tk.Button(toolbar, text="Clear", command=self.clear_text).pack(side="right")

        # Text Area
        self.text_area = tk.Text(self.root, wrap='word', undo=True)
        self.text_area.pack(expand=1, fill='both')
        self.text_area.bind("<<Modified>>", lambda e: self.update_word_count())
        self.set_font()

        # Status bar
        self.status = tk.Label(self.root, text="Words: 0", anchor='w')
        self.status.pack(fill='x')

    def setup_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Generate PDF", command=self.generate_pdf)
        file_menu.add_command(label="Print Preview", command=self.print_preview)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        format_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Font", command=self.set_font)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Saved", "File saved successfully.")

    def generate_pdf(self):
        content = self.text_area.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Empty", "No content to generate PDF.")
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font(self.font_family.get(), size=self.font_size.get())
        for line in content.split('\n'):
            pdf.multi_cell(0, 10, line)
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("PDF Generated", f"PDF saved as {os.path.basename(file_path)}")

    def print_preview(self):
        preview = tk.Toplevel(self.root)
        preview.title("Print Preview")
        text = tk.Text(preview, wrap='word', font=(self.font_family.get(), self.font_size.get()))
        text.insert(tk.END, self.text_area.get(1.0, tk.END))
        text.pack(expand=1, fill='both')

    def set_font(self):
        current_font = font.Font(family=self.font_family.get(), size=self.font_size.get())
        self.text_area.configure(font=current_font)

    def make_bold(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            bold_font = font.Font(self.text_area, self.text_area.cget("font"))
            bold_font.configure(weight="bold")
            self.text_area.tag_configure("bold", font=bold_font)
            self.text_area.tag_add("bold", "sel.first", "sel.last")

    def make_italic(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            italic_font = font.Font(self.text_area, self.text_area.cget("font"))
            italic_font.configure(slant="italic")
            self.text_area.tag_configure("italic", font=italic_font)
            self.text_area.tag_add("italic", "sel.first", "sel.last")

    def make_underline(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "underline" in current_tags:
            self.text_area.tag_remove("underline", "sel.first", "sel.last")
        else:
            underline_font = font.Font(self.text_area, self.text_area.cget("font"))
            underline_font.configure(underline=1)
            self.text_area.tag_configure("underline", font=underline_font)
            self.text_area.tag_add("underline", "sel.first", "sel.last")

    def clear_text(self):
        if messagebox.askyesno("Clear", "Do you really want to clear the text?"):
            self.text_area.delete(1.0, tk.END)

    def update_word_count(self):
        content = self.text_area.get(1.0, tk.END)
        words = len(content.split())
        self.status.config(text=f"Words: {words}")
        self.text_area.edit_modified(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentManager(root)
    root.mainloop()
