import customtkinter
import threading

from src.controllers.AIAssistant import AIAssistant
from tkinter import filedialog, TclError
from src.database.db import Gestore_DB
from tkinter import messagebox

assistant = AIAssistant('llama3.2')

class LeftSidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        # super().__init__ chiama il costruttore della classe padre (CTkFrame)
        # Qui passiamo le configurazioni che prima erano in Root
        super().__init__(master, corner_radius=0, width=170)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        
        self.lbl_title = customtkinter.CTkLabel(self, text="Note", corner_radius=0, font=customtkinter.CTkFont(size=16, weight="bold", family="Arial"), text_color="white")
        self.lbl_title.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")
        
        self.btn_new_note = customtkinter.CTkButton(self, text="Nuova nota", corner_radius=0, command = self.new_note)
        self.btn_new_note.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="e")
        
        self.btn_delete_note = customtkinter.CTkButton(self, text="Elimina nota", corner_radius=0, command = self.delete_note)
        self.btn_delete_note.grid(row=1, column=1, padx=(0, 20), pady=5, sticky="e")
        
        self.scrollable_note = customtkinter.CTkScrollableFrame(self)
        
        self.scrollable_note.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.all_note()
        
    def all_note(self):
        for widget in self.scrollable_note.winfo_children():
            widget.destroy()
            
        notes = self.master.db.get_all_notes()
        for note in notes:
            display_title = note[1].strip() if note[1] else ""
            if not display_title:
                display_title = "Nota senza titolo"
                
            label = customtkinter.CTkLabel(
                self.scrollable_note,
                text=display_title,
                fg_color="transparent",
                cursor="hand2",
                corner_radius=0)
            label.pack(pady=5, padx=10, fill="x", anchor="w")
            
            label.bind("<Button-1>", lambda event, note_id=note[0]: self.master.show_note(note_id))
    
    def new_note(self):
        if self.master.is_generating == True:
            return
        else:
            self.master.main_frame.set_ui_state("normal")
            self.master.main_frame.editor.delete("0.0", "end")
            self.master.main_frame.clear_ia_output()
            self.master.main_frame.toolbar.title.delete(0, "end")
            self.master.main_frame.toolbar.title.insert(0, "Nuova nota")
            
            new_id = self.master.db.new_note(title = "Nuova nota", content = "", last_modified_at = "", ia_output = "")
            if new_id:
                self.master.current_note_id = new_id
                
            self.all_note()
        
    def delete_note(self):
        if self.master.is_generating == True:
            return
        else:
            if self.master.current_note_id is not None:
                confirm = messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare la nota?")
                
                if confirm: 
                    self.master.db.delete_note(self.master.current_note_id)
                    self.master.current_note_id = None
                    self.master.main_frame.editor.delete("0.0", "end")
                    self.master.main_frame.clear_ia_output()
                    self.master.main_frame.toolbar.title.delete(0, "end")
                    self.master.main_frame.set_ui_state("disabled")
                    self.all_note()
        
class RightSidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        # super().__init__ chiama il costruttore della classe padre (CTkFrame)
        super().__init__(master, corner_radius=0, width=80)
        
        self.btn_ia_create_prompt = customtkinter.CTkButton(self, text="IA Prompt", corner_radius=0, command=lambda: self.start_process("prompt"))
        self.btn_ia_create_prompt.pack(side="top", fill="x", pady=20, padx=20)
        
        self.btn_ia_create_ticket = customtkinter.CTkButton(self, text="IA Ticket", corner_radius=0, command=lambda: self.start_process("ticket"))
        self.btn_ia_create_ticket.pack(side="top", fill="x", pady=20, padx=20)
        
        self.btn_ia_create_script = customtkinter.CTkButton(self, text="IA Script", corner_radius=0, command=lambda: self.start_process("script"))
        self.btn_ia_create_script.pack(side="top", fill="x", pady=20, padx=20)

    def start_process(self, task_type):
        self.btn_ia_create_prompt.configure(state="disabled")
        self.btn_ia_create_ticket.configure(state="disabled")
        self.btn_ia_create_script.configure(state="disabled")
        
        if task_type == "prompt":
            self.btn_ia_create_prompt.configure(text="⏳ Elaborazione...")
        elif task_type == "ticket":
            self.btn_ia_create_ticket.configure(text="⏳ Elaborazione...")
        elif task_type == "script":
            self.btn_ia_create_script.configure(text="⏳ Elaborazione...")
            
        # Punto 2: Thread impostato come daemon per non bloccare la chiusura dell'app
        threading.Thread(target=self.process_task, args=(task_type,), daemon=True).start()

    def process_task(self, task_type):
        try:
            self.master.is_generating = True
            input_text = self.master.main_frame.editor.get("sel.first", "sel.last")
            
            self.master.after(0, lambda: self.master.main_frame.ia_output.configure(state="normal"))
            self.master.after(0, lambda: self.master.main_frame.ia_output.delete("0.0", "end"))
            
            for chunk in assistant.chat(input_text, task_type=task_type):
                self.master.after(0, lambda c=chunk: self.master.main_frame.ia_output.insert("end", c))
                
        except TclError:
            print("Nessun testo selezionato!")
        except Exception as e:
            print(f"Errore imprevisto: {e}")
        finally:
            # Punto 1: Utilizzo sicuro di after() per ripristinare i widget dal thread secondario
            self.master.after(0, lambda: self.btn_ia_create_prompt.configure(text="IA Prompt", state="normal"))
            self.master.after(0, lambda: self.btn_ia_create_ticket.configure(text="IA Ticket", state="normal"))
            self.master.after(0, lambda: self.btn_ia_create_script.configure(text="IA Script", state="normal"))
            self.master.after(0, lambda: self.master.main_frame.ia_output.configure(state="disabled"))
            self.master.after(0, lambda: setattr(self.master, 'is_generating', False))
            
class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        # super().__init__ chiama il costruttore della classe padre (CTkFrame)
        super().__init__(master, corner_radius=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=30)
        self.grid_rowconfigure(1, weight=3, minsize=400)
        self.grid_rowconfigure(2, weight=1, minsize=250)
        
        self.toolbar = customtkinter.CTkFrame(self, corner_radius=0, height=50)
        self.toolbar.grid(row=0, column=0, sticky="nsew")
        
        self.toolbar.grid_columnconfigure(0, weight=0)
        self.toolbar.grid_columnconfigure(1, weight=0)
        self.toolbar.grid_columnconfigure(2, weight=0)
        
        btn_width = 90
        
        self.toolbar.title = customtkinter.CTkEntry(self.toolbar, corner_radius=0, width=300, state = "disabled")
        self.toolbar.title.grid(row=0, column=0, sticky="nsew", padx=(10,10))
        
        self.toolbar.btn_save_note = customtkinter.CTkButton(self.toolbar, text="salva", width=btn_width, corner_radius=0, state="disabled", command = self.master.save_note)
        self.toolbar.btn_save_note.grid(row=0, column=1, sticky="nsew", padx=5)
        
        self.toolbar.btn_export = customtkinter.CTkButton(self.toolbar, text="esporta", width=btn_width, corner_radius=0, state="disabled", command = self.ia_export)
        self.toolbar.btn_export.grid(row=0, column=2, sticky="nsew", padx=(5,10))
        
        self.editor = customtkinter.CTkTextbox(self, corner_radius=0, state="disabled")
        self.editor.grid(row=1, column=0, sticky="nsew")
                
        self.ia_output = customtkinter.CTkTextbox(self, corner_radius=0, height=250, state="disabled")
        self.ia_output.grid(row=2, column=0, sticky="nsew")
    
    def set_ui_state(self, state):
        self.toolbar.title.configure(state=state)
        self.toolbar.btn_save_note.configure(state=state)
        self.toolbar.btn_export.configure(state=state)
        self.editor.configure(state=state)
        
    def ia_export(self):
        if self.master.is_generating == True:
            return
        else:
            export_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if export_file:
                content = self.ia_output.get("0.0", "end")
                with open(export_file, "w", encoding="utf-8") as f:
                    f.write(content.rstrip("\n"))
            
    def clear_ia_output(self):
        self.ia_output.configure(state="normal")
        self.ia_output.delete("0.0", "end")
        self.ia_output.configure(state="disabled")
        
    def load_ia_output(self, text):
        self.ia_output.configure(state="normal")
        self.ia_output.delete("0.0", "end")
        if text:
            self.ia_output.insert("end", text)
        self.ia_output.configure(state="disabled")

class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.db = Gestore_DB()
        self.current_note_id = None
        self.is_generating = False
        
        self.geometry("1600x900")
        try:
            self.state("zoomed")
        except Exception:
            try:
                self.attributes("-zoomed", True)
            except Exception:
                pass
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
        if self.is_generating == True:
            return
        else:
            self.current_note_id = note_id
            self.main_frame.set_ui_state("normal")
            note = self.db.get_note_by_id(note_id)
            self.main_frame.toolbar.title.delete(0, "end")
            self.main_frame.toolbar.title.insert(0, note[1])
            self.main_frame.editor.delete("0.0", "end")
            self.main_frame.editor.insert("0.0", note[2])
            self.main_frame.load_ia_output(note[5])
        
    def save_note(self):
        if self.is_generating == True:
            return
        else:
            if self.current_note_id is not None:
                title = self.main_frame.toolbar.title.get()
                content = self.main_frame.editor.get("0.0", "end-1c")
                ia_output = self.main_frame.ia_output.get("0.0", "end-1c")
                
                import datetime
                last_modified_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
                self.db.update_note(self.current_note_id, title, content, last_modified_at, ia_output)
                self.sidebar_left.all_note()
    
    def on_closing(self):
        self.destroy()
        
root = Root()
root.mainloop()