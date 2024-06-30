import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pymel

import os
import pickle



def add(key, pyObject):
    clipBoardData = _getClipBoardData()
    clipBoardData[key] = pyObject
    pickle.dump( clipBoardData, open(_getClipBoardFile(), "wb") )
    return pyObject

def get(key, defaultValue=None):
    clipBoardData = _getClipBoardData()
    return clipBoardData.get(key, defaultValue)

def _getClipBoardFile():
    userPrefDir = pymel.internalVar(userPrefDir=True)
    return os.path.join(userPrefDir, 'ka_clipBoard.p')

def _getClipBoardData():
    clipBoardFile = _getClipBoardFile()
    try:
        clipBoardData = pickle.load( open( clipBoardFile, "rb" ) )
    except:
        pymel.warning('clipBoard experienced an error, and has been reset')
        clipBoardData = {}
        pickle.dump( {}, open( clipBoardFile, "wb" ) )

    return clipBoardData