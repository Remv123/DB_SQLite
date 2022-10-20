#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton
from PyQt5.Qt import pyqtSignal
from ResourcePath import resource_path
from PyQt5 import QtWidgets,uic
from CustomTableView import TableViewer
from ValidacionesAlumnos import ValidarBoleta
from ValidacionesCuentas import ValidarFecha


class CuentasBorrar(QDialog):
    close_signal=pyqtSignal()

    def __init__(self,DBconnection):
        super(CuentasBorrar,self).__init__()
        uic.loadUi(resource_path("UI/EliminarCuentas.ui"),self)
        self.con=DBconnection
        self.cursor=DBconnection.cursor()
        self.input1=self.findChild(QLineEdit,"Boleta")
        self.button1=self.findChild(QPushButton,"Borrar")
        self.button1.clicked.connect(self.BorrarCuenta)
        self.button2=self.findChild(QPushButton,"Ver")
        self.button2.clicked.connect(self.VerCuentas)
        self.TV=None #TableViewer

   
        
    def BorrarCuenta(self):
        Boleta=self.input1.text()
       
        oracion="""delete from Cuenta where CveAlumno=?"""
        if self.ValidacionesBorrar(Boleta):
            self.cursor.execute(oracion,(Boleta,))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExitoBorrar()
    
    
    def ClearLineEdits(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
    
    def ValidacionesBorrar(self,Boleta):
        Mensaje=""
        if len(Boleta)==0 :
            Mensaje+="Existe algún campo vacio\n"
        else:
            Mensaje=ValidarBoleta(Boleta, Mensaje)
        if Mensaje!="":
            Mensajes.MostrarErroresBorrar(Mensaje)
            return False
        else:
            return True
        
        
    
    def VerCuentas(self):
        self.TV=TableViewer("Cuenta", self.cursor)
        self.TV.show()
    def closeEvent(self,event):
        self.on_close()
    def on_close(self):
        if self.TV is not None:
            self.TV.close()
        self.close_signal.emit()
      
    
if __name__=="__main__":
    con=sqlite.Connection("../DB/ESM.db")
    app=QtWidgets.QApplication(sys.argv)
    window=CuentasBorrar(con)
    window.show()
    app.exec()
        