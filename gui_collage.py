# -*- coding: utf-8 -*-
"""
Created on Tue May  1 11:44:35 2018

@author: Pascha
"""
import os
import tkinter as tk
import time
from PIL import ImageTk, Image

import imageCapture
import printer
#import telegram
import collage

root = tk.Tk()

# Geometrie des Fensters
root.geometry("1024x600")

# Hintergrund
background_image=tk.PhotoImage(file="background/bg.png")
background_label = tk.Label(root, image=background_image, width="1024",height="600")
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_image


# Alle ButtonImage
photo_BildDrucken=tk.PhotoImage(file="buttons/BildDrucken.png")
photo_JA=tk.PhotoImage(file="buttons/JA.png")
photo_Nochmal=tk.PhotoImage(file="buttons/Nochmal.png")
photo_Start=tk.PhotoImage(file="buttons/Start.png")
photo_Einzelbild=tk.PhotoImage(file="buttons/Einzelbild.png")
photo_Collage=tk.PhotoImage(file="buttons/Collage.png")

# Alle Buttons
buttons = [tk.Button(root,image=photo_Start,width="220",height="82"),
           tk.Button(root,image=photo_Einzelbild,width="220",height="81"),
           tk.Button(root,image=photo_BildDrucken,width="240",height="80"),
           tk.Button(root,image=photo_Nochmal,width="222",height="82"),
           tk.Button(root,image=photo_Start,width="220",height="81"),
           tk.Button(root,image=photo_Collage,width="220",height="81"),
           tk.Button(root,image=photo_JA, width = "221", height="82")]

# Alle Labels
labels = tk.Label(root)
labels.config(font=("Courier", 44))
pic = tk.Label(root)

# Bild resize (Größe des Previews)
basewidth = 600

# Location
folder_name = imageCapture.giveFolderName()

# Counter
printPage = 0

# Sonstiges
fileName = None
path = None
listofimages = []

# Hilfsfunktionen:
def Countdown():
    labels.config(text = "Achtung!")
    root.update()
    time.sleep(1)
    for sek in ["3","2","1"]:
        labels.config(text = "Foto wird geschossen in \n" + sek)
        root.update()
        time.sleep(1)

def ButtonsDelete():
    for i in range(len(buttons)):
        buttons[i].place_forget()

def deletePreview():
    try:
        os.remove(folder_name + "/Preview.jpg")
        print("Löschen von 'Preview.jpg'")
    except:
        print("Preview war nicht vorhanden")
        
# Dialoge:
def WelcomePhotoBooth():
    ButtonsDelete()
    pic.place_forget() 
    global listofimages
    listofimages = []
    
    labels.config(text = "Willkommen zur PhotoBooth")
    buttons[5].place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    buttons[5].config(command = AreYouReady)
    labels.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    root.update()        
        
def AreYouReady():
    pic.place_forget()
    ButtonsDelete()
    deletePreview()
    labels.config(text ="Seid ihr bereit?")
    buttons[6].place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    buttons[6].config(command = CaptureImage)       
        
def CaptureImage():
    ButtonsDelete()
    Countdown()
    labels.config(text = "Lächeln!!") 
    root.update()
    imageCapture.captureImages()
    labels.config(text = "Einen Moment noch...")
    root.update() 
    imageCapture.renameFiles()
    global fileName, path
    fileName = imageCapture.giveFileName()
    path = folder_name + "/" + fileName    
    PictureReview()         
        
def PictureReview():
    labels.config(text = "Error")
    
    img = Image.open(path)
    
    # Image resize:
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save("Preview.jpg")
    
    # Place Preview
    path_Preview = folder_name + "/" + "Preview.jpg"
    image = Image.open(path_Preview)
    photo = ImageTk.PhotoImage(image)
    pic.config(image=photo)
    pic.image = photo # keep a reference!  
    pic.place(relx = 0.5, rely = 0.4, anchor=tk.CENTER)
    
    if len(listofimages) < 4:        
        buttons[2].config(command = NextPicture)
        buttons[3].config(command = DeletePicture)
        buttons[2].place(relx=0.8, rely=0.9, anchor=tk.CENTER)
        buttons[3].place(relx=0.2, rely=0.9, anchor=tk.CENTER)
    if len(listofimages) == 4:
        buttons[2].config(command = Printing)
        buttons[3].config(command = WelcomePhotoBooth) # Komplett löschen
        buttons[2].place(relx=0.8, rely=0.9, anchor=tk.CENTER)
        buttons[3].place(relx=0.2, rely=0.9, anchor=tk.CENTER)

def NextPicture():
    global listofimages, fileName, path
    listofimages.append(path)
    if len(listofimages) < 4:
        AreYouReady()
    if len(listofimages) == 4:
        ButtonsDelete()
        pic.place_forget()
        labels.config(text = "Collage wird erstellt... \n Einen Moment bitte...")
        root.update()
        collage.create_collage(6000,4000,listofimages) #ggfs ändern
        fileName = collage.giveFileName()
        path = folder_name + "/" + fileName    
        print(fileName)
        PictureReview()

def DeletePicture():
    global listofimages
    del listofimages[-1]
    AreYouReady()    
        
def Printing():
    pic.place_forget()   
    ButtonsDelete()
    deletePreview()
    
    labels.config(text = "Bild wird gedruckt...\n ...einen Moment")
    root.update()
    printer.printImage(path)
    global printPage
    printPage += 1
    time.sleep(1)
    if printPage == 2: #Todo noch ändern
        telegram.BotMessage("Papier ist bald leer...")
        printPage = -1
        
    time.sleep(30)
    WelcomePhotoBooth()        
        
