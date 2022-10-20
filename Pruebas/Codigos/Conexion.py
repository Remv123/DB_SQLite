#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QFileDialog,QMessageBox,QMainWindow,QLineEdit,QPushButton
import sqlite3
from ValidacionesUsuario import VerificarUsuario
from Menu import MainWindow
from ResourcePath import resource_path
class ConexionDB(QMainWindow):
    def __init__(self):
        super(ConexionDB,self).__init__()
        uic.loadUi(resource_path("UI/Conexion.ui"),self)
       
        self.Usuario=self.findChild(QLineEdit,"Usuario")
        self.Contrasena=self.findChild(QLineEdit,"Contrasena")
        self.Conectar=self.findChild(QPushButton,"Conectar")
        self.Conectar.clicked.connect(self.ConectarDB)
    
    def ConectarDB(self):
        mensaje=QMessageBox()
        name=self.Usuario.text()
        password=self.Contrasena.text()
        conexion,a=QFileDialog.getOpenFileName(self,"Base de datos",filter="*.db")
        self.con=sqlite3.connect(conexion) #conexión a la base de datos
        if VerificarUsuario(name, password, self.con):
             MainWindow(self.con,name).show()
             self.close()
        else:
            mensaje.setText("Usuario o Contrasena no valido")
            mensaje.exec_()
            self.con.close()
        
        
    
    
if __name__ =="__main__":           
    if not QtWidgets.QApplication.instance():
        app=QtWidgets.QApplication(sys.argv)
    else:
        app=QtWidgets.QApplication.instance()
    Window=ConexionDB()
    Window.show()
    app.exec()
        