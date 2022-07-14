#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets,uic
from  InsertarMaterias import Materia
from  InsertarAlumnos import Alumnos
from InsertarGrupos import Grupo
from Cuentas import Cuentas
from EliminarAlumnos import AlumnoBorrar
from EliminarCuentas import CuentasBorrar
from EliminarMaterias import MateriasBorrar
from EliminarGrupo import GrupoBorrar
from InsertarCuentasMat import CuentasMaterias
from EliminarCuentasMat import CuentaMateriaBorrar
import sys,sqlite3,Archivos

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("../UI/Menuprincipal.ui",self) #Carga la interfaz grafica con el nombre especificado
        
        self.Menu=None
        self.BuildUI()
        self.BuildAlumnosUI()
        self.BuildMateriasUi()
        self.BuildGrupoUi()      
           
    def BuildUI(self):
        self.cargar=self.findChild(QtWidgets.QAction,"actionCargar")
        self.cargar.triggered.connect(self.Cargarbase)
        self.button1=self.findChild(QtWidgets.QPushButton,"Alumnos")
        self.button1.clicked.connect(self.MostrarSubMenuAlumnos)
        self.button1.setCheckable(True)
        self.button2=self.findChild(QtWidgets.QPushButton, "Materias")
        self.button2.clicked.connect(self.MostrarSubMenuMaterias)
        self.button2.setCheckable(True)
        self.button3=self.findChild(QtWidgets.QPushButton,"Grupos")
        self.button3.clicked.connect(self.MostrarSubMenuGrupo)
        self.button3.setCheckable(True)
        
    def BuildAlumnosUI(self):
        #construcción submenu alumnos
        self.buttonRegistrarAl=self.findChild(QtWidgets.QPushButton,"RegistrarAl")
        self.buttonRegistrarAl.hide()
        self.buttonRegistrarAl.clicked.connect(lambda: self.MostrarVentanas( Alumnos(self.con)))
        self.buttonRegistrarCu=self.findChild(QtWidgets.QPushButton,"RegistrarCuentas")
        self.buttonRegistrarCu.hide()
        self.buttonRegistrarCu.clicked.connect(lambda: self.MostrarVentanas(Cuentas(self.con)))
        self.buttonEliminarAl=self.findChild(QtWidgets.QPushButton,"EliminarAl")
        self.buttonEliminarAl.hide()
        self.buttonEliminarAl.clicked.connect(lambda: self.MostrarVentanas(AlumnoBorrar(self.con)))
        self.buttonEliminarCu=self.findChild(QtWidgets.QPushButton,"EliminarCuentas")
        self.buttonEliminarCu.hide()
        self.buttonEliminarCu.clicked.connect(lambda: self.MostrarVentanas(CuentasBorrar(self.con)))
        self.buttonCuentaMateria=self.findChild(QtWidgets.QPushButton,"AsignarMateriasAl")
        self.buttonCuentaMateria.clicked.connect(lambda: self.MostrarVentanas(CuentasMaterias(self.con)))
        self.buttonCuentaMateria.hide()
        self.buttonCuentaMateriaB=self.findChild(QtWidgets.QPushButton,"EliminarMateriasAl")
        self.buttonCuentaMateriaB.clicked.connect(lambda: self.MostrarVentanas(CuentaMateriaBorrar(self.con)))
        self.buttonCuentaMateriaB.hide()
     
    def BuildMateriasUi(self):   #Construcción submenu Materias
        self.buttonRegistrarMat=self.findChild(QtWidgets.QPushButton, "RegistrarMat")
        self.buttonRegistrarMat.hide()
        self.buttonRegistrarMat.clicked.connect(lambda: self.MostrarVentanas(Materia(self.con)))
        self.buttonElimnarMat=self.findChild(QtWidgets.QPushButton, "EliminarMat")
        self.buttonElimnarMat.hide()
        self.buttonElimnarMat.clicked.connect(lambda: self.MostrarVentanas(MateriasBorrar(self.con)))
   
    def BuildGrupoUi(self):
     #construcción submenu Grupo
        self.buttonRegistrarGpo=self.findChild(QtWidgets.QPushButton,"RegistrarGpo")
        self.buttonRegistrarGpo.hide()
        self.buttonRegistrarGpo.clicked.connect(lambda: self.MostrarVentanas(Grupo(self.con)))
        self.buttonEliminarGpo=self.findChild(QtWidgets.QPushButton,"EliminarGpo")
        self.buttonEliminarGpo.hide()
        self.buttonEliminarGpo.clicked.connect(lambda: self.MostrarVentanas(GrupoBorrar(self.con)))

    def MostrarSubMenuAlumnos(self):
        if self.button1.isChecked():
            self.buttonRegistrarAl.show()
            self.buttonRegistrarCu.show()
            self.buttonEliminarAl.show()
            self.buttonEliminarCu.show()
            self.buttonCuentaMateria.show()
            self.buttonCuentaMateriaB.show()
        else:
            self.buttonRegistrarAl.hide()
            self.buttonRegistrarCu.hide()
            self.buttonEliminarAl.hide()
            self.buttonEliminarCu.hide()
            self.buttonCuentaMateria.hide()
            self.buttonCuentaMateriaB.hide()

    def MostrarSubMenuMaterias(self):
        if self.button2.isChecked():
            self.buttonRegistrarMat.show()
            self.buttonElimnarMat.show()
        else:
            self.buttonRegistrarMat.hide()
            self.buttonElimnarMat.hide()
    def MostrarSubMenuGrupo(self):
        if self.button3.isChecked():
            self.buttonRegistrarGpo.show()
            self.buttonEliminarGpo.show()
        else:
            self.buttonRegistrarGpo.hide()
            self.buttonEliminarGpo.hide()

            
    def MostrarVentanas(self,window):
        if self.Menu is None:
            self.Menu=window
            self.Menu.show()
        else:
            self.Menu.close()
            self.Menu=None
    def Cargarbase(self):
        conexion=Archivos.openFileNameDialog(self)
        self.con=sqlite3.Connection(conexion) #conexión a la base de datos
   
   
 
   
        
    def __exit__(self):
        self.con.close()
    
            
if __name__ =="__main__":           
    if not QtWidgets.QApplication.instance():
        app=QtWidgets.QApplication(sys.argv)
    else:
        app=QtWidgets.QApplication.instance()
    Window=MainWindow()
    Window.show()
    app.exec()