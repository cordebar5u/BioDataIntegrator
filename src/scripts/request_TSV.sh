#!/usr/bin/awk -f

BEGIN{
    # Verifier que le nombre d'arguments est correct
    if (ARGC != 5) {
        exit 1
    }
    # Retrieve the arguments
    tsv_fichier = ARGV[1]
    colonne = ARGV[2]
    motif = ARGV[3]
    afficherColonne = ARGV[4]
    FS = "\t"
}
{
    if($colonne ~ motif) {
        if (NR > 1) {
            printf ","
        }
        printf $afficherColonne
    }
}
END{
    exit 0
}
