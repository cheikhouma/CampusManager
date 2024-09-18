import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox

def open_add_student_window(parent, treeview):
    def generate_student_id():
        import random
        from datetime import datetime
        random_part = random.randint(10000, 99999)
        year_part = datetime.now().year
        return f"{random_part}{year_part}"

    def submit_form():
        # Génération de l'ID unique
        identifiant = generate_student_id()

        # Récupération des données
        data = {
            "Identifiant": identifiant,
            "Nom": nom_entry.get(),
            "Prénom": prenom_entry.get(),
            "Sexe": sexe_combobox.get(),
            "Date de Naissance": date_naissance_entry.get(),
            "Adresse": adresse_entry.get(),
            "Téléphone": telephone_entry.get(),
            "Bâtiment": batiment_entry.get(),
            "Numéro de Chambre": numero_chambre_entry.get(),
            "Paiements": {mois2: var.get() for mois2, var2 in paiement_vars.items()}
        }

        # Affichage des données dans la Treeview
        treeview.insert("", "end", values=(
            identifiant,
            nom_entry.get(),
            prenom_entry.get(),
            sexe_combobox.get(),
            date_naissance_entry.get(),
            adresse_entry.get(),
            telephone_entry.get(),
            batiment_entry.get(),
            numero_chambre_entry.get()
        ))

        # Affichage des données pour vérification
        print("Données soumises :", data)
        messagebox.showinfo("Succès", "Votre nouveau étudiant est ajouté avec succées ont été soumises avec succès.")
        add_student_window.destroy()

    # Création de la fenêtre d'ajout d'étudiant
    add_student_window = tk.Toplevel(parent)
    add_student_window.title("Ajouter un Étudiant")
    add_student_window.geometry("500x800")

    # Style personnalisé
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TEntry', font=('Arial', 13))
    style.configure('TButton', font=('Arial', 12), background='#007ACC', foreground='white')
    style.configure('TCombobox', font=('Arial', 12))
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabelFrame', font=('Arial', 12, 'bold'))

    # Cadre principal
    main_frame = ttk.Frame(add_student_window, padding="20")
    main_frame.pack(fill='both', expand=True)

    # Titre de la section
    title_label = ttk.Label(main_frame, text="Formulaire d'enregistrement", font=('Arial', 16, 'bold'))
    title_label.pack(pady=10)

    # Cadre pour le formulaire
    form_frame = ttk.LabelFrame(main_frame, text="Formulaire d'inscription", padding="10")
    form_frame.pack(pady=20, fill='x')

    # Fonction pour créer les champs du formulaire
    def create_form_row(frame, text, row, widget, **kwargs):
        label = ttk.Label(frame, text=text)
        label.grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        entry = widget(frame, **kwargs)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.EW)
        return entry

    # Champs du formulaire (sans identifiant)
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

    mois = ["Octobre", "Novembre", "Décembre", "Janvier", "Février", "Mars",
            "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre"]

    # Nombre de colonnes pour la grille
    columns = 3
    paiement_vars = {}
    for idx, mois_nom in enumerate(mois):
        var = tk.BooleanVar()
        cb = ttk.Checkbutton(paiement_frame, text=mois_nom, variable=var)
        cb.grid(row=idx // columns, column=idx % columns, padx=10, pady=5, sticky=tk.W)
        paiement_vars[mois_nom] = var

    # Bouton pour soumettre le formulaire
    submit_btn = ttk.Button(main_frame, text="Valider", command=submit_form)
    submit_btn.pack(pady=20)

    # S'assurer que les colonnes s'ajustent correctement
    for i in range(2):
        form_frame.columnconfigure(i, weight=1)
        chambre_frame.columnconfigure(i, weight=1)
        paiement_frame.columnconfigure(i, weight=1)
