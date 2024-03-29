import com_drugbank as cdb

def medicaments_soignant_symptomes(maladies):
    '''
    Obtenir les médicaments soignant une indication/symptome donnée

    Args:
        indication (str): indication/symptome
    
    Returns:
        medicaments (list): liste des médicaments soignant

    '''

    exist_medicaments = False
 
    retour= []   # liste avec le chemin, les maladies et les médicaments
    medicaments = []

    fichier_xml = "data/DRUGBANK/drugbank_modifiee.xml"

    for maladie in maladies:
        medicaments.extend(cdb.rechercher_medicament(fichier_xml, maladie[1], "")) # Recherche les médicaments soignant les maladies
        medicaments = list(set(medicaments))  # Supprime les doublons

        retour.append([maladie[0], maladie[1], medicaments])

        if medicaments != [] and not exist_medicaments:
            exist_medicaments = True
        
        medicaments = [] # Réinitialise la liste des médicaments


    if not exist_medicaments:
        print("Aucun médicament trouvé soignant l'indication/symptome.")

    else:
        print("\n\n\nLes médicaments soignant les maladies sont : ")
        for i in retour :
            print(i[2])
    print("\n\n\n")
    return retour