import json
#import xml.etree.ElementTree as ET
import svgwrite

dwg = svgwrite.Drawing('XJ_convertor', profile='tiny')

#tree = ET.ElementTree(file="fichier.xml")
#root = tree.getroot()
#for descendant in root.iter(): 
   # print(descendant.tag)
#dessiner restangle

dwg.add(dwg.rect((10, 10), (1800, 2048),
    stroke=svgwrite.rgb(10, 10, 16, '%'),
    fill='#8FBC8F')
)



print('\nfichier json\n')
with open('fichier.json') as json_data: 
    data_dict = json.load(json_data)
    

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
    # Recuperation de la liste des attributs
    
       
i=i+1     
print('lensemble des entites: ')
x=50
y=80
val=0
for l in range(len(listeEntites)):
    print(listeEntites[l])
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
    for k in range(afficheAttribut[l]):   
        dwg.add(dwg.text(listeAttributs[val+k],
        insert=(x+90,y+50),
        stroke='none',
        fill=svgwrite.rgb(15, 15, 15, '%'),
        font_size='25px',
        font_weight="bold")
        )   
        y=y+20
    k=k+1
    x=x+600
    if x >= 1800 :
        x=50
        y=900
    val=val+k
l=l+1
    
dwg.save()
for attr in afficheAttribut:
    print(attr)
print('\nlensemble des attributs: ')
for attribut in listeAttributs:
    print(attribut)


