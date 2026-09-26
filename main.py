import customtkinter

from src.controllers.AIAssistant import AIAssistant

assistant = AIAssistant('llama3.2')

class LeftSidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        # super().__init__ chiama il costruttore della classe padre (CTkFrame)
        # Qui passiamo le configurazioni che prima erano in Root
        super().__init__(master, corner_radius=0, width=170)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.lbl_title = customtkinter.CTkLabel(self, text="Note", corner_radius=0, font=customtkinter.CTkFont(size=16, weight="bold", family="Arial"), text_color="white")
        self.lbl_title.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")
        
        self.btn_new_note = customtkinter.CTkButton(self, text="Nuova nota", corner_radius=0)
        self.btn_new_note.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="e")
        
class RightSidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        # super().__init__ chiama il costruttore della classe padre (CTkFrame)
        # Qui passiamo le configurazioni che prima erano in Root
        super().__init__(master, corner_radius=0, width=80)
        
        self.btn_ia_create_prompt = customtkinter.CTkButton(self, text="IA Prompt", corner_radius=0)
        self.btn_ia_create_prompt.pack(side="top", fill="x", pady=20, padx=20)
        
        self.btn_ia_create_ticket = customtkinter.CTkButton(self, text="IA Ticket", corner_radius=0)
        self.btn_ia_create_ticket.pack(side="top", fill="x", pady=20, padx=20)
        
        self.btn_ia_create_script = customtkinter.CTkButton(self, text="IA Script", corner_radius=0)
        self.btn_ia_create_script.pack(side="top", fill="x", pady=20, padx=20)

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        # super().__init__ chiama il costruttore della classe padre (CTkFrame)
        # Qui passiamo le configurazioni che prima erano in Root
        super().__init__(master, corner_radius=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=50)
        self.grid_rowconfigure(1, weight=3, minsize=400)
        self.grid_rowconfigure(2, weight=1, minsize=250)
        
        self.toolbar = customtkinter.CTkFrame(self, corner_radius=0, height=50)
        self.toolbar.grid(row=0, column=0, sticky="nsew")
                
        self.editor = customtkinter.CTkTextbox(self, corner_radius=0)
        self.editor.grid(row=1, column=0, sticky="nsew")
                
        self.ia_output = customtkinter.CTkTextbox(self, corner_radius=0, height=250)
        self.ia_output.grid(row=2, column=0, sticky="nsew")

class Root(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
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

root = Root()
root.mainloop()

try:
    while True:
        request = input("Inserisci la domanda: (exit per uscire)\n")
        cleaned_request = request.strip()
        if cleaned_request.lower() == "exit":
            print("Uscita!")
            break
           
        if not cleaned_request: #Filtro stringa vuota
                print("Nessuna domanda fornita")
                continue
        
        print("Inviando la domdanda a Ollama, attendere...\n")
        respons = assistant.chat(request)
        
        print("--- RISPOSTA DELL'IA ---")
        for resp in respons:
            print(resp, end='', flush=True)
        print()
        
except KeyboardInterrupt:
    print("\nProgramma interrotto dall'utente.")