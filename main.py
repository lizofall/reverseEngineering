import json
import sys
import os
import xml.etree.ElementTree as ET
import svgwrite
import requests
from svgwrite import cm, mm   

#gestion des argument
if len(sys.argv) == 7:
    formatFichier = sys.argv[2]
    option = sys.argv[3]
    if option == '-f':
        fichier = sys.argv[4]
        if formatFichier == "json":
            with open(fichier) as json_data: 
                data_dict = json.load(json_data)

            dwg = svgwrite.Drawing(sys.argv[6], profile='tiny')
            dwg.add(dwg.rect((10, 10), (1800, 2048),
                stroke=svgwrite.rgb(10, 10, 16, '%'),
                fill='#8FBC8F')
            )
            listeEntites = []
            listeAttributs = []
            afficheAttribut = []
            nbEntites = len(data_dict)
            m=0
            cmptAt=0
            # Parcours de chaque entite
            for i in range(nbEntites):

                # Recuperation de la liste des entites
                for key in data_dict[i].keys():
                    listeEntites.append(key)                    
                # Recuperation du nombre d'attributs
                j=0
                comp=0
                for m in range(len(listeEntites)):
                    nbAttributs = len(data_dict[i][listeEntites[m]][0].keys())
                    afficheAttribut.append(nbAttributs)
                    while j< nbAttributs:
                        for key in data_dict[i][listeEntites[j]][0].keys():
                            listeAttributs.append(key)
                        j=j+1
                        cmptAt = cmptAt + nbAttributs                        
                m=m+1                              
            i=i+1  
            x=50
            y=80
            val=0
            for l in range(len(listeEntites)):
                #creation de tableau pour chaque entites
                dwg.add(dwg.rect((x, y-30), (300, 300),
                stroke=svgwrite.rgb(10, 10, 16, '%'),
                fill='white')
                )
                #ecriture des entites dans le tableay crée
                dwg.add(dwg.text(listeEntites[l],
                insert=(x+90,y),
                stroke='none',
                fill=svgwrite.rgb(15, 15, 15, '%'),
                font_size='25px',
                font_weight="bold")
                )
                #creation du deuxieme rectangle
                dwg.add(dwg.rect((x, y+10), (300, 300),
                stroke=svgwrite.rgb(10, 10, 16, '%'),
                fill='white')
                )
                #affichage des attributs de chaque entité dans le tableau dentites correspondant
                k=0
                for k in range(afficheAttribut[l]):   
                    dwg.add(dwg.text(listeAttributs[k+val],
                    insert=(x+90,y+50),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='25px',
                    font_weight="bold")
                    )   
                    y=y+30
                
                k=k+1
                x=x+600
                dwg.add(dwg.line((x-300,y), (x+300,y), 
                stroke="black")) 
                y=y-60
                if x >= 1800 :
                    x=50
                    y=900
                
                
                val=val+k 
            l=l+1   
            dwg.save ()             
        else:
            if formatFichier == "xml":
                #parsing du fichier xml
                tree = ET.ElementTree(file=sys.argv[4])

                #recuperation de la racine
                root = tree.getroot()
                #declarations
                entites=[]
                attributs=[]
                nbreattri_tab=[]
                relation=[]
                att=[]

                x=50
                y=80
                i=0
                l=0
                j=0
                for child in root: 
                    for childs in child:
                        if childs.tag!="relation":
                            entites.insert(i,childs.tag)           # recuperation des entites dans un tableau
                            nbattribut=0
                            for attribut in childs :
                                attributs.insert(j,attribut.tag)  # recuperation des attributs dune entite dans un tableau
                                nbattribut+=1 
                                j=j+1
                            nbreattri_tab.append(nbattribut)      # recuperer le nbre dattributs de chaque entite dans un tableau
                            i=i+1 
                    dwg = svgwrite.Drawing(sys.argv[6], profile='tiny')
                    
                        ##dessiner rectangle
                    
                    dwg.add(dwg.rect((10, 10), (1800, 2048),
                    stroke=svgwrite.rgb(10, 10, 16, '%'),
                    fill='#8FBC8F')
                    )
                    
                comp=0     
                for l in range(len(entites)):

                        #creation de rectangle pour chaque entite

                        dwg.add(dwg.rect((x, y-30), (200, 200),
                        stroke=svgwrite.rgb(10, 10, 16, '%'),
                        fill='white')
                        )

                        #ecrire chaque entite dans rectangle

                        dwg.add(dwg.text(entites[l],
                        insert=(x+30,y),
                        stroke='none',
                        fill=svgwrite.rgb(15, 15, 15, '%'),
                        font_size='25px',
                        font_weight="bold")
                        )
                        #creation de sous rectangle pour chaque rectangle

                        dwg.add(dwg.rect((x, y+10), (200, 200),
                        stroke=svgwrite.rgb(10, 10, 16, '%'),
                        fill='white')
                        )
                        k=0
                        for k in range(nbreattri_tab[l]):

                            #lister les attributs de chaque entite 
                                        
                            dwg.add(dwg.text(attributs[comp+k],
                            insert=(x,y+30),
                            stroke='none',
                            fill=svgwrite.rgb(15, 15, 15, '%'),
                            font_size='25px',
                            font_weight="bold"))
                            k=k+1
                            y=y+20
                        # dwg.add(dwg.line((x+200,y), (x+400,y), 
                        # stroke="black"))  
                        x=x+400
                        y=y-60
                        if x >= 1024 :
                            x=50
                            y=450
                        
                        l=l+1
                        comp=comp+k

               
                
                #relations

                dwg.add(dwg.line( (250,180), (450,180),
                stroke="black")) 
                dwg.add(dwg.line( (650,180), (850,180),
                stroke="black"))
                dwg.add(dwg.line( (190,290), (190,480),
                stroke="black"))
                dwg.add(dwg.line( (190,480), (1000,480),
                stroke="black")) 
                dwg.add(dwg.line( (1000,480), (1000,290),
                stroke="black")) 
                dwg.add(dwg.text("1..*",
                    insert=(270,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("0..*",
                    insert=(420,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("livrer",
                    insert=(360,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("affecter",
                    insert=(748,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("passer commande",
                    insert=(500,476),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("1..1",
                    insert=(820,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("0..*",
                    insert=(664,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("1..*",
                    insert=(192,330),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("0..*",
                    insert=(965,330),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                
                # write svg file to disk
                dwg.save()
            else:
                print('format incorrect: Exemple d’utilisation :\n avec xml: XJ_Convertor.py -i xml -f monfichier.xml -o monfichier.svg\n avec json: J_Convertor.py -i json -f monfichier.json -o monfichier.svg')

    else:
        if option == '-h':       
            fichier = requests.get(sys.argv[4])
            
            if formatFichier == "json":
                new_fichier='fichierHttp.json'
                fichier1 = open(new_fichier, "w")
                fichier1.write(fichier.text)
                fichier1.close()  
                with open(new_fichier) as json_data: 
                    data_dict = json.load(json_data)
                dwg = svgwrite.Drawing(sys.argv[6], profile='tiny')
                dwg.add(dwg.rect((10, 10), (1800, 2048),
                    stroke=svgwrite.rgb(10, 10, 16, '%'),
                    fill='#8FBC8F')
                )
                listeEntites = []
                listeAttributs = []
                afficheAttribut = []
                nbEntites = len(data_dict)
                m=0
                cmptAt=0
                # Parcours de chaque entite
                for i in range(nbEntites):

                    # Recuperation de la liste des entites
                    for key in data_dict[i].keys():
                        listeEntites.append(key)                    
                    # Recuperation du nombre d'attributs
                    j=0
                    comp=0
                    for m in range(len(listeEntites)):
                        nbAttributs = len(data_dict[i][listeEntites[m]][0].keys())
                        afficheAttribut.append(nbAttributs)
                        while j< nbAttributs:
                            for key in data_dict[i][listeEntites[j]][0].keys():
                                listeAttributs.append(key)
                            j=j+1
                            cmptAt = cmptAt + nbAttributs                        
                    m=m+1                              
                i=i+1  
                x=50
                y=80
                val=0
                for l in range(len(listeEntites)):
                    #creation de tableau pour chaque entites
                    dwg.add(dwg.rect((x, y-30), (300, 300),
                    stroke=svgwrite.rgb(10, 10, 16, '%'),
                    fill='white')
                    )
                    #ecriture des entites dans le tableay crée
                    dwg.add(dwg.text(listeEntites[l],
                    insert=(x+90,y),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='25px',
                    font_weight="bold")
                    )
                    #creation du deuxieme rectangle
                    dwg.add(dwg.rect((x, y+10), (300, 300),
                    stroke=svgwrite.rgb(10, 10, 16, '%'),
                    fill='white')
                    )
                    #affichage des attributs de chaque entité dans le tableau dentites correspondant
                    k=0
                    for k in range(afficheAttribut[l]):   
                        dwg.add(dwg.text(listeAttributs[k+val],
                        insert=(x+90,y+50),
                        stroke='none',
                        fill=svgwrite.rgb(15, 15, 15, '%'),
                        font_size='25px',
                        font_weight="bold")
                        )   
                        y=y+30
                    dwg.add(dwg.line((x+300,y), (x+600,y), 
                    stroke="black")) 
                    k=k+1
                    x=x+600
                    y=y-60
                    if x >= 1800 :
                        x=50
                        y=900
                    
                    
                    val=val+k 
                l=l+1   
                #relations

                dwg.add(dwg.line( (290,180), (490,180),
                stroke="black")) 
                dwg.add(dwg.line( (690,180), (890,180),
                stroke="black"))
                dwg.add(dwg.line( (190,290), (190,480),
                stroke="black"))
                dwg.add(dwg.line( (190,480), (1000,480),
                stroke="black")) 
                dwg.add(dwg.line( (1000,480), (1000,290),
                stroke="black")) 
                dwg.add(dwg.text("1..*",
                    insert=(294,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("0..*",
                    insert=(458,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("livrer",
                    insert=(360,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("affecter",
                    insert=(748,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("passer commande",
                    insert=(500,476),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("1..1",
                    insert=(858,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("0..*",
                    insert=(694,176),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("1..*",
                    insert=(192,330),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                dwg.add(dwg.text("0..*",
                    insert=(965,330),
                    stroke='none',
                    fill=svgwrite.rgb(15, 15, 15, '%'),
                    font_size='18px',
                    font_weight="bold"))
                
                dwg.save ()      
                
            else:
                if formatFichier == "xml":                    
                    new_fichier='fichierHttp.xml'
                    fichier1 = open(new_fichier, "w")
                    fichier1.write(fichier.text)
                    fichier1.close()  
                     #parsing du fichier xml
                    tree = ET.ElementTree(file=sys.argv[4])

                    #recuperation de la racine
                    root = tree.getroot()
                    #declarations
                    entites=[]
                    attributs=[]
                    nbreattri_tab=[]
                    relation=[]
                    att=[]

                    x=50
                    y=80
                    i=0
                    l=0
                    j=0
                    for child in root: 
                        for childs in child:
                            if childs.tag!="relation":
                                entites.insert(i,childs.tag)           # recuperation des entites dans un tableau
                                nbattribut=0
                                for attribut in childs :
                                    attributs.insert(j,attribut.tag)  # recuperation des attributs dune entite dans un tableau
                                    nbattribut+=1 
                                    j=j+1
                                nbreattri_tab.append(nbattribut)      # recuperer le nbre dattributs de chaque entite dans un tableau
                                i=i+1 
                        dwg = svgwrite.Drawing(sys.argv[6], profile='tiny')
                        
                            ##dessiner rectangle
                        
                        dwg.add(dwg.rect((10, 10), (1800, 2048),
                        stroke=svgwrite.rgb(10, 10, 16, '%'),
                        fill='#8FBC8F')
                        )
                        
                    comp=0     
                    for l in range(len(entites)):

                            #creation de rectangle pour chaque entite

                            dwg.add(dwg.rect((x, y-30), (200, 200),
                            stroke=svgwrite.rgb(10, 10, 16, '%'),
                            fill='white')
                            )

                            #ecrire chaque entite dans rectangle

                            dwg.add(dwg.text(entites[l],
                            insert=(x+30,y),
                            stroke='none',
                            fill=svgwrite.rgb(15, 15, 15, '%'),
                            font_size='25px',
                            font_weight="bold")
                            )
                            #creation de sous rectangle pour chaque rectangle

                            dwg.add(dwg.rect((x, y+10), (200, 200),
                            stroke=svgwrite.rgb(10, 10, 16, '%'),
                            fill='white')
                            )
                            k=0
                            for k in range(nbreattri_tab[l]):

                                #lister les attributs de chaque entite 
                                            
                                dwg.add(dwg.text(attributs[comp+k],
                                insert=(x,y+30),
                                stroke='none',
                                fill=svgwrite.rgb(15, 15, 15, '%'),
                                font_size='25px',
                                font_weight="bold"))
                                k=k+1
                                y=y+20
                            dwg.add(dwg.line((x+200,y), (x+400,y), 
                            stroke="black"))  
                            x=x+400
                            y=y-60
                            if x >= 1024 :
                                x=50
                                y=450
                            
                            l=l+1
                            comp=comp+k

                
                    

                    # write svg file to disk
                    dwg.save()
                else:
                    print('format incorrect: Exemple d’utilisation :\n avec xml: XJ_Convertor.py -i xml -f monfichier.xml -o monfichier.svg\n avec json: J_Convertor.py -i json -f monfichier.json -o monfichier.svg')

        else:
            print('format incorrect: Exemple d’utilisation :\n avec xml: XJ_Convertor.py -i xml -f monfichier.xml -o monfichier.svg\n avec json: J_Convertor.py -i json -f monfichier.json -o monfichier.svg')
else:
    print('format incorrect: Exemple d’utilisation :\n avec xml: XJ_Convertor.py -i xml -f monfichier.xml -o monfichier.svg\n avec json: J_Convertor.py -i json -f monfichier.json -o monfichier.svg')

