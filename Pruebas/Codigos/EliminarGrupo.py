#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton
from PyQt5.Qt import pyqtSignal
from ResourcePath import resource_path
from CustomTableView import TableViewer
from ValidacionesGrupo import ValidarClaveGrupo


class GrupoBorrar(QDialog):
    close_signal=pyqtSignal()

    def __init__(self,DBconnection):
        super(GrupoBorrar,self).__init__()  
        uic.loadUi(resource_path("UI/EliminarGrupos.ui"),self)
        self.con=DBconnection
        self.cursor=DBconnection.cursor()
        self.input1=self.findChild(QLineEdit,"Grupo")
        self.button1=self.findChild(QPushButton,"Borrar")
        self.button1.clicked.connect(self.BorrarGrupo)
        self.button2=self.findChild(QPushButton, "Ver")
        self.button2.clicked.connect(self.VerTabla)
        self.TV=None #TableViewer

       
    def BorrarGrupo(self):
        Clave=self.input1.text()
        oracion="Delete from Grupo where CveGrupo=?"
        if self.VerificarDatos(Clave):
            self.cursor.execute(oracion,(Clave,))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExitoBorrar()
    def ClearLineEdits(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
    def VerificarDatos(self,Grupo):
        Mensaje=""
        Mensaje=ValidarClaveGrupo(Grupo)
        if Mensaje!="":
            Mensajes.MostrarErroresBorrar(Mensaje)
            return False
        else:
            return True
    def VerTabla(self):
        self.TV=TableViewer("Grupo", self.cursor)
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
    window=GrupoBorrar(con)
    window.show()
    app.exec() 
