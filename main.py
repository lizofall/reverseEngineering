import json

 ss
print('\nfichier json\n')
with open('fichier.json') as json_date: 
    data_dict = json.load(json_date)

listeEntites = []
listeAttributs = []
nbEntites = len(data_dict)

# Parcours de chaque entite
for i in range(nbEntites):

    # Recuperation de la liste des entites
    for key in data_dict[i].keys():
        listeEntites.append(key)

    # Recuperation du nombre d'attributs
    nbAttributs = len(data_dict[i][listeEntites[i]][0].keys())

    # Recuperation de la liste des attributs
    for j in range(nbAttributs):
        for key in data_dict[i][listeEntites[i]][0].keys():
            listeAttributs.append(key)
print('lensemble des entites: ')
for l in range(len(listeEntites)):
    print(listeEntites[l])

print('\nlensemble des attributs: ')
for k in range(nbAttributs):
    print(listeAttributs[k])

