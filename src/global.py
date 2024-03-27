import com_drugbank as cdb # Evite les conflits entre differents imports
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
    indication = input("Veuillez entrer votre maladie (indication) : ").strip()
    output = execute_shell_command("request_TSV", "SIDER/meddra.tsv", 4, indication, 1)
    
    print(output)
    for element in output:
        print(element)

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