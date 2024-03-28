import com_drugbank as cdb # Evite les conflits entre differents imports
import com_hpo as hpo
import com_hpo_annotations as hpoa
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

# Prendre Acute abdomen comme exemple
def maladies_responsables():

    noms_maladies = []
    preferred_label = []
    CUIs = []

    indication = input("Veuillez entrer votre maladie (indication) : ").strip()
    sortie = execute_shell_command("request_TSV", "SIDER/meddra.tsv", 4, indication, 1)

    # Garde les identifiants uniques des concepts (CUI) dans une liste

    CUIs = list(set(sortie))
    if len(CUIs) != 0:
        for CUI in CUIs:
            preferred_label.extend(execute_shell_command("request_CSV", "OMIM/omim_onto.csv", 6, CUI, 2)) # Possiblement rien
    else : 
            preferred_label = execute_shell_command("request_CSV", "OMIM/omim_onto.csv", 2, indication, 3) # Possiblement rien
            preferred_label.extend(execute_shell_command("request_CSV", "OMIM/omim_onto.csv", 3, indication, 2)) # Possiblement rien

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

        for i in sign_id:
            i = i.replace("HPO:", "HP:")
            noms_maladies.extend(hpoa.search_hpo(conn, i))
            
    
    return noms_maladies



# Exécute la fonction principale
if __name__ == "__main__":
    maladies_responsables()










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