import re

# Lire mon fichier keg:
with open('data/STITCH - ATC/br08303.keg', 'r') as file:
    levels_E_F = []
    
    # Lire chaque ligne du fichier
    for line in file:
        # Vérifier si la ligne commence par les niveaux E ou F
        if line.startswith("E") or line.startswith("F"):
            # Ajouter la ligne à la liste des niveaux E et F
            levels_E_F.append(line.strip())

# Afficher les niveaux E et F
for level in levels_E_F:
    print(level)


# Exporter le dictionnaire schema_keg dans un fichier JSON
import json



    # F -> Drunkbank id
    # E ->  Code ATC