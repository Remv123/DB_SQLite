#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets, uic
from CustomTableView import TableViewer
from ValidacionesAlumnos import ValidarBoleta
from ValidacionesCuentas import ValidarUsuario,ValidarFecha,VerificarBoletaCuenta,VerificarUsuarioCuenta
import sys,sqlite3,secrets,string,Mensajes
class Cuentas(QtWidgets.QDialog):
    def __init__(self,DBConnection):
        super(Cuentas,self).__init__()
        uic.loadUi("../UI/Cuentas.ui",self)
        
        self.con=DBConnection
        self.input1=self.findChild(QtWidgets.QLineEdit,"Boleta")
        self.input2=self.findChild(QtWidgets.QLineEdit,"Usuario")
        self.input3=self.findChild(QtWidgets.QLineEdit,"Contrasena")
        self.input4=self.findChild(QtWidgets.QLineEdit,"Fecha")
        self.button1=self.findChild(QtWidgets.QPushButton,"Generar")
        self.button1.clicked.connect(self.GenerarContrasena)
        self.button2=self.findChild(QtWidgets.QPushButton,"Insertar")
        self.button2.clicked.connect(self.InsertarDatosCuenta)
        self.buttonVer=self.findChild(QtWidgets.QPushButton,"Ver")
        self.buttonVer.clicked.connect(self.VerCuentas)
        self.buttonAl=self.findChild(QtWidgets.QPushButton,"VerAl")
        self.buttonAl.clicked.connect(self.VerAlumnos)
        
    def GenerarContrasena(self):
        alphabet= string.ascii_lowercase+string.digits+string.punctuation
        password=''.join(secrets.choice(alphabet) for i in range(6))
        self.input3.setText(password)
        
    def InsertarDatosCuenta(self):
        cursor=self.con.cursor()
        Boleta=self.input1.text()
        Usuario=self.input2.text()
        Contrasena=self.input3.text()
        Fecha=self.input4.text()
        oracion="""insert or ignore into Cuenta(CveAlumno,NombreCuenta,Contrasena,Semestre) values(?,?,?,?)"""
        if  self.VerificarDatos(Boleta, Usuario, Contrasena, Fecha):
            cursor.execute(oracion,(Boleta,Usuario,Contrasena,Fecha))
            self.con.commit()
            Mensajes.MostrarExito()
    
    def VerificarDatos(self,Boleta,Usuario,Contrasena,Fecha):
        errores=0
        Mensaje=""
        if len(Boleta)==0 or len(Usuario)==0 or len(Contrasena)==0 or len(Fecha)==0:
            Mensaje+="Existen campos sin llenar\n"
            errores+=1
        Mensaje,errores=ValidarBoleta(Boleta, Mensaje, errores)
        Mensaje,errores=ValidarUsuario(Usuario, Mensaje, errores)
        Mensaje,errroes=ValidarFecha(Fecha, Mensaje, errores)
        Mensaje, errores=VerificarBoletaCuenta(Boleta, Mensaje,errores,self.con)
        Mensaje, errores=VerificarUsuarioCuenta(Boleta,Fecha,Mensaje,errores,self.con)
        if errores>0:
            Mensajes.MostrarErroresInsercion(Mensaje)
            return False
        else:
            return True
            
 
   
    
    
   
     
    def VerCuentas(self):
        self.TV=TableViewer("Cuenta", self.con)
        self.TV.show()
    def VerAlumnos(self):
          self.TV=TableViewer("Alumno", self.con)
          self.TV.show()
        
    def __exit__(self):
        self.con.close()
        
if __name__=="__main__":
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    app=QtWidgets.QApplication(sys.argv)
    window=Cuentas(con)
    window.show()
    app.exec()
        