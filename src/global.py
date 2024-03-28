import com_drugbank as cdb # Evite les conflits entre differents imports
import com_hpo as hpo
import com_hpo_annotations as hpoa
import com_omim_txt as omim
import subprocess # Pour exécuter des commandes shell


def execute_shell_command(exec, data, index, motif, afficher):
    requete = f"src/scripts/{exec}.sh data/{data} {index} '{motif}' {afficher}"
    process = subprocess.Popen(requete, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    output_lines = []
    while True:
        line = process.stdout.readline()
        if not line or "/usr/bin/" in line:
            break
        output_lines.append(line.strip())
        
    return output_lines

def entrer_indication():
    indication = input("Veuillez entrer votre maladie (indication) : ").strip()
    maladies_responsables(indication)
    medicaments_responsables(indication) 
    return indication

# Prendre Acute abdomen ou Enterovirus comme exemple
def maladies_responsables(indication):

    noms_maladies = []
    preferred_label = []
    CUIs = []

    sortie = execute_shell_command("request_TSV", "SIDER/meddra.tsv", 4, indication, 1)

    # Garde les identifiants uniques des concepts (CUI) dans une liste

    CUIs = list(set(sortie))
    print("Les CUIs des maladies responsables de l'indication/symptome sont : ", CUIs)
    if len(CUIs) != 0:
        for CUI in CUIs:
            preferred_label.extend(execute_shell_command("request_CSV", "OMIM/omim_onto.csv", 6, CUI, 2)) # Possiblement rien
            print(preferred_label)
    else : 
            preferred_label = execute_shell_command("request_CSV", "OMIM/omim_onto.csv", 2, indication, 3) # Regarde dans les PreferredLabel directement et stocke les synonymes - Possiblement rien  
            preferred_label.extend(execute_shell_command("request_CSV", "OMIM/omim_onto.csv", 3, indication, 2)) # Regarde dans les synonymes et stocke les PreferredLabel - Possiblement rien
            preferred_label.extend(execute_shell_command("request_CSV", "OMIM/omim_onto.csv", 2, indication, 2)) # Regarde dans les PreferredLabel et stocke les PreferredLabel - Possiblement rien

    # Travail sur le libellé préféré des maladies (Abscess)
            
    noms_maladies = obtenir_nom_maladies_hpo(indication)
    print("Les maladies responsables de l'indication/symptome sont : ", noms_maladies)
    return noms_maladies  

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
        indication = [indication]
    
    for i in indication: 
        sign_id = hpo.recherche_symptome(i, False)
        id_maladie = omim.recherche(i)

        for i in sign_id:
            i = i.replace("HPO:", "HP:")
            noms_maladies.extend(hpoa.search_hpo(conn, i))

        for i in id_maladie:
            i = i.replace("OMIM:", "")
            noms_maladies.extend(hpoa.search_hpo(conn, i))
    
    noms_maladies = list(set(noms_maladies))
    return noms_maladies

def medicaments_responsables(indication):
    '''
    Obtenir les médicaments responsables d'une indication/symptome donnée 

    Args:
        indication (str): indication/symptome
    
    Returns:
        medicaments (list): liste des médicaments responsables

    '''

    medicaments = []
    medicaments = obtenir_medicaments_responsables_drugbank(indication)
    #medicaments.extend(obtenir_medicaments_responsables_atc(indication))

    if medicaments == []:
        print("Aucun médicament trouvé ayant pour effet secondaire l'indication/symptome.")
    else:
        print("Les médicaments responsables de l'indication/symptome sont : ", medicaments)
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
    medicaments = cdb.rechercher_medicament_par_toxicity("data/DRUGBANK/drugbank.xml", indication)
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
    print(code_medDRa)

    if code_medDRa != []:
        for code in code_medDRa:
            code[3].replace("0", "s")
            code_ATC.extend(execute_shell_command("request_TSV", "STITCH\ -\ ATC/chemical.sources.v5.0.tsv", 1, code, 4))
            code_ATC = list(set(code_ATC))
            print(code_ATC)
        if code_ATC != []:
            for code in code_ATC:
                medicaments.extend(execute_shell_command("request_KEG", "STITCH\ -\ ATC/br08303.keg", 2, code, 3))
        else: 
            print("Aucun médicament trouvé ayant ce code MedDra dans STITCH.")
    else: 
        print("Aucun médicament trouvé ayant pour effet secondaire l'indication/symptome dans MedDra.")
    return medicaments

# Exécute la fonction principale
if __name__ == "__main__":
    entrer_indication()










#import os
# fonction pour executer un script shell (.sh) avec des parametres
# def execute_shell_command(exec, data, index, motif):    
#     requete = "src/scripts/" + exec +".sh data/" + data + " "+ str(index) + " '" + motif + "'"
#     os.system(requete)


# def maladies_responsables():
#     indication = input("Veuillez entrer votre maladie (indication) : ").strip()
    
#     print(execute_shell_command("request_TSV", "SIDER/meddra.tsv", 4, indication))

#src/scripts/request_TSV.sh data/SIDER/meddra.tsv  4 'Acute abdomen'

#a = execute_shell_command("request_TSV", "SIDER/meddra.tsv", 4, "Acute abdomen")
# Vous pouvez étendre cette fonction pour demander également la toxicité si nécessaire.

# Appel de la fonction pour rechercher des médicaments
# Assurez-vous que le fichier XML est correctement spécifié ici
#fichier_xml = "data/DRUGBANK/drugbank.xml"
#cdb.rechercher_medicament(fichier_xml, indication, "")