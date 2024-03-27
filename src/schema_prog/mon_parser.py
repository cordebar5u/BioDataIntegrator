import xml.sax

class MyContentHandler(xml.sax.ContentHandler):
    def __init__(self, indication_recherchee):
        self.indication_recherchee = indication_recherchee
        self.current_element = ''
        self.current_content = ''  # Utilisé pour accumuler le contenu textuel
        self.current_name = ''
        self.current_indication = ''
        self.medicaments_trouves = []

    def startElement(self, name, attrs):
        self.current_element = name
        self.current_content = ''  # Réinitialiser pour le nouvel élément

    def characters(self, content):
        self.current_content += content.strip()  # Accumuler le contenu

    def endElement(self, name):
        if name == 'name':
            self.current_name = self.current_content
        elif name == 'indication':
            self.current_indication = self.current_content

        if name == 'drug':
            if self.indication_recherchee in self.current_indication:
                self.medicaments_trouves.append(self.current_name)
                            
            # Réinitialiser les variables pour le prochain élément <drug>
            self.current_name = ''
            self.current_indication = ''

def rechercher_medicament_par_indication(fichier_xml, indication):
    handler = MyContentHandler(indication)
    xml.sax.parse(fichier_xml, handler)
    return handler.medicaments_trouves



class MyContentHandler2(xml.sax.ContentHandler):
    def __init__(self, toxicity_recherchee):
        self.toxicity_recherchee = toxicity_recherchee
        self.current_element = ''
        self.current_content = ''  # Utilisé pour accumuler le contenu textuel
        self.current_name = ''
        self.current_toxicity = ''
        self.medicaments_trouves = []

    def startElement(self, name, attrs):
        self.current_element = name
        self.current_content = ''  # Réinitialiser pour le nouvel élément

    def characters(self, content):
        self.current_content += content.strip()  # Accumuler le contenu

    def endElement(self, name):
        if name == 'name':
            self.current_name = self.current_content
        elif name == 'toxicity':
            self.current_toxicity = self.current_content

        if name == 'drug':
            if self.toxicity_recherchee in self.current_toxicity:
                self.medicaments_trouves.append(self.current_name)
                            
            # Réinitialiser les variables pour le prochain élément <drug>
            self.current_name = ''
            self.current_toxicity = ''

def rechercher_medicament_par_toxicity(fichier_xml, toxicity):
    handler = MyContentHandler2(toxicity)
    xml.sax.parse(fichier_xml, handler)
    return handler.medicaments_trouves


def  rechercher_medicament(fichier_xml, indication, toxicity):
    if indication != '':
        medicaments = rechercher_medicament_par_indication(fichier_xml, indication)
    else:
        medicaments = rechercher_medicament_par_toxicity(fichier_xml, toxicity)
    for medicament in medicaments:
        print(medicament)


rechercher_medicament("../../data/DRUGBANK/drugbank.xml", "thrombocytopenia","")
#rechercher_medicament("../../data/DRUGBANK/drugbank.xml","", "Renal failure")



# Utilisation de la fonction
#medicaments = rechercher_medicament_par_indication("/Users/benjamincordebar/Desktop/2A/S8/SGBD/biodataintegrator/data/DRUGBANK/drugbank.xml", "thrombocytopenia")

# Afficher les noms des médicaments trouvés
#for medicament in medicaments:
#    print(medicament)
        

# Utilisation de la fonction
#medicaments = rechercher_medicament_par_toxicity("mon_document2.xml", "Renal failure")

# Afficher les noms des médicaments trouvés
#for medicament in medicaments:
#    print(medicament)

