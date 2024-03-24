import sqlite3
import os
import csv


data_path = os.path.join("data/STITCH\ -\ ATC/")

# Créer un fichier CSV à partir du fichier KEG
if  os.system("find " + data_path + "atc.csv") != 0:
    os.system("touch " + data_path + "/atc.csv")
    os.system("grep '^E' " + data_path + "/br08303.keg | sed 's/  */,/g' > " + data_path + "/atc.csv")
    print("Fichier CSV créé")


conn = sqlite3.connect("data/STITCH - ATC/atc.db")
cursor = conn.cursor()

# Créer une connexion à la base de données SQLite
c = conn.cursor()

# Créer la table
c.execute('''CREATE TABLE substances(
            codeATC VARCHAR(16),
            chemicalSubstance VARCHAR(30)
          )''')

with open(os.path.join('data/STITCH - ATC/atc.csv'), "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=",")
    reader = [(row[1], row[2]) for row in reader]
    cursor.executemany("""
        INSERT INTO substances VALUES (?, ?);
    """, reader)
conn.commit()
conn.close()
