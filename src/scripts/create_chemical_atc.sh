#!/bin/bash
chmod +x src/scripts/*.sh
src/scripts/request_TSV.sh data/STITCH\ -\ ATC/chemical.sources.v5.0.tsv  3 'ATC' 0 > data/STITCH\ -\ ATC/chemical_atc.tsv