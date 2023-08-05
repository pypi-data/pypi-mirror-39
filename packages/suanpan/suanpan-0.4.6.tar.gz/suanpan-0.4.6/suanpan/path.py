# coding=utf-8
from __future__ import print_function

import hashlib
import os
import shutil
import base64


def safeMkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def safeMkdirsForFile(filepath):
    return safeMkdirs(os.path.dirname(os.path.abspath(filepath)))


def merge(paths, dist, mode="move"):
    safeMkdirs(dist)
    mergeFunc = getattr(shutil, mode)
    for path in paths:
        if os.path.isfile(path):
            mergeFunc(path, dist)
        else:
            for p in os.listdir(path):
                subpath = os.path.join(path, p)
                mergeFunc(subpath, dist)
            if mode == "move":
                os.rmdir(path)
    return dist


def md5(filepath, block_size=64 * 1024):
    with open(filepath, "rb") as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
    return base64.b64encode(md5.digest()).decode()


def empty(folder):
    return [remove(os.path.join(folder, path)) for path in os.listdir(folder)]


def remove(path):
    removeFunction = removeFile if os.path.isfile(path) else removeFolder
    return removeFunction(path)


def removeFile(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)
    return filePath


def removeFolder(folderPath):
    if os.path.exists(folderPath):
        shutil.rmtree(folderPath)
    return folderPath
