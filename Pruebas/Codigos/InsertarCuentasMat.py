#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog,QComboBox,QLineEdit,QPushButton
from PyQt5.Qt import pyqtSignal
from CustomTableView import TableViewer
from ValidacionesCuentas import ValidarUsuario,VerificarCuentaExista, ValidarFecha
from ResourcePath import resource_path

class CuentasMaterias(QDialog):
    close_signal=pyqtSignal()
    def __init__(self,DBconnection):
        super(CuentasMaterias,self).__init__()
        uic.loadUi(resource_path("UI/CuentasMaterias.ui"),self)
        self.con=DBconnection
        self.cursor=DBconnection.cursor()

        self.input1=self.findChild(QLineEdit,"NombreCuenta")
        self.cb3=self.findChild(QComboBox,"Semestre")
        self.cb3.addItems(self.LlenarComboSemestre())
        self.cb3.currentTextChanged.connect(lambda: self.UpdateCb())
        self.cb1=self.findChild(QComboBox,"AbrMat")
        self.cb1.addItems(self.LlenarComboMat())
        self.cb2=self.findChild(QComboBox,"Grupo")
        self.cb2.addItems(self.LLenarComboGrupo())
        self.input2=self.findChild(QLineEdit,"Fecha")
        self.button1=self.findChild(QPushButton,"Insertar")
        self.button1.clicked.connect(self.InsertarValores)
        self.button2=self.findChild(QPushButton,"Ver")
        self.button2.clicked.connect(self.VerTabla)
        self.button3=self.findChild(QPushButton,"VerCuentas")
        self.button3.clicked.connect(self.VerTablaCuentas)
        self.TV=None #TableViewer

   
 
    def LlenarComboMat(self): #obtiene la lista de resultados de la Base para meterlos a la combobox
        self.cb1.clear()
        Semestre=self.cb3.currentText()
        oracion="select distinct NombreMateria from Materias where SemestreMateria=? order by NombreMateria"
        self.cursor.execute(oracion,(Semestre,))
        resultados=[]
        for row in self.cursor.fetchall():
            resultados.append(row[0])
        return resultados
    
    def LLenarComboGrupo(self):
        self.cb2.clear()
        Semestre=self.cb3.currentText()
        resultados=[]
        oracion="""select CveGrupo from Grupo where GrupoSemestre=? order by substr(CveGrupo,1,3),
        substr(CveGrupo,4,9)*1"""
      
        self.cursor.execute(oracion,(Semestre,))
        for row in self.cursor.fetchall():
            resultados.append(row[0])
        return resultados
    
    def LlenarComboSemestre(self):
        oracion="Select distinct SemestreMateria from Materias order by substr(SemestreMateria,1,2)*1"
        self.cursor.execute(oracion)
        resultados=[]
        for row in self.cursor.fetchall():
            resultados.append(row[0])
        return resultados
        
    
    def UpdateCb(self):#cuando se actualice el nombre de la materia solamente mostrara los grupos validos
       self.cb2.addItems(self.LLenarComboGrupo())
       self.cb1.addItems(self.LlenarComboMat())
   
        
    def InsertarValores(self):
        Cuenta=self.input1.text()
        Materia=self.cb1.currentText()
        Grupo=self.cb2.currentText()
        Semestre=self.input2.text()
       
        ClaveMat=""
        obtenerClaveMat="""select CveMateria from Materias inner join Grupo
        on Grupo.GrupoSemestre=Materias.SemestreMateria where NombreMateria=? and CveGrupo=?
        """
        oracion="""insert or ignore into CuentaMaterias(NombreCuenta,NomMateria,
        CveGrupo,SemestreCuentaMaterias) values(?,?,?,?)"""
        #agregar Validaciones
        self.cursor.execute(obtenerClaveMat,(Materia,Grupo))
        ClaveMat=self.cursor.fetchone()[0]
        if self.ValidacionesDatos(Cuenta,Semestre):
            self.cursor.execute(oracion,(Cuenta,ClaveMat,Grupo,Semestre))
            self.con.commit()
            self.ClearLineEdits()
            Mensajes.MostrarExito()
            
    def ClearLineEdits(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
            
    def ValidacionesDatos(self,Cuenta,Fecha):
        Mensaje=""
        if len(Cuenta)==0: 
            Mensaje+="Existen campos vacios\n"
        else:
            Mensaje=ValidarUsuario(Cuenta, Mensaje)
            Mensaje=VerificarCuentaExista(Cuenta, Mensaje,  self.con)
            Mensaje=ValidarFecha(Fecha, Mensaje)
        print(Mensaje)
        if Mensaje!="":
            Mensajes.MostrarErroresInsercion(Mensaje)
            return False
        else:
            return True
    
    def VerTabla(self):
        self.TV=TableViewer("CuentasMaterias",self.cursor)
        self.TV.show()
    def VerTablaCuentas(self):
         self.TV=TableViewer("Cuenta",self.cursor)
         self.TV.show()
   
    def closeEvent(self,event):
        self.on_close()
    def on_close(self):
        if self.TV is not None:
            self.TV.close()
        self.close_signal.emit()




if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    #con=sqlite.Connection("../DB/ESM.db")
    app=QtWidgets.QApplication(sys.argv)
    window=CuentasMaterias(con)
    window.show()
    app.exec() 
            