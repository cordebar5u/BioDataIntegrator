import sqlite3

def connect_to_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn

def search_hpo(db, motif):
    """Rechercher le motif dans la colonne spécifiée et renvoyer les lignes correspondantes."""
    cursor = db.cursor()
    query = f"SELECT disease_db, disease_label FROM phenotype_annotation WHERE disease_id LIKE ? OR sign_id LIKE ?"
    cursor.execute(query, (motif, motif,))
    rows = cursor.fetchall()
    return rows

# Exemple d'utilisation
conn = connect_to_db('data/HPO/hpo_annotations.sqlite')
motif = 'HP:0000008'

rows = search_hpo(conn, motif)
for row in rows:
    print(row)
