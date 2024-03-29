import com_hpo as hpo
import com_hpo_annotations as hpoa
import com_omim_txt as omim
import synonymes as syn
from shell_commande import execute_shell_command 

# Prendre Acute abdomen ou Enterovirus comme exemple
def maladies_responsables(indication_initiale):

    noms_maladies = []
    liste_symptome = [indication_initiale]

    #A MODIFIER AVEC LABEL PAR GESTION DE LISTE
    liste_symptome = syn.obtenir_synonyme_label(indication_initiale)  # Récupère les synonymes de l'indication/symptome

    if (type(liste_symptome) == str):
        liste_symptome = [liste_symptome]
    
    for symptome in liste_symptome:
        noms_maladies.extend(obtenir_nom_maladies_meddra(symptome))  # anciennement indication à la place de preferred_label
        noms_maladies.extend(obtenir_nom_maladies_hpo(symptome))  # anciennement indication à la place de preferred_label

    noms_maladies = list(set(noms_maladies))  # Supprime les doublons

    return noms_maladies  

def obtenir_nom_maladies_meddra(indication):

    maladies = []
    maladies = execute_shell_command("request_TSV", "SIDER/meddra_all_indications.tsv", 7, indication, 4)
    maladies.extend(execute_shell_command("request_TSV", "SIDER/meddra_all_indications.tsv", 4, indication, 7))
    maladies = list(set(maladies))  # Supprime les doublons
    maladies = [('MedDra', i) for i in maladies]

    return maladies


def obtenir_nom_maladies_hpo(indication): 
    '''
    Obtenir les noms des maladies responsables d'une indication/symptome donnée par HPO

    Args: 
        indication (str): indication/symptome
    
    Returns:
        noms_maladies (list): liste des noms des maladies responsables

    '''
    noms_maladies = []
    sign_id = []
    conn = hpoa.connect_to_db('data/HPO/hpo_annotations.sqlite')

    if type(indication) == str:
        indication = [indication]   # Si l'indication est un string, on le met dans une liste (sinon c'est deja une liste de string (str))
    
    for i in indication: 
        sign_id = hpo.recherche_symptome(i, False)   # Deuxième argument pour la verbose
        id_maladie = omim.recherche(i)

        for i in sign_id:  # Premier chemin
            i = i.replace("HPO:", "HP:")
            noms_maladies.extend(hpoa.search_hpo(conn, i))

        for i in id_maladie:  # Deuxième chemin
            i = i.replace("OMIM:", "")
            noms_maladies.extend(hpoa.search_hpo(conn, i))
    
    noms_maladies = list(set(noms_maladies))  # Supprime les doublons
    return noms_maladies

if __name__ == "__main__":
    maladies_responsables("Headache") # Test avec un exemple
