import re

# Lire mon fichier keg:
with open('data/STITCH - ATC/br08303.keg', 'r') as file:
    arbre_kegg = file.read()

# Fonction qui récupère les lignes commençant par "A" et les stocke dans une liste
def extract_keg(arbre_kegg):
    liste_keg = []
    for ligne in arbre_kegg.split('\n'):
        if re.match(r'^A', ligne):
            liste_keg.append(ligne)
    return liste_keg

# Fonction qui determine les sous-categories AT
# Exemple d'une sous-catégorie de A :  "B  Axx xxxx" de B :  "B  Bxx xxxx"; de C : "B  Cxx xxxx"
def extract_subcategories(liste_keg):
    liste_subcategories = []
    for ligne in arbre_kegg.split('\n'):
        if re.match(r'^B', ligne):
            liste_subcategories.append(ligne)
    return liste_subcategories

liste_keg = extract_keg(arbre_kegg)
liste_subcategories = extract_subcategories(arbre_kegg)

schema_keg = {}  

for keg in liste_keg:
    schema_keg[keg] = []

for keg in liste_keg:
    for subcategory in liste_subcategories:
        if keg[1] == subcategory[3]:
            schema_keg[keg].append(subcategory)


# Exporter le dictionnaire schema_keg dans un fichier JSON
import json
with open('data/STITCH - ATC/schema_keg.json', 'w') as file:
    json.dump(schema_keg, file, indent=4)