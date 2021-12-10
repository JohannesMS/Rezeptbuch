#Den gesamten Inhalt der Tex Datei in die Datei Sortierung.txt kopieren, dann Code ausführen, dann den Inhalt der Datei Sortiert.txt in die Tex Datei einfügen

reader = open("/Users/johannes/Desktop/Rezeptbuch LATEX/Code/Sortierung.txt", "r")
Zutaten = reader.read()

Rezepte = Zutaten.split("%------------------------------------------------------------------------------------------------------------------")
SortedRecipes = Rezepte[1:-1]
sortiert = sorted(SortedRecipes)

finish = ""+Rezepte[0]
for rezept in sortiert:
    #i = 0
    finish = finish + "%------------------------------------------------------------------------------------------------------------------" + rezept
    #i = i+1

finish = finish + "%------------------------------------------------------------------------------------------------------------------" +Rezepte[-1] 

text_file = open("/Users/johannes/Desktop/Rezeptbuch LATEX/Code/Sortiert.txt", "w")
text_file.write(finish)
text_file.close()