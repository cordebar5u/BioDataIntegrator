#!/usr/bin/awk -f

BEGIN{
    # Verifier que le nombre d'arguments est correct
    if (ARGC != 5) {
        exit 1
    }
    tsv_fichier = ARGV[1]
    colonne = ARGV[2]
    motif = ARGV[3]
    afficherColonne = ARGV[4]
    FS = ","
}
{
    if($colonne ~ motif) {
        print $afficherColonne
    }
}
END{
    exit 0
}