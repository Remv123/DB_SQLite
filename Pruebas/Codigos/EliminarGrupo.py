#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5 import QtWidgets,uic
from CustomTableView import TableViewer
from ValidacionesGrupo import ValidarClaveGrupo

class GrupoBorrar(QtWidgets.QDialog):
    def __init__(self,DBconnection):
        super(GrupoBorrar,self).__init__()  
        uic.loadUi("../UI/EliminarGrupos.ui",self)
        self.con=DBconnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"Grupo")
        self.button1=self.findChild(QtWidgets.QPushButton,"Borrar")
        self.button1.clicked.connect(self.BorrarGrupo)
        self.button2=self.findChild(QtWidgets.QPushButton, "Ver")
        self.button2.clicked.connect(self.VerTabla)
       
      
    
    def BorrarGrupo(self):
        cursor=self.con.cursor()
        Clave=self.input1.text()
        oracion="Delete from Grupo where CveGrupo=?"
        if self.VerificarDatos(Clave):
            cursor.execute(oracion,(Clave,))
            self.con.commit()
            Mensajes.MostrarExitoBorrar()
    
    def VerificarDatos(self,Grupo):
        Mensaje,Errores=ValidarClaveGrupo(Grupo)
        if Errores>0:
            Mensajes.MostrarErroresBorrar(Mensaje)
            return False
        else:
            return True
    def VerTabla(self):
        self.TV=TableViewer("Grupo", self.con)
        self.TV.show()
    
    def __exit__(self):
        self.con.close()

if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=GrupoBorrar(con)
    window.show()
    app.exec() 
