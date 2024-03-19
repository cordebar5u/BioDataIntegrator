import sqlite3
import json

# Fonction pour extraire le schéma du fichier SQL
def extraire_schema_sqlite(nom_fichier_sql):
    conn = sqlite3.connect(nom_fichier_sql)
    cursor = conn.cursor()

    # Obtenir les noms de toutes les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = {}

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        schema[table_name] = column_names

    conn.close()
    return schema

# Fonction pour exporter le schéma au format JSON
def exporter_schema_json(schema, nom_fichier_json):
    with open(nom_fichier_json, 'w') as f:
        json.dump(schema, f, indent=4)

# Nom du fichier SQL
nom_fichier_sql = 'data/HPO/hpo_annotations.sqlite'
nom_fichier_json = 'data/HPO/schema_hpo.json'
schema = extraire_schema_sqlite(nom_fichier_sql)
exporter_schema_json(schema, nom_fichier_json)
