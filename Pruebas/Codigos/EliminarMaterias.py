#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton
from PyQt5.Qt import pyqtSignal
from ResourcePath import resource_path
from CustomTableView import TableViewer
from ValidacionesMaterias import ValidarEliminacionMaterias


class MateriasBorrar(QDialog):
    close_signal=pyqtSignal()

    def __init__(self,DBconnection):
        super(MateriasBorrar,self).__init__()
        uic.loadUi(resource_path("UI/EliminarMateria.ui"),self)
        self.con=DBconnection
        self.cursor=DBconnection.cursor()
        self.Clave=self.findChild(QLineEdit,"Clave")
        self.buttonBorrar=self.findChild(QPushButton,"Borrar")
        self.buttonBorrar.clicked.connect(self.BorrarMaterias)
        self.buttonVer=self.findChild(QPushButton,"Ver")
        self.buttonVer.clicked.connect(self.MostrarTabla)
        self.TV=None #TableViewer

   
    def BorrarMaterias(self):
       
        Abreviatura=self.Clave.text()
        oracion="Delete from Materias where CveMateria=?"
        if self.ValidarDatos(Abreviatura):
            self.cursor.execute(oracion,(Abreviatura,))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExitoBorrar()
    
    def ClearLineEdits(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
            
    def ValidarDatos(self,Abreviatura):
        mensaje=""
       
        if len(Abreviatura)==0:
            mensaje+="El campo esta vacio\n"
           
        else:
            mensaje=ValidarEliminacionMaterias(Abreviatura, mensaje, self.cursor)
        if mensaje!="":
            Mensajes.MostrarErroresBorrar(mensaje)
            return False
        else:
            return True
        
    

    def MostrarTabla(self):
        self.TV=TableViewer("Materias", self.cursor) 
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
    window=MateriasBorrar(con)
    window.show()
    app.exec() 