#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic
import sys,sqlite3,Mensajes
from CustomTableView import TableViewer
from ValidacionesAlumnos import ValidarApellidos,ValidarBoleta,ValidarCorreo,ValidarNombre

class Alumnos(QtWidgets.QDialog):
    def __init__(self,DBconnection):
        super(Alumnos,self).__init__()
        uic.loadUi("../UI/Alumnos.ui",self)
        self.con=DBconnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"Boleta")
        self.input2=self.findChild(QtWidgets.QLineEdit,"Nombre")
        self.input3=self.findChild(QtWidgets.QLineEdit,"ApPat")
        self.input4=self.findChild(QtWidgets.QLineEdit,"Correo")
       
        self.button1=self.findChild(QtWidgets.QPushButton,"Insertar")
        self.button1.clicked.connect(self.InsertarValoresAlumnos)
        self.button2=self.findChild(QtWidgets.QPushButton,"Ver")
        self.button2.clicked.connect(self.verTabla)
    
    def InsertarValoresAlumnos(self):
        cursor=self.con.cursor()
        Boleta=self.input1.text()
        Nombre=self.input2.text()
        Apellidos=self.input3.text()
        Correo=self.input4.text()
        if self.ValidacionesDatos(Boleta,Nombre,Apellidos,Correo):
            oracion="insert or ignore into Alumno values(?,?,?,?)"
            cursor.execute(oracion,(Boleta,Nombre,Apellidos,Correo))
            self.con.commit()
            Mensajes.MostrarExito()
    
   
    def ValidacionesDatos(self,Boleta,Nombre,Apellidos,Correo):        
        Errores=0
        Error=""
        if len(Boleta)==0 or len(Nombre)==0 or len(Apellidos)==0 or len(Correo)==0:
            Error+="Existen campos sin llenar\n"
            Errores+=1
        Error,Errores=ValidarBoleta(Boleta, Error, Errores)
        Error,Errores=ValidarNombre(Nombre, Error, Errores)
        Error,Errores=ValidarApellidos(Apellidos, Error, Errores)
        Error,Errores=ValidarCorreo(Correo, Error, Errores)
        if Errores>0:
            Mensajes.MostrarErroresInsercion(Error)
            return False
        else:
           return True
       
    def verTabla(self):
       self.TV=TableViewer("Alumno",self.con)
       self.TV.setWindowTitle("Alumnos")
       self.TV.show()
 

     
    def __exit__(self):
        self.con.close()


     
if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=Alumnos(con)
    window.show()
    app.exec()
        





        
        