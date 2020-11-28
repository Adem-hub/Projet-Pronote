import requests
from bs4 import BeautifulSoup  #Permet de recuperer des infos sur une page html
from selenium import webdriver #Permet d'appuyer sur des boutons, d'aller sur le navigateur notamment
from selenium.webdriver.firefox.options import Options #Permet de modifier les attributs de la requete
import time
import os
import requests #FAire des requetes
import json 


options = Options()
options.add_argument('--headless') #Ne pas afficher la page


os.chdir("C:\\Users\\Ridha\\Desktop\\Pronote")
path="C:\\Users\\Ridha\\Desktop\\Pronote"



class Pronote:
    def __init__(self,ide,mdp,token_pushbullet):
        #La c'est les attrs, la personne rentre donc son ID et son mdp ENT pour justement qu'on accede à Pronote ainsi que ses Notes justement. Le token pushbullet est utilisé ici pour envoyer des notifications grace a l'application pushbullet sur telephone. Pour l'obtenir: Creer un compte --> Reglages --> Creer un token. L'attribut driver lui permet d'acceder au Nagivateur Firefox. Puis ensuite, on appelle les methodes Aller_Sur_Pronote, puis Onglet_Moyenne
        self.identifiant=ide
        self.mdp=mdp
        self.token_pushbullet=token_pushbullet
        self.driver = webdriver.Firefox(options=options,executable_path='C://Users//Ridha//.wdm//drivers//geckodriver//win64//v0.28.0//geckodriver.exe')
        self.Aller_Sur_Pronote()
        self.Onglet_Moyenne()

#Comme dit precedemment, cette methode permet d'envoyer les notifs. On ecrit ce que l'on veut envoyer (titre, msg) sur un fichier Json, puis on push, donc on envoie gräce a une requete le titre et le message au destinataire, grace a son token. Le resp.status_code ici permet de gerer les erreurs, enfin presque. Si il est egal à 200, alors ca signifie qu'il n'y a eu aucune erreur, que le message a bien été envoyé. Sinon, ca signifie qu'il y a une erreur qq part (message unqiement accepté, erreur dans le json, acces refusé, paiment requis etc... tous ces status correspondent à un nombre. Celui qui ne comprend aucune erreur est donc le 200)
    def pushbullet_message(self,title, body):
        msg = {"type": "note", "title": title, "body": body}
        TOKEN = 'PUSHBULLET_TOKEN'
        resp = requests.post('https://api.pushbullet.com/v2/pushes',
                            data=json.dumps(msg),
                            headers={'Authorization': 'Bearer ' + self.token_pushbullet,
                                    'Content-Type': 'application/json'})
        if resp.status_code != 200:
            raise Exception('Error',resp.status_code)
        else:
            print ('Message envoyé')
#Grace a Selenium, on va reussir à naviguer sur la page web. en effet, on va ller sur l'ent , remplir les cases nom et prénom, valider, puis aller sur Pronote. les time.sleep lors des differentes modifications de la page permettent de laisser du temps à la page pour charger mais aussi pour faire en sorte que la page ne detecte pas que l'on est un robot. On switch ensuite de fenetre car Proonote s'ouvre sur un deuxieme onglet.
    def Aller_Sur_Pronote(self):
        self.driver.get("https://ent.iledefrance.fr/auth/login?callback=https%3A%2F%2Fent.iledefrance.fr%2Ftimeline%2Ftimeline")

        time.sleep(5)
        id = self.driver.find_element_by_id('email')
        password= self.driver.find_element_by_id('password')

        id.send_keys(self.identifiant)
        password.send_keys(self.mdp)
        password.submit()
        time.sleep(8)

        apps=self.driver.find_elements_by_class_name('apps')[0]

        apps.click()
        time.sleep(5)
        pronote=self.driver.find_elements_by_class_name('pronote')[0]
        pronote.click()
        self.driver.switch_to.window(self.driver.window_handles[1])

        print("C'est bon tu est sur Pronote ! ")

#Ici on va chercher le petit onglet qui correspond a la moyenne sur pronote, si tout c'est passé sans aucune erreur, on lance la methode qui permet de récuperer les notes. S'il y en a une , alors on ferme le driver et on passe à la personne suivante dans la boucle. L'erreur est soit due à un time.sleep trop faicle, ne permettant pas a la page de charger, soit à une erreur que l'on ne peut résoudre, la page à mal chargé ou bien ell detecte que l'onn est un bot.
    def Onglet_Moyenne(self):
        try:
            time.sleep(5)
            Notes=self.driver.find_elements_by_class_name("label-menu_niveau0")[3]
            Notes.click()
            time.sleep(3)
            print("Tres bien, maintenant va chercher tes moyennes avec la methode Moyenne")
            self.Analyse_Nouvelle_Note()
            self.driver.quit()
        except:
            print("Une petite erreur visiblement!")
            self.driver.quit()


#Le programme ici ne fonctionne pas pour le moment, ou presque, à cause du probleme current avec les trimestres. En effet, le programme, lorsqu'il clique sur l'onglet note, le trimesre 2 apparaît automatiquement car on a depassé la date du 1er. Or le 2nd ne contient aucune note, et donc pas de bouton 'chronologique' sur lequel on peut appuyer et recuperer le nombre de notes (pourquoi pas ajouter un argument à la class qui choisit le trimestre). Si jamais des notes sont ajoutées, on compte le nombre de notes, grace au nombre de tableaux dans l'html de la page. Puis, dans un second temps, on lit dans un fhichier le nombre de notes qu'il avait auparavant. Si le fichier n'existe pas, on en lui crée un avec son nom, et on ecrit le nombre de notes. enfin, si le nombre de notes sur le fichier texte et le nombre de notes lorsqu'on lance le programme est different, cela veut dire qu'une nouvelle note a été ajoutée. On envoie donc une notification à l'utilisateur, l'informant de la note, de la moyenne de la classe et de la meilleur note. 
    def Analyse_Nouvelle_Note(self):
        #On se place dans le button radio chronologique, et on compte le nombre de notes
        Label=self.driver.find_elements_by_tag_name("label")
        Label[2].click()
        time.sleep(3)
        page=self.driver.page_source
        soup = BeautifulSoup(page)
        Tr_Notes=soup.find_all("tr")
        Toutes_les_Notes=len(Tr_Notes)-1
        
        Nom_Prenom=self.identifiant.replace('.',' ')
        #On ecrit le nombre de notes dans le fichier qui correspond. Si il n'existe pas, on le crée.
        try:
            with open(Nom_Prenom+'.txt','r') as file:
                len_Notes=int(file.read())
               
        except:
            with open(Nom_Prenom+'.txt','w+') as file:
                file.write(str(Toutes_les_Notes))
                len_Notes=Toutes_les_Notes
        #On send la ou les notif(s)
        if Toutes_les_Notes!=int(len_Notes):
            for i in range(Toutes_les_Notes -int(len_Notes)):
                self.pushbullet_message('Pronote : Une nouvelle note est apparue !', str(Tr_Notes[i+1].get_text()))
            with open(Nom_Prenom+'.txt','w') as file:
                file.write(str(Toutes_les_Notes))
                
        else:
            print('Rien de neuf')
