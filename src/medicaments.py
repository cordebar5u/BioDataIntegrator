import synonymes as syn
import com_drugbank as cdb
from shell_commande import execute_shell_command


def medicaments_responsables(indication_initiale):    # attention ici il faut récupérer le preferred label de la maladie
    '''
    Obtenir les médicaments responsables d'une indication/symptome donnée 

    Args:
        indication(toxicity) (str): indication/symptome
    
    Returns:
        medicaments (list): liste des médicaments responsables

    '''
    medicaments = []
    liste_symptome = [indication_initiale]

    #A MODIFIER AVEC LABEL PAR GESTION DE LISTE
    liste_symptome = syn.obtenir_synonyme_label(indication_initiale)  # Récupère les synonymes de l'indication/symptome 

    if (type(liste_symptome) == str):
        liste_symptome = [liste_symptome]
    
    for symptome in liste_symptome:
        medicaments.extend(obtenir_medicaments_responsables_drugbank(symptome))  # indication ici c'est toxicity dans la fonction
        medicaments.extend(obtenir_medicaments_responsables_atc(symptome))  # indication ici c'est toxicity dans la fonction

    return medicaments

def obtenir_medicaments_responsables_drugbank(indication):
    '''
    Obtenir les médicaments responsables d'une indication/symptome donnée par DrugBank

    Args:
        indication (str): indication/symptome
    
    Returns:
        medicaments (list): liste des médicaments responsables

    '''

    medicaments = []
    medicaments = cdb.rechercher_medicament("data/DRUGBANK/drugbank_modifiee.xml", "", indication)  # Recherche les médicaments responsables de l'indication/symptome
    medicaments = [['DrugBank', medicament] for medicament in medicaments]
    return medicaments

def obtenir_medicaments_responsables_atc(indication):
    '''
    Obtenir les médicaments responsables d'une indication/symptome donnée par ATC

    Args:
        indication (str): indication/symptome
    
    Returns:
        medicaments (list): liste des médicaments responsables

    '''

    medicaments = []
    code_medDRa = []
    code_ATC = []

    code_medDRa = execute_shell_command("request_TSV", "SIDER/meddra_all_se.tsv", 6, indication, 2)
    code_medDRa = list(set(code_medDRa))

    if code_medDRa != []:
        for code in code_medDRa:
            code = code[:3] + 's' + code[4:]
            code_ATC.extend(execute_shell_command("request_TSV", "STITCH\ -\ ATC/chemical_atc.tsv", 2, code, 4))
            code_ATC = list(set(code_ATC))
        if code_ATC != []:
            for code in code_ATC:
                medicaments.extend(execute_shell_command("request_KEG", "STITCH\ -\ ATC/br08303.keg", 2, code, 3))
        else: 
            print("Aucun médicament trouvé ayant ces codes MedDra dans STITCH.")
    else: 
        print("Aucun médicament trouvé ayant pour effet secondaire l'indication/symptome dans MedDra.")
    
    medicaments = list(set(medicaments))

    medicaments = [['ATC', medicament] for medicament in medicaments]
    return medicaments

if __name__ == "__main__":
    print(medicaments_responsables("Injection site necrosis"))
    #CID000439260

