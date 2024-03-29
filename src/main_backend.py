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

    maladies.extend(maladies_responsables(liste_indications[0])) # Recherche les maladies responsables de l'indication/symptome 
    #medicaments.extend(medicaments_responsables(liste_indications[0])) # Recherche les médicaments responsables de l'indication/symptome
    #medicaments_soignant_symptomes([('thrombocytopenezrfia', 'thrombocytopenia')])  # Merci de modifier la drubank à l'aide du fichier nv_drugbank.py avant d'utiliser cette fonction

    if len(liste_indications)!=1:
        for i in range(1, len(liste_indications)):
            nouvelles_maladies_responsables = maladies_responsables(liste_indications[i])
            nouveaux_medicaments_responsables = medicaments_responsables(liste_indications[i])
            #nouveaux_medicaments_soignant = medicaments_soignant_symptomes(nouvelles_maladies_responsables)

            maladies = list(set(maladies) & set(nouvelles_maladies_responsables))
            medicaments = list(set(medicaments) & set(nouveaux_medicaments_responsables))
            #medicaments_soignant = list(set(medicaments_soignant) & set(nouveaux_medicaments_soignant))
    
    print("\n\n\nLes maladies responsables de l'indication/symptome sont à la fin : ", maladies)
    print("\n\n\nLes médicaments responsables de l'indication/symptome sont à la fin: ", medicaments)

    return indication

# Prendre Acute abdomen ou Enterovirus comme exemple
def maladies_responsables(indication_initiale):

    noms_maladies = []
    liste_symptome = [indication_initiale]

    #A MODIFIER AVEC LABEL PAR GESTION DE LISTE
    liste_symptome = obtenir_synonyme_label(indication_initiale)  # Récupère les synonymes de l'indication/symptome

    if (type(liste_symptome) == str):
        liste_symptome = [liste_symptome]
    
    for symptome in liste_symptome:
        noms_maladies = obtenir_nom_maladies_hpo(symptome)  # anciennement indication à la place de preferred_label
        
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
    liste_symptome = obtenir_synonyme_label(indication_initiale)  # Récupère les synonymes de l'indication/symptome 

    if (type(liste_symptome) == str):
        liste_symptome = [liste_symptome]
    
    for symptome in liste_symptome:
        medicaments.extend(obtenir_medicaments_responsables_drugbank(symptome))  # indication ici c'est toxicity dans la fonction
        print(medicaments)

    medicaments = list(set(medicaments))  # Supprime les doublons

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
            code_ATC.extend(execute_shell_command("request_TSV", "STITCH\ -\ ATC/chemical_atc.tsv", 1, code, 4))
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

def obtenir_synonyme_label(indication):
    ''' 
    Obtenir les synonymes d'une indication/symptome donnée

    Args:
        indication (str): indication/symptome
    
    Returns:
        synonymes (list): liste des synonymes

    '''
    '''synonymes = [indication]
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
'''
    # Travail sur le libellé préféré des maladies (Abscess)

    return indication

# Exécute la fonction principale
if __name__ == "__main__":
    entrer_indication()