#! /usr/bin/env python3
#-*- coding:utf-8 -*-
import os, argparse

def add_copyright(f, copyright_data):
    updated_files = {}
    
    for file in f:
        if isinstance(file, str):
            file = {file:f[file]}
        for filename in file:
            file_content = file[filename]
            if contains_copyright(file_content):
                file = file_content
                file = remove_copyright(file)
                file = insert_copyright(file, copyright_data.values())
                updated_files[filename] = file
    return updated_files

def contains_copyright(f):
    """Returns True if argument contains begin copyright tag, else returns a empty list which evaluates to False"""
    return [True for line in f if 'BEGIN COPYRIGHT' in line]

def remove_copyright(f):
    """Removes old copyright information and inserts a newline in between begin and end tags"""
    beginnings  = get_all_in(f, 'BEGIN COPYRIGHT')
    endings     = get_all_in(f, 'END COPYRIGHT')

    #Need to delete backwards else the indexes get corrupted
    for x in range(len(beginnings) - 1, -1, -1):
        f[beginnings[x] + 1 : endings[x]] = "\n"
    return f

def insert_copyright(f, copyright_data):
    """Inserts new copyright information between the begin and end tags"""
    beginnings = get_all_in(f, 'BEGIN COPYRIGHT')

    #Need to insert backwards else the indexes get corrupted
    for beginning in reversed(beginnings):
        for copyright_lines in copyright_data:  
            for x, line in enumerate(copyright_lines, start = 1):
                f.insert(beginning + x, line)
    return f
        

def get_files(f, extension=None):
    """Returns all lines from a file inserted to a dict with filename as key and content as value and appended to a list, if a folder is given, multiple dicts gets appenden to the list"""
    if os.path.isdir(f):
        if f[-1] != '/': f += '/'
        files = []
        for file in os.listdir(f):
            #Recursive, first param is the folder + filename
            files.append(get_files(f + file, extension))
        return files
    else:
        try:
            f_buffer = open(f)
            lines = {}
            #If file has same extension as given extension
            if extension and same_extension(f, extension):
                lines[f] = f_buffer.readlines()
            elif not extension:
                lines[f] = f_buffer.readlines()
            return lines
        except:
            raise IOError
        finally:
            f_buffer.close()

def same_extension(f_extension, s_extension):
    if f_extension.split('.')[-1] == s_extension.split('.')[-1]:
        return True
    return False

def get_in_index(haystack, needle):
    """Get index of first occurrence"""
    for index, line in enumerate(haystack):
        if needle in line:
            return index

def get_all_in(haystack, needle):
    """Get all indexes of the occurrences"""
    return [i for i, line in enumerate(haystack) if needle in line]

def get_new_extension(f, f_extension):
    f_extension = f_extension.split('.')[-1]
    f = f.split('.')
    return '.'.join(f[:-1]) + '.' + f_extension

def write_files(f, f_extension):
    for file in f:
        file_name = file
        if f_extension:
            file_name = get_new_extension(file, f_extension)
        f_buffer = open(file_name, 'w')
        for line in f[file]:
            f_buffer.write(line)
        if f_extension:
            remove_files(file)

def remove_files(file):
    os.remove(file)

def dev_print(f):
    for file in f:
        print(file)
        print("_" * 20)
        for line in f[file]:
            print(line)

parser = argparse.ArgumentParser(description='Add or replace copyright information.')
parser.add_argument('copyright', help='The file which holds the copyright data.')
parser.add_argument('files', help='The folder or files that the operation should work on.')
parser.add_argument('-f', help='Choose which extensions the operation should work on.')
parser.add_argument('-s', help='Choose file extension for the result file.')
args = parser.parse_args()

f = get_files(args.files, extension = args.f)
cpy = get_files(args.copyright)
f = add_copyright(f, cpy)

print("STARTING")
write_files(f, args.s)
#dev_print(f)
print("DONE")
