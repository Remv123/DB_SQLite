#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets, uic
import sys,sqlite3
from CustomTableView import TableViewer
import Mensajes

class Materia(QtWidgets.QDialog):
    def __init__(self,DBconnection):
        super(Materia,self).__init__()
        uic.loadUi("../UI/Materias.ui",self)
        self.con=DBconnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"Clave")
        self.input2=self.findChild(QtWidgets.QLineEdit,"Nombre")
        self.input3=self.findChild(QtWidgets.QLineEdit,"Semestre")
        self.input4=self.findChild(QtWidgets.QComboBox,"Departamento")
        self.button1=self.findChild(QtWidgets.QPushButton, "Insertar")
        self.button1.clicked.connect(self.InsertarValoresMaterias)
        self.button2=self.findChild(QtWidgets.QPushButton,"Imprimir")
        self.button2.clicked.connect(self.VerTabla)
    
    def InsertarValoresMaterias(self):
        cursor=self.con.cursor()
        clave=self.input1.text()
        Nombre=self.input2.text()
        Semestre=self.input3.text()
        Departamento=self.input4.currentText()
        oracion="""insert or ignore into Materias(CveMateria,
        NombreMateria,SemestreMateria,DepartamentoMateria) values(?,?,?,?)"""
        if self.ValidarDatos(clave,Nombre,Semestre):
            cursor.execute(oracion,(clave,Nombre,Semestre,Departamento))
            Mensajes.MostrarExito()
            self.con.commit()
    
    def ValidarDatos(self,clave,nombre,semestre):
        mensaje=""
        errores=0
        if len(clave)==0  or len(nombre)==0 or len(semestre)==0:
            errores+=1
            mensaje="Existe algun campo vacio\n"
        if len(clave)>15:
            errores+=1
            mensaje="La abreviatura es demasiado grande\n"
        if any(c.isdigit() for c in nombre):
            errores+=1
            mensaje+="El nombre de la materia no puede contener numeros\n"
        if any(c.isalpha() for c in semestre):
            errores+=1
            mensaje+="El semestre no debe contener letras"
        if errores>0:
            Mensajes.MostrarErroresInsercion(mensaje)
            return False
        else:
            return True
            
    def __exit__(self):
        self.con.close()
    def VerTabla(self):
        self.TV=TableViewer("Materias",self.con)
        self.TV.setWindowTitle("Materias")
        self.TV.show()
    
if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=Materia(con)
    window.show()
    app.exec()

