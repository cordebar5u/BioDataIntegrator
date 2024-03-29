import os, os.path
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import re

class Symptome :
	""" Objet représentant un symptôme"""

	def __init__(self, id: str = None, symptome: str = None, synonyme: str = None):
		self.id: str = id
		self.symptome: str = symptome
		self.synonyme: str = synonyme

	def setId(self,id: str):
		self.id = id

	def setSymptome(self,symptome: str):
		self.symptome = symptome

	def setSynonyme(self,synonyme: str):
		self.synonyme = synonyme

	def getId(self) -> str:
		return self.id

	def getSymptome(self) -> str:
		return self.symptome
	
	def getSynonyme(self) -> str:
		return self.synonyme
	

# Définit le schéma de l'index
	
def creer_index():

	schema = Schema(id=ID(stored=True), symptome=TEXT(stored=True), synonyme=TEXT(stored=True))
	data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'HPO','index')
	ix = create_in(data_dir, schema)
	writer = ix.writer()
	
	# Ajoute les données à l'index
	ajout_donnees(writer)


# Ajoute les données à l'index
	
def ajout_donnees(writer):

	# Ouvrir le fichier
	donnee_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'HPO')
	donnee_fichier = os.path.join(donnee_dir, 'hpo.obo')
	fichier = open(donnee_fichier, "r")
	 
	# Lire le fichier ligne par ligne
	ligne = fichier.readline()
	symptome:Symptome = None

	while (ligne != ""):
		if ligne == "[Term]\n":
			if (symptome != None):
				writer.add_document(id = symptome.getId(), symptome = symptome.getSymptome(), synonyme = symptome.getSynonyme())
			symptome = Symptome()

		elif ligne.startswith("id: HP:"):
			id = ligne.replace("id: HP:","").replace("\n","")
			symptome.setId(id)

		elif ligne.startswith("name: "):
			symptome.setSymptome(ligne.replace("name: ","").replace("\n",""))

		elif ligne.startswith("synonym: "):
			ligne = ligne.replace("synonym: ","").replace("\n","")
			texte = re.findall(r'\"(.*?)\"', ligne)
			if symptome.getSynonyme() == None:
				symptome.setSynonyme(texte[0])
			else:
				symptome.setSymptome(symptome.getSynonyme() + ", " + texte[0])
		ligne = fichier.readline()
	writer.commit()
	fichier.close()

def recherche_symptome(symptome: str, verbose: bool = False):

	# Regarde si l'index existe
	donnee_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'HPO', 'index')
	try:
		ix = open_dir(donnee_dir)
	except:
		creer_index()
		ix = open_dir(donnee_dir)
	
	# Recherche dans l'index
	parser = QueryParser("symptome",ix.schema)
	myquery = parser.parse(symptome)
	s = ix.searcher()
	resultats = s.search(myquery)

	# Affiche les résultats si demandé
	if verbose :
		print("Résultats de la recherche :")
		for resultat in resultats :
			chaine = "===" + resultat.get("id") + "===\n"
			chaine = chaine + resultat.get("symptome") + "\n"
			if resultat.get("synonyme") != None:
				chaine = chaine + resultat.get("synonyme") + "\n"
			print(chaine)

	resultatsListe = list()
	for resultat in resultats :
		resultatsListe.append("HPO:" + resultat.get("id"))
	return resultatsListe

def test():
	creer_index()
	print(recherche_symptome("abnormality of the nervous system", False))


if __name__ == "__main__":
	creer_index()
	test()