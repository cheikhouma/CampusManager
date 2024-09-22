# # import tkinter as tk
# # from tkinter import ttk

# # # Fenêtre principale
# # add_student_window = tk.Tk()
# # add_student_window.title("Sélection de mois")

# # # Cadre principal
# # main_frame = ttk.Frame(add_student_window, padding="20")
# # main_frame.pack(fill='both', expand=True)

# # # Dictionnaire des mois initialisé à True
# # mois = {
# #     "Janvier": False, "Février": True, "Mars": True, "Avril": True,
# #     "Mai": True, "Juin": False, "Juillet": True, "Août": True,
# #     "Septembre": True, "Octobre": False, "Novembre": True, "Décembre": False
# # }

# # # Nombre de colonnes pour la grille
# # columns = 3
# # paiement_vars = {}

# # # Fonction pour mettre à jour le dictionnaire
# # def update_dict(nom, var):
# #     mois[nom] = var.get()  # Met à jour la valeur dans le dictionnaire

# # # Création des cases à cocher
# # for idx, mois_nom in enumerate(mois.keys()):
# #     var = tk.BooleanVar(value=mois[mois_nom])  # Initialise avec la valeur du dictionnaire
# #     cb = ttk.Checkbutton(main_frame, text=mois_nom, variable=var, command=lambda nom=mois_nom: update_dict(nom, var))
# #     cb.grid(row=idx // columns, column=idx % columns, padx=10, pady=5, sticky=tk.W)
# #     paiement_vars[mois_nom] = var

# # # # Fonction pour soumettre les mois cochés
# # def submit():
# #     mois_coches = [mois_nom for mois_nom, var in paiement_vars.items() if var.get()]
# #     print("Mois sélectionnés :", mois_coches)
    
# #     # Si vous voulez mettre à jour le dictionnaire avec les mois sélectionnés
# #     for month in mois.keys():
# #         mois[month] = month in mois_coches
# #     print(mois)

# # # Bouton pour soumettre le formulaire
# # submit_btn = ttk.Button(main_frame, text="Valider", command=submit)
# # submit_btn.grid(row=(len(mois) // columns) + 1, column=0, columnspan=columns, pady=20)

# # # Lancement de la boucle principale
# # add_student_window.mainloop()


# import database
# import sqlite3
# print(database.get_students_from_db())

# import sqlite3

# def get_student_by_id(student_id):
#     conn = sqlite3.connect('bd_campus_ept.db')  # Assurez-vous que le chemin est correct
#     cursor = conn.cursor()

#     # Requête pour récupérer les données de l'étudiant avec l'identifiant spécifié
#     cursor.execute('''
#         SELECT e.id_etudiant, e.prenom, e.nom, e.genre, e.date_naissance, e.addresse, 
#                e.telephone, e.batiment, e.chambre, 
#                l.janvier, l.fevrier, l.mars, l.avril, l.mai, l.juin, 
#                l.juillet, l.aout, l.septembre, l.octobre, l.novembre, l.decembre
#         FROM etudiant e
#         LEFT JOIN location l ON e.id_etudiant = l.id_etudiant
#         WHERE e.id_etudiant = ?
#     ''', (student_id,))

#     student_data = cursor.fetchone()
#     conn.close()

#     if student_data:
#         return {
#             'id_etudiant': student_data[0],
#             'prenom': student_data[1],
#             'nom': student_data[2],
#             'genre': student_data[3],
#             'date_naissance': student_data[4],
#             'addresse': student_data[5],
#             'telephone': student_data[6],
#             'batiment': student_data[7],
#             'chambre': student_data[8],
#             'location': {
#                 'janvier': bool(student_data[9]),
#                 'fevrier': bool(student_data[10]),
#                 'mars': bool(student_data[11]),
#                 'avril': bool(student_data[12]),
#                 'mai': bool(student_data[13]),
#                 'juin': bool(student_data[14]),
#                 'juillet': bool(student_data[15]),
#                 'aout': bool(student_data[16]),
#                 'septembre': bool(student_data[17]),
#                 'octobre': bool(student_data[18]),
#                 'novembre': bool(student_data[19]),
#                 'decembre': bool(student_data[20])
#             }
#         }

#     return None  # Retourner None si aucun étudiant n'est trouvé

# student = get_student_by_id(15840)
# # # print(student)
# # print(student['location'])


# def save_student_to_db(data):
#     conn, cursor = database.connect_db()
    
#     # Vérifier si l'étudiant existe déjà
#     cursor.execute("SELECT id_etudiant FROM etudiant WHERE id_etudiant = ?", (data['id_etudiant'],))
#     result = cursor.fetchone()

#     if result:
#         # Mise à jour des informations de l'étudiant
#         cursor.execute(''' 
#             UPDATE etudiant
#             SET prenom = ?, nom = ?, genre = ?, date_naissance = ?, addresse = ?, telephone = ?, batiment = ?, chambre = ?
#             WHERE id_etudiant = ?
#         ''', (data['prenom'], data['nom'], data['genre'], data['date_naissance'], 
#               data['addresse'], data['telephone'], data['batiment'], data['chambre'], data['id_etudiant']))

#         # Mise à jour des paiements
#         cursor.execute('''
#             UPDATE location
#             SET janvier = ?, fevrier = ?, mars = ?, avril = ?, mai = ?, juin = ?, juillet = ?, aout = ?, septembre = ?, octobre = ?, novembre = ?, decembre = ?
#             WHERE id_etudiant = ?
#         ''', (int(data['location']['janvier']), int(data['location']['fevrier']), int(data['location']['mars']),
#               int(data['location']['avril']), int(data['location']['mai']), int(data['location']['juin']),
#               int(data['location']['juillet']), int(data['location']['aout']), int(data['location']['septembre']),
#               int(data['location']['octobre']), int(data['location']['novembre']), int(data['location']['decembre']),
#               data['id_etudiant']))
#     else:
#         # Insertion d'un nouvel étudiant
#         cursor.execute('''
#             INSERT INTO etudiant (prenom, nom, genre, date_naissance, addresse, telephone, batiment, chambre)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (data['prenom'], data['nom'], data['genre'], data['date_naissance'], 
#               data['addresse'], data['telephone'], data['batiment'], data['chambre']))
        
#         # Récupérer l'ID de l'étudiant nouvellement inséré
#         etudiant_id = cursor.lastrowid
        
#         # Insertion des paiements
#         cursor.execute('''
#             INSERT INTO location (id_etudiant, janvier, fevrier, mars, avril, mai, juin, juillet, aout, septembre, octobre, novembre, decembre)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (etudiant_id, int(data['location']['janvier']), int(data['location']['fevrier']), int(data['location']['mars']),
#               int(data['location']['avril']), int(data['location']['mai']), int(data['location']['juin']),
#               int(data['location']['juillet']), int(data['location']['aout']), int(data['location']['septembre']),
#               int(data['location']['octobre']), int(data['location']['novembre']), int(data['location']['decembre'])))

#     conn.commit()
#     conn.close()
