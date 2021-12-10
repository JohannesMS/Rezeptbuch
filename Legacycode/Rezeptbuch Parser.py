#Rezeptzutaten in die Datei Rezepte.txt aus Word kopieren, dann Code ausführen, die formatierten Zutaten finden sich dann in der Datei Rezepte.txt am Ende
reader = open("/Users/johannes/Desktop/Rezeptbuch LATEX/Code/Rezepte.txt", "r")
Zutaten = reader.read()


def gTrenner(Zutat1):
    liste = []
    for strq in Zutat1:
        words = strq.split(" ")
        indexRemove = words[-1].find("\\")
        words[-1] = words[-1][:indexRemove]
        words[0] = words[0][1:]
        if len(Zutat1) == 1:
            continue
        if words[0].find("g") != -1:
           index = words[0].find("g")
           x = words[0][:index]
           words.pop(0)
           words.insert(0,x)
           words.insert(1,"g")
           liste.append(words)
        elif words[0].find("ml") != -1:    
           index = words[0].find("ml")
           x = words[0][:index]
           words.pop(0)
           words.insert(0,x)
           words.insert(1,"ml")
           liste.append(words)
        else:
            liste.append(words)
    return liste

def splitter1(Zutaten, delimiter):
    return Zutaten.split(delimiter)
    

def latexOut(finalList):
    textdatei = []
    textdatei.append("\\begin{recipe}{}{}{}\n")
    for ingredient in finalList:
        x = ""
        #Wenn die Länge 1 ist, kein [] sondern direkt in {}
        if len(ingredient) == 1:
            x = x + "\ing" + "[]" + "{}" + "{" + ingredient[0] + "}" + "\n"
            textdatei.append(x)
            continue
        x = "\ing" + "[" +ingredient[0] + "]"
        if len(ingredient) <= 2:
            x = x + "{}" + "{" + ingredient[1] + "}" + "\n"
            textdatei.append(x)
            continue
        x = x + "{" + ingredient[1] + "}"
        if len(ingredient) > 2:
            y = "".join(ingredient[2:])
            x = x + "{" + y + "}" + "\n"
            textdatei.append(x)
            continue
        textdatei.append(x)
    textdatei.append("\end{recipe}")
    return textdatei

#Hier ist der Einput ein String der Zutaten, die Methode splittet ihn nach den • und es entsteht eine 
#zweidimensionale Liste
ZutatenListe1 = splitter1(Zutaten, "•")
#print(ZutatenListe1)
listentest = gTrenner(ZutatenListe1)
listentest.pop(0)
print(listentest)
textdatei = latexOut(listentest)
print(textdatei)

text_file = open("/Users/johannes/Desktop/Rezeptbuch LATEX/Code/Rezepte.txt", "w")
text_file.write(Zutaten)
for ingredient in textdatei:
    text_file.write(ingredient)
text_file.close()

#TODO
