import sqlite3

def connect_db():
    """Connecte à la base de données SQLite."""
    conn = sqlite3.connect('bd_campus_ept.db')
    cursor = conn.cursor()
    return conn, cursor


def get_student_by_id(student_id):
    conn = sqlite3.connect('bd_campus_ept.db')  # Assurez-vous que le chemin est correct
    cursor = conn.cursor()

    # Requête pour récupérer les données de l'étudiant avec l'identifiant spécifié
    cursor.execute('''
        SELECT e.id_etudiant, e.prenom, e.nom, e.genre, e.date_naissance, e.addresse, 
               e.telephone, e.batiment, e.chambre, 
               l.janvier, l.fevrier, l.mars, l.avril, l.mai, l.juin, 
               l.juillet, l.aout, l.septembre, l.octobre, l.novembre, l.decembre
        FROM etudiant e
        LEFT JOIN location l ON e.id_etudiant = l.id_etudiant
        WHERE e.id_etudiant = ?
    ''', (student_id,))

    student_data = cursor.fetchone()
    conn.close()

    if student_data:
        return {
            'id_etudiant': student_data[0],
            'prenom': student_data[1],
            'nom': student_data[2],
            'genre': student_data[3],
            'date_naissance': student_data[4],
            'addresse': student_data[5],
            'telephone': student_data[6],
            'batiment': student_data[7],
            'chambre': student_data[8],
            'location': {
                'janvier': bool(student_data[9]),
                'fevrier': bool(student_data[10]),
                'mars': bool(student_data[11]),
                'avril': bool(student_data[12]),
                'mai': bool(student_data[13]),
                'juin': bool(student_data[14]),
                'juillet': bool(student_data[15]),
                'aout': bool(student_data[16]),
                'septembre': bool(student_data[17]),
                'octobre': bool(student_data[18]),
                'novembre': bool(student_data[19]),
                'decembre': bool(student_data[20])
            }
        }

    return None  # Retourner None si aucun étudiant n'est trouvé



def create_tables():
    conn, cursor = connect_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS etudiant (
            id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT, 
            prenom TEXT,
            nom TEXT,
            genre INTEGER,
            date_naissance DATE,
            addresse TEXT,
            telephone TEXT,
            batiment TEXT,
            chambre INTEGER
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS location (
            id_etudiant INTEGER,  -- Clé étrangère pour référencer l'étudiant
            janvier INTEGER,
            fevrier INTEGER,
            mars INTEGER,
            avril INTEGER,
            mai INTEGER,
            juin INTEGER,
            juillet INTEGER,
            aout INTEGER,
            septembre INTEGER,
            octobre INTEGER,
            novembre INTEGER,
            decembre INTEGER,
            FOREIGN KEY (id_etudiant) REFERENCES etudiant(id_etudiant) -- Définition de la clé étrangère
        );
    ''')
    conn.commit()
    conn.close()

def update_student(student_id, **kwargs):
    conn, cursor = connect_db()
    set_clause = ', '.join(f"{key} = ?" for key in kwargs)
    values = list(kwargs.values())
    values.append(student_id)
    cursor.execute(f'''
    UPDATE etudiant
    SET {set_clause}
    WHERE identifiant = ?
    ''', values)
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn, cursor = connect_db()
    cursor.execute('DELETE FROM etudiant WHERE identifiant = ?', (student_id,))
    conn.commit()
    conn.close()



def get_students_from_db():
    """Récupère tous les étudiants avec leurs données de location."""
    conn, cursor = connect_db()
    
    query = '''
        SELECT e.id_etudiant, e.prenom, e.nom, e.genre, e.date_naissance, e.addresse, 
               e.telephone, e.batiment, e.chambre, 
               l.janvier, l.fevrier, l.mars, l.avril, l.mai, l.juin, 
               l.juillet, l.aout, l.septembre, l.octobre, l.novembre, l.decembre
        FROM etudiant e
        LEFT JOIN location l ON e.id_etudiant = l.id_etudiant
    '''
    
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    students_list = []
    for row in rows:
        student = {
            'id_etudiant': row[0],
            'prenom': row[1],
            'nom': row[2],
            'genre': row[3],
            'date_naissance': row[4],
            'addresse': row[5],
            'telephone': row[6],
            'batiment': row[7],
            'chambre': row[8],
            'location': {
                'janvier': bool(row[9]),
                'fevrier': bool(row[10]),
                'mars': bool(row[11]),
                'avril': bool(row[12]),
                'mai': bool(row[13]),
                'juin': bool(row[14]),
                'juillet': bool(row[15]),
                'aout': bool(row[16]),
                'septembre': bool(row[17]),
                'octobre': bool(row[18]),
                'novembre': bool(row[19]),
                'decembre': bool(row[20])
            }
        }
        students_list.append(student)
    
    return students_list

def save_student_to_db(data):
    conn, cursor = connect_db()
    
    # Vérifier si l'étudiant existe déjà
    cursor.execute("SELECT id_etudiant FROM etudiant WHERE id_etudiant = ?", (data['id_etudiant'],))
    result = cursor.fetchone()

    if result:
        # Mise à jour des informations de l'étudiant
        cursor.execute(''' 
            UPDATE etudiant
            SET prenom = ?, nom = ?, genre = ?, date_naissance = ?, addresse = ?, telephone = ?, batiment = ?, chambre = ?
            WHERE id_etudiant = ?
        ''', (data['prenom'], data['nom'], data['genre'], data['date_naissance'], 
              data['addresse'], data['telephone'], data['batiment'], data['chambre'], data['id_etudiant']))

        # Mise à jour des paiements
        cursor.execute('''
            UPDATE location
            SET janvier = ?, fevrier = ?, mars = ?, avril = ?, mai = ?, juin = ?, juillet = ?, aout = ?, septembre = ?, octobre = ?, novembre = ?, decembre = ?
            WHERE id_etudiant = ?
        ''', (int(data['location']['janvier']), int(data['location']['fevrier']), int(data['location']['mars']),
              int(data['location']['avril']), int(data['location']['mai']), int(data['location']['juin']),
              int(data['location']['juillet']), int(data['location']['aout']), int(data['location']['septembre']),
              int(data['location']['octobre']), int(data['location']['novembre']), int(data['location']['decembre']),
              data['id_etudiant']))
        print(int(data['location']['janvier']))
    else:
        # Insertion d'un nouvel étudiant
        cursor.execute('''
            INSERT INTO etudiant (prenom, nom, genre, date_naissance, addresse, telephone, batiment, chambre)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['prenom'], data['nom'], data['genre'], data['date_naissance'], 
              data['addresse'], data['telephone'], data['batiment'], data['chambre']))
        
        # Récupérer l'ID de l'étudiant nouvellement inséré
        etudiant_id = cursor.lastrowid
        
        # Insertion des paiements
        cursor.execute('''
            INSERT INTO location (id_etudiant, janvier, fevrier, mars, avril, mai, juin, juillet, aout, septembre, octobre, novembre, decembre)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (etudiant_id, int(data['location']['janvier']), int(data['location']['fevrier']), int(data['location']['mars']),
              int(data['location']['avril']), int(data['location']['mai']), int(data['location']['juin']),
              int(data['location']['juillet']), int(data['location']['aout']), int(data['location']['septembre']),
              int(data['location']['octobre']), int(data['location']['novembre']), int(data['location']['decembre'])))

    conn.commit()
    conn.close()

def delete_student_by_id(student_id):
    conn, cursor = connect_db()
    
    try:
        # Supprimer d'abord l'étudiant de la table 'location'
        cursor.execute('DELETE FROM location WHERE id_etudiant = ?', (student_id,))
        
        # Ensuite, supprimer l'étudiant de la table 'etudiant'
        cursor.execute('DELETE FROM etudiant WHERE id_etudiant = ?', (student_id,))
        
        # Confirmer la suppression
        conn.commit()
        print(f"L'étudiant avec l'ID {student_id} a été supprimé avec succès.")
    
    except sqlite3.Error as e:
        print(f"Une erreur est survenue lors de la suppression de l'étudiant : {e}")
    
    finally:
        conn.close()
