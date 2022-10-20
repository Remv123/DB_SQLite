#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLineEdit,QPushButton,QDialog
from PyQt5.Qt import pyqtSignal
import sys,sqlite3,Mensajes
from CustomTableView import TableViewer
from ValidacionesAlumnos import ValidarApellidos,ValidarBoleta,ValidarCorreo,ValidarNombre
from ResourcePath import resource_path
class Alumnos(QDialog):
    close_signal=pyqtSignal()
    def __init__(self,DBconnection):
        super(Alumnos,self).__init__()
        uic.loadUi(resource_path("UI/Alumnos.ui"),self)
        self.con=DBconnection
        self.cursor=DBconnection.cursor()
        self.Boleta=self.findChild(QLineEdit,"Boleta")
        self.Nombre=self.findChild(QLineEdit,"Nombre")
        self.Apellidos=self.findChild(QLineEdit,"ApPat")
        self.Correo=self.findChild(QLineEdit,"Correo")
        self.buttonInsertar=self.findChild(QPushButton,"Insertar")
        self.buttonInsertar.clicked.connect(self.InsertarValoresAlumnos)
        self.buttonVer=self.findChild(QPushButton,"Ver")
        self.buttonVer.clicked.connect(self.verTabla)
        self.TV=None #TableViewer
       
    
   
    
    def InsertarValoresAlumnos(self):
        Boleta=self.Boleta.text()
        Nombre=self.Nombre.text()
        Apellidos=self.Apellidos.text()
        Correo=self.Correo.text()
        if self.ValidacionesDatos(Boleta,Nombre,Apellidos,Correo):
            oracion="insert or ignore into Alumno values(?,?,?,?)"
            
            self.cursor.execute(oracion,(Boleta,Nombre,Apellidos,Correo))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExito()
    
   
    def ClearLineEdits(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
    def ValidacionesDatos(self,Boleta,Nombre,Apellidos,Correo):        
       
        Error=""
        if len(Boleta)==0 or len(Nombre)==0 or len(Apellidos)==0 or len(Correo)==0:
            Error+="Existen campos sin llenar\n"
        else:
            Error=ValidarBoleta(Boleta, Error)
            Error=ValidarNombre(Nombre, Error)
            Error=ValidarApellidos(Apellidos, Error)
            Error=ValidarCorreo(Correo, Error)
        if Error!="":
            Mensajes.MostrarErroresInsercion(Error)
            return False
        else:
           return True
       
    def verTabla(self):
       self.TV=TableViewer("Alumno",self.cursor)
       self.TV.setWindowTitle("Alumnos")
       self.TV.show()
    def closeEvent(self,event):
        self.on_close()
    def on_close(self):
        if self.TV is not None:
            self.TV.close()
        self.close_signal.emit()

     
   


     
if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=Alumnos(con)
    window.show()
    app.exec()
        





        
        