#!/usr/bin/awk -f

BEGIN{
    # Verifiez que le nombre d'argument est correct
    if (ARGC < 3) {
        exit 1
    }
    # Associez les arguments à des variables
    fichier = ARGV[1]
    colonne = ARGV[2]
    FS = "	"
}
{
    if (NR > 1) {
        printf ","
    }
    printf $colonne
}
END{
    printf "\n"
    exit 0
}
