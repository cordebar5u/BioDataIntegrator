#!/usr/bin/awk -f

BEGIN{
    if (ARGC != 5) {
        exit 1
    }
    fichier_tsv = ARGV[1]
    colonne = ARGV[2]
    motif = ARGV[3]
    FS = ","
}
{
    if($colonne ~ motif) {
        print $0
    }
}
END{
    exit 0
}
