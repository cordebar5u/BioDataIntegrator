#!/bin/bash

# Vérifiez si le nombre correct d'arguments a été fourni
if [ "$#" -ne 4 ]; then
    exit 1
fi

# Assignez les arguments à des variables pour une meilleure lisibilité
keg_fichier=$1
testerColonne=$2
motif=$3
afficherColonne=$4

# Exécutez la commande
grep "^E" "$keg_fichier" | sed 's/  */,/g' | awk -F"," -v column=$testerColonne -v motif=$motif '{ if ($column ~ motif) { print $0 }}' | awk -F"," -v column=$afficherColonne 'BEGIN { printf "[" } NR > 1 { printf "," } { printf "%s", $column } END { printf "]\n" }'
