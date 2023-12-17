# miel-abeilles
Lors d'un projet concernant la recherche d'un chemin optimal parcourant différent point predéfini j'ai exploré différentes méthode et ce fichier python en est la conclusion.
Les différents paramètre sont à entrer en fin de script.
Il y a le nombre de génération à créer dans la ruche.
Le nombre d'abeille conservé entre 2 générations.
Le mode de séléction des parents :      0 tirage aléatoire uniforme parmis les abeille concervé avec remise
					1 tirage aléatoire favorisant les meilleures abeille parmis les abeille concervé avec remise
					2 tirage aléatoire uniforme parmis les abeille concervé sans remise

Mode de selection du génome :		0 creation du chemin à partir de la moitié du chemin du premier parent et de la moitié du chemin du deuxieme parent
					1 création du chemin en choisissant un point aléatoirement pour découper la séquence du chemin
					2 création du chemin en choissant 2 point aléatoire pour découper la séquence du chemin
Mode de mutation :			None aucune mutation
					0 Décale d'1 indice toute les position des fleurs sur la séquence d'une abeille
					1 Interverti 2 fleurs dans la séquence d'une abeille
					2 on utilise les 2 méthode ci dessus avec leurs méthode respectives
Le pourcentage de chance qu'une mutation de type décalage des fleurs intervienne
Le pourcentage de chance qu'une mutation de type intervertion des fleurs intervienne
Le nombre de fleurs à intervertir
La seed si necessaire pour reproduire un essai ou comparer différent essais
