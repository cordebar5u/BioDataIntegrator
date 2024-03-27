#!/usr/bin/awk -f

BEGIN{
    # Verifier que le nombre d'arguments est correct
    if (ARGC != 4) {
        exit 1
    }
    # Retrieve the arguments
    tsv_fichier = ARGV[1]
    colonne = ARGV[2]
    motif = ARGV[3]
    saut_ligne = ARGV[4]
    FS = "	"
}
{
    if($colonne ~ motif) {
        print $0
    }
}
END{
    exit 0
}
