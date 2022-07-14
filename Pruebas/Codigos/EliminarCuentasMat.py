#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5 import QtWidgets,uic
from CustomTableView import TableViewer
from ValidacionesCuentas import ValidarFecha,ValidarUsuario

class CuentaMateriaBorrar(QtWidgets.QDialog):
    def __init__(self,DBconnection):
        super(CuentaMateriaBorrar, self).__init__()
        uic.loadUi("../UI/EliminarCuentasMaterias.ui",self)
        self.con=DBconnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"Cuenta")
        self.input1.textChanged.connect(self.ActualizarCombo)
        self.input2=self.findChild(QtWidgets.QLineEdit,"Semestre")
        self.input2.textChanged.connect(self.ActualizarCombo)
        self.cb1=self.findChild(QtWidgets.QComboBox,"NomMat")
        self.cb1.addItems(self.LlenarComboMat())
        
        self.button1=self.findChild(QtWidgets.QPushButton,"Eliminar")
        self.button1.clicked.connect(self.EliminarRelacion)
        self.button2=self.findChild(QtWidgets.QPushButton, "Ver")
        self.button2.clicked.connect(self.VerTabla)
        
    def LlenarComboMat(self):
        cursor=self.con.cursor()
        Cuenta=self.input1.text()
        Semestre=self.input2.text()
        resultados=[]
        oracion="select NomMateria from CuentaMaterias where NombreCuenta=? and SemestreCuentaMaterias=? order by NomMateria"
        cursor.execute(oracion,(Cuenta,Semestre))
        for row in cursor.fetchall():
            resultados.append(row[0])
        return resultados
    
    def ActualizarCombo(self):
        self.cb1.addItems(self.LlenarComboMat())
        
    def EliminarRelacion(self):
        cursor=self.con.cursor()
        Cuenta=self.input1.text()
        Materia=self.cb1.currentText()
        Semestre=self.input2.text()
        oracion="delete from CuentaMaterias where NombreCuenta=? and NomMateria=? and SemestreCuentaMaterias=?"
        if self.ValidacionesDatos(Cuenta, Semestre):
            cursor.execute(oracion,(Cuenta,Materia,Semestre))  
            self.con.commit()
            Mensajes.MostrarExitoBorrar()
    
    def ValidacionesDatos(self,Cuenta,Semestre):
        Mensaje=""
        Errores=0
        if len(Cuenta)==0 or len(Semestre)==0:
            Mensaje+="Existen Campos Vacios\n"
            Errores+=1
        Mensaje,Errores=ValidarUsuario(Cuenta, Mensaje, Errores)
        Mensaje,Errores=ValidarFecha(Semestre, Mensaje, Errores)
        if Errores>0:
            Mensajes.MostrarErroresBorrar(Mensaje)
            return False
        else:
            return True
            
            
    
    def VerTabla(self):
        self.TV=TableViewer("CuentasMaterias",self.con)
        self.TV.show()
    def __exit__(self):
         self.con.close()

        
if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=CuentaMateriaBorrar(con)
    window.show()
    app.exec() 