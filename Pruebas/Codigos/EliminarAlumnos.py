#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3,Mensajes,sys
from PyQt5 import QtWidgets, uic
from CustomTableView import TableViewer
from ValidacionesAlumnos import ValidarBoleta,VerificarBoletaBaseDatos

class AlumnoBorrar(QtWidgets.QDialog):
    def __init__(self,DBconnection):
        super(AlumnoBorrar,self).__init__()
        uic.loadUi("../UI/ElimnarAlumno.ui",self)
        self.con=DBconnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"Boleta")
        self.button1=self.findChild(QtWidgets.QPushButton,"Eliminar")
        self.button1.clicked.connect(self.BorrarAlumno)
        self.button2=self.findChild(QtWidgets.QPushButton,"Ver")
        self.button2.clicked.connect(self.VerTabla)
    
    def BorrarAlumno(self):
        cursor=self.con.cursor()
        Boleta=self.input1.text()
        oracion="Delete from Alumno where CveAlumno=?"
        if self.ValidacionesDatos(Boleta):
            cursor.execute(oracion,(Boleta,))
            Mensajes.MostrarExitoBorrar()
            self.con.commit()
    
    def ValidacionesDatos(self,Boleta):        
        Errores=0
        Mensaje=""
        Mensaje,Errores=ValidarBoleta(Boleta, Mensaje, Errores)
        Mensaje,Errores=VerificarBoletaBaseDatos(Boleta, Mensaje, Errores, self.con)
        if Errores>0:
             Mensajes.MostrarErroresBorrar(Mensaje)
             return False
        else:
            return True
    
    def VerTabla(self):
        self.TV=TableViewer("Alumno", self.con)
        self.TV.show()

if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=AlumnoBorrar(con)
    window.show()
    app.exec()
        
        
    
    
        