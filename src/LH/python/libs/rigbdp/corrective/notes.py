'''
This list is meant to be a breadcrumb trail of UI features and strings used in UI elements that can be used to search the SHAPES library to find the code calls we need for executing code.

I will also list the mel source filenames and line numbers to make it easy to find each resource in the future

Export Keywords:
A. Tools (Dropdown menu item)
    1. Export Node Data… #command --- shapesUI_buildExportUI
        (opens options UI window) 
    2. Export Dialogue
        (new window) 
        a. Custom Export Path # --- 
            (check True) 
        b. Export Path # --- 
        c. Options  # --- 
            (subcategory)
            i.   Export Only # --- 
            ii.  All Targets # --- 
            iii. Smooth (set False) # --- 
            iv.  File format (set Maya ASCII) # --- 
!!!---> d. Export
            (This will call the command that you need)

Import
B. Tools (Dropdown menu item)
    1. Import Node Data… > #command --- shapesUtil_buildImportMenu
        a. Select File …
            (opens filepath UI window)
    C. Select Node Setup
        (new window)
        1. Filename 
            (full path, file and file - '.mel' - included) set a filepath also make sure to include the mel file and extension. ( This seems to be with \\ but probably sets to forward slashes?)
        2. Select 
            likely this will be an arg in the mel procedure, but could be a global


            







EXPORT PROCEDURE : write out a mel file that will allow you to export your system.

code in : SHAPES_utilities.mel
at line : 619
to line : 


IMPORT PROCEDURE

'''