import requests
from bs4 import BeautifulSoup
import re
import os
import time

def Fonction_principale(recherche,chemin):
    #recherche=str(input("que voulez-vous chercher ?: "))
    
    lien="https://stock.adobe.com/fr/search?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bcontent_type%3Aimage%5D=1&k="+recherche+"&order=relevance&safe_search=1&search_page=1&search_type=usertyped&acp=&aco=+"+recherche+"&get_facets=0"
    requete = requests.get(lien)
    page = requete.content
    soup = BeautifulSoup(page,features="html.parser")
    all_links = soup.find_all("a",{"class": "js-search-result-thumbnail non-js-link"})
    all_links=str(all_links).split('<a class="js-search-result-thumbnail non-js-link"')
    liste_link=[]
    for i in range(len(all_links)-1):
        try:
            liste_link.append(all_links[i].split("<img alt=")[0].split('href="')[1][0:-36])
        except IndexError:
            continue

    if len(liste_link)>1:
        try:
            if not os.path.exists(chemin):
                os.makedirs(chemin)
            os.mkdir(chemin+recherche.title())
        except FileExistsError:
            print("dossier déjà existant")
        
        print(" ")
        print("Pictures could be find...")
        print("Knowing that the maximum is "+str(len(liste_link)))
        limite_image=int(input("How much do you want ?: "))
        print(" ")
        print("The downloading will start...")
        print(" ")
        #os.startfile("C:/Users/Antonin Achard/Desktop/downloaded_Img/"+recherche.title())
        #limite_image=int(input("Sachant que le maximum est "+str(len(liste_link)-1)+",combien d'images voulez vous téléchargé ?: "))
        
        if limite_image!=len(liste_link)-1:
            limite_image+=1
        pourcent=0
        bar=0
        print("Downloading...")
        for i in range(limite_image):
            lien=liste_link[i]
            requete = requests.get(lien)
            page = requete.content
            soup = BeautifulSoup(page,features="html.parser")
            all_links = soup.find_all("meta")
            principale_picture=str(all_links[6])
            principale_picture=principale_picture[15:-23]
            file1=open(chemin+recherche.title()+"/links.txt","a")
            file1.write(str(i)+"  "+lien+"\n")
            file1.close()

            try:
                aaa=requests.get(principale_picture)
                file = open(chemin+recherche.title()+"/Image_"+recherche.title()+"_"+str(i)+".jpg", "wb")
                file.write(aaa.content)
                file.close()
                
                pourcent=pourcent+100/limite_image
                bar=bar+10/limite_image
                print("#"*round(bar)+" "*round(10-bar)+"|"+str(round(pourcent))+"%",end="\r")
            except requests.exceptions.MissingSchema:
                continue
            

requete=str(input("What do you want pictures of ?: "))
chemin=str(input("In which folder ? (ex: C:/Users/Username/Desktop/FolderName/ ): "))
Fonction_principale(requete,chemin)