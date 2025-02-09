#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 08:36:52 2024

@author: j.troussier
"""

import os
def generalfilecreator():
    print("game name ?")
    title = input(":")
    os.mkdir("jeufini/"+title)
    return "jeufini/"+title