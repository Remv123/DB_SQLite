#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton,QComboBox
from PyQt5.Qt import pyqtSignal

import sys,sqlite3
from CustomTableView import TableViewer
from ValidacionesMaterias import ValidarMaterias
import Mensajes

class Materia(QDialog):
    close_signal=pyqtSignal()
    def __init__(self,DBconnection):
        super(Materia,self).__init__()
        uic.loadUi("../UI/Materias.ui",self)
        self.con=DBconnection
        self.cursor=DBconnection.cursor()
        self.input1=self.findChild(QLineEdit,"Clave")
        self.input2=self.findChild(QLineEdit,"Nombre")
        self.input3=self.findChild(QLineEdit,"Semestre")
        self.input4=self.findChild(QComboBox,"Departamento")
        self.input5=self.findChild(QComboBox,"Trimestre")
        self.button1=self.findChild(QPushButton, "Insertar")
        self.button1.clicked.connect(self.InsertarValoresMaterias)
        self.button2=self.findChild(QPushButton,"Imprimir")
        self.button2.clicked.connect(self.VerTabla)
        self.TV=None #TableViewer

        
  
  
    
    def InsertarValoresMaterias(self):
        clave=self.input1.text()
        Nombre=self.input2.text()
        Semestre=self.input3.text()
        Departamento=self.input4.currentText()
        Trimestre=self.input5.currentText()
        oracion="""insert or ignore into Materias(CveMateria,
        NombreMateria,SemestreMateria,DepartamentoMateria,Trimestre) values(?,?,?,?,?)"""
        if self.ValidarDatos(clave,Nombre,Semestre):
            self.cursor.execute(oracion,(clave,Nombre,Semestre,Departamento,Trimestre))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExito()
            
            
    def ClearLineEdits(self):
         for child in self.findChildren(QLineEdit):
             child.clear()
    
    def ValidarDatos(self,clave,nombre,semestre):
        mensaje=""
        errores=0
        if len(clave)==0  or len(nombre)==0 or len(semestre)==0:
            errores+=1
            mensaje="Existe algun campo vacio\n"
        mensaje,errores=ValidarMaterias(clave, nombre, semestre, errores, mensaje)
        if errores>0:
            Mensajes.MostrarErroresInsercion(mensaje)
            return False
        else:
            return True
            
    def __exit__(self):
        self.con.close()
    def VerTabla(self):
        self.TV=TableViewer("Materias",self.cursor)
        self.TV.setWindowTitle("Materias")
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
    window=Materia(con)
    window.show()
    app.exec()

