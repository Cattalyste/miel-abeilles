# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 20:15:38 2023

@author: Saganne
"""

import random
import sys
from math import sqrt
import matplotlib.pyplot as plt
import time
import numpy as np
#import graphviz                            #mis en commentaire car n'est pas présent sur l'environnement de tout le monde merci de le télécharger par avance
import winsound

class Environnement:                        #class qui gère l'espace de jeu des abeilles et qui créer la matrice des distances
    def __init__(self):
        self.fleurs_layout = [796,310],[774,130],[116,69],[908,534],[708,99],[444,428],[220,307],[501,287],[345,560],[628,311],[901,639],[436,619],[938,646],[45,549],[837,787],[328,489],[278,434],[704,995],[101,482],[921,964],[493,970],[494,898],[929,389],[730,742],[528,794],[371,429],[98,711],[724,631],[573,903],[964,726],[213,639],[549,329],[684,273],[273,105],[897,324],[508,31],[758,405],[862,361],[898,898],[2,897],[951,209],[189,739],[602,68],[437,601],[330,410],[3,517],[643,404],[875,407],[761,772],[276,666]
        self.dist_array=[]
        temp=[]
        
        for i in range(50):                 #Fct qui calcule la matrice des distances euclidienne une seule fois pour économiser du temps de calculs par la suite car pour chaque demande ce sera un temps de lecture et non de calcul
            for j in range(50):
                temp.append(int(sqrt(pow(self.fleurs_layout[j][0]-self.fleurs_layout[i][0],2) +
                                     pow(self.fleurs_layout[j][1]-self.fleurs_layout[i][1],2))))      #calcul de la distance euclidienne entre chaque pairs de fleur par rapport à la ième fleur
            self.dist_array.append(temp)                                                         #ajout de chaque ligne à notre variable qui sauvegarde toute les distances
            temp=[]                                                                         #remise à 0 de notre variable qui represente une ligne dans notre tableau 2D
        
    def calc_path(self,arr):                #fct qui retourne le score d'une abeille et additionnant les distance intra-fleur ainsi que le départ et le retour à la ruche
        dist=[]
        dist.append(int(sqrt(pow(self.fleurs_layout[arr[0]][0]-500,2) + pow(self.fleurs_layout[arr[0]][1]-500,2)))) #ajout de la distance ruche => première fleur
        for i in range(len(arr)-1):
            dist.append(self.dist_array[arr[i]][arr[i+1]])                                                                   #ajout de l'ensemble des distances intra-fleurs
        dist.append(int(sqrt(pow(self.fleurs_layout[arr[49]][0]-500,2) + pow(self.fleurs_layout[arr[49]][1]-500,2)))) #ajout de la distance dernière fleur => ruche
        return int(sum(dist)),dist    




class Bee():                                #classe abeille qui contient les différent attributs des abeilles en tant qu'individu
    identifiant=0                           #attribut initialisé à 0 qui correspond à la "carte d'identité" unique d'une abeille de la colonie
    def end():
        Bee.identifiant=0                   #fct utilisé lors de la création de multiple ruche pour reprendre une ruche à 0
    
    def create_random(self,terrain):        #fct utilisé pour la génération de la première génétation d'abeille avec un patern totalement aléatoire
        self.path=random.sample(range(len(terrain.fleurs_layout)),len(terrain.fleurs_layout))   #création d'une liste aléatoire contenant une unique fois chaques fleurs
        self.score,self.score_array=terrain.calc_path(self.path)                                            #création de 2 attribu : la somme des distances (score final) et un array des scores intermédiaires
        self.id=Bee.identifiant                                                                             #création d'un identifiant unique (arbre généa)
        Bee.identifiant+=1                                                                                  #incrémentation de l'attribu unique de l'identifiant
        self.parent=[-1,-1]                                                                                 #création de l'attribut parent
    
    def delete_duplicate(self):
        self.path=list(dict.fromkeys(self.path))                                                            #suppression des doublons sans changer l'ordre des fleurs
    def add_missing(self):
        temp = [ele for ele in range(50) if ele not in self.path]                       #ajout des fleurs manquantes dans le chemin de l'abeille de façon aléatoire
        for i in temp:
            self.path.insert(random.randint(0,len(self.path)-1),i)

    def mutation(self,mode):                                                            #création de la fonctione mutation qui prend un mode en input afin de définir comment seront fait les mutations
        if mode == 0:                                                                   #avec le mode à 0 cela fait glisser l'ordre des fleurs en placant la fleur initiale à la fin de la liste d'une abeille si le nombre aléatoire généré entre 0 et 100 inclus est inférieur au seuil défini par l'utilisateur
            if random.randint(0, 100) < pourcen_muta_rota:
                self.path.append(self.path.pop(0))                                      #permet d'intervetir 2 éléments dans une liste sans utiliser de valeurs tampon en réutilisant l'élément supprimé par pop dans un append
        if mode == 1:                                                                   #mode 1 equivaut à intervertir 2 fleurs dans la liste d'une abeille
            if random.randint(0, 100) < pourcen_muta_swap:
                indice = random.sample(range(0, 49), nb_swap*2)
                for i in indice[::2]:                                                   #permet de parcourir la liste indice avec un pas de 2 (en sautant une valeurs à chaque fois)
                    self.path.insert(i, self.path.pop(i+1))                             #utilise 2 elements de la liste indice pour swap les fleurs à ces indices
        if mode == 2:                                                                   #si le mode est à 2 on utilise les 2 précédentes mutation avec leur propre probabilité indépendante
            self.mutation(0)
            self.mutation(1)


    def create_baseline(self,breeder,mode_muta):                                        #fonctione commune aux différentes façon utilisé pour créer une abeille
        self.mutation(mode_muta)                                                        #appel la fonction mutation si un mode est défini
        self.id=Bee.identifiant                                                         #attribue un identifiant unique puis l'incrémente à la ligne suivant
        Bee.identifiant+=1
        self.parent=[breeder[0].id,breeder[1].id]                                       #attribue l'id des parents afin de pouvoir creer l'arbre généalogique d'une abeille en fin de ruche
        self.delete_duplicate()                                                         #appel la fonction qui supprime les doublons
        self.add_missing()                                                              #appel la fonction qui ajoute les fleurs manquantes
        self.score,self.score_array=terrain.calc_path(self.path)                        #calcul le score de cet abeille ainsi que la liste des distances intermédiaires (initialement pour calculer le degré d'effiscience dans son parcours)
        
    def create_abeille(self,breeder,mode_decoupe_genome,mode_muta):                     #fonction qui créer une abeille selon différentes règles
        if mode_decoupe_genome == 0 :                                                   #si le mode de découpe est à 0 on utilise la première moitié du génome du premier parent puis la second moitié du deuxieme parent
            self.path = breeder[0].path[:25]+breeder[1].path[25:]    
            self.create_baseline(breeder,mode_muta)                                     #appel la fct de création commune
        elif mode_decoupe_genome == 1 :                                                 #avec le mode =1 on découpe le génome selon un pivot choisi aléatoirement en conservant la fleur initiale du parent1 et la derniere fleur du parent2 dans un cas extreme
            alea=random.randint(1,48)
            self.path = breeder[0].path[:alea]+breeder[1].path[alea:]    
            self.create_baseline(breeder,mode_muta)
        elif mode_decoupe_genome == 2:                                                  #création du chemin d'une abeille à partir de 2 pivots ainsi une première partie du parent1 est choisi puis une seconde du parents2 et enfin on complete la fin avec le parent1
            alea1=random.randint(0,25)
            alea2=random.randint(25,49)
            self.path = breeder[0].path[:alea1]+breeder[1].path[alea1:alea2]+breeder[0].path[alea2:]
            self.create_baseline(breeder,mode_muta)


class Beehive():#classe qui représente la ruche et centralise beaucoup de paramètre de configuration
    
    def __init__(self,terrain,nb_abeille_conserve_entre_chaque_generation,mode_selection_parent,mode_selection_genome,mode_mutation):
        self.nb_ab=nb_abeille_conserve_entre_chaque_generation
        self.mode_selection_parent=mode_selection_parent
        self.mode_selection_genome=mode_selection_genome
        self.mode_mutation=mode_mutation
        self.nb_abeille = 100
        self.population=[]
        self.old_population=[]
        self.score_ruche=[]
        self.parent_array=[]
        for i in range(self.nb_abeille):       #création de notre ruche de 100 abeilles ouvrières
            self.population.append(Bee())
            self.population[i].create_random(terrain) #appel de la fonction création aléa qui génère des abeilles avec un parcour aléatoire
        
    def sort(self):                                                         #classe les abeille d'une génération dans la ruche selon leurs score respectifs
        self.population=sorted(self.population,key=lambda x:x.score)
        score_temp=sum(x.score for x in self.population)
        self.score_ruche.append(int(score_temp/self.nb_abeille))            #additione les scores sur la ligne précédente et divise par le nombre d'abeille pour obtenir le score moyen d'une génération
    
    def select(self,parent_array=[]):
        if self.mode_selection_parent == 0 :
            return random.choices(self.population[:self.nb_ab],k=2) #selectionne 2 parents dans les abeilles conservé entre chaque génération selon une loi d'aléatoire uniforme p(abeille0)=p(abeille49) et selon un tirage avec remise
        elif self.mode_selection_parent == 1 :
            weights=[int((1/(0.01*(i+5)**0.3))) for i in range(self.nb_ab)]
            return random.choices(self.population[:self.nb_ab],weights,k=2) #selectionne 2 parents dans le nb d'abeille conservé selon une loi de proba mathématique : (1/(0.01*(x+5)**0.3)) afin que les meilleurs ai plus de chances d'être selectionné parmis les parents conservés et selon un tirage avec remise
        elif self.mode_selection_parent == 2 :
            if parent_array==[]:
                parent_array=self.population[:self.nb_ab]                   #selectionne 2 parents parmis le nb d'abeille conservé et si ce parents n'a pas été déjà parents avant que tout les autre l'ai été (tirage sans remise)
            breeder=random.sample(parent_array,2)                           #selon une loi uniforme
            parent_array.remove(breeder[0])                                 #retire les parents de l'ensemble pouvant être tiré au sort
            parent_array.remove(breeder[1])
            return breeder,parent_array
    
    def breed(self,indice):
        if self.mode_selection_parent==2:
            temp_breeder,self.parent_array=self.select(self.parent_array)  #appel la fonctione de selection des parents
            self.population[indice].create_abeille(temp_breeder,self.mode_selection_genome,self.mode_mutation)
        else:
            temp_breeder=self.select()      #appel la fonctione de selection des parents
            self.population[indice].create_abeille(temp_breeder,self.mode_selection_genome,self.mode_mutation)  #creer une nouvelle abeille selon le mode choisi
    
    def nouvelle_generation(self,nombre_conserve):                #fct qui genere une nouvelle génération
        self.old_population += self.population[nombre_conserve:]  #conservation des ancienne abeille en mémoire
        del self.population[nombre_conserve:]                     #supprime les anciennes abeilles
        for i in range(self.nb_abeille-nombre_conserve):
            self.population.append(Bee())
            self.breed(i+nombre_conserve)                         #création de nouvelles abeilles
        ruche.sort()                                              #classement de la ruche selon le score des abeilles
    def end(self,nombre_conserve=None):                           #fct à lancer à la fin du programme pour sauvegarder les dernière abeilles
        self.old_population += self.population[:]
        del self.score_ruche[:]                                   #remise à 0 du score de la ruche dans le cas de création de plusieurs ruches



class Screen():                                                                 #classe gérant l'affichage en fin de programme
    def creation_path_parfait(self,ruche):                                      #fct qui permet de liste la liste des fleurs visité selon x et y afin de générer le chemin de la meilleur abeille
        path_x=[]
        path_y=[]
        path_x.append(500)                                                      #ajout de la ruche au départ
        path_y.append(500)
        for i in range(len(ruche.population[0].path)):
            path_x.append(terrain.fleurs_layout[ruche.population[0].path[i]][0])
            path_y.append(terrain.fleurs_layout[ruche.population[0].path[i]][1])
        path_x.append(500)                                                      #ajout de la ruche en fin de simulation
        path_y.append(500)
        return path_x,path_y 
    
    def show_path(self,ruche):                                                  #fait un plot du déplacement de la meilleur abeille
        path_parfait_x,path_parfait_y=self.creation_path_parfait(ruche)
        plt.plot(path_parfait_x, path_parfait_y, 'bo', linestyle="--")
        plt.title("Le score de ce chemin est : %i" %ruche.score_ruche[-1])
        plt.xlabel("La seed est : %i" %seed)
        plt.show()
    
    def show_genealogy(self,nb_abeille):
        f = graphviz.Digraph(filename = "output/Arbre_de_famille.gv")
        genealogy_table=[]
        ruche.end(nb_abeille)
        best=ruche.population[-100]
        genealogy_table.append(best.id,best.parent[0],best.parent[1])
        f.node(str(best.id))
        def recurence(abeille):
            if abeille.id==-1:
                return
            else:
                genealogy_table.append([abeille.id ,abeille.parent[0],abeille.parent[1]])
                f.node(str(abeille.id))
                recurence(abeille.parent[0])
                recurence(abeille.parent[1])
        
        for i in ruche.old_population :
            genealogy_table.append([i.id ,i.parent[0],i.parent[1]])
            f.node(str(i.id))

        for i in genealogy_table :
            if i[1] & i[2] != -1:
                f.edge(str(i[1]),str(i[0]))
                f.edge(str(i[2]),str(i[0]))
        f.format='png'
        f.render('my_graph', view=False) 
        
    def show_both(self,ruche):                                                  #fait un plot avec le score d'une ruche+le chemin de la meilleur abeille ainsi qu'un graphe montrant l'évolution du score de la ruche sur le temps
        path_parfait_x,path_parfait_y=self.creation_path_parfait(ruche)
        figure, axis = plt.subplots(1, 2,figsize=(16,4.5))
        axis[0].plot(ruche.score_ruche)

        axis[1].plot(path_parfait_x, path_parfait_y, 'bo', linestyle="--")
        axis[1].set_title("Le score de ce chemin est : %i" %ruche.score_ruche[-1])
        axis[1].set_xlabel("La seed est : %i" %seed)
        plt.show()

        print("Le nombre de génération :",len(ruche.score_ruche))
        print("Le score atteint est :",ruche.score_ruche[-1])
        print("La seed est :", seed)
        print("Le nombre de ruche est de :",nb_ruche)


timer1=time.time()
#score_moyen=[]
seed = random.randrange(sys.maxsize)                 #permet de conservé la seed afin de relancer une simulation à l'identique
rng = random.seed(seed)

nb_ruche=0                                           #initialisation de la variable nombre de ruche ainsi que de plusieurs variables
nombre_generation=1000
nb_abeille_conserve_entre_chaque_generation=50        #nombre d'abeilles conservées entre chaque générations
mode_selection_parent=2                               #0 pour prendre au hazard parmis x conservés selon loi uniforme avec remise, 1 pour prendre hasard selon coube biaisé avec remise, 2 pour prendre sans remise
mode_selection_genome=2                               #0 pour couper le genome en 50/50, 1 pour couper le génome aléatoirement, 2 pour couper selon 2 pivot
mode_mutation=1                                       #None pour aucune mutation, 0 pour le glissement des fleurs dans le path d'une abeille, 1 pour un échange de 2 fleurs dans le chemin de l'abeille, 2 pour une utilisation des 2 méthodes précédentes avec leurs proba respective et donc indépendantes
pourcen_muta_rota=75
pourcen_muta_swap=50
nb_swap=5                                             #nombre de PAIRES de fleurs qui vont être échangé

terrain=Environnement()                               #création du terrain de jeu des abeilles
plot=Screen()                                         #création de la variable qui appelle la classe plot
ruche=Beehive(terrain,nb_abeille_conserve_entre_chaque_generation,mode_selection_parent,mode_selection_genome,mode_mutation) #création de la ruche
ruche.sort()                                                                                                                #classement des abeilles
ruche.nouvelle_generation(nb_abeille_conserve_entre_chaque_generation)                                                      #génération d'une seconde génération



while ruche.score_ruche[-1]>12000 :                                                                     #recherche d'un score à atteindre avant de selectionner une nouvelle ruche
#while nb_ruche<100:
    seed = random.randrange(sys.maxsize)
    rng = random.seed(seed)                                                                             #utilisation d'une nouvelle seed pour une nouvelle ruche
    ruche.end()
    Bee.end()
    ruche=Beehive(terrain,nb_abeille_conserve_entre_chaque_generation,mode_selection_parent,mode_selection_genome,mode_mutation)
    ruche.sort()
    ruche.nouvelle_generation(nb_abeille_conserve_entre_chaque_generation)

    if mode_mutation != None:
        while len(ruche.score_ruche)<nombre_generation:                               #dans le cadre d'une reproduction avec mutation on va aller jusqu'au nombre de génération voulu
            ruche.nouvelle_generation(nb_abeille_conserve_entre_chaque_generation)
    else:
        while ruche.score_ruche[-1] != ruche.score_ruche[-2]:
            ruche.nouvelle_generation(nb_abeille_conserve_entre_chaque_generation)    #dans le cadre d'une reproduction sans mutation au bout d'un moments les abeilles sont des clones et donc on peut détecter la fin d'amélioration d'une ruche en comparant le score moyen entre deux génération qui devient identique et ne changera plus
    nb_ruche+=1
    #score_moyen.append(ruche.population[0].score)
print(int(time.time()-timer1))                                                        #affichage du temps de calcul pour comparer les méthodes
#print(sum(score_moyen)/len(score_moyen))
plot.show_both(ruche)                                                                 #affichage des plots voulus
#winsound.Beep(500, 500)                                                              #fait un son à la fin du programme (utile lors de la recherche de nouvelle ruche record afin d'être prevenus de la fin de la recherche et de la trouvaille d'une nouvelle pepite représentatant la génération ultime)



"""
#code utilisé lors de la génération d'une ruche unique
seed = random.randrange(sys.maxsize)
rng = random.seed(42)

nb_ruche=1
nombre_generation=5000
nb_abeille_conserve_entre_chaque_generation=70        #nombre d'abeilles conservées entre chaque générations
mode_selection_parent=2                               #0 pour prendre au hazard parmis x conservés, 1 pour prendre hasard selon coube biaisé
mode_selection_genome=2                               #0 pour couper le genome en 50/50, 1 pour couper le génome aléatoirement
mode_mutation=2
pourcen_muta_rota=50
pourcen_muta_swap=90


terrain=Environnement()
plot=Screen()
ruche=Beehive(terrain,nb_abeille_conserve_entre_chaque_generation,mode_selection_parent,mode_selection_genome,mode_mutation)
ruche.sort()
ruche.nouvelle_generation(nb_abeille_conserve_entre_chaque_generation)

if mode_mutation != None:
    while len(ruche.score_ruche)<nombre_generation:
        ruche.nouvelle_generation(nb_abeille_conserve_entre_chaque_generation)
else:
    while ruche.score_ruche[-1] != ruche.score_ruche[-2]:
        ruche.nouvelle_generation(nb_abeille_conserve_entre_chaque_generation)


plot.show_both(ruche)
"""



























