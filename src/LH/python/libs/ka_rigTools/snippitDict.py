{

'set attr on Loop':'''
import pymel.core as pymel
myList = pymel.ls(selection)
for each in myList:
    each.attrName.set(#)
'''

}
