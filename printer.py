# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 18:18:00 2018

@author: Pascha
"""
import os, subprocess

dummy = False
printername = "Canon_SELPHY_CP1300"

def printImage(path):
    if dummy:
        print("DummyDrucker druckt...")
    else:
        print(path)
        triggerPrint = "lp -d" + printername + " " + path
        print(triggerPrint)
        os.system(triggerPrint)
    
    
