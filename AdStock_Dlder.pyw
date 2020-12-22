import requests
from bs4 import BeautifulSoup
import re
import os
import time
from tkinter import *
from PIL import Image,ImageTk
import PIL
import sys

def f_image(chemin,name_ph,sizex=166,sizey=50):
    name_ph=Image.open(chemin)
    name_ph=name_ph.resize((sizex,sizey))
    name_ph=ImageTk.PhotoImage(name_ph)
    return name_ph





def download_pic(liste_link,limite,chemin,recherche):
    for i in range(limite):
        lien=liste_link[i]
        requete = requests.get(lien)
        page = requete.content
        soup = BeautifulSoup(page,features="html.parser")
        all_links = soup.find_all("meta")
        #[print(all_links[x]) for x in range(len(all_links))]
        principale_picture=all_links[7]["content"]
        file1=open(chemin+recherche.title()+"/links.txt","a")
        file1.write(str(i)+"  "+lien+"\n")
        file1.close()

        try:
            aaa=requests.get(principale_picture)
            file_ = open(chemin+recherche.title()+"/Image_"+recherche.title()+"_"+str(i)+".jpg", "wb")
            file_.write(aaa.content)
            file_.close()
        except requests.exceptions.MissingSchema:
            continue



def link_finder(recherche,chemin):
    lien="https://stock.adobe.com/fr/search?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bcontent_type%3Aimage%5D=1&k="+recherche+"&order=relevance&safe_search=1&search_page=1&search_type=usertyped&acp=&aco=+"+recherche+"&get_facets=0"
    requete = requests.get(lien)
    page = requete.content
    soup = BeautifulSoup(page,features="html.parser")
    all_links = soup.find_all("a",{"class": "js-search-result-thumbnail non-js-link"})
    #all_links=str(all_links).split('<a class="js-search-result-thumbnail non-js-link"') 
    liste_link=[]
    for i in range(len(all_links)-1):
        try:
            liste_link.append(all_links[i]["href"])
        except IndexError:
            continue
    if len(liste_link)>1:
        try:
            if not os.path.exists(chemin):
                os.makedirs(chemin)
            os.mkdir(chemin+recherche.title())
        except FileExistsError:
            print("dossier déjà existant")
        return len(liste_link),liste_link
    else:
        return "aucune image trouvée désolée",liste_link
        
    

class App():
    def __init__(self):
        self.fenetre1=Tk()
        self.fenetre1.title("AdStock_Dlder")
        self.fenetre1.geometry("500x500+710+290")
        self.chemin=""
        self.recherche=""
        self.liste=[]
        self.entree1,self.entree2,self.entree3="","",""
        self.cansv=""
        self.first()

    
    def first(self):
        write_color="white"
        self.cansv=Canvas(self.fenetre1,width=500,height=500,bd=-2)
        self.cansv.pack()
        logo,valider_b,check,bg="","","",""
        logo=f_image("C:/Users/Antonin Achard/Desktop/AdStock/asddownloader.png",logo,70,70)
        valider_b=f_image("C:/Users/Antonin Achard/Desktop/AdStock/valider.png",valider_b,70,70)
        check=f_image("C:/Users/Antonin Achard/Desktop/AdStock/check2.png",check,30,30)
        bg=f_image("C:/Users/Antonin Achard/Desktop/AdStock/background.jpg",bg,800,540)
        self.cansv.create_image(250,250,image=bg)
        self.cansv.create_image(250,10,image=logo,anchor=N)
        
        self.cansv.create_text(250,100,text="Adobe Stock Downloader",anchor=N,font=("Arial",25),fill=write_color)
        self.cansv.create_text(250,150,text="Que voulez vous télécharger ?",font=(30),fill=write_color)
        self.entree1 = Entry(self.cansv,width=40,font=(15))
        self.cansv.create_window(250,180,height=25,window=self.entree1)

        self.cansv.create_text(250,220,text="Dans quel dossier voulez vous stocker les images ?",font=(30),fill=write_color)
        self.cansv.create_text(250,240,text="ex: C:/Users/Username/Desktop/photos_de_chat/",font=(25),fill="grey")
        self.entree2 = Entry(self.cansv,width=40,font=(15))
        self.cansv.create_window(250,260,height=25,window=self.entree2,anchor=N)

        liste,dossier,recherche="","",""
        bouton_valider=self.cansv.create_image(250,280,image=valider_b,anchor=N)
        self.cansv.tag_bind(bouton_valider,"<Button-1>",self.launch_download)
        self.sontdisp=self.cansv.create_text(250,350,text="",font=(15),fill=write_color)
        self.combien=self.cansv.create_text(250,370,text="",font=(15),fill=write_color)
        self.entree3=Entry(self.cansv,width=5,font=(15))
        self.combien2=self.cansv.create_window(260,390,anchor=NE,state=HIDDEN,window=self.entree3)
        self.checkb=self.cansv.create_image(290,385,image=check,state=HIDDEN,anchor=NE)
        self.cansv.tag_bind(self.checkb,"<Button-1>",self.download)
        self.complete=self.cansv.create_text(250,450,text="Téléchargement terminé !",font=(15),state=HIDDEN,fill=write_color)
        self.fenetre1.mainloop()
    
    def launch_download(self,event):
            self.recherche=self.entree1.get()
            self.dossier=self.entree2.get()
            total,self.liste=link_finder(self.recherche,self.dossier)
            if isinstance(total,int):
                self.cansv.itemconfig(self.sontdisp,text="{} images sont disponibles".format(total))
                self.cansv.itemconfig(self.combien,text="Combien en voulez vous ?")
                self.cansv.itemconfig(self.combien2,state=NORMAL)
                self.cansv.itemconfig(self.checkb,state=NORMAL)
            else:
                def yo():
                    self.cansv.itemconfig(self.sontdisp,text="")
                
                self.cansv.itemconfig(self.sontdisp,text="Désolé aucune image disponible")
                self.cansv.after(3000,yo)
    
    def download(self,event):
        def disspation():
            self.cansv.itemconfig(self.complete,state=HIDDEN)
            self.cansv.itemconfig(self.sontdisp,text="")
            self.cansv.itemconfig(self.combien,text="")
            self.cansv.itemconfig(self.combien2,state=HIDDEN)
            self.cansv.itemconfig(self.checkb,state=HIDDEN)
        
        limite=int(self.entree3.get())
        download_pic(self.liste,limite,self.dossier,self.recherche)
        self.cansv.itemconfig(self.complete,state=NORMAL)
        self.cansv.after(3000,disspation)
    
hey=App()