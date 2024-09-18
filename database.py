import sqlite3

def connect_db():
    """Connecte à la base de données SQLite."""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    return conn, cursor

def create_tables():
    conn, cursor = connect_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS etudiant (
            identifiant INTEGER PRIMARY KEY AUTOINCREMENT, -- Utilisation de AUTOINCREMENT pour générer les identifiants automatiquement
            prenom TEXT,
            nom TEXT,
            genre BOOLEAN,
            date_naissance DATE,
            addresse TEXT,
            telephone TEXT,
            batiment TEXT,
            chambre INTEGER
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS location (
            etudiant_id INTEGER,  -- Clé étrangère pour référencer l'étudiant
            janvier BOOLEAN,
            fevrier BOOLEAN,
            mars BOOLEAN,
            avril BOOLEAN,
            mai BOOLEAN,
            juin BOOLEAN,
            juillet BOOLEAN,
            aout BOOLEAN,
            septembre BOOLEAN,
            octobre BOOLEAN,
            novembre BOOLEAN,
            decembre BOOLEAN,
            FOREIGN KEY (etudiant_id) REFERENCES etudiant(identifiant) -- Définition de la clé étrangère
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



def fetch_students_from_db():
    """Récupère tous les étudiants depuis la base de données."""
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM etudiant')
    students = cursor.fetchall()
    conn.close()
    return students

def insert_student_into_db(prenom, nom, genre, date_naissance, adresse, telephone, batiment, chambre):
    """Insère un étudiant dans la base de données."""
    conn, cursor = connect_db()
    cursor.execute('''
        INSERT INTO etudiant (prenom, nom, genre, date_naissance, addresse, telephone, batiment, chambre)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (prenom, nom, genre, date_naissance, adresse, telephone, batiment, chambre))
    conn.commit()
    conn.close()

