#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import uic,QtWidgets
from CustomTableView import TableViewer
from ValidacionesGrupo import ValidarClaveGrupo

import sqlite3,Mensajes,sys

class Grupo(QtWidgets.QDialog):
    def __init__(self,DBconnection):
        super(Grupo, self).__init__()
        uic.loadUi("../UI/Grupos.ui",self)
        self.con=DBconnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"Grupo")
        self.button1=self.findChild(QtWidgets.QPushButton,"Insertar")
        self.button1.clicked.connect(self.InsertarGrupo)
        self.button2=self.findChild(QtWidgets.QPushButton,"Ver")
        self.button2.clicked.connect(self.VerGrupos)
     
    def InsertarGrupo(self):
        cursor=self.con.cursor()
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
            cursor.execute(oracion,(NombreGrupo,Semestre))
            self.con.commit()
            Mensajes.MostrarExito()
    
    def ValidarGrupo(self,Grupo):
        Mensaje=""
        Errores=0
        Mensaje,Errores=ValidarClaveGrupo(Grupo)
        if Errores>0:
            Mensajes.MostrarErroresInsercion(Mensaje)
            return False
        else:
            return True

       
    def __exit__(self):
        self.con.close()
            
    
    
    def VerGrupos(self):
        self.TV=TableViewer("Grupo", self.con)
        self.TV.show()
        
    
if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=Grupo(con)
    window.show()
    app.exec()
        
    

        