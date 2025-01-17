#====================================================================================
#====================================================================================
#
# __init__ of ka_rigTools
#
# DESCRIPTION:
#   will import all specified modules globaly so that they can be activly called by
#   hotkeys and menu items (which will also be setup during this process)
#
# DEPENDENCEYS:
#   run the following code to setup the tool kit:
#
#   import ka_rigTools
#   reload(ka_rigTools)
#
#   and the rest will be setup by similar __inits__
#
#
# AUTHOR:
#   Kris Andrews (3dkris@3dkris.com)
#
#====================================================================================
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are
#met:

    #(1) Redistributions of source code must retain the above copyright
    #notice, this list of conditions and the following disclaimer.

    #(2) Redistributions in binary form must reproduce the above copyright
    #notice, this list of conditions and the following disclaimer in
    #the documentation and/or other materials provided with the
    #distribution.

    #(3)The name of the author may not be used to
    #endorse or promote products derived from this software without
    #specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
#INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#POSSIBILITY OF SUCH DAMAGE.
#====================================================================================
import os
import sys
import importlib
sys.dont_write_bytecode = True


import maya.cmds as cmds
cmds.evalDeferred("import maya.cmds as cmds")
import maya.mel as mel
cmds.evalDeferred("import maya.mel as mel")

cmds.evalDeferred("import pymel.core as pymel")

# insure that the user directory is the first in sys.path
userScriptDir = os.path.abspath(os.path.join(cmds.internalVar(userScriptDir=True), '..', '..', 'scripts'))
if userScriptDir in sys.path:
    sys.path.remove(userScriptDir)
    sys.path.insert(0, userScriptDir)

#
#dirList = os.listdir(os.path.dirname(__file__))
#pyFiles = []
#melFiles = []
#for file in dirList:
#    if not file.startswith('__'):
#        file = file.split('.')
#        if len(file) == 2:
#            if file[1] == 'py':
#                pyFiles.append(file[0])
#            elif file[1] =='mel':
#                melFiles.append(file[0])

try:  #------------------------------------------------------------------------------
    print('\nloading ka_rigTools...')

    #import ka_hotkeys
    #reload(ka_hotkeys)
    #print '    -loaded: ka_hotkeys -loaded '
    #
    #import ka_menu
    #reload(ka_menu)
    #print '    -loaded: ka_menu -loaded '

    from . import ka_mayaCommandOverrides
    importlib.reload(ka_mayaCommandOverrides)
    print('    -loaded: ka_mayaCommandOverrides')

#    mel.eval("source ka_library;")
#    print '    -sourced: ka_library'
#
#    mel.eval("source ka_hyperGraphMM;")
#    print '    -sourced: ka_hyperGraphMM'


    print('loaded ka_rigTools successfully')
except:
    print("Unexpected error:", sys.exc_info()[0])
    print('\n  FAILED to fully load ka_rigTools')

#log = 0
#importList = ['ka_hotkeys', 'ka_menu', 'ka_menu_modelEditor', 'ka_menu_hyperShade', 'ka_mayaCommandOverrides', 'ka_weightPainting', 'ka_util', 'ka_hyperShade', 'ka_hyperShade', ]
#sourceList = ['ka_library']

#
#print 'ka_rigTools loading #################################################################################################################\n'
#
#try:
#    for each in importList:
#        print each+'...',
#
#        try:  #------------------------------------------------------------------------------
#            if log:print "from ka_rigTools import %s; reload(%s)" % (each, each)
#            cmds.evalDeferred("from ka_rigTools import %s; reload(%s)" % (each, each))
#            #eval('reload('+each+')')
#            print '      ...loaded'
#        except:
#            print "Unexpected error:", sys.exc_info()[0]
#            print '\n  FAILED to load'
#
#
#        pass
#    for each in sourceList:
#        try:  #------------------------------------------------------------------------------
#            if log:print "from ka_rigTools import %s; reload(%s)" % (each, each)
#            mel.eval("source %s;" % each)
#            print '%s loaded ' % each
#            if log:print ' '
#        except:
#            print 'FAILED to load "%s" \n' % each
#
#
#    print '\nka_rigTools loaded successfully #####################################################################################################\n'
#except:
#    print '\n!ka_rigTools experienced errors X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!X!\n'
