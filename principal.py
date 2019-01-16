import xml.etree.ElementTree as ET
import svgwrite
#parsing du fichier xml
tree = ET.ElementTree(file="fic1.xml")
#recuperation de la racine
root = tree.getroot()
#declarations
entites=[]
attributs=[]
nbreattri_tab=[]
x=50
y=80
i=0
l=0
j=0

# creation du fichier svg

for child in root: 
       
    entites.insert(i,child.tag)           # recuperation des entites dans un tableau
    print(entites[i])
    nbattribut=0
    for attribut in child :
        attributs.insert(j,attribut.tag)  # recuperation des attributs dune entite dans un tableau
        print(attributs[j])
        nbattribut+=1 
        j=j+1
    nbreattri_tab.append(nbattribut)      # recuperer le nbre dattributs de chaque entite dans un tableau
    i=i+1
for nbre in nbreattri_tab:
    print(nbre)
    dwg = svgwrite.Drawing('XJ_convertor.svg', profile='tiny')
    
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
            
        x=x+400
        if x >= 1024 :
            x=50
            y=450
        
        l=l+1
        comp=comp+k






# write svg file to disk
dwg.save()





    