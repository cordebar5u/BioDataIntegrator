import com_drugbank as cdb

def medicaments_soignant_symptomes(maladies):
    '''
    Obtenir les médicaments soignant une indication/symptome donnée

    Args:
        indication (str): indication/symptome
    
    Returns:
        medicaments (list): liste des médicaments soignant

    '''
    medicaments = []

    fichier_xml = "data/DRUGBANK/drugbank_modifiee.xml"

    medicaments.extend(cdb.rechercher_medicament(fichier_xml, maladies[0][1], ""))  # Recherche les médicaments soignant les maladies
    medicaments = list(set(medicaments))  # Supprime les doublons
    
    if medicaments == []:
        print("Aucun médicament trouvé soignant l'indication/symptome.")

    else:
        print("\n\n\nLes médicaments soignant les maladies sont : ")
        for i in medicaments:
            print(i)
    print("\n\n\n")
    return medicaments