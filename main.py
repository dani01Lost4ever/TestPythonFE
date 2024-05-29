import tkinter as tk
from tkinter import messagebox, ttk
import requests

# Define API endpoints
BASE_URL = "http://localhost:5000"


class EmployeeApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management")

        self.token = None

        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Email:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_email = tk.Entry(self.login_frame)
        self.entry_email.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_password = tk.Entry(self.login_frame, show='*')
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        self.btn_login = tk.Button(self.login_frame, text="Login", command=self.login)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)

        self.main_frame = tk.Frame(root)
        self.create_main_interface()

    def create_main_interface(self):
        # Labels and entry fields for employee details
        tk.Label(self.main_frame, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_nome = tk.Entry(self.main_frame)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.main_frame, text="Cognome:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_cognome = tk.Entry(self.main_frame)
        self.entry_cognome.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.main_frame, text="Data Nascita (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        self.entry_data_nascita = tk.Entry(self.main_frame)
        self.entry_data_nascita.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.main_frame, text="Comune Nascita:").grid(row=3, column=0, padx=10, pady=5)
        self.entry_comune_nascita = tk.Entry(self.main_frame)
        self.entry_comune_nascita.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.main_frame, text="Provincia Nascita:").grid(row=4, column=0, padx=10, pady=5)
        self.entry_provincia_nascita = tk.Entry(self.main_frame)
        self.entry_provincia_nascita.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.main_frame, text="Sesso (M/F):").grid(row=5, column=0, padx=10, pady=5)
        self.entry_sesso = tk.Entry(self.main_frame)
        self.entry_sesso.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self.main_frame, text="Codice Fiscale:").grid(row=6, column=0, padx=10, pady=5)
        self.entry_codice_fiscale = tk.Entry(self.main_frame)
        self.entry_codice_fiscale.grid(row=6, column=1, padx=10, pady=5)

        # Button to insert employee
        self.btn_inserisci = tk.Button(self.main_frame, text="Inserisci Dipendente", command=self.inserisci_dipendente)
        self.btn_inserisci.grid(row=7, column=0, columnspan=2, pady=10)

        # Button to view employees list
        self.btn_visualizza = tk.Button(self.main_frame, text="Visualizza Lista Dipendenti",
                                        command=self.visualizza_lista_dipendenti)
        self.btn_visualizza.grid(row=8, column=0, columnspan=2, pady=10)

        # Listbox to display employees
        self.listbox_dipendenti = tk.Listbox(self.main_frame, width=50)
        self.listbox_dipendenti.grid(row=9, column=0, columnspan=2, pady=10)


        # Button to calculate fiscal code
        tk.Label(self.main_frame, text="Dipendente Id:").grid(row=10, column=0, padx=10, pady=5)
        self.entry_id_dipendente = tk.Entry(self.main_frame)
        self.entry_id_dipendente.grid(row=10, column=1, padx=10, pady=5)

        self.btn_calcola_codice = tk.Button(self.main_frame, text="Calcola Codice Fiscale",
                                            command=self.calcola_codice_fiscale)
        self.btn_calcola_codice.grid(row=13, column=0, columnspan=2, pady=10)

        self.listbox_codici_fiscali = tk.Listbox(self.main_frame, width=50)
        self.listbox_codici_fiscali.grid(row=14, column=0, columnspan=2, pady=10)

    def login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            self.token = response.json().get("token")
            messagebox.showinfo("Success", "Login Successful")
            self.login_frame.pack_forget()
            self.main_frame.pack(pady=20)
        else:
            messagebox.showerror("Error", "Login Failed")

    def inserisci_dipendente(self):
        employee_data = {
            "Nome": self.entry_nome.get(),
            "Cognome": self.entry_cognome.get(),
            "DataNascita": self.entry_data_nascita.get(),
            "ComuneNascita": self.entry_comune_nascita.get(),
            "ProvinciaNascita": self.entry_provincia_nascita.get(),
            "Sesso": self.entry_sesso.get(),
            "CodiceFiscale": self.entry_codice_fiscale.get()
        }
        if self.token:
            headers = {"Authorization": self.token}
            response = requests.post(f"{BASE_URL}/insert_employee", json=employee_data, headers=headers)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Dipendente inserito con successo")
                self.entry_nome.delete(0, tk.END)
                self.entry_cognome.delete(0, tk.END)
                self.entry_data_nascita.delete(0, tk.END)
                self.entry_comune_nascita.delete(0, tk.END)
                self.entry_provincia_nascita.delete(0, tk.END)
                self.entry_sesso.delete(0, tk.END)
                self.entry_codice_fiscale.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Errore nell'inserimento del dipendente")

    def visualizza_lista_dipendenti(self):
        if self.token:
            headers = {"Authorization": self.token}
            response = requests.get(f"{BASE_URL}/search_employee", headers=headers, params={"search_text": ""})
            if response.status_code == 200:
                employees = response.json().get('employees', [])
                self.listbox_dipendenti.delete(0, tk.END)
                for emp in employees:
                    self.listbox_dipendenti.insert(tk.END, f"{emp['id']} --- {emp['Nome']} {emp['Cognome']} - {emp['DataNascita']}")
            else:
                messagebox.showerror("Error", "Errore nel recupero della lista dipendenti")

    def calcola_codice_fiscale(self):
        id = self.entry_id_dipendente.get()
        if self.token:
            headers = {"Authorization": self.token}
            responseCF = requests.get(f"{BASE_URL}/calculate_tax_code_by_id", headers=headers, params={"id": id})
            if responseCF.status_code == 200:
                response = requests.get(f"{BASE_URL}/search_employee", headers=headers, params={"search_text": id})
                employees = response.json().get('employees', [])
                self.listbox_codici_fiscali.delete(0, tk.END)
                found = False
                for emp in employees:
                    codice_fiscale = emp['CodiceFiscale']
                    self.listbox_codici_fiscali.insert(tk.END, f"{emp['Nome']} {emp['Cognome']} - {codice_fiscale}")
                    found = True
                if not found:
                    messagebox.showerror("Error", "Dipendente non trovato")
            else:
                messagebox.showerror("Error", "Errore nel recupero dei dettagli del dipendente")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()