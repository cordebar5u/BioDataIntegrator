from shell_commande import execute_shell_command


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