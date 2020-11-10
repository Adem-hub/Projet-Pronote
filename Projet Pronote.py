import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

options = Options()
options.add_argument('--headless')







class Pronote:
    def __init__(self,ide,mdp):
        self.identifiant=ide
        self.mdp=mdp
        self.driver = webdriver.Firefox(options=options,executable_path='C://Users//Ridha//.wdm//drivers//geckodriver//win64//v0.28.0//geckodriver.exe')


    def Aller_Sur_Pronote(self):
        self.driver.get("https://ent.iledefrance.fr/auth/login?callback=https%3A%2F%2Fent.iledefrance.fr%2Ftimeline%2Ftimeline")

        time.sleep(5)
        id = self.driver.find_element_by_id('email')
        password= self.driver.find_element_by_id('password')

        id.send_keys(self.identifiant)
        password.send_keys(self.mdp)
        password.submit()
        time.sleep(5)

        apps=self.driver.find_elements_by_class_name('apps')[0]
        apps.click()
        time.sleep(5)
        pronote=self.driver.find_elements_by_class_name('pronote')[0]
        pronote.click()
        self.driver.switch_to.window(self.driver.window_handles[1])

        print("C'est bon tu est sur Pronote ! ")


    def Onglet_Moyenne(self):
        try:
            time.sleep(7)
            Notes=self.driver.find_elements_by_id("GInterface.Instances[0].Instances[1]_Combo2")[0]
            Notes.click()
            time.sleep(5)
            print("Tres bien, maintenant va chercher tes moyennes avec la methode Moyenne")
        except:
            print("tu dois d'abord aller sur Pronote!")

    def Moyenne(self,nom):

        a=self.driver.page_source
        soup = BeautifulSoup(a)
        b=soup.find_all("div", class_="Gras Espace")
        Dico={}
        for elt in b:
            if nom.upper() in elt['aria-label']:
                hey=elt.find('div',style="float: right;")
                Note=hey.text
                Matiere=elt.text.replace(Note,'')
                Matiere=Matiere.replace(' ','')
                Dico[Matiere]=Note
        if Dico=={}:
            return "est tu allé sur l'onglet Moyenne ?"
        return Dico










