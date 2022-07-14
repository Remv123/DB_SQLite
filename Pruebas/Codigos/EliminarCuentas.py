#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5 import QtWidgets,uic
from CustomTableView import TableViewer
from ValidacionesAlumnos import ValidarBoleta
from ValidacionesCuentas import ValidarFecha

class CuentasBorrar(QtWidgets.QDialog):
    def __init__(self,DBconnection):
        super(CuentasBorrar,self).__init__()
        uic.loadUi("../UI/EliminarCuentas.ui",self)
        self.con=DBconnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"Boleta")
        self.input2=self.findChild(QtWidgets.QLineEdit,"Semestre")
        self.button1=self.findChild(QtWidgets.QPushButton,"Borrar")
        self.button1.clicked.connect(self.BorrarCuenta)
        self.button2=self.findChild(QtWidgets.QPushButton,"Ver")
        self.button2.clicked.connect(self.VerCuentas)
        
    def BorrarCuenta(self):
        cursor=self.con.cursor()
        Boleta=self.input1.text()
        Semestre=self.input2.text()
        oracion="""delete from Cuenta where CveAlumno=? and Semestre=?"""
        if self.ValidacionesBorrar(Boleta,Semestre):
            cursor.execute(oracion,(Boleta,Semestre))
            self.con.commit()
            Mensajes.MostrarExitoBorrar()
    
    def ValidacionesBorrar(self,Boleta,Semestre):
        Errores=0
        Mensaje=""
        if len(Boleta)==0 or len(Semestre)==0:
            Mensaje+="Existe algún campo vacio\n"
            Errores+=1
        Mensaje,Errores=ValidarBoleta(Boleta, Mensaje, Errores)
        Mensaje,Errores=ValidarFecha(Semestre, Mensaje, Errores)
        if Errores>0:
            Mensajes.MostrarErroresBorrar(Mensaje)
            return False
        else:
            return True
        
        
    
    def VerCuentas(self):
        self.TV=TableViewer("Cuenta", self.con)
        self.TV.show()
      
    def __exit__(self):
        self.con.close()
if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=CuentasBorrar(con)
    window.show()
    app.exec()
        