#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 19:57:13 2022

@author: rafael
"""

from PyQt5 import uic,QtWidgets



class VerificarContrasena(QtWidgets.QDialog):
    def __init__(self):
        super(VerificarContrasena,self).__init__()
        uic.loadUi("../UI/VerificarContrasena.ui",self)
        self.line1=self.findChild(QtWidgets.QLineEdit,"Contrasena")
        self.Button1=self.findChild(QtWidgets.QPushButton,"Verificar")
        self.password=""
        self.Button1.clicked.connect(self.CheckPassword)
        
    
    def CheckPassword(self):
        self.password=self.line1.text() 
        self.accept()
        return self.password
    
    def GetValue(self):
        return self.password



   
   
    
    

    