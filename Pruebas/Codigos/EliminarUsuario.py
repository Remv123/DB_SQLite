#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton
from PyQt5.Qt import pyqtSignal

from CustomTableView import TableViewer 
import sys,sqlite3,Mensajes

class EliminarUsuario(QDialog):
    close_signal=pyqtSignal()

    def __init__(self,DBconn):
        super(EliminarUsuario, self).__init__()
        uic.loadUi("../UI/EliminarUsuarios.ui",self)
        self.con=DBconn
        self.Cursor=DBconn.cursor()
        self.Usuario=self.findChild(QLineEdit,"Usuario")
       
        self.buttonEliminar=self.findChild(QPushButton,"Eliminar")
        self.buttonEliminar.clicked.connect(self.EliminarValoresUsuarios)
        self.buttonVer=self.findChild(QPushButton,"Ver")
        self.buttonVer.clicked.connect(self.VerTablaUsuarios)
        self.TV=None #TableViewer

        
    
    def EliminarValoresUsuarios(self):
        Usuario=self.Usuario.text()
        oracion="Delete from Usuarios where NombreUsuario=?"
        self.Cursor.execute(oracion,(Usuario,))
        self.con.commit()
        self.ClearLineEdits()
        Mensajes.MostrarExitoBorrar()
    
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
   app=QtWidgets.QApplication(sys.argv)
   window=EliminarUsuario(con)
   window.show()
   app.exec()
