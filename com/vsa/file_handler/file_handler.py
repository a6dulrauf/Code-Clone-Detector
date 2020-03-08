# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 01:35:25 2019

@author: Syed Hassan Ali
"""

from com.vsa.elements.features import Features
from com.vsa.utilities.directories import Directory
import os

class File_Handler:
    
    def __init__(self):
        pass

    def read_file(self, file_path):
        try:
            with open(file_path) as f:
                return f.readlines()
        except Exception as e:
            print(e.__str__)

    def read_file_bi_gram(file_path):
        try:
            with open(file_path) as f:
                s = ''
                for line in f.readlines():
                    s = s+line
                return s
        except Exception as e:
            print(e.__str__)
            
    def normalize(lines):
        replaceLines = lines
        normalizedLines = ''
        ''''
        for line in lines.split('\n'):
            for word in line.split(' '):
                if word in Features.features:
                    normalizedLines+=word+' '
                for ch in word:
                    if ch in Features.features:
                        normalizedLines+=ch+' '
    
        '''
        for line in replaceLines.split('\n'):
            
            s = ''
            for word in line.split(' '):
                if word not in Features.features:
                    line = line.replace(word,'')
            normalizedLines += line

        #print(normalizedLines)
        return normalizedLines

    @staticmethod
    def write_file(file, path):
        path = Directory.get_directory_of(path)
        with open(path + str(file.name), "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    @staticmethod
    def delete_all_files(path):
        path = Directory.get_directory_of(path)

        for file in os.listdir(path):
            os.remove(file)
