#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys,Mensajes,sqlite3
from PyQt5 import QtWidgets,uic
from CustomTableView import TableViewer
from ValidacionesCuentas import ValidarUsuario,ValidarFecha

class CuentasMaterias(QtWidgets.QDialog):
    def __init__(self,DBconnection):
        super(CuentasMaterias,self).__init__()
        uic.loadUi("../UI/CuentasMaterias.ui",self)
        self.con=DBconnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"NombreCuenta")
        self.input2=self.findChild(QtWidgets.QLineEdit,"Periodo")
        self.cb1=self.findChild(QtWidgets.QComboBox,"AbrMat")
        self.cb1.addItems(self.LlenarComboMat())
        self.cb1.currentTextChanged.connect(self.UpdateCbGrupo)
        self.cb2=self.findChild(QtWidgets.QComboBox,"Grupo")
        self.cb2.addItems(self.LLenarComboGrupo())
        self.button1=self.findChild(QtWidgets.QPushButton,"Insertar")
        self.button1.clicked.connect(self.InsertarValores)
        self.button2=self.findChild(QtWidgets.QPushButton,"Ver")
        self.button2.clicked.connect(self.VerTabla)
        self.button3=self.findChild(QtWidgets.QPushButton,"VerCuentas")
        self.button3.clicked.connect(self.VerTablaCuentas)
        
          
    def LlenarComboMat(self): #obtiene la lista de resultados de la Base para meterlos a la combobox
        cursor=self.con.cursor()
        oracion="select distinct NombreMateria from Materias order by NombreMateria"
        cursor.execute(oracion,())
        resultados=[]
        for row in cursor.fetchall():
            resultados.append(row[0])
        return resultados
    def LLenarComboGrupo(self):
        self.cb2.clear()
        cursor=self.con.cursor()
        Semestre=self.cb1.currentText()
        resultados=[]
        oracion="""select CveGrupo from Grupo inner join Materias 
        on Grupo.GrupoSemestre=Materias.SemestreMateria where NombreMateria=? order by substr(CveGrupo,1,3),
        substr(CveGrupo,4,9)*1"""
        cursor.execute(oracion,(Semestre,))
        for row in cursor.fetchall():
            resultados.append(row[0])
        return resultados
    
    def UpdateCbGrupo(self):#cuando se actualice el nombre de la materia solamente mostrara los grupos validos
       self.cb2.addItems(self.LLenarComboGrupo())
    
    def InsertarValores(self):
        cursor=self.con.cursor()
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
        cursor.execute(obtenerClaveMat,(Materia,Grupo))
        ClaveMat=cursor.fetchone()[0]
        if self.ValidacionesDatos(Cuenta,Semestre):
            cursor.execute(oracion,(Cuenta,ClaveMat,Grupo,Semestre))
            self.con.commit()
            Mensajes.MostrarExito()
        
    def ValidacionesDatos(self,Cuenta,Semestre):
        Mensaje=""
        Errores=0
        if len(Cuenta)==0 or len(Semestre)==0:
            Mensaje+="Existen campos vacios\n"
            Errores+=1
        Mensaje,Errores=ValidarUsuario(Cuenta, Mensaje, Errores)
        Mensaje,Errores=ValidarFecha(Semestre, Mensaje, Errores)
       
        if Errores>0:
            Mensajes.MostrarErroresInsercion(Mensaje)
            return False
        else:
            return True
    
    def VerTabla(self):
        self.TV=TableViewer("CuentasMaterias",self.con)
        self.TV.show()
    def VerTablaCuentas(self):
         self.TV=TableViewer("Cuenta",self.con)
         self.TV.show()
    def __exit__(self):
          self.con.close()



if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=CuentasMaterias(con)
    window.show()
    app.exec() 
            