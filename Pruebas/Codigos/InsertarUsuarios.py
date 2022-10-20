#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QLineEdit,QPushButton,QDialog,QApplication
from PyQt5.Qt import pyqtSignal
from ValidacionesUsuario import ValidarUsuarioApliacion
from CustomTableView import TableViewer 
import sys,sqlite3,Mensajes
from ResourcePath import resource_path
class RegistrarUsuario(QDialog):
    close_signal=pyqtSignal()

    def __init__(self,DBconn):
        super(RegistrarUsuario, self).__init__()
        uic.loadUi(resource_path("UI/Usuarios.ui"),self)
        self.con=DBconn
        self.Cursor=DBconn.cursor()
        self.Usuario=self.findChild(QLineEdit,"Usuario")
        self.Password=self.findChild(QLineEdit,"Contrasena")
        self.buttonRegistrar=self.findChild(QPushButton,"Registrar")
        self.buttonRegistrar.clicked.connect(self.InsertarValoresUsuarios)
        self.buttonVer=self.findChild(QPushButton,"Ver")
        self.buttonVer.clicked.connect(self.VerTablaUsuarios)
        self.TV=None
        
    
    def InsertarValoresUsuarios(self):
        Usuario=self.Usuario.text()
        password=self.Password.text()
        oracion="insert or ignore into Usuarios values(?,?)"
        if self.ValidarUsuario(Usuario,password):
            self.Cursor.execute(oracion,(Usuario,password))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExito()
        
    
    def ValidarUsuario(self,Usuario,password):
        Mensaje=""
        Mensaje=ValidarUsuarioApliacion(Usuario, password, Mensaje)
        if Mensaje!="":
            Mensajes.MostrarErroresInsercion(Mensaje)
            return False
        else:
            return True
        

    
    def ClearLineEdits(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
    def VerTablaUsuarios(self):
        self.TV=TableViewer("Usuarios", self.Cursor)
        self.TV.show()    
    def closeEvent(self,event):
        self.on_close()
    def on_close(self):
        if self.TV is not None:
            self.TV.close()
        self.close_signal.emit()

     
    
if __name__=="__main__":
   con=sqlite3.Connection("../DB/ESM_pruebas.db")
   app=QApplication(sys.argv)
   window=RegistrarUsuario(con)
   window.show()
   app.exec()
