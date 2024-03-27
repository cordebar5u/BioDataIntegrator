import os, os.path
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

class Maladie :
    """ Objet représentant une maladie"""

    def __init__(self, id: str = None, symptome: str = None):
        self.id: str = id
        self.symptome: str = symptome

    def setId(self,id: str):
        self.id = id

    def setSymptome(self,symptome: str):
        self.symptome = symptome

    def getId(self) -> str:
        return self.id

    def getSymptome(self) -> str:
        return self.symptome


# Définit le schéma de l'index
def creer_index():
	schema = Schema(id=ID(stored=True), symptome=TEXT(stored=True))
	data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'OMIM','index')
	ix = create_in(data_dir, schema)
	writer = ix.writer()
	
	# Ajoute les données à l'index
	ajout_donnees(writer)


# Ajoute les données à l'index
def ajout_donnees(writer):

	# Ouvrir le fichier
	donnee_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'OMIM')
	donnee_fichier = os.path.join(donnee_dir, 'omim.txt')
	fichier = open(donnee_fichier, "r")
     
	# Lire le fichier ligne par ligne
	ligne = fichier.readline()
	maladie:Maladie = None

	while (ligne != ""):
		if ligne == "*RECORD*\n":
			if (maladie != None):
				writer.add_document(id = maladie.getId(), symptome = maladie.getSymptome())
			maladie = Maladie()

		elif ligne == "*FIELD* NO\n":
			ligne = fichier.readline()
			id = ligne.replace("\n","")
			maladie.setId(id)

		elif ligne == "*FIELD* CS\n":
			texte=""
			ligne=fichier.readline()
			while (ligne[0]!='*'):
				if ligne.find(":\n") == -1 :
					texte = texte + ligne
				ligne = fichier.readline()
			texte = texte.replace("\n","")
			texte = texte.replace(";","")
			texte.lower()
			maladie.setSymptome(texte)

		ligne = fichier.readline()
	writer.commit()
	fichier.close()

# Recherche dans l'index
def recherche(symptome: str, verbose =False):
      
	# Regarde si l'index existe
	data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'OMIM', 'index')
	try:
		print("Index trouvé")
		ix = open_dir(data_dir)
	except:
		creer_index()
		ix = open_dir(data_dir)

	# Recherche dans l'index
	parser = QueryParser("symptome",ix.schema)
	myquery = parser.parse(symptome)
	s = ix.searcher()
	results = s.search(myquery)

	print(verbose)
	# Affiche les résultats si demandé
	if verbose :
		print("Résultats de la recherche :")
		for result in results :
			chaine = "===\n" + result.get("id") + "===\n"
			chaine += "---\n" + str(result.get("symptome")) + "---\n"
			print(chaine)
	
	resultsList = list()
	for result in results :
		resultsList.append("OMIM:" + result.get("id"))
	return resultsList


def test():
	print(recherche("abnormality of the nervous system", True))

if __name__ == '__main__':
	creer_index()
	test()




