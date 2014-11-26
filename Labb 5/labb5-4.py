#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os, sys

functions = [
            'pwd',    'cd',
            'ls',     'cat'
            ]

def pwd(PATH):
    print(PATH)

def cd(PATH):
    new_path = args[0]
    
    if new_path == '..':
        PATH = PATH.split('/')
        PATH = '/'.join(PATH[:-2])

    elif new_path == '/':
        PATH = ""
        
    elif os.path.isdir(PATH + new_path):
        PATH += new_path.rstrip('/')
        
    else:
        print("Dir does not exist.")
        return None     #If not valid arg, dont add slash and return from function
        
    PATH += '/'
    return PATH
    
def ls(PATH):
    #If not path add to list, if path add to list with '/' at end
    l = ([obj + '/' if os.path.isdir(PATH + obj) else obj for obj in os.listdir(PATH)])
    for obj in l:
        print(obj)
    
def cat(PATH):
    #obj = args[0]
    for obj in args:
        if os.path.isfile(PATH + obj):
            f = open(PATH + obj)
            f_content = f.read()
            print(f_content)
            
def call_function(PATH):
    temp = ""
    if cm in functions:                 #if command is valid
        temp = eval(cm)(PATH)
    
    if temp ==  None:
        return PATH
    else:
        return temp

PATH = '/home/'
while(True):
    cm = input('command> ').split(' ')  #Split command from args
    cm, args = cm[0], cm[1:]            #cm = command and args = arguments
    PATH = call_function(PATH)
