import numpy as np
import pandas as pd

pd.set_option('expand_frame_repr', False)

#Lire le dataset
df=pd.read_csv('data\World University Rankings 2023.csv')

#Les 6 colonnes à selectionner
cols=['Name of University','University Rank','Location','No of student','International Student','Research Score','Teaching Score']

#extraire le nouveau jdd
univ=df[cols]


#les types des colonnes
"""
print(univ.dtypes)

Name of University        object
University Rank           object
Location                  object
No of student             object
International Student     object
Research Score           float64
dtype: object

"""
#Selectionner les 200 premières universités
#on doit tout d'abord rendre la colonne "University Rank" numeric (float64)
univ['University Rank']=pd.to_numeric(univ["University Rank"], errors='coerce')

Top_200_univs=univ.loc[univ["University Rank"]<=200]

#Pour enlever la virgule flottante .0 on le rend en int
Top_200_univs["University Rank"]=Top_200_univs["University Rank"].astype(int)

#Modifier le type des autres colonnes
Top_200_univs["Name of University"]=Top_200_univs["Name of University"].astype("string")
Top_200_univs["Location"]=Top_200_univs["Location"].astype("string")
Top_200_univs["No of student"]=Top_200_univs["No of student"].str.replace(',','') #car dans le dataset les milliers sont écrits avec ,
Top_200_univs["No of student"]=Top_200_univs["No of student"].astype("int",errors='ignore')
#La colonne International Student est écrite en pourcentage
Top_200_univs["International Student"]=Top_200_univs["International Student"].str.rstrip('%').astype("float")/100
Top_200_univs["Research Score"]=Top_200_univs["Research Score"].astype("float")
Top_200_univs["Teaching Score"]=Top_200_univs["Teaching Score"].astype("float")
'''
print(Top_200_univs.dtypes)
Name of University        string
University Rank            int32
Location                  string
No of student              int32
International Student    float64
Research Score           float64
dtype: object
'''


#Identifier les colonnes avec valeurs nulles
'''
print(Top_200_univs.isna().any())

retourne 
Name of University       False
University Rank          False
Location                  True
No of student            False
International Student    False
Research Score           False
dtype: bool
'''

'''
Pour détecter les lignes nulles de la colonne "Location"
#print(Top_200_univs.loc[Top_200_univs["Location"].isna()])
'''

#Pour des buts d'analyse et d'études sur la localisation des universités on a décidé de remplir manuellement les localisations indéfinies

Top_200_univs.loc[15,'Location'] ='China'
Top_200_univs.loc[16, "Location"] ='China'
Top_200_univs.loc[18, 'Location'] ='Singapore'
Top_200_univs.at[29, 'Location'] ='Germany'
Top_200_univs.at[30, 'Location'] ='Hong Kong'
Top_200_univs.at[32, 'Location'] ='Germany'
Top_200_univs.at[41, 'Location'] ='Belgium'
Top_200_univs.at[42, 'Location'] ='Germany'
Top_200_univs.at[44, 'Location'] ='Hong Kong'
Top_200_univs.at[45, 'Location'] ='Canada'
Top_200_univs.at[52, 'Location'] ='Australia'
Top_200_univs.at[53, 'Location'] ='United Kingdom'
Top_200_univs.at[57, 'Location'] ='Hong Kong'
Top_200_univs.at[66, 'Location'] ='China'
Top_200_univs.at[71, 'Location'] ='Australia'
Top_200_univs.at[73, 'Location'] ='China'
Top_200_univs.at[74, 'Location'] ='Netherlands'
Top_200_univs.at[75, 'Location'] ='United Kingdom'
Top_200_univs.at[76, 'Location'] ='Netherlands'
Top_200_univs.at[77, 'Location'] ='South Korea'
Top_200_univs.at[78, 'Location'] ='Hong Kong'
Top_200_univs.at[79, 'Location'] ='Netherlands'
Top_200_univs.at[82, 'Location'] ='United Kingdom'
Top_200_univs.at[84, 'Location'] ='Canada'
Top_200_univs.at[87, 'Location'] ='Australia'
Top_200_univs.at[98, 'Location'] ='Hong Kong'
Top_200_univs.at[101, 'Location'] ='Saudi Arabia'
Top_200_univs.at[104, 'Location'] ='United Kingdom'
Top_200_univs.at[110, 'Location'] ='Canada'
Top_200_univs.at[114, 'Location'] ='France'
Top_200_univs.at[115, 'Location'] ='United Kingdom'
Top_200_univs.at[132, 'Location'] ='Australia'
Top_200_univs.at[137, 'Location'] ='Canada'
Top_200_univs.at[139, 'Location'] ='Australia'
Top_200_univs.at[140, 'Location'] ='Netherlands'
Top_200_univs.at[155, 'Location'] ='USA'
Top_200_univs.at[159, 'Location'] ='South Africa'
Top_200_univs.at[160, 'Location'] ='Italy'
Top_200_univs.at[161, 'Location'] ='Germany'
Top_200_univs.at[163, 'Location'] ='South Korea'
Top_200_univs.at[164, 'Location'] ='China'
Top_200_univs.at[170, 'Location'] ='South Korea'
Top_200_univs.at[172, 'Location'] ='South Korea'
Top_200_univs.at[175, 'Location'] ='United Kingdom'
Top_200_univs.at[185, 'Location'] ='United Kingdom'
Top_200_univs.at[186, 'Location'] ='Taiwan'
Top_200_univs.loc[197, 'Location'] ='United Kingdom'

#On choisit la colonne du rang comme indexe de notre dataframe
Top_200_univs.set_index('University Rank',inplace=True)

#print(Top_200_univs)

#Enregistrer le résultat dans un fichier csv
Top_200_univs.to_csv('data\Top_200_univs.csv', sep=';', encoding='utf-8')