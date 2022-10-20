#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton
from PyQt5.Qt import pyqtSignal
from ResourcePath import resource_path
from CustomTableView import TableViewer
from ValidacionesAlumnos import ValidarBoleta
from ValidacionesCuentas import VerificarBoletaCuenta,VerificarUsuarioCuenta
import sys,sqlite3,secrets,string,Mensajes

class Cuentas(QDialog):
    close_signal=pyqtSignal()

    def __init__(self,DBConnection):
        super(Cuentas,self).__init__()
        uic.loadUi(resource_path("UI/Cuentas.ui"),self)
        self.con=DBConnection
        self.cursor=DBConnection.cursor()
        self.input1=self.findChild(QLineEdit,"Boleta")
        self.input3=self.findChild(QLineEdit,"Contrasena")
        self.button1=self.findChild(QPushButton,"Generar")
        self.button1.clicked.connect(self.GenerarContrasena)
        self.button2=self.findChild(QPushButton,"Insertar")
        self.button2.clicked.connect(self.InsertarDatosCuenta)
        self.buttonVer=self.findChild(QPushButton,"Ver")
        self.buttonVer.clicked.connect(self.VerCuentas)
        self.buttonAl=self.findChild(QPushButton,"VerAl")
        self.buttonAl.clicked.connect(self.VerAlumnos)
        self.TV=None #TableViewer

    
    def GenerarContrasena(self):
        longitud=6 
        alphabet= string.ascii_lowercase+string.digits+string.punctuation
        password=''.join(secrets.choice(alphabet) for i in range(longitud))
        self.input3.setText(password)
        
    def InsertarDatosCuenta(self):
        Boleta=self.input1.text()
        Contrasena=self.input3.text()
        oracion="""insert or ignore into Cuenta(CveAlumno,NombreCuenta,Contrasena) values(?,?,?)"""
        if  self.VerificarDatos(Boleta, Contrasena):
            self.cursor.execute(oracion,(Boleta,Boleta,Contrasena))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExito()
    def ClearLineEdits(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
    
    def VerificarDatos(self,Boleta,Contrasena):
        Mensaje=""
        if len(Boleta)==0  or len(Contrasena)==0:
            Mensaje+="Existen campos sin llenar\n"
          
        else:
            Mensaje=ValidarBoleta(Boleta, Mensaje)
            Mensaje=VerificarBoletaCuenta(Boleta, Mensaje,self.con)
            Mensaje=VerificarUsuarioCuenta(Boleta,Mensaje,self.con)
        if Mensaje!="":
            Mensajes.MostrarErroresInsercion(Mensaje)
            return False
        else:
            return True
            
     
    def VerCuentas(self):
        self.TV=TableViewer("Cuenta", self.cursor)
        self.TV.show()
    def VerAlumnos(self):
          self.TV=TableViewer("Alumno", self.cursor)
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
    window=Cuentas(con)
    window.show()
    app.exec()
        