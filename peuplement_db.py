import database

# Exemple de données d'étudiants sénégalais
students_data = [
    {
        'id_etudiant': None,
        'prenom': 'Cheikh Oumar',
        'nom': 'DIALLO',
        'genre': 'M',
        'date_naissance': '15-02-2003',
        'addresse': 'Diamaguene',
        'telephone': '774189439',
        'batiment': 'H2',
        'chambre': 18,
        'location': {
            'janvier': False, 'fevrier': False, 'mars': False, 'avril': False,
            'mai': False, 'juin': False, 'juillet': False, 'aout': False,
            'septembre': False, 'octobre': True, 'novembre': True, 'decembre': False
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Abdoulaye SY',
        'nom': 'NDAW',
        'genre': 'M',
        'date_naissance': '03-12-2024',
        'addresse': 'Maristes',
        'telephone': '774584454',
        'batiment': 'H2',
        'chambre': 18,
        'location': {
            'janvier': False, 'fevrier': False, 'mars': False, 'avril': False,
            'mai': False, 'juin': False, 'juillet': False, 'aout': False,
            'septembre': False, 'octobre': True, 'novembre': True, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Moussa',
        'nom': 'BA',
        'genre': 'M',
        'date_naissance': '22-08-2002',
        'addresse': 'Guédiawaye',
        'telephone': '774145633',
        'batiment': 'H1',
        'chambre': 10,
        'location': {
            'janvier': True, 'fevrier': True, 'mars': False, 'avril': True,
            'mai': True, 'juin': False, 'juillet': False, 'aout': True,
            'septembre': False, 'octobre': False, 'novembre': True, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Aissatou',
        'nom': 'SOW',
        'genre': 'F',
        'date_naissance': '30-01-2003',
        'addresse': 'Dakar Plateau',
        'telephone': '775234567',
        'batiment': 'H3',
        'chambre': 15,
        'location': {
            'janvier': True, 'fevrier': True, 'mars': True, 'avril': True,
            'mai': True, 'juin': False, 'juillet': False, 'aout': True,
            'septembre': False, 'octobre': False, 'novembre': False, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Aminata',
        'nom': 'DIA',
        'genre': 'F',
        'date_naissance': '10-06-2001',
        'addresse': 'Pikine',
        'telephone': '774889345',
        'batiment': 'H4',
        'chambre': 20,
        'location': {
            'janvier': False, 'fevrier': True, 'mars': True, 'avril': True,
            'mai': True, 'juin': False, 'juillet': False, 'aout': True,
            'septembre': True, 'octobre': False, 'novembre': True, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Saliou',
        'nom': 'GUEYE',
        'genre': 'M',
        'date_naissance': '21-11-2002',
        'addresse': 'Mermoz',
        'telephone': '775001234',
        'batiment': 'H1',
        'chambre': 12,
        'location': {
            'janvier': True, 'fevrier': True, 'mars': True, 'avril': True,
            'mai': True, 'juin': False, 'juillet': False, 'aout': False,
            'septembre': False, 'octobre': True, 'novembre': False, 'decembre': False
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Mame Diarra',
        'nom': 'DIOP',
        'genre': 'F',
        'date_naissance': '14-09-2002',
        'addresse': 'Yoff',
        'telephone': '775987654',
        'batiment': 'H2',
        'chambre': 9,
        'location': {
            'janvier': False, 'fevrier': False, 'mars': True, 'avril': True,
            'mai': False, 'juin': True, 'juillet': True, 'aout': False,
            'septembre': False, 'octobre': True, 'novembre': False, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Oumar',
        'nom': 'SECK',
        'genre': 'M',
        'date_naissance': '02-04-2003',
        'addresse': 'Saint-Louis',
        'telephone': '773456789',
        'batiment': 'H3',
        'chambre': 5,
        'location': {
            'janvier': True, 'fevrier': True, 'mars': True, 'avril': False,
            'mai': True, 'juin': True, 'juillet': True, 'aout': False,
            'septembre': True, 'octobre': False, 'novembre': False, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Fatoumata',
        'nom': 'MENDY',
        'genre': 'F',
        'date_naissance': '17-06-2001',
        'addresse': 'Thiès',
        'telephone': '776000000',
        'batiment': 'H4',
        'chambre': 13,
        'location': {
            'janvier': True, 'fevrier': False, 'mars': True, 'avril': True,
            'mai': False, 'juin': False, 'juillet': False, 'aout': True,
            'septembre': True, 'octobre': True, 'novembre': True, 'decembre': False
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Binta',
        'nom': 'NDIAYE',
        'genre': 'F',
        'date_naissance': '12-08-2002',
        'addresse': 'Kaolack',
        'telephone': '775678921',
        'batiment': 'H2',
        'chambre': 22,
        'location': {
            'janvier': False, 'fevrier': True, 'mars': False, 'avril': True,
            'mai': True, 'juin': True, 'juillet': False, 'aout': True,
            'septembre': False, 'octobre': False, 'novembre': True, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Ibrahime',
        'nom': 'NDAO',
        'genre': 'M',
        'date_naissance': '11-05-2003',
        'addresse': 'Ziguinchor',
        'telephone': '772345678',
        'batiment': 'H3',
        'chambre': 8,
        'location': {
            'janvier': False, 'fevrier': False, 'mars': True, 'avril': False,
            'mai': True, 'juin': True, 'juillet': False, 'aout': False,
            'septembre': True, 'octobre': True, 'novembre': False, 'decembre': False
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Seydou',
        'nom': 'MBENGUE',
        'genre': 'M',
        'date_naissance': '07-03-2001',
        'addresse': 'Pikine',
        'telephone': '774098765',
        'batiment': 'H1',
        'chambre': 14,
        'location': {
            'janvier': True, 'fevrier': True, 'mars': False, 'avril': True,
            'mai': True, 'juin': False, 'juillet': True, 'aout': True,
            'septembre': False, 'octobre': True, 'novembre': False, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Aminatou',
        'nom': 'THIAM',
        'genre': 'F',
        'date_naissance': '22-01-2003',
        'addresse': 'Tivaouane',
        'telephone': '775120344',
        'batiment': 'H4',
        'chambre': 3,
        'location': {
            'janvier': True, 'fevrier': False, 'mars': True, 'avril': True,
            'mai': False, 'juin': True, 'juillet': False, 'aout': True,
            'septembre': False, 'octobre': True, 'novembre': False, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Elimane',
        'nom': 'LONDI',
        'genre': 'M',
        'date_naissance': '25-07-2002',
        'addresse': 'Bamako',
        'telephone': '774112233',
        'batiment': 'H3',
        'chambre': 16,
        'location': {
            'janvier': True, 'fevrier': True, 'mars': True, 'avril': True,
            'mai': False, 'juin': False, 'juillet': False, 'aout': False,
            'septembre': True, 'octobre': False, 'novembre': False, 'decembre': True
        }
    },
    {
        'id_etudiant': None,
        'prenom': 'Mariama',
        'nom': 'MBOUP',
        'genre': 'F',
        'date_naissance': '05-12-2001',
        'addresse': 'Kaolack',
        'telephone': '775998877',
        'batiment': 'H2',
        'chambre': 6,
        'location': {
            'janvier': True, 'fevrier': False, 'mars': False, 'avril': True,
            'mai': True, 'juin': True, 'juillet': False, 'aout': False,
            'septembre': True, 'octobre': True, 'novembre': True, 'decembre': False
        }
    }
]


# Insérer les étudiants dans la base de données
for student in students_data:
    database.save_student_to_db(student)
print("Données des étudiants insérées avec succès.")
