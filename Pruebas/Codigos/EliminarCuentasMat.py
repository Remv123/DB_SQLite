#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton,QComboBox
from PyQt5.Qt import pyqtSignal
from CustomTableView import TableViewer
from ValidacionesCuentas import ValidarFecha,ValidarUsuario
from ResourcePath import resource_path

class CuentaMateriaBorrar(QDialog):
    close_signal=pyqtSignal()

    def __init__(self,DBconnection):
        super(CuentaMateriaBorrar, self).__init__()
        uic.loadUi(resource_path("UI/EliminarCuentasMaterias.ui"),self)
        self.con=DBconnection
        self.cursor=DBconnection.cursor()
        self.input1=self.findChild(QLineEdit,"Cuenta")
        self.input1.textChanged.connect(self.ActualizarCombo)
        self.input2=self.findChild(QLineEdit,"Semestre")
        self.input2.textChanged.connect(self.ActualizarCombo)
        self.cb1=self.findChild(QComboBox,"NomMat")
        self.cb1.addItems(self.LlenarComboMat())
        
        self.button1=self.findChild(QPushButton,"Eliminar")
        self.button1.clicked.connect(self.EliminarRelacion)
        self.button2=self.findChild(QPushButton, "Ver")
        self.button2.clicked.connect(self.VerTabla)
        self.TV=None #TableViewer
 
   
    def LlenarComboMat(self):
       
        Cuenta=self.input1.text()
        Semestre=self.input2.text()
        resultados=[]
        oracion="select NombreMateria from CuentaMaterias inner join Materias on CuentaMaterias.NomMateria=Materias.CveMateria where NombreCuenta=? and SemestreCuentaMaterias=? order by NomMateria"
        
        self.cursor.execute(oracion,(Cuenta,Semestre))
        for row in self.cursor.fetchall():
            resultados.append(row[0])
        return resultados
    
    def ActualizarCombo(self):
        self.cb1.addItems(self.LlenarComboMat())
        
    def EliminarRelacion(self):
        Cuenta=self.input1.text()
        Materia=self.cb1.currentText()
        Semestre=self.input2.text()
        
        oracion="delete from CuentaMaterias where NombreCuenta=? and NomMateria=? and SemestreCuentaMaterias=?"
        if self.ValidacionesDatos(Cuenta, Semestre,Materia):
            clave="select CveMateria from Materias where NombreMateria=?"
            self.cursor.execute(clave,(Materia,))
            Abreviatura=self.cursor.fetchone()[0]
            self.cursor.execute(oracion,(Cuenta,Abreviatura,Semestre))  
            self.con.commit()
            Mensajes.MostrarExitoBorrar()
    
    def ValidacionesDatos(self,Cuenta,Semestre,Materia):
        Mensaje=""
       
        if len(Cuenta)==0 or len(Semestre)==0 or len(Materia)==0:
            Mensaje+="Existen Campos Vacios\n"
            
        Mensaje=ValidarUsuario(Cuenta, Mensaje)
        Mensaje=ValidarFecha(Semestre, Mensaje)
        if Mensaje!="":
            Mensajes.MostrarErroresBorrar(Mensaje)
            return False
        else:
            return True
            
            
    
    def VerTabla(self):
        self.TV=TableViewer("CuentasMaterias",self.cursor)
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
    window=CuentaMateriaBorrar(con)
    window.show()
    app.exec() 