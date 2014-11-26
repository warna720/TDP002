#! /usr/bin/env python3
#-*- coding: utf-8 -*-

"""6a__________________________________________________________________"""

def linear_search(haystack, needle, field = lambda l: l['title']):
    for obj in haystack:
        if str(field(obj)).lower() == str(needle).lower(): #More correct search
            return obj

"""6b__________________________________________________________________"""


def binary_search(haystack, needle, f = lambda l: l['title']):
    field = lambda l: f(l).lower() #More correct search
    needle = needle.lower() #More correct serch
    
    haystack.sort(key = field) #Bin search only works if it is sorted. Sorting based on searching field
    
    low = 0
    high = len(haystack) - 1
    
    while low <= high:
        mid = (low + high) // 2 #Get middle of current low and high values with integer division
        if field(haystack[mid]) < needle: #If choosen index of haystack[mid] less than needle
            low = mid + 1
        elif field(haystack[mid]) > needle: #If choosen index of haystack[mid] greater than needle
            high = mid - 1
        else: return haystack[mid]          #If match then return object


"""6c__________________________________________________________________"""

def insertion_sort(db, field = lambda l: l[0]):

    for point in range(len(db)): #For range of length of db

        #While point greater than 0 and choosen index of db[point - 1] greater than choosen index of db[point]
        while point > 0 and field(db[point - 1]) > field(db[point]):
            #Swap values
            db[point - 1], db[point] = db[point], db[point - 1]
            #Decrement by one
            point -= 1


db = [('j', 'g'), ('a', 'u'),
      ('k', 'l'), ('o', 'i'),
      ('b', 's'), ('@', '.'),
      ('p', 's'), ('o', 'e')

    ]

print("Before Insertion sort...")
print(db)
print()

insertion_sort(db, lambda e: e[0])
print("After Insertion sort...")
print(db)

print("_"*65, end="\n\n")


"""6d__________________________________________________________________"""

def quicksort(db, field = lambda l: l[0]):

    less = []
    equal = []
    greater = []

    if len(db) > 1: #If more than one obj
        pivot = db[len(db)//2] #Pivot value = middle of list

        for obj in db:
            if field(obj) < field(pivot): #If obj less than pivot
                less.append(obj)
            elif field(obj) == field(pivot): #If obj equals pivot
                equal.append(obj)
            elif field(obj) > field(pivot): #If obj greater than pivot
                greater.append(obj)
                
        #Return recursive quicksort of the lesser and greater. Return equals in middle
        return quicksort(less) + equal + quicksort(greater)
    
    else: #If one or less obj
        return db


db = [('j', 'g'), ('a', 'u'),
      ('k', 'l'), ('o', 'i'),
      ('b', 's'), ('@', '.'),
      ('p', 's'), ('o', 'e')

    ]

print("Before Quicksort...")
print(db)
print()

db = quicksort(db, lambda e: e[0])
print("After Quicksort...")
print(db)

print("_"*65, end="\n\n")


"""6e__________________________________________________________________"""

#See file 'labb6.e.py'
