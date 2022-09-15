#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3,Mensajes,sys
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton
from PyQt5.Qt import pyqtSignal

from PyQt5 import QtWidgets, uic
from CustomTableView import TableViewer
from ValidacionesAlumnos import ValidarBoleta,VerificarBoletaBaseDatos

class AlumnoBorrar(QDialog):
    close_signal=pyqtSignal()

    def __init__(self,DBconnection):
        super(AlumnoBorrar,self).__init__()
        uic.loadUi("../UI/ElimnarAlumno.ui",self)
        self.con=DBconnection
        self.cursor=DBconnection.cursor()
        self.input1=self.findChild(QLineEdit,"Boleta")
        self.button1=self.findChild(QPushButton,"Eliminar")
        self.button1.clicked.connect(self.BorrarAlumno)
        self.button2=self.findChild(QPushButton,"Ver")
        self.button2.clicked.connect(self.VerTabla)
        self.TV=None #TableViewer

  
    def BorrarAlumno(self):
        Boleta=self.input1.text()
        oracion="Delete from Alumno where CveAlumno=?"
        if self.ValidacionesDatos(Boleta):
            self.cursor.execute(oracion,(Boleta,))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExitoBorrar()
            
    def ClearLineEdits(self):
         for child in self.findChildren(QLineEdit):
             child.clear()
    
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
    window=AlumnoBorrar(con)
    window.show()
    app.exec()
        
        
    
    
        