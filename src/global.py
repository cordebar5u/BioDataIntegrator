import com_drugbank as cdb # Evite les conflits entre differents imports
import maladies as mal
import medicaments as med
import medicaments_soignant as med_soignant

def entrer_indication():

    maladies = []
    medicaments = []
    medicaments_soignant = []
    nouvelles_maladies_responsables = []
    nouveaux_medicaments_responsables = []
    nouveaux_medicaments_soignant = []

    indication = input("Veuillez entrer votre maladie (indication) : ").strip()    # Demande à l'utilisateur d'entrer une indication/symptome

    if indication == "":
        print("Indication/symptome non valide.")
        return

    liste_indications = parser_indication(indication)  # Parse l'indication/symptome

    if len(liste_indications) == 0:
        print("Problème lors du parsing de l'indication/symptome.")
        return
    
    print("Les indications/symptomes sont : ", liste_indications)

    maladies.extend(mal.maladies_responsables(liste_indications[0])) # Recherche les maladies responsables de l'indication/symptome 
    medicaments.extend(med.medicaments_responsables(liste_indications[0])) # Recherche les médicaments responsables de l'indication/symptome
    med_soignant.medicaments_soignant_symptomes([('', 'thrombocytopenia')])  # Merci de modifier la drubank à l'aide du fichier nv_drugbank.py avant d'utiliser cette fonction

    if len(liste_indications)!=1:
        for i in range(1, len(liste_indications)):
            nouvelles_maladies_responsables = mal.maladies_responsables(liste_indications[i])
            nouveaux_medicaments_responsables = med.medicaments_responsables(liste_indications[i])
            #nouveaux_medicaments_soignant = medicaments_soignant_symptomes(nouvelles_maladies_responsables)

            maladies = list(set(maladies) & set(nouvelles_maladies_responsables))
            medicaments = list(set(medicaments) & set(nouveaux_medicaments_responsables))
            #medicaments_soignant = list(set(medicaments_soignant) & set(nouveaux_medicaments_soignant))
    
    print("\n\n\nLes maladies responsables de l'indication/symptome sont à la fin : ", maladies)
    print("\n\n\nLes médicaments responsables de l'indication/symptome sont à la fin: ", medicaments)

    return indication

def parser_indication(indication):
    '''
    Parser l'indication/symptome donnée par l'utilisateur

    Args:
        indication (str): indications/symptomes entrés par l'utilisateur
    
    Returns:
        liste_indications (list): liste des indications/symptomes

    '''

    liste_indications = []
    liste_indications = indication.split("ET")  # Sépare les indications/symptomes par des virgules
    liste_indications = [i.strip() for i in liste_indications]  # Enlève les espaces inutiles

    return liste_indications


# Exécute la fonction principale
if __name__ == "__main__":
    entrer_indication()