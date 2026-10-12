import customtkinter
import threading

from src.controllers.AIAssistant import AIAssistant
from tkinter import filedialog, TclError
from src.database.db import Gestore_DB

assistant = AIAssistant('llama3.2')

class LeftSidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        # super().__init__ chiama il costruttore della classe padre (CTkFrame)
        # Qui passiamo le configurazioni che prima erano in Root
        super().__init__(master, corner_radius=0, width=170)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        self.lbl_title = customtkinter.CTkLabel(self, text="Note", corner_radius=0, font=customtkinter.CTkFont(size=16, weight="bold", family="Arial"), text_color="white")
        self.lbl_title.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")
        
        self.btn_new_note = customtkinter.CTkButton(self, text="Nuova nota", corner_radius=0, command = self.new_note)
        self.btn_new_note.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="e")
        
        self.scrollable_note = customtkinter.CTkScrollableFrame(self)
        
        self.scrollable_note.grid(row=1, column=0, columnspan=2, padx=20, pady=20, fill="both", sticky="nsew")
        self.all_note()
        
    def all_note(self):
        for widget in self.scrollable_note.winfo_children():
            widget.destroy()
            
        notes = self.master.db.get_all_notes()
        for note in notes:
            label = customtkinter.CTkLabel(
                self.scrollable_note,
                text=note[1],
                fg_color="transparent",
                cursor="hand2",
                corner_radius=0)
            label.pack(pady=5, padx=10, fill="x", anchor="w")
            
            label.bind("<Button-1>", lambda event, note_id=note[0]: self.master.show_note(note_id))
    
    def new_note(self):
        self.master.main_frame.editor.delete("0.0", "end")
        self.master.main_frame.ia_output.delete("0.0", "end")
        self.master.main_frame.toolbar.title.delete(0, "end")
        self.master.main_frame.toolbar.title.insert(0, "Nuova nota")
        
        new_id = self.master.db.new_note(title = "Nuova nota", content = "", created_at = "", last_modified_at = "")
        if new_id:
            self.master.current_note_id = new_id
            
        self.all_note()
        
class RightSidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        # super().__init__ chiama il costruttore della classe padre (CTkFrame)
        super().__init__(master, corner_radius=0, width=80)
        
        self.btn_ia_create_prompt = customtkinter.CTkButton(self, text="IA Prompt", corner_radius=0, command = self.ia_crate_prompt_click)
        self.btn_ia_create_prompt.pack(side="top", fill="x", pady=20, padx=20)
        
        
        self.btn_ia_create_ticket = customtkinter.CTkButton(self, text="IA Ticket", corner_radius=0, command = self.ia_crate_ticket_click)
        self.btn_ia_create_ticket.pack(side="top", fill="x", pady=20, padx=20)
        
        self.btn_ia_create_script = customtkinter.CTkButton(self, text="IA Script", corner_radius=0, command = self.ia_crate_script_click)
        self.btn_ia_create_script.pack(side="top", fill="x", pady=20, padx=20)

    def ia_crate_prompt_click(self):
        self.btn_ia_create_prompt.configure(text="⏳ Elaborazione...", state="disabled")
        threading.Thread(target=self.process_prompt).start()    
    
    def process_prompt(self):
        try:
            input_text = self.master.main_frame.editor.get("sel.first", "sel.last")
            self.master.after(0, lambda: self.master.main_frame.ia_output.delete("0.0", "end"))
            
            for chunk in assistant.chat(input_text, task_type="prompt"):
                self.master.after(0, lambda c=chunk: self.master.main_frame.ia_output.insert("end", c))
            
            self.master.after(0, lambda: self.master.sidebar_right.btn_ia_create_prompt.configure(text="IA Prompt", state="normal"))
        except TclError:
            self.master.sidebar_right.btn_ia_create_prompt.configure(text="IA Prompt", state="normal")
            print("Nessun testo selezionato!")
        except Exception as e:
            self.master.sidebar_right.btn_ia_create_prompt.configure(text="IA Prompt", state="normal")
            print(f"Errore imprevisto: {e}")
            
    def ia_crate_ticket_click(self):
        self.btn_ia_create_ticket.configure(text="⏳ Elaborazione...", state="disabled")
        threading.Thread(target=self.process_ticket).start()
            
    def process_ticket(self):
        try:
            input_text = self.master.main_frame.editor.get("sel.first", "sel.last")
            self.master.after(0, lambda: self.master.main_frame.ia_output.delete("0.0", "end"))
            
            for chunk in assistant.chat(input_text, task_type="ticket"):
                self.master.after(0, lambda c=chunk: self.master.main_frame.ia_output.insert("end", c))
            
            self.master.after(0, lambda: self.master.sidebar_right.btn_ia_create_ticket.configure(text="IA Ticket", state="normal"))
        except TclError:
            self.master.sidebar_right.btn_ia_create_ticket.configure(text="IA Ticket", state="normal")
            print("Nessun testo selezionato!")
        except Exception as e:
            self.master.sidebar_right.btn_ia_create_ticket.configure(text="IA Ticket", state="normal")
            print(f"Errore imprevisto: {e}")

    def ia_crate_script_click(self):
        self.btn_ia_create_script.configure(text="⏳ Elaborazione...", state="disabled")
        threading.Thread(target=self.process_script).start()
            
    def process_script(self):
        try:
            input_text = self.master.main_frame.editor.get("sel.first", "sel.last")
            self.master.after(0, lambda: self.master.main_frame.ia_output.delete("0.0", "end"))
            
            for chunk in assistant.chat(input_text, task_type="script"):
                self.master.after(0, lambda c=chunk: self.master.main_frame.ia_output.insert("end", c))
            
            self.master.after(0, lambda: self.master.sidebar_right.btn_ia_create_script.configure(text="IA Script", state="normal"))
        except TclError:
            self.master.sidebar_right.btn_ia_create_script.configure(text="IA Script", state="normal")
            print("Nessun testo selezionato!")
        except Exception as e:
            self.master.sidebar_right.btn_ia_create_script.configure(text="IA Script", state="normal")
            print(f"Errore imprevisto: {e}")
            
class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        # super().__init__ chiama il costruttore della classe padre (CTkFrame)
        super().__init__(master, corner_radius=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=50)
        self.grid_rowconfigure(1, weight=3, minsize=400)
        self.grid_rowconfigure(2, weight=1, minsize=250)
        
        self.toolbar = customtkinter.CTkFrame(self, corner_radius=0, height=50)
        self.toolbar.grid(row=0, column=0, sticky="nsew")
        
        self.toolbar.grid_columnconfigure(0, weight=1)
        self.toolbar.grid_columnconfigure(1, weight=1)
        self.toolbar.grid_columnconfigure(2, weight=1)
        
        self.toolbar.title = customtkinter.CTkEntry(self.toolbar, corner_radius=0)
        self.toolbar.title.grid(row=0, column=0, sticky="nsew")
        
        self.toolbar.btn_save_note = customtkinter.CTkButton(self.toolbar, text="save", corner_radius=0, command = self.master.save_note)
        self.toolbar.btn_save_note.grid(row=0, column=1, sticky="nsew")
        
        self.toolbar.btn_export = customtkinter.CTkButton(self.toolbar, text="export", corner_radius=0, command = self.ia_export)
        self.toolbar.btn_export.grid(row=0, column=2, sticky="nsew")
                 
        self.editor = customtkinter.CTkTextbox(self, corner_radius=0)
        self.editor.grid(row=1, column=0, sticky="nsew")
                
        self.ia_output = customtkinter.CTkTextbox(self, corner_radius=0, height=250)
        self.ia_output.grid(row=2, column=0, sticky="nsew")
        
    def ia_export(self):
        self.ia_output.get("0.0", "end")
        export_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if export_file:
            with open(export_file, "w", encoding="utf-8") as f:
                f.write(self.ia_output.get("0.0", "end"))

class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.db = Gestore_DB()
        self.current_note_id = None
        
        self.geometry("1600x900")
        self.state("zoomed")
        self.title("NoteWork")
        self.grid_columnconfigure(0, weight=0, minsize=170)
        self.grid_columnconfigure(1, weight=3, minsize=850)
        self.grid_columnconfigure(2, weight=1, minsize=80)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar_left = LeftSidebar(self)
        self.sidebar_left.grid(row=0, column=0, sticky="nsew")
        
        self.sidebar_right = RightSidebar(self)
        self.sidebar_right.grid(row=0, column=2, sticky="nsew")
        
        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        
    def show_note(self, note_id):
        self.current_note_id = note_id
        note = self.db.get_note_by_id(note_id)
        self.main_frame.toolbar.title.delete(0, "end")
        self.main_frame.toolbar.title.insert(0, note[1])
        self.main_frame.editor.delete("0.0", "end")
        self.main_frame.editor.insert("0.0", note[2])
        self.main_frame.ia_output.delete("0.0", "end")
        
    def save_note(self):
        if self.current_note_id is not None:
            title = self.main_frame.toolbar.title.get()
            content = self.main_frame.editor.get("0.0", "end-1c")
            
            import datetime
            last_modified_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            self.db.update_note(self.current_note_id, title, content, last_modified_at)
            self.sidebar_left.all_note()
    
    def on_closing(self):
        self.destroy()
        
root = Root()
root.mainloop()