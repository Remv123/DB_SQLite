#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import  QFileDialog




def openFileNameDialog(obj):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(obj,"Cargar Base de datos", "","All Files (*);;Database file (*.db)", options=options)
    if fileName:
        return fileName


def SaveFileNameDialog(obj):
    opcion=""
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(obj,"Respaldar Base de datos", "","All Files (*);;Database file (*.db);;Excel files(.xlsx)", options=options)
    if fileName:
        return fileName
    
   
    
   
