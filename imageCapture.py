from time import sleep
from datetime import datetime
import signal, os, subprocess

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

triggerCommand = "gphoto2 --capture-image-and-download"

folder_name = shot_date
save_location = "/home/pi/Desktop/photobooth_pascal/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create the new directory.")
    os.chdir(save_location)
    
def captureImages():
    os.system(triggerCommand)
    print("Bild wurde geschossen")
    
def renameFiles():
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".jpg"):
                global shot_time
                shot_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                os.rename(filename, (shot_time + ".jpg"))
                print("Renamed the JPG.")

def giveFolderName():
    return save_location

def giveFileName():
    return shot_time + ".jpg"
#createSaveFolder()
#captureImages()
#renameFiles()


    
        
