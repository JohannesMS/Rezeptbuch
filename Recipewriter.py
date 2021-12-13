from os import read
import os
import shutil
import subprocess
from datetime import date, datetime

#Falls das Programm auf einem anderen PC verwendet wird müssen die Pfadvariablen aktualisiert werden, ebenfalls wie die Pfade in der der Funktion create_pdf

ing_list, ing_list_output = [], []
recipe_instruction, recipe_final, ing_or_ins, eingabe, recipe_book_path, spice_checker = "", "", "", "", "", ""
recipe_book_path_master = "/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Master.tex"
recipe_book_paths = []
recipe_book_paths.append("/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Rezeptbuch Beilagen/Rezeptbuch_Beilagen.tex")
recipe_book_paths.append("/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Rezeptbuch Brot/Rezeptbuch_Brot.tex")
recipe_book_paths.append("/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Rezeptbuch Desserts/Rezeptbuch_Desserts.tex")
recipe_book_paths.append("/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Rezeptbuch Gewürze/Rezeptbuch_Gewürze.tex")
recipe_book_paths.append("/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Rezeptbuch Main/Rezeptbuch_Main.tex" )

def create_pdf():
    #Führt im Terminal den Befehl pdflatex aus und kompiliert die Master.tex
    #Frag nicht wieso, manchmal muss pdflatex mehrfach ausgeführt werden um das TOC richtig zu generieren
    return_value = subprocess.call(['pdflatex', recipe_book_path_master], shell=False)
    return_value = subprocess.call(['pdflatex', recipe_book_path_master], shell=False)
    return_value = subprocess.call(['pdflatex', recipe_book_path_master], shell=False)

    #Standardoutput in den Pfad User/johannes, alle Dateien werden an die richtige Stelle verschoben und dann die PDF kopiert
    shutil.move("/Users/johannes/Master.pdf","/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Master.pdf")
    shutil.move("/Users/johannes/Master.aux","/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Master.aux")
    shutil.move("/Users/johannes/Master.log","/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Master.log")
    shutil.move("/Users/johannes/Master.out","/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Master.out")
    shutil.move("/Users/johannes/Master.toc","/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Master.toc")
    shutil.copy("/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Master.pdf", "/Users/johannes/Desktop/Rezeptbuch LATEX/Rezeptbuch.pdf")
    subprocess.call(['open', "/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Master.pdf"], shell=False)

def path_chooser(input):
    #Die anfängliche Eingabe bestimmt den Pfad in dem die Tex angesteuert werden soll
    if input == "1" or input == "Beilagen":
        return recipe_book_paths[0]
    elif input == "2" or input == "Brot":
        return recipe_book_paths[1]
    elif input == "3" or input == "Desserts":
        return recipe_book_paths[2]
    elif input == "4" or input == "Gewürze":
        return recipe_book_paths[3]
    elif input == "5" or input == "Hauptgerichte": 
        return recipe_book_paths[4]
    elif input == "6" or input == "Sortieren": 
        sort_recipe_books()
    elif input == "7" or input == "PDF erstellen": 
        create_pdf()
        exit()
    else:
        print("Fehler")
        exit()
    
def ing_converter(ing_list_raw):
    #Konvertiert halbgar die Zutaten in listenform für die spätere Verwendung
    liste = []
    for strq in ing_list_raw:
        words = strq.split(" ")
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

def latexOut(finalList):
    #Die in ing_converter ausgegebene Liste wird hier in Texform gebracht
    textdatei = []
    for ingredient in finalList:
        x = ""
        #Wenn die Länge 1 ist, kein [] sondern direkt in {}
        if len(ingredient) == 1:
            x += "\ing" + "[]" + "{}" + "{" + ingredient[0] + "}" + "\n"
            textdatei.append(x)
            continue
        x = "\ing" + "[" +ingredient[0] + "]"
        if len(ingredient) <= 2:
            x += "{}" + "{" + ingredient[1] + "}" + "\n"
            textdatei.append(x)
            continue
        x += "{" + ingredient[1] + "}"
        if len(ingredient) > 2:
            y = "".join(ingredient[2:])
            x += "{" + y + "}" + "\n"
            textdatei.append(x)
            continue
        textdatei.append(x)
    return textdatei

def first_letter_replacer(name):
    #Wenn der erste Buchstabe des Rezeptnamens klein ist wird nicht richtig sortiert, hier wird der erste Buchstabe groß gemacht
    if name[0].islower() == True:
        recipe_name_list = list(name)
        recipe_name_list[0] = recipe_name_list[0].upper()
        name = "".join(recipe_name_list)
    return name

def sort_recipe_books():
    #Sortiert alle Rezepte in allen Büchern
    for recipe_book_path_sorting in recipe_book_paths:
        print("Sorting recipe book: " + recipe_book_path_sorting)
        sorted_recipes = ""
        recipes = ""
        recipe_book = ""  

        recipe_book = custom_reader(recipe_book_path_sorting)

        recipes = recipe_book.split("%------------------------------------------------------------------------------------------------------------------")
        sorted_recipes = sorted(recipes)
        sorted_recipes = sorted_recipes[1::]
        recipe_book = ""
        for recipes in sorted_recipes:
            recipe_book = recipe_book + recipes + "%------------------------------------------------------------------------------------------------------------------"

        #öffnet die Texdatei zum schreiben
        custom_writer(recipe_book_path_sorting, recipe_book)
        print("Sorting complete")
    create_pdf()
    exit()

def custom_writer(destination, source):
    #Schreibt den inhalt source in die Daten destionation, der ursprüngliche Inhalt wird gelöscht
    text_file = open(destination, "w")
    text_file.truncate(0)
    text_file.write(source)
    text_file.close()

def custom_reader(destination):
    #Liest den Inhalt der Datei destination und gibt sie zurück
    reader = open(destination, "r")
    output = reader.read()
    reader.close()  
    return output
    
def backup():
    #Speichert alle Tex-Dateien in dem Backupordner (falls, ganz unvorhergesehen, mal was so richtig schief läuft)
    name = "rezeptbuch_backup_" + str(datetime.now())
    shutil.make_archive(name,"zip","/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output")
    shutil.move("/Users/johannes/" + name + ".zip","/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Backup/")
    backups = os.listdir("/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Backup")
    backups = backups[1:]
    while len(backups)>=10:
        os.remove("/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Backup/"+backups[1])
        backups = os.listdir("/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Backup")
        backups = backups[1:]

    

    #subprocess.call("cd /Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Backup")
    #subprocess.call("ls")
    print("Backup erfolgreich")


#Main Loop
backup()
spice_checker = input("1: Beilagen\n2: Brot\n3: Desserts\n4: Gewürze\n5: Hauptgericht\n6: Sortieren\n7: PDF erzeugen\n\n")
recipe_book_path = path_chooser(spice_checker)
recipe_name =  first_letter_replacer(input("Name des Rezepts?\n"))

if spice_checker == "4":
    recipe_begin = "\n\\begin{recipe}{" +recipe_name+ "}{}{}"
else:
    num_persons = input("Für wie viele Personen?\n")
    amount_time = input("Zubereitungszeit in Minuten?\n")
    recipe_begin = "\n\\begin{recipe}{" +recipe_name+ "}{" +num_persons+ " Personen}{" +amount_time+ " Minuten}"
recipe_end = "\\end{recipe} \n\n%------------------------------------------------------------------------------------------------------------------"
recipe_final = recipe_begin + "\n"

while ing_or_ins != "e" or ing_or_ins != "E":
    ing_or_ins = input("Z/z für Zutat oder A/a für Anweisung, zum abschließen E/e, zum abbrechen X/x \n")

    if ing_or_ins == "X" or ing_or_ins == "x":
        print("Programm wird beendet")
        exit()
    #sorry für den Teil
    if ing_or_ins == "Z" or ing_or_ins == "z":
        while ing_or_ins != "a" or ing_or_ins != "A" or ing_or_ins != "e" or ing_or_ins != "E":
            ing_or_ins = input("Jetzt bitte die Zutat eingeben\n")
            if (ing_or_ins == "a" or ing_or_ins == "A" or ing_or_ins == "e" or ing_or_ins == "E"):
                break
            else:
                ing_list.append(ing_or_ins)
    if ing_or_ins == "A" or ing_or_ins == "a":
        recipe_instruction = input("Jetzt bitte die Anweisung zur Verarbeitung der eben genannten Zutaten eingeben\n")
        recipe_instruction = recipe_instruction.replace("Grad","\\0C")
        recipe_instruction = recipe_instruction.replace("Grad C","\\0C")
        recipe_instruction = recipe_instruction.replace("grad","\\0C")
        recipe_instruction = recipe_instruction.replace("grad C","\\0C")
        recipe_instruction = recipe_instruction.replace("°C","\\0C")
        #Nachdem eine Anweisung gegeben wurde kann die erste Iteration der Verarbeitung ausgeführt und geschrieben werden, dann den Zwischenspeicher löschen
        #splittet die Wörter in die richtige Reihenfolge
        ing_list_output = ing_converter(ing_list)
   
        #konvertiert die Liste in Latexform
        ing_list_output = latexOut(ing_list_output)

        #Wenn die Zutatenliste leer ist und nur eine Anweisung kommt soll ein leerer Baustein für eine Zutat eingefügt werden
        if not ing_list:
            ing_list_output.append("\ing[]{}{}\n")

        #konkateniert die Zutatenliste in den Textkörper
        for Zutat in ing_list_output:
            recipe_final = recipe_final + str(Zutat)

        #fügt die Anweisung der Zutaten ein    

        recipe_final = recipe_final + recipe_instruction + "\n\n"

        #setzt Zutaten und Anweisungen zurück
        ing_list = []
        recipe_instruction = ""
        continue
    if ing_or_ins == "E" or ing_or_ins == "e":
        recipe_final += recipe_end

        #öffnet die Texdatei zum auslesen und zwischenspeichern
        recipe_book = custom_reader(recipe_book_path) 
        recipe_book += "\n" + recipe_final 
        
        #öffnet die Texdatei zum schreiben
        custom_writer(recipe_book_path, recipe_book)
        #Frage ob in Tex bearbeitet werden soll
        tempQuery = input("Soll die .tex Datei bearbeitet werden? J/j oder N/n\n")
        if(tempQuery == "J" or tempQuery == "j"):
            subprocess.call(['open', recipe_book_path], shell=False)
            tempQuery = input("Fertig? J/j\n")
        create_pdf()

        
        #subprocess.call(['open', "/Users/johannes/Desktop/Rezeptbuch LATEX/Hauptteil/Rezeptbuch PDF Output/Master.pdf"], shell=False)
        
        break

"""
Bugs:


Todo:


Rezepte:
Labskaus
Rösti
Apfelmus
Fleischkroketten ändern

Anleitung:
Z für Zutaten versetzt in eine Eingabeloop, zum abbrechen A oder a und zum Beenden E oder e
Irgendwas muss immer als Anweisung hingeschrieben werden (Bug oder Feature?)
"""

