#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton
from PyQt5.Qt import pyqtSignal

from CustomTableView import TableViewer
from ValidacionesAlumnos import ValidarBoleta
from ValidacionesCuentas import ValidarUsuario,ValidarFecha,VerificarBoletaCuenta,VerificarUsuarioCuenta
import sys,sqlite3,secrets,string,Mensajes

class Cuentas(QDialog):
    close_signal=pyqtSignal()

    def __init__(self,DBConnection):
        super(Cuentas,self).__init__()
        uic.loadUi("../UI/Cuentas.ui",self)
        
        self.con=DBConnection
        self.cursor=DBConnection.cursor()
        self.input1=self.findChild(QLineEdit,"Boleta")
        self.input2=self.findChild(QLineEdit,"Usuario")
        self.input3=self.findChild(QLineEdit,"Contrasena")
        self.input4=self.findChild(QLineEdit,"Fecha")
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
        alphabet= string.ascii_lowercase+string.digits+string.punctuation
        password=''.join(secrets.choice(alphabet) for i in range(6))
        self.input3.setText(password)
        
    def InsertarDatosCuenta(self):
        Boleta=self.input1.text()
        Usuario=self.input2.text()
        Contrasena=self.input3.text()
        Fecha=self.input4.text()
        oracion="""insert or ignore into Cuenta(CveAlumno,NombreCuenta,Contrasena,Semestre) values(?,?,?,?)"""
        if  self.VerificarDatos(Boleta, Usuario, Contrasena, Fecha):
            self.cursor.execute(oracion,(Boleta,Usuario,Contrasena,Fecha))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExito()
    def ClearLineEdits(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
    
    def VerificarDatos(self,Boleta,Usuario,Contrasena,Fecha):
        errores=0
        Mensaje=""
        if len(Boleta)==0 or len(Usuario)==0 or len(Contrasena)==0 or len(Fecha)==0:
            Mensaje+="Existen campos sin llenar\n"
            errores+=1
        Mensaje,errores=ValidarBoleta(Boleta, Mensaje, errores)
        Mensaje,errores=ValidarUsuario(Usuario, Mensaje, errores)
        Mensaje,errroes=ValidarFecha(Fecha, Mensaje, errores)
        Mensaje, errores=VerificarBoletaCuenta(Boleta, Mensaje,errores,self.con)
        Mensaje, errores=VerificarUsuarioCuenta(Boleta,Fecha,Mensaje,errores,self.con)
        if errores>0:
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
        