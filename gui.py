# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 10:45:54 2018

@author: Pascha
"""
import os
import tkinter as tk
import time
from PIL import ImageTk, Image

import imageCapture
import printer
import telegram
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
    labels.config(text = "Willkommen zur PhotoBooth")
    buttons[0].config(command = ChooseSelection)
    buttons[0].place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    labels.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    root.update()

def ChooseSelection():
    pic.place_forget()
    ButtonsDelete()
    deletePreview()
    
    labels.config(text ="Was wollt ihr drucken?")
    buttons[1].place(relx=0.3, rely=0.5, anchor=tk.CENTER)
    buttons[1].config(command = lambda: AreYouReady(CaptureImage))
    buttons[5].place(relx=0.7, rely=0.5, anchor=tk.CENTER)
    buttons[5].config(command = lambda: AreYouReady(Collage))
    root.update()
    
def AreYouReady(com):
    pic.place_forget()
    ButtonsDelete()
    deletePreview()
    if com == CaptureImage:
        labels.config(text ="Seid ihr bereit?")
    if com == Collage:
        labels.config(text ="Jetzt werden vier Bilder \n in kurzer Zeit gemacht! \n \n" +
                      "Seid ihr bereit?")
    buttons[6].place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    buttons[6].config(command = com)

def Collage():
    ButtonsDelete()
    
    listofimages = []
    for nbImage in range(4):
        Countdown()
        labels.config(text = "Lächeln!!") 
        root.update()
        imageCapture.captureImages()
        labels.config(text = "Nächstes Foto")
        root.update()
        imageCapture.renameFiles()
        
        fileName_temp = imageCapture.giveFileName()
        
        listofimages.append(folder_name + "/" + fileName_temp)
    
    labels.config(text = "Collage wird erstellt... \n Einen Moment bitte...")
    root.update()
    collage.create_collage(6000,4000,listofimages) #ggfs ändern
    global fileName
    fileName = collage.giveFileName()
    print(fileName)
    PictureReview()

def CaptureImage():
    ButtonsDelete()
    Countdown()
    labels.config(text = "Lächeln!!") 
    root.update()
    imageCapture.captureImages()
    labels.config(text = "Einen Moment noch...")
    root.update() 
    imageCapture.renameFiles()
    global fileName
    fileName = imageCapture.giveFileName()    
    PictureReview()  
    
def PictureReview():
    labels.config(text = "Error")
    
    global path
    path = folder_name + "/" + fileName
    img = Image.open(path)   
    
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save("Preview.jpg")
    
    print("Image was resized")
    
    ####################
    path_Preview = folder_name + "/" + "Preview.jpg"
    image = Image.open(path_Preview)
    photo = ImageTk.PhotoImage(image)
    pic.config(image=photo)
    pic.image = photo # keep a reference!  
    pic.place(relx = 0.5, rely = 0.4, anchor=tk.CENTER)
    
    buttons[2].config(command = Printing)
    buttons[3].config(command = ChooseSelection)
    #buttons5.config(command = lambda: UploadTelegram(path_Preview))
    buttons[2].place(relx=0.8, rely=0.9, anchor=tk.CENTER)
    buttons[3].place(relx=0.2, rely=0.9, anchor=tk.CENTER)
    #buttons5.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

def UploadTelegram(path): # oder durch Bluetooth ersetzen
    telegram.BotPhoto(path)
    PictureReview()

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
