#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 20:30:53 2022

@author: rafael
"""



from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog




def openFileNameDialog(obj):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(obj,"Cargar Base de datos", "","All Files (*);;Database file (*.db)", options=options)
    if fileName:
        return fileName
    
   
    
   
