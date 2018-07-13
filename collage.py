from PIL import Image, ImageOps
from datetime import datetime
import signal, os, subprocess

shot_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

def create_collage(width, height, listofimages,modus):
    cols = 2 #Anzahl der Bilder 2x2
    rows = 2
    
    global shot_time    
    
    if modus == 1:
        a = int(0.075 * width) # Prozent der Gesamtbreite
        thumbnail_width = width //cols - a # // := Nachkomma stelle abgerundet
        thumbnail_height = height //rows - a
        size = thumbnail_width, thumbnail_height # Bildgroesse
        new_im = Image.open("/home/pi/Desktop/photobooth/background/collage_bg_text_new.jpg") # Hintergrund der Collage
        new_im.thumbnail((width, height))
        #new_im = Image.new('RGB', (width, height),"white")
        ims = []
        for p in listofimages:
            im = Image.open(p)
            im.thumbnail(size)
            im_with_border = ImageOps.expand(im,border=20,fill='white') # Bilderrahmen
            ims.append(im_with_border)
        i = 0
        x = a + 80 # Startwert
        y = 100 # Startwert
        for col in range(cols): # Platzieren der verkleinerten Bilder auf new_img
            for row in range(rows):
                #print(i, x, y)
                new_im.paste(ims[i], (x, y))
                i += 1
                y += thumbnail_height + 90
            x += thumbnail_width - 130
            y = 100
        shot_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        new_im.save(shot_time + "_collage.jpg")
    
    elif modus == 2: 
        a = int(0.08 * width)
        #b = int(0.1 * height)
        thumbnail_width = width //cols -30 # // := Nachkomma stelle abgerundet
        thumbnail_height = height //rows -30
        size = thumbnail_width, thumbnail_height # Bildgroesse
        #        new_im = Image.open("background/collage_bg_text.jpg")
        #        new_im.thumbnail((width, height))
        new_im = Image.new('RGB', (width, height),"white")
        ims = []
        for p in listofimages:
            im = Image.open(p)
            im.thumbnail(size)
            im_with_border = ImageOps.expand(im,border=30,fill='white')
            ims.append(im_with_border)
        i = 0
        x = 30 # Startwert
        y = 0 # Startwert
        for col in range(cols):
            for row in range(rows):
                #print(i, x, y)
                new_im.paste(ims[i], (x, y))
                i += 1
                y += thumbnail_height
            x += thumbnail_width
            y = 0    
        shot_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        new_im.save(shot_time + "_collage.jpg")  

def giveFileName():
    return shot_time + "_collage.jpg"

#create_collage(6000, 4000, listofimages)
