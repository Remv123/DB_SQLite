#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import uic,QtWidgets
from PyQt5.Qt import pyqtSignal
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton
from CustomTableView import TableViewer
from ValidacionesGrupo import ValidarClaveGrupo
import sqlite3,Mensajes,sys
from ResourcePath import resource_path
class Grupo(QDialog):
    close_signal=pyqtSignal()
    def __init__(self,DBconnection):
        super(Grupo, self).__init__()
        uic.loadUi(resource_path("UI/Grupos.ui"),self)
        self.con=DBconnection
        self.cursor=DBconnection.cursor()


        self.input1=self.findChild(QLineEdit,"Grupo")
        self.button1=self.findChild(QPushButton,"Insertar")
        self.button1.clicked.connect(self.InsertarGrupo)
        self.button2=self.findChild(QPushButton,"Ver")
        self.button2.clicked.connect(self.VerGrupos)
        self.TV=None #TableViewer

        
    
    def InsertarGrupo(self):
        NombreGrupo=self.input1.text()
        oracion="insert or ignore into Grupo(CveGrupo,GrupoSemestre) values (?,?)"
        if self.ValidarGrupo(NombreGrupo):
            Semestre=NombreGrupo[0]+"°"
            if NombreGrupo[0]=="A":
                Semestre="10°"
            if NombreGrupo[0]=="B":
                Semestre="11°"
            if NombreGrupo[0]=="C":
                Semestre="12°"

            self.cursor.execute(oracion,(NombreGrupo,Semestre))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExito()
    def ClearLineEdits(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
    def ValidarGrupo(self,Grupo):
        Mensaje=""
     
        Mensaje=ValidarClaveGrupo(Grupo)
        if Mensaje!="":
            Mensajes.MostrarErroresInsercion(Mensaje)
            return False
        else:
            return True

      
    def closeEvent(self,event):
        self.on_close()
    def on_close(self):
        if self.TV is not None:
            self.TV.close()
        self.close_signal.emit()
    
            
    
    
    def VerGrupos(self):
        self.TV=TableViewer("Grupo", self.cursor)
        self.TV.show()
        
    
if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=Grupo(con)
    window.show()
    app.exec()
        
    

        