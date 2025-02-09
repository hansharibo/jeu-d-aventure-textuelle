#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 08:35:16 2024

@author: j.troussier
"""
import os
from tkinter import *

def worldcreation(granddirector):
    try:
        os.mkdir(granddirector+"/world")
    except:
        print()
    print("welcome to the world creator")
    print("how many world do you wish to create ?")
    number = input(":")
    for i in range(int(number)):
        os.mkdir(granddirector+"/world/"+"world" + str(i))
    mywin = Tk()
    mywin.title("creation room")
    mywin.geometry("300x200")