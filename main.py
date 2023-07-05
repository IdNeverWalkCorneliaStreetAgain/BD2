from tkinter import *
from tkinter.ttk import *
import pymongo.cursor
from QueryDb import *
from load_db import checkInizializza
from dataCleaning import mydataCleaning

queries = ["Inserisci un Libro", "Modifica un Libro", "Rimuovi un Libro",
           "Inserisci un Rating", "Modifica un Rating", "Rimuovi un Rating",
           "Inserisci un Utente", "Modifica un Utente", "Rimuovi un Utente",
           "Mostra i libri pubblicati un determinato anno",
           "Dettagli essenziali di un libro + rating medio",
           "Libri di una casa editrice che hanno un rating superiore a uno specifico",
           "Mostra gli utenti con meno di 30 anni che abitano in una specifica città",
           "Utenti che hanno assegnato a un libro un punteggio superiore a quanto dato in input"]

class Window(Tk):

    def __init__(self):
        super().__init__()
        # Importo il file sun-valley.tcl per usare il tema
        self.tk.call("source", "./Sun-Valley-ttk-theme-master/sun-valley.tcl")
        # Setto il tema preferito
        self.tk.call("set_theme", "dark")
        self.configure(background='#8fbc8f')
        self.geometry('1250x750')
        self.title('Libreria')
        self.iconbitmap("library.ico")

        # Stile per i widgets: 'label error' e 'label not found'
        styleError = Style()
        styleError.configure("Error.Message.TLabel", foreground="red", background="#fff")
        correctStyle = Style()
        correctStyle.configure("BW.TLabel", foreground="green", background="#fff")

        # Menubutton
        self.menu_button = Menubutton(self, text='Scegli un operazione', width=100)
        self.selected_query = IntVar()
        self.selected_query.trace("w", self.menu_item_selected)
        self.create_menu_button()

        # Frames
        self.inputFrame = Frame(self, relief=GROOVE, borderwidth=1)
        self.outputFrame = Frame(self, width=900, height=600, relief=GROOVE, borderwidth=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.outputFrame.rowconfigure(0, weight=1)
        self.outputFrame.columnconfigure(0, weight=1)

        # Creo widgets e variables per l'area di input
        self.labelsAndEntries = {}
        self.radioVar = StringVar()
        self.radioMedal = StringVar()
        self.createLabelsAndEntries()
        self.labelError = Label(self, text="", style="BW.TLabel")
        self.subtmitbtn = Button(self, text="Esegui", command=self.callQuery)

        # Creo widgets e variables per l'area di output
        self.tree = Treeview(self.outputFrame)
        self.labelNotFound = Label(self.outputFrame, text="")
        self.canvas = None

    def checkInput(self, key):
        #Verifico che l'input sia nel formato corretto. Se no, restituisco None
        self.focus
        entry = self.labelsAndEntries[key][1]
        inputField = None
        inputField = entry.get()

        if key == "AnnoPubblicazione" or key == "Eta" or key == "Rating" or key == "ID":  # check on integers
                try:
                    inputField = int(inputField)
                except:
                    return None
        elif key == "isbn":
                if len(inputField) != 10:
                    inputField = None
                else:
                      inputField = entry.get()
        elif key == "ID":
                if len(inputField) > 6:
                    inputField = None
                else:
                      inputField = entry.get()            
        else:  # verifica sulle stringhe
                if inputField is None:
                    return None
                special_characters = "\"!@#$%^&*()+?_=<>/\""
                if any(c in special_characters for c in inputField):# verifica sui caratteri speciali
                    inputField = None
                elif all(c in " " for c in inputField): # stringhe con spazi bianchi
                    inputField = None
        
        return inputField

    def callQuery(self):
        #Prendo l'input dal form e invio la query al db
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.pack_forget()
        errorText = update_op = ""
        val = int(self.selected_query.get())
        res = None
        numQuery = 0

        if val == 0:
            # Inserimento libro
            isbn = self.checkInput("isbn")
            titolo = self.checkInput("Titolo")
            autore= self.checkInput("Autore")
            year = self.checkInput("AnnoPubblicazione")
            publisher = self.checkInput("Editore")
            category = self.checkInput("Categoria")            
            if isbn is None:
                errorText = "Inserisci un ISBN valido"
            elif titolo is None:
                errorText = "Inserisci un Titolo valido"
            elif autore is None:
                errorText = "Inserisci un Autore valido"
            elif year is None:
                errorText = "Inserisci un Anno di Pubblicazione valido"
            elif publisher is None:
                errorText = "Inserisci un Editore valido"
            elif category is None:
                errorText = "Inserisci una Categoria valida"
            else:
                book = {"isbn": isbn, "titolo": titolo, "autore":autore, "year": year, "publisher": publisher, "category": category}
                res = insertBook(book)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Inserimento completato."
            
        elif val == 1:
            # Modifica libro
            isbn = self.checkInput("isbn")
            titolo = self.checkInput("Titolo")
            autore= self.checkInput("Autore")
            year = self.checkInput("AnnoPubblicazione")
            publisher = self.checkInput("Editore")
            category = self.checkInput("Categoria")            
            if isbn is None:
                errorText = "Inserisci un ISBN valido"
            elif titolo is None:
                errorText = "Inserisci un Titolo valido"
            elif autore is None:
                errorText = "Inserisci un Autore valido"
            elif year is None:
                errorText = "Inserisci un Anno di Pubblicazione valido"
            elif publisher is None:
                errorText = "Inserisci un Editore valido"
            elif category is None:
                errorText = "Inserisci una Categoria valida"
            else:
                book = {"isbn": isbn, "titolo": titolo, "autore":autore, "year": year, "publisher": publisher, "category": category}
                res = updateBook(book)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Modifica completata."
        
        elif val == 2:
            #Elimina libro
            isbnBook = self.checkInput("isbn")
            if isbnBook is None:
                errorText = "Inserisci un Isbn corretto - L'Isbn deve essere numerico"
            elif checkBook(isbnBook) is None:
                errorText = "Inserisci un Isbn corretto - Isbn non presente nel db"
            else:
                res = deleteBook(isbnBook)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Cancellazione completata."

        elif val == 3:
            # Inserimento rating
            user_id = self.checkInput("ID")
            isbn = self.checkInput("isbn")
            rating= self.checkInput("Rating")            
            if user_id is None:
                errorText = "Inserisci un User ID valido"
            elif isbn is None:
                errorText = "Inserisci un Isbn valido"
            elif rating is None:
                errorText = "Inserisci un Rating valido"
            else:
                rating = {"user_id": user_id, "isbn": isbn, "rating":rating}
                res = insertRating(rating)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Inserimento completato."

        elif val == 4:
            # Modifica rating
            user_id = self.checkInput("ID")
            isbn = self.checkInput("isbn")
            rating= self.checkInput("Rating")            
            if user_id is None:
                errorText = "Inserisci un User ID valido"
            elif isbn is None:
                errorText = "Inserisci un Isbn valido"
            elif rating is None:
                errorText = "Inserisci un Rating valido"
            else:
                rating = {"user_id": user_id, "isbn": isbn, "rating":rating}
                res = updateRating(rating)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Modifica completata."

        elif val == 5:
            #Elimina rating
            user_id = self.checkInput("ID")
            isbn = self.checkInput("isbn")

            if user_id is None and isbn is None:
                errorText = "Inserisci un User ID valido"
                errorText = "Inserisci un Isbn valido"
            elif checkUserRating(user_id) is None and checkIsbnRating(isbn) is None:
                errorText = "Inserisci un ID corretto - ID non presente nel db"
                errorText = "Inserisci un Isbn corretto - Isbn non presente nel db"
            elif checkIsbnRating(isbn) is None:
                res = deleteRatingUtente(user_id)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Cancellazione completata."
            elif checkUserRating(user_id) is  None:
                res = deleteRatingIsbn(isbn)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Cancellazione completata."
            else:
                res = deleteRatingIsbnEUtente(user_id,isbn)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Cancellazione completata."          
        
        elif val == 6:
            # Inserimento utente
            id_utente = self.checkInput("ID")
            eta = self.checkInput("Età")
            citta= self.checkInput("Città")
            nazione = self.checkInput("Nazione")
            stato = self.checkInput("Stato")           
            if id_utente is None:
                errorText = "Inserisci un User ID valido"
            elif eta is None:
                errorText = "Inserisci un Eta valida"
            elif citta is None:
                errorText = "Inserisci una Citta valida"
            elif nazione is None:
                errorText = "Inserisci una Nazione valida"
            elif stato is None:
                errorText = "Inserisci uno Stato valido"
            else:
                user = {"user_id": id_utente, "eta": eta, "citta":citta, "nazione": nazione, "stato": stato}
                res = insertUser(user)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Inserimento completato."
        
        elif val == 7:
            # Modifica utente
            id_utente = self.checkInput("ID")
            eta = self.checkInput("Età")
            citta= self.checkInput("Città")
            nazione = self.checkInput("Nazione")
            stato = self.checkInput("Stato")           
            if id_utente is None:
                errorText = "Inserisci un User ID valido"
            elif eta is None:
                errorText = "Inserisci un Eta valida"
            elif citta is None:
                errorText = "Inserisci una Citta valida"
            elif nazione is None:
                errorText = "Inserisci una Nazione valida"
            elif stato is None:
                errorText = "Inserisci uno Stato valido"
            else:
                user = {"user_id": id_utente, "eta": eta, "citta":citta, "nazione": nazione, "stato": stato}
                res = updateUser(user)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Modifica completata."

        elif val == 8:
            #Elimina utente
            idUser = self.checkInput("ID")
            if idUser is None:
                errorText = "Inserisci un ID corretto - L'ID deve essere numerico"
            elif checkUser(idUser) is None:
                errorText = "Inserisci un ID corretto - ID non presente nel db"
            else:
                res = deleteUser(idUser)
                if res is None:
                    errorText = "Operazione fallita. Riprova."
                else:
                    update_op = "Cancellazione completata."

        elif val == 9:
           #Libri pubblicati lo stesso anno
            anno = self.checkInput("AnnoPubblicazione")
            if anno is not None:
                res, numQuery = query1(anno)
            else:
                errorText = "Inserisci un anno valido"
                
        elif val == 10:
            #Libro + rating medio
            libro = self.checkInput("isbn")
            if libro is not None:
                res, numQuery = query2(libro)
            else:
                errorText = "Inserisci un ISBN valido"
                
        elif val == 11:
            #Libri di un certo publisher con punteggio superiore a uno dato in input
            editore = self.checkInput("Editore")
            punteggio = self.checkInput("Rating")
            if punteggio is None:
                errorText = "Inserisci un rating valido"
            if editore is None:
                errorText = "Inserisci un editore valido"
            else:
                res, numQuery = query3(editore, punteggio)
                
        elif val == 12:
            #Utenti con meno di 30 anni che abitano in una data città
            città = self.checkInput("Città")
            if città is not None:
                res, numQuery = query4(città)
            else:
                errorText = "Inserisci una città valida"
                
        elif val == 13:
            #Utenti che hanno assegnato un punteggio superiore rispetto a quello in input 
            #ad uno specifico libro
            isbn = self.checkInput("isbn")
            punteggio = self.checkInput("Rating")
            if punteggio is None:
                errorText = "Inserisci un rating valido"
            if isbn is None:
                errorText = "Inserisci un ISBN valido"
            else:
                res, numQuery = query5(isbn, punteggio)

        if errorText != "":
            self.labelError.config(text=errorText, style="Error.Message.TLabel")
            self.labelError.grid(row=3, column=0, padx=1, pady=4)
        elif update_op != "":
            self.labelError.config(text=update_op, style="BW.TLabel")
            self.labelError.grid(row=3, column=0, padx=1, pady=4)
        else:
            self.labelError.grid_remove()
            if res is not None and numQuery != 0:
                self.showResults(res, numQuery)

    def createLabelsAndEntries(self):
        # Creo widgets e un dizionario per raggrupparli
        
        # BOOK
        labelIsbn = Label(self.inputFrame, text="Isbn")
        labelTitolo = Label(self.inputFrame, text="Titolo")
        labelAutore = Label(self.inputFrame, text="Autore")
        labelAnno = Label(self.inputFrame, text="AnnoPubblicazione")
        labelEditore = Label(self.inputFrame, text="Editore")
        labelCategoria = Label(self.inputFrame, text="Categoria")
        
        entryIsbn = Entry(self.inputFrame)
        entryTitolo = Entry(self.inputFrame)
        entryAutore = Entry(self.inputFrame)
        entryAnno = Entry(self.inputFrame)
        entryEditore = Entry(self.inputFrame)
        entryCategoria = Entry(self.inputFrame)

        # UTENTE
        labelIDUtente = Label(self.inputFrame, text="ID")
        labelEta = Label(self.inputFrame, text="Età")
        labelCitta = Label(self.inputFrame, text="Città")
        labelNazione = Label(self.inputFrame, text="Nazione")
        labelStato = Label(self.inputFrame, text="Stato")

        entryIDUtente = Entry(self.inputFrame)
        entryEta = Entry(self.inputFrame)
        entryCitta = Entry(self.inputFrame)
        entryNazione = Entry(self.inputFrame)
        entryStato = Entry(self.inputFrame)

        # RATING
        labelRating = Label(self.inputFrame, text="Rating")
  
        entryRating = Entry(self.inputFrame)
        
        self.labelsAndEntries = {"isbn": [labelIsbn, entryIsbn], "Titolo": [labelTitolo, entryTitolo],
                                 "Autore": [labelAutore, entryAutore], "AnnoPubblicazione": [labelAnno, entryAnno],
                                 "Editore": [labelEditore, entryEditore], "Categoria": [labelCategoria, entryCategoria],
                                 "ID": [labelIDUtente, entryIDUtente], "Età": [labelEta, entryEta],
                                 "Città": [labelCitta, entryCitta], "Nazione": [labelNazione, entryNazione],
                                 "Stato": [labelStato,entryStato], "Rating": [labelRating, entryRating]}
    
    def showFields(self, key, riga):
        # Dispongo labels e entries nell'input frame
        label = self.labelsAndEntries[key][0]
        entry = self.labelsAndEntries[key][1]

        label.grid(row=riga, column=0, padx=2, pady=2)
        entry.grid(row=riga, column=1, padx=2, pady=2)
        entry.focus_set() # focus sulla prima entry nel form
        self.subtmitbtn.grid(row=2, column=0, pady=5)
        self.bind('<Return>', lambda event: self.callQuery()) # Press enter key to execute query

    def hideFields(self):
       # Nascondo i fields già creati per rimpiazzarli con i nuovi
        for item in self.labelsAndEntries.values():     
            item[0].grid_remove()
            item[1].grid_remove()
        self.labelError.grid_remove()
        self.labelNotFound.pack_forget()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.pack_forget()
        if self.canvas is not None:
            self.canvas.get_tk_widget().pack_forget()
            self.outputFrame.grid_remove()

    def menu_item_selected(self, *args):
        # menu selected event 
        self.inputFrame.grid(row=1, column=0, padx=10, pady=10)
        val = int(self.selected_query.get())
        self.menu_button.config(text=queries[val])
        self.hideFields()
        if val == 0 or val == 1:
            self.showFields("isbn", 0)
            self.showFields("Titolo", 1)
            self.showFields("Autore", 2)
            self.showFields("AnnoPubblicazione", 3)
            self.showFields("Editore", 4)
            self.showFields("Categoria", 5)
        elif val == 2 or val == 10:
            self.showFields("isbn", 0)
        elif val == 3 or val == 4:
            self.showFields("ID", 0)
            self.showFields("isbn", 1)
            self.showFields("Rating", 2)   
        elif val == 5:
            self.showFields("ID", 0)
            self.showFields("isbn", 1)
        elif val == 6 or val == 7:
            self.showFields("ID", 0)
            self.showFields("Età", 1)
            self.showFields("Città", 2)
            self.showFields("Nazione", 3)
            self.showFields("Stato", 4)
        elif val == 8:
            self.showFields("ID", 0)
        elif val == 9:
            self.showFields("AnnoPubblicazione", 0)
        elif val == 11:
            self.showFields("Editore", 0)
            self.showFields("Rating", 1)
        elif val == 12:
            self.showFields("Città", 0)
        elif val == 13:
            self.showFields("isbn", 0)
            self.showFields("Rating", 1)
   
    def showResults(self, results, numQuery):
        # Dispongo i widgets nell'area di output
        self.labelNotFound.pack_forget()
        self.outputFrame.grid(row=4, columnspan=4, padx=10, pady=10, sticky=E+W+N+S)
        # Verifico la lunghezza dei risultati: se 0, label for no result
        if (type(results) is list and len(results) == 0) or (type(results) is dict and len(results.keys())==0):
            self.labelNotFound.config(text="Nessun risultato trovato")
            self.labelNotFound.pack(fill="both", expand=True)
        else:
            cols = list(results[0].keys())
            cols = tuple(cols)
            self.tree.config(col=cols, show="headings")
            for col in cols:
                self.tree.heading(col, text=col)
                minWidth = 0
                if col == "Età" or col == "Rating" or col == "ID":
                    width = 50
                elif col == "AnnoPubblicazione" or col == "Categoria" or col == "Città" or col == "Nazione" or col == "Stato":
                    width = 100
                else:
                    width = 150
                self.tree.column(col, minwidth=minWidth, width=width)
                
            for result in results:
                myValues = []
                for col in cols:
                    myValues.append(result[col])
                self.tree.insert("", "end", values=tuple(myValues))
            self.tree.pack(fill="both", expand=True) # Show results

    def create_menu_button(self):
        # menu per la selezione delle query
        menu = Menu(self.menu_button, tearoff=False)
        # Numero elementi MENU
        numbers = [x for x in range(0, 14)]  # indexes for queries
        for number in numbers:
            menu.add_radiobutton(
                label=str(number + 1) + ". " + queries[number],
                value=number,
                variable=self.selected_query)
        # Associo menu con Menubutton
        self.menu_button["menu"] = menu
        self.menu_button.grid(row=0, column=0, padx=10, pady=10)

if __name__ == "__main__":
    #mydataCleaning()
    #checkInizializza()
    window = Window()
    window.mainloop()
