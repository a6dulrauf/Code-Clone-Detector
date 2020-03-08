# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 00:05:20 2019

@author: Syed Hassan Ali
"""

import os
import shutil


class Directory:
    
    @staticmethod
    def path(target_dir):
        dirs = None
        current_dir = os.getcwd()
        if current_dir.find('gui') != -1:
            dirs = current_dir.replace('gui', f'{target_dir}\\')
        else:
            dirs = f"{target_dir}\\"
        
        return dirs

    @staticmethod
    def get_directory_of(path):
        path = os.path.join(os.path.realpath(path) + "\\")
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def delete_dir(dir):
        print(dir)
        path = os.path.join(os.path.realpath(dir) + "\\")
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(e.__str__())

    @staticmethod
    def get_all_folders(dir):
        return os.listdir(dir)

    @staticmethod
    def make_dir(path):
        if os.path.exists(path):
            return True
        os.mkdir(path)

    @staticmethod
    def is_exist_dir(dir):
        if os.path.exists(dir):
            return True
        return False

    @staticmethod
    def search_directories(target_dir, ext):
        dirs = []
        s = ''
        for root, dirs, files in os.walk(str(target_dir)):
            for file in files:
                if file.endswith(ext):
                     s = s + os.path.join(root, file) + ','
                     
        return [x for x in s.split(',')]

    @staticmethod
    def search_directory_path(target_dir, ext):
        s = ''
        for root, dirs, files in os.walk(str(target_dir)):
            for file in files:
                if file.endswith(ext):
                     s = s + os.path.join(root, file) + ','
                     