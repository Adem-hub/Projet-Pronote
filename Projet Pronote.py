import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
import requests
import json


options = Options()
options.add_argument('--headless')


os.chdir("C:\\Users\\Ridha\\Desktop\\Pronote")
path="C:\\Users\\Ridha\\Desktop\\Pronote"



class Pronote:
    def __init__(self,ide,mdp,token_pushbullet):
        self.identifiant=ide
        self.mdp=mdp
        self.token_pushbullet=token_pushbullet
        self.driver = webdriver.Firefox(options=options,executable_path='C://Users//Ridha//.wdm//drivers//geckodriver//win64//v0.28.0//geckodriver.exe')
        self.Aller_Sur_Pronote()
        self.Onglet_Moyenne()


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


    def Analyse_Nouvelle_Note(self):
        #On se place dans le button radio chronologique, et on compte le nombre de notes
        Label=self.driver.find_elements_by_tag_name("label")
        Label[2].click()
        time.sleep(3)
        page=self.driver.page_source
        soup = BeautifulSoup(page)
        Tr_Notes=soup.find_all("tr")
        Toutes_les_Notes=len(Tr_Notes)-1

        #On ecrit le nombre de notes dans le fichier qui correspond. Si il n'existe pas, on le crée.
        try:
            with open(self.identifiant+'.txt','r') as file:
                len_Notes=int(file.read())
                file.close()
        except:
            with open(self.identifiant+'.txt','w+') as file:
                file.write(str(Toutes_les_Notes))
                len_Notes=Toutes_les_Notes
                file.close()

        #On send la ou les notif(s)
        if Toutes_les_Notes!=int(len_Notes):
            for i in range(Toutes_les_Notes -int(len_Notes)):
                self.pushbullet_message('Pronote : Une nouvelle note est apparue !', str(Tr_Notes[i+1].get_text()))
            with open(self.identifiant+'.txt','w') as file:
                file.write(str(Toutes_les_Notes))
                file.close()
        else:
            print('Rien de neuf')





def Look_New_Mark():
    while True:
        Othman=Pronote('othman.boudarga','Boudarga31082005',"o.J669zeEpYeZpHcWte0C0tt5ONmkXgZsr")
        Adem=Pronote('adem.benrhouma','Adem2003@',"o.J669zeEpYeZpHcWte0C0tt5ONmkXgZsr")
        time.sleep(1200)





















