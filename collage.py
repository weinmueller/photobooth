from PIL import Image
from datetime import datetime
import signal, os, subprocess

shot_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

def create_collage(width, height, listofimages):
    cols = 2
    rows = 2
    thumbnail_width = width //cols # // := Nachkomma stelle abgerundet
    thumbnail_height = height //rows
    size = thumbnail_width -20, thumbnail_height -20 # Bildgroesse
    new_im = Image.new('RGB', (width, height),"white")
    ims = []
    for p in listofimages:
        im = Image.open(p)
        im.thumbnail(size)
        ims.append(im)
    i = 0
    x = 10 # Startwert
    y = 10 # Startwert
    for col in range(cols):
        for row in range(rows):
            #print(i, x, y)
            new_im.paste(ims[i], (x, y))
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 10
    global shot_time    
    shot_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    new_im.save(shot_time + "_collage.jpg")

def giveFileName():
    return shot_time + "_collage.jpg"

#create_collage(450, 300, listofimages)