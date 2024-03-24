#! /bin/sh

sed -n '/\*FIELD\* CS/,/\*FIELD\*/p' omim.txt > temp.txt
grep -oP '^[A-Za-z ]*(?=:\s*$)' temp.txt | cut -d: -f1 | sort -u -f > CS_categories.txt 

#(?=:\s*$) assertion positive pour voir si il y a un : et un ou plusieurs signes d'espacements à la fin de la ligne