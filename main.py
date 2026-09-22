from src.controllers.AIAssistant import AIAssistant

assistant = AIAssistant('llama3.2')

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