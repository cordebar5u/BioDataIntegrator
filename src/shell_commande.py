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