import os
import hou

def createGeoFolders():
    path = hou.pwd().parm('sopoutput').eval()
    basepath = path[:path.rindex("/")]
    if not os.path.exists(basepath):
        try:
            os.makedirs(basepath)
        except WindowsError:
            pass

def createAlembicFolders():
    path = hou.pwd().parm('filename').eval()
    basepath = path[:path.rindex("/")]
    if not os.path.exists(basepath):
        try:
            os.makedirs(basepath)
        except WindowsError:
            pass

def createMantraFolders():
    path = hou.pwd().parm('vm_picture').eval()
    basepath = path[:path.rindex("/")]
    if not os.path.exists(basepath):
        try:
            os.makedirs(basepath)
        except WindowsError:
            pass

def createCopFolders():
    path = hou.pwd().parm('copoutput').eval()
    basepath = path[:path.rindex("/")]
    if not os.path.exists(basepath):
        try:
            os.makedirs(basepath)
        except WindowsError:
            pass

def createOglFolders():
    path = hou.pwd().parm('picture').eval()
    basepath = path[:path.rindex("/")]
    if not os.path.exists(basepath):
        try:
            os.makedirs(basepath)
        except WindowsError:
            pass
