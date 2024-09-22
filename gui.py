import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ajout_etudiant  # Importer le fichier ajout_etudiant
import database  # Assurez-vous d'importer votre module de base de données

def open_add_student_page():

    add_student = ajout_etudiant.open_add_student_window(root, tree)
    add_student.wait_window()
    actualiser()



def actualiser():
    global students
    students = database.get_students_from_db()
    update_treeview(students)
    search_var.set("")  # Vide le champ de recherche


def calculate_paid_months(location):
    total_months = 12  # Il y a 12 mois au total
    paid_months = sum(location.values())  # Compte le nombre de mois payés (True)
    return f"{paid_months}/{total_months}"

def extract_paid_months(student):
    # Extrait le dictionnaire de paiements pour l'étudiant
    return sum(student['location'].values())  # On suppose que 'location' contient les mois payés


def sort_by(column):
    global sort_column, sort_order

    # Déterminer l'ordre de tri
    if sort_column == column:
        sort_order = "desc" if sort_order == "asc" else "asc"
    else:
        sort_column = column
        sort_order = "asc"

    reverse = (sort_order == "desc")

    # Mappage des noms de colonnes vers les clés du dictionnaire
    column_mapping = {
        "Identifiant": "id_etudiant",
        "Nom": "nom",
        "Prénom": "prenom",
        "Sexe": "genre",
        "Date de Naissance": "date_naissance",
        "Adresse": "addresse",
        "Téléphone": "telephone",
        "Bâtiment": "batiment",
        "Chambre": "chambre",
        "Loyer": "location"
    }

    # Vérifier que la colonne demandée existe dans le mapping
    if column not in column_mapping:
        return

    column_key = column_mapping[column]  # Récupérer la clé correspondante

    # Tri spécifique pour la date de naissance
    if column_key == "date_naissance":
        sorted_items = sorted(
            students,
            key=lambda x: tuple(map(int, x['date_naissance'].split('-'))),  # Convertir en tuple (jour, mois, année)
            reverse=reverse
        )
    elif column_key == "location":
        sorted_items = sorted(students, key=lambda x: calculate_paid_months(x['location']), reverse=reverse)
    else:
        # Effectuer le tri avec la clé correspondante
        sorted_items = sorted(students, key=lambda x: str(x.get(column_key, "")), reverse=reverse)

    update_treeview(sorted_items)  # Mettre à jour l'affichage


def update_treeview(data):
    # Effacer les éléments existants
    for item in tree.get_children():
        tree.delete(item)

    # Insérer les données dans la Treeview avec des couleurs alternées
    for index, student in enumerate(data):
        loyer = calculate_paid_months(student['location'])  # Calcul du loyer
        values = (student['id_etudiant'], student['nom'], student['prenom'], student['genre'],
                  student['date_naissance'], student['telephone'], student['addresse'], 
                  student['batiment'], student['chambre'], loyer)
        if index % 2 == 0:
            tree.insert("", tk.END, iid=student['id_etudiant'], values=values, tags=("even_row",))
        else:
            tree.insert("", tk.END, iid=student['id_etudiant'], values=values, tags=("odd_row",))

    # Appliquer un style pour les lignes alternées
    tree.tag_configure("even_row", background="#e0e0e0")
    tree.tag_configure("odd_row", background="#ffffff")

def search_data(search_term):
    search_term = search_term.lower()
    filtered_data = [item for item in students if any(search_term in str(value).lower() for value in item.values())]
    update_treeview(filtered_data)

def get_selected_student():
    # Récupérer l'élément sélectionné
    selected_item = tree.selection()
    
    if selected_item:
        # Récupérer l'ID de l'étudiant sélectionné
        student_id = tree.item(selected_item[0], "values")[0]
        
        # Rechercher l'étudiant correspondant dans la liste "students"
        for student in students:
            if student['id_etudiant'] == int(student_id):
                return student

    return None

def modify_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant à modifier.")
        return

    student_id = selected_item[0]
    add_student = ajout_etudiant.open_add_student_window(root, tree, student_id)
    add_student.wait_window()
    actualiser()


def delete_student():
    # Récupérer l'élément sélectionné dans le Treeview
    selected_item = tree.selection()
    
    if not selected_item:
        messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant à supprimer.")
        return

    # Récupérer l'ID de l'étudiant à partir de la sélection
    student_id = tree.item(selected_item, 'values')[0]  # Supposons que l'ID est dans la première colonne

    # Demander une confirmation avant suppression
    confirmation = messagebox.askyesno("Confirmer la suppression", "Êtes-vous sûr de vouloir supprimer cet étudiant ?")
    
    if confirmation:
        # Appeler la fonction de suppression dans la base de données
        database.delete_student_by_id(student_id)
        
        # Actualiser l'affichage du Treeview après la suppression
        actualiser()

        messagebox.showinfo("Succès", f"L'étudiant avec l'ID {student_id} a été supprimé.")


# Création de la fenêtre principale
root = tk.Tk()
root.title("Gestionnaire des Étudiants du Campus")
root.state('zoomed')

# Style personnalisé
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=('Arial', 12))
style.configure('TButton', font=('Arial', 13, 'bold'), background='#007ACC', foreground='white')
style.configure('Treeview', font=('Arial', 13))
style.configure('Treeview.Heading', font=('Arial', 13))
style.configure("Custom.TCheckbutton", font=("Arial", 14))  # Change font here


# Création de la barre de menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu "Fichier"
fichier_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Fichier", menu=fichier_menu)
fichier_menu.add_command(label="Actualiser", command=actualiser)
fichier_menu.add_separator()
fichier_menu.add_command(label="Quitter", command=root.quit)

# Menu "Ajouter"
etudiant = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Étudiant", menu=etudiant)
etudiant.add_command(label="Ajouter", command=open_add_student_page)
etudiant.add_separator()
etudiant.add_command(label="Modifier", command=modify_student)
etudiant.add_separator()
etudiant.add_command(label="Supprimer", command=delete_student)

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
search_entry = ttk.Entry(search_frame, textvariable=search_var, font=('Arial', 16, ))
search_button = ttk.Button(search_frame, text="Rechercher", command=lambda: search_data(search_var.get()))

# Disposition centrée
search_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
search_button.grid(row=0, column=1, padx=5, pady=5)

# Assurer que la barre de recherche prend toute la largeur disponible
search_frame.columnconfigure(0, weight=1)

# Cadre pour la liste des étudiants
tree_frame = ttk.Frame(main_frame)
tree_frame.pack(pady=20, fill='both', expand=True)

# Création de la Treeview
columns = ("Identifiant", "Nom", "Prénom", "Sexe", "Date de Naissance", "Téléphone", "Adresse", "Bâtiment", "Chambre", "Loyer")

tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
tree.pack(side='left', fill='both', expand=True)

# Fonction pour la gestion du tri
def on_heading_click(col):
    sort_by(col)


# Définir les colonnes avec en-têtes cliquables
for col in columns:
    tree.heading(col, text=col, command=lambda c=col: on_heading_click(c))
    tree.column(col, anchor=tk.W, width=150)

# Exemple de données
students = database.get_students_from_db()

# Initialiser l'ordre de tri
sort_column = 0
sort_order = "asc"

# Afficher les données initiales
update_treeview(students)

# Gestion de la fermeture de l'application
root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

root.mainloop()
