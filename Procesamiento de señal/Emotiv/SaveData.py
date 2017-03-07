# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 15:09:26 2017

@author: User
"""


import csv
w = csv.writer(open("output.csv", "w"))
for key, val in dict.items():
    w.writerow([key, val])

dict = {}
for key, val in csv.reader(open("input.csv")):
    dict[key] = val