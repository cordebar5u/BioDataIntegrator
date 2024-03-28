from lxml import etree


### --- Fichier python permettant de conserver uniquement les éléments de la base de données drungbank qui nous intéressent --- ###

def conserver_elements_specifiques(fichier_xml):
    tree = etree.parse(fichier_xml)
    root = tree.getroot()
    
    # Gestion des espaces de noms
    ns = {'db': 'http://www.drugbank.ca'}

    for drug in root.findall('db:drug', namespaces=ns):
        # Conserver la première balise <name>
        first_name = drug.find('db:name', namespaces=ns)
        
        # Identifier tous les éléments à supprimer
        elements_a_supprimer = []
        for child in drug:
            if child.tag not in [etree.QName(ns['db'], 'indication'), etree.QName(ns['db'], 'toxicity'), etree.QName(ns['db'], 'atc-codes'), etree.QName(ns['db'], 'synonyms')] and child != first_name:
                elements_a_supprimer.append(child)

        # Supprimer les éléments non désirés
        for element in elements_a_supprimer:
            drug.remove(element)
        
        # Conserver uniquement les enfants de <atc-codes> et <synonyms>
        for atc_code in drug.findall('db:atc-codes', namespaces=ns):
            for child in atc_code:
                if child.tag != etree.QName(ns['db'], 'atc-code'):
                    atc_code.remove(child)

        for synonym in drug.findall('db:synonyms', namespaces=ns):
            for child in synonym:
                if child.tag != etree.QName(ns['db'], 'synonym'):
                    synonym.remove(child)

    # Sauvegarder le fichier modifié
    tree.write('data/DRUGBANK/drugbank_modifiee.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8')

# Utiliser la fonction sur votre fichier
conserver_elements_specifiques('data/DRUGBANK/drugbank.xml')
