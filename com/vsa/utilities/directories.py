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
        current_dir = os.getcwd()
        if current_dir.find('gui') != -1:
            return os.path.join(current_dir.replace('gui', target_dir), '')
        return os.path.join(target_dir, '')

    @staticmethod
    def get_directory_of(path):
        path = os.path.realpath(path) + os.sep
        os.makedirs(path, exist_ok=True)
        return path

    @staticmethod
    def delete_dir(dir):
        path = os.path.realpath(dir)
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass
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
        # ext may be a single extension ('.java') or an iterable of them
        # (('.cpp', '.h')). str.endswith accepts a tuple of suffixes.
        exts = (ext,) if isinstance(ext, str) else tuple(ext)
        s = ''
        for root, subdirs, files in os.walk(str(target_dir)):
            for file in files:
                if file.endswith(exts):
                     s = s + os.path.join(root, file) + ','

        return [x for x in s.split(',')]
                     