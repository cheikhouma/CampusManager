import tkinter as tk
from tkinter import ttk
import ajout_etudiant  # Importer le fichier ajout_etudiant

def open_add_student_page():
    ajout_etudiant.open_add_student_window(root, tree)

def calculate_paid_months(months):
    total_months = len(months)
    paid_months = sum(months.values())
    return f"{paid_months}/{total_months}"

def extract_paid_months(student):
    # Extrait le nombre total de mois payés
    months = student[9]  # La colonne des paiements est maintenant la 9ème
    return sum(months.values())

def sort_by(column):
    global sort_column, sort_order

    if sort_column == column:
        sort_order = "desc" if sort_order == "asc" else "asc"
    else:
        sort_column = column
        sort_order = "asc"

    reverse = (sort_order == "desc")

    if column == 9:  # Index de la colonne "Loyer"
        # Trier en utilisant le nombre total de mois payés
        sorted_items = sorted(students, key=extract_paid_months, reverse=reverse)
    else:
        # Trier normalement pour les autres colonnes
        sorted_items = sorted(students, key=lambda x: x[column], reverse=reverse)

    update_treeview(sorted_items)


def update_treeview(data):
    # Effacer les éléments existants
    for item in tree.get_children():
        tree.delete(item)

    # Insérer les données dans la Treeview avec des couleurs alternées
    for index, student in enumerate(data):
        loyer = calculate_paid_months(student[9])  # Calcul du loyer
        if index % 2 == 0:
            tree.insert("", tk.END, iid=student[0], values=(*student[:9], loyer), tags=("even_row",))
        else:
            tree.insert("", tk.END, iid=student[0], values=(*student[:9], loyer), tags=("odd_row",))

    # Appliquer un style pour les lignes alternées
    tree.tag_configure("even_row", background="#e0e0e0")  # Gris clair pour les lignes paires
    tree.tag_configure("odd_row", background="#ffffff")  # Blanc pour les lignes impaires


def search_data(search_term):
    search_term = search_term.lower()
    filtered_data = [item for item in students if any(search_term in str(value).lower() for value in item)]
    update_treeview(filtered_data)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestionnaire des étudaints du Campus")
root.state('zoomed')

# Style personnalisé
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=('Arial', 12))
style.configure('TButton', font=('Arial', 13, 'bold'), background='#007ACC', foreground='white')
style.configure('Treeview', font=('Arial', 13))
style.configure('Treeview.Heading', font=('Arial', 13))

# Création de la barre de menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu "Fichier"
fichier_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Fichier", menu=fichier_menu)
fichier_menu.add_command(label="Nouveau")
fichier_menu.add_command(label="Ouvrir")
fichier_menu.add_separator()
fichier_menu.add_command(label="Quitter", command=root.quit)

# Menu "Ajouter"
nouveau_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ajouter", menu=nouveau_menu)
nouveau_menu.add_command(label="Ajouter un étudiant", command=open_add_student_page)

# Menu "Options"
options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Préférences")

# Menu "Aide"
aide_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Aide", menu=aide_menu)
aide_menu.add_command(label="À propos")

# Cadre principal
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill='both', expand=True)

# Titre de la page
title_label = ttk.Label(main_frame, text="Liste des Étudiants", font=('Arial', 30, 'bold'))
title_label.pack(pady=10)

# Cadre pour la barre de recherche
search_frame = ttk.Frame(main_frame)
search_frame.pack(pady=10, fill='x')

# Barre de recherche
search_var = tk.StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var, font=('Arial', 16, 'bold'))
search_button = ttk.Button(search_frame, cursor=None, takefocus=None, text="Rechercher",
                           command=lambda: search_data(search_var.get()))

# Disposition centrée
search_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
search_button.grid(row=0, column=1, padx=5, pady=5)

# Assurer que la barre de recherche prend toute la largeur disponible
search_frame.columnconfigure(0, weight=1)
search_frame.rowconfigure(0, weight=1)

# Cadre pour la liste des étudiants
tree_frame = ttk.Frame(main_frame)
tree_frame.pack(pady=20, fill='both', expand=True)

# Création de la Treeview
columns = ("Identifiant", "Nom", "Prénom", "Sexe", "Date de Naissance", "Téléphone", "Adresse", "Bâtiment", "Chambre", "Loyer")

tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
tree.pack(side='left', fill='both', expand=True)

# Fonction pour la gestion du tri
def on_heading_click(cols):
    sort_by(columns.index(cols))

# Définir les colonnes avec en-têtes cliquables
for col in columns:
    tree.heading(col, text=col, command=lambda c=col: on_heading_click(c))
    tree.column(col, anchor=tk.W, width=150)

# Exemple de données
students = [
    ["1", "Dupont", "Jean", "Masculin", "01-01-2000", "0601020304", "123 Rue de Paris", "H1", "101",
     {"Janvier": True, "Fevrier": True, "Mars": True, "Avril": True, "Mai": True, "Juin": True, "Juillet": True,
      "Aout": True, "Septembre": True, "Octobre": True, "Novembre": True, "Decembre": True}],
    ["2", "Martin", "Claire", "Féminin", "15-05-1999", "0611223344", "456 Avenue des Champs", "H2", "202",
     {"Janvier": True, "Fevrier": False, "Mars": False, "Avril": True, "Mai": True, "Juin": True, "Juillet": False,
      "Aout": False, "Septembre": False, "Octobre": True, "Novembre": False, "Decembre": True}],
    ["3", "Durand", "Paul", "Masculin", "22-11-1998", "0622334455", "789 Boulevard du Mont", "H1", "303",
     {"Janvier": True, "Fevrier": False, "Mars": True, "Avril": False, "Mai": True, "Juin": False, "Juillet": False,
      "Aout": True, "Septembre": False, "Octobre": False, "Novembre": False, "Decembre": True}]
]

# Initialiser l'ordre de tri
sort_column = 0
sort_order = "asc"

# Afficher les données initiales
update_treeview(students)

# Associer l'événement de double-clic
tree.bind("<Double-1>", on_tree_double_click)

# Gestion de la fermeture de l'application
root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

root.mainloop()


