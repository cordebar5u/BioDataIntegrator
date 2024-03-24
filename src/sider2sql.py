import sqlite3
import os
import csv

data_path = os.path.join("data/SIDER")
conn = sqlite3.connect("data/SIDER/sider.db")
cursor = conn.cursor()

# Cassecouille
cursor.execute("DROP TABLE IF EXISTS meddra;")
cursor.execute("DROP TABLE IF EXISTS meddra_all_se;")
cursor.execute("DROP TABLE IF EXISTS meddra_all_indications;")
cursor.execute("DROP TABLE IF EXISTS meddra_freq;")

# Créer la table meddra
cursor.execute("""
    CREATE TABLE meddra (
        CUI VARCHAR(30),
        type_terme VARCHAR(5),
        stitch_compound_id VARCHAR(30),
        symptome VARCHAR(500)
    );
""")
meddra_path = os.path.join(data_path, "meddra.tsv")
with open(meddra_path, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    cursor.executemany("""
        INSERT INTO meddra VALUES (?, ?, ?, ?);
    """, reader)

conn.commit()

# Créer la table meddra_all_se
cursor.execute("""
    CREATE TABLE meddra_all_se (
        MeddraCode1 VARCHAR(30),
        MeddraCode2 VARCHAR(30),
        CUI VARCHAR(30),
        type_terme VARCHAR(30),
        id_terme VARCHAR(30),
        symptome VARCHAR(50)
    );
""")
meddra_all_se_path = os.path.join(data_path, "meddra_all_se.tsv")
with open(meddra_all_se_path, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    cursor.executemany("""
        INSERT INTO meddra_all_se VALUES (?, ?, ?, ?, ?, ?);
    """, reader)

conn.commit()

# Créer la table meddra_all_indications
cursor.execute("""
    CREATE TABLE meddra_all_indications (
        MeddraCode VARCHAR(30),
        CUI VARCHAR(30),
        mention_texte VARCHAR(50),
        nom_concept VARCHAR(50),
        type_terme VARCHAR(30),
        CUI_principal VARCHAR(30),
        symptome VARCHAR(50)
    );
""")
meddra_all_indications_path = os.path.join(data_path, "meddra_all_indications.tsv")
with open(meddra_all_indications_path, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    cursor.executemany("""
        INSERT INTO meddra_all_indications VALUES (?, ?, ?, ?, ?, ?, ?);
    """, reader)

conn.commit()

# Créer la table meddra_freq
cursor.execute("""
    CREATE TABLE meddra_freq (
        MeddraCode1 VARCHAR(30),
        MeddraCode2 VARCHAR(30),
        CUI VARCHAR(30),
        placebo_ou_pas VARCHAR(30),
        frequence DECIMAL(5,2),
        limite_inférieure_frequence DECIMAL(5,2),
        limite_superieure_frequence DECIMAL(5,2),
        type_terme VARCHAR(30),
        CUI_principal VARCHAR(30),
        symptome VARCHAR(100)
    );
""")
meddra_freq_path = os.path.join(data_path, "meddra_freq.tsv")
with open(meddra_freq_path, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    next(reader)
    cursor.executemany("""
        INSERT INTO meddra_freq VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, reader)

conn.commit()

conn.close()