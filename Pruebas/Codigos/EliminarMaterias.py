#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5 import QtWidgets,uic
from CustomTableView import TableViewer

class MateriasBorrar(QtWidgets.QDialog):
    def __init__(self,DBconnection):
        super(MateriasBorrar,self).__init__()
        uic.loadUi("../UI/EliminarMateria.ui",self)
        self.con=DBconnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"Clave")
        self.buttonA=self.findChild(QtWidgets.QPushButton,"Borrar")
        self.buttonA.clicked.connect(self.BorrarMaterias)
        self.buttonB=self.findChild(QtWidgets.QPushButton,"Ver")
        self.buttonB.clicked.connect(self.MostrarTabla)
        
    def BorrarMaterias(self):
        cursor=self.con.cursor()
        Abreviatura=self.input1.text()
        oracion="Delete from Materias where CveMateria=?"
        cursor.execute(oracion,(Abreviatura,))
        self.con.commit()
        Mensajes.MostrarExitoBorrar()

    def MostrarTabla(self):
        self.TV=TableViewer("Materias", self.con) 
        self.TV.show()
          
    def __exit__(self):
        self.con.close()

if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=MateriasBorrar(con)
    window.show()
    app.exec() 