import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import database

# Fonction pour ouvrir la fenêtre d'ajout/modification d'étudiant
def open_add_student_window(parent, treeview, student_id=None):

    # Récupérer les données de l'étudiant à partir de la base de données en utilisant l'identifiant
    student_data = database.get_student_by_id(student_id) if student_id else None

    from datetime import datetime

        # Fonction pour ajouter un zéro devant jour/mois si nécessaire
    def format_date_naissance(event=None):
        try:
            # Récupérer la date entrée
            date_naissance = date_naissance_entry.get()

            # Convertir la date en objet datetime
            parsed_date = datetime.strptime(date_naissance, "%d-%m-%Y")

            # Reformater la date en ajoutant des zéros si besoin
            formatted_date = parsed_date.strftime("%d-%m-%Y")
            
            # Mettre à jour le champ avec la date correctement formatée
            date_naissance_entry.delete(0, tk.END)
            date_naissance_entry.insert(0, formatted_date)

        except ValueError:
            # Si la date n'est pas valide, ne rien faire ou afficher un message
            messagebox.showerror("Erreur", "La date de naissance est invalide.")

    # Lier l'événement à la fonction pour formater la date lorsqu'elle est changée
    

    def validate_fields():
        if not nom_entry.get().strip():
            messagebox.showerror("Erreur", "Le nom est requis.")
            return False
        if not prenom_entry.get().strip():
            messagebox.showerror("Erreur", "Le prénom est requis.")
            return False
        if sexe_combobox.get() not in ["M", "F"]:
            messagebox.showerror("Erreur", "Veuillez sélectionner un genre.")
            return False
        format_date_naissance()
        if not telephone_entry.get().isdigit() or len(telephone_entry.get()) != 9:
            messagebox.showerror("Erreur", "Le téléphone doit être un numéro valide de 9 chiffres.")
            return False
        if not any(var.get() for var in paiement_vars.values()):
            messagebox.showerror("Erreur", "Veuillez sélectionner au moins un mois de paiement.")
            return False
        return True


    def submit_form():
        if not validate_fields():
            add_student_window.destroy()
        mois_coches = [mois_nom for mois_nom, var in paiement_vars.items() if var.get()]

        mois = student_data['location'] if student_data else {mois: False for mois in paiement_vars.keys()}
        
        # Mettre à jour le dictionnaire des paiements
        for month in mois.keys():
            mois[month] = month in mois_coches
        mois_lowercase = {month.lower(): status for month, status in mois.items()}

        data = {
            "id_etudiant": student_data['id_etudiant'] if student_data else None,
            "prenom": prenom_entry.get(),
            "nom": nom_entry.get(),
            "genre": sexe_combobox.get(),
            "date_naissance": date_naissance_entry.get(),
            "addresse": adresse_entry.get(),
            "telephone": telephone_entry.get(),
            "batiment": batiment_entry.get(),
            "chambre": numero_chambre_entry.get(),
            "location": mois
        }

        # Sauvegarde dans la base de données
        database.save_student_to_db(data)

        # Fermer la fenêtre après la soumission
        add_student_window.destroy()


    # Création de la fenêtre d'ajout/modification
    add_student_window = tk.Toplevel(parent)
    add_student_window.title("Modifier un Étudiant" if student_data else "Ajouter un Étudiant")
    add_student_window.geometry("500x800")

    # Configuration de style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TEntry', font=('Arial', 13))
    style.configure('TButton', font=('Arial', 12), background='#007ACC', foreground='white')
    style.configure("Custom.TCheckbutton", font=("Arial", 14))  


    # Cadre principal
    main_frame = ttk.Frame(add_student_window, padding="20")
    main_frame.pack(fill='both', expand=True)

    # Cadre pour le formulaire
    form_frame = ttk.LabelFrame(main_frame, text="Formulaire d'inscription", padding="10")
    form_frame.pack(pady=20, fill='x')

    # Fonction pour créer les champs du formulaire
    def create_form_row(frame, text, row, widget, **kwargs):
        label = ttk.Label(frame, text=text)
        label.grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        entry = widget(frame, **kwargs, font=('Arial', 13, ))
        entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.EW)
        return entry

    # Champs du formulaire
    nom_entry = create_form_row(form_frame, "Nom", 0, ttk.Entry)
    prenom_entry = create_form_row(form_frame, "Prénom", 1, ttk.Entry)
    sexe_combobox = create_form_row(form_frame, "Sexe", 2, ttk.Combobox, values=["M", "F"], state="readonly")
    date_naissance_entry = create_form_row(form_frame, "Date de Naissance", 3, DateEntry, date_pattern="dd-mm-yyyy", width=19)
    adresse_entry = create_form_row(form_frame, "Adresse", 4, ttk.Entry)
    telephone_entry = create_form_row(form_frame, "Téléphone", 5, ttk.Entry)

    # Cadre pour les informations sur la chambre
    chambre_frame = ttk.LabelFrame(main_frame, text="Informations sur la Chambre", padding="10")
    chambre_frame.pack(padx=20, pady=10, fill='x')
    batiment_entry = create_form_row(chambre_frame, "Bâtiment", 0, ttk.Combobox, state='readonly', values=["H1", "H2", "H3", "H4", "H5"])
    numero_chambre_entry = create_form_row(chambre_frame, "Numéro de Chambre", 1, ttk.Entry)

    # Cadre pour les paiements
    paiement_frame = ttk.LabelFrame(main_frame, text="Paiements du Loyer", padding="10")
    paiement_frame.pack(padx=20, pady=10, fill='x')

    # Initialisation des mois (ici on utilise une liste de mois pour l'exemple)
    mois_noms = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 
                 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']

    # Si l'étudiant est nouveau, on initialise avec tous les mois à False
    if student_data:
        mois = student_data['location']  # Récupérer les paiements existants
    else:
        mois = {mois: False for mois in mois_noms}  # Initialisation pour un nouvel étudiant
    # Nombre de colonnes pour la grille
    columns = 3
    paiement_vars = {}

    # Fonction pour mettre à jour le dictionnaire
    def update_dict(nom, var):
        mois[nom] = var.get()  # Met à jour la valeur dans le dictionnaire

    # Création des cases à cocher
    for idx, mois_nom in enumerate(mois.keys()):
        var = tk.BooleanVar(value=mois[mois_nom])  # Initialise avec la valeur du dictionnaire
        cb = ttk.Checkbutton(paiement_frame, text=mois_nom, style="Custom.TCheckbutton", variable=var, command=lambda nom=mois_nom: update_dict(nom, var))
        cb.grid(row=idx // columns, column=idx % columns, padx=10, pady=5, sticky=tk.W)
        paiement_vars[mois_nom] = var
    # Préremplissage des champs si un étudiant est sélectionné
    if student_data:
        # Assuming student_data is a dictionary like the one you provided
        nom_entry.insert(0, student_data['nom'])
        prenom_entry.insert(0, student_data['prenom'])
        sexe_combobox.set(student_data['genre'])
        date_naissance_entry.set_date(student_data['date_naissance'])
        adresse_entry.insert(0, student_data['addresse'])
        telephone_entry.insert(0, student_data['telephone'])
        batiment_entry.set(student_data['batiment'])
        numero_chambre_entry.insert(0, student_data['chambre'])

        # Load the payment data
        for mois_nom, var in paiement_vars.items():
            var.set(student_data['location'].get(mois_nom, False))
    
    # Bouton pour soumettre le formulaire
    submit_btn = ttk.Button(main_frame, text="Valider", command=submit_form)
    submit_btn.pack(pady=20)
    # S'assurer que la fenêtre se ferme proprement
    return add_student_window
     