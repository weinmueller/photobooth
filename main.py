# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 18:13:15 2018

@author: Pascha
"""

# gphoto --auto-detect

import gui
import imageCapture
import telegram

# main
# 0. Telegram Bot starten
telegram.BotMessage("Hallo, die Photobooth wurde gestartet!")

# 1. Ordner erstellen + Pfad herauslesen
imageCapture.createSaveFolder()

# 2. Gui starten
gui.WelcomePhotoBooth()

# 3. Dauerschleife GUI
gui.root.mainloop()