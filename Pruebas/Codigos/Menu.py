#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QThread
from PyQt5.Qt import pyqtSignal

from PyQt5.QtWidgets import QInputDialog,QProgressDialog
from PyQt5.QtWidgets import QFileDialog,QMenu,QMessageBox,QAction,QLineEdit,QPushButton,QMainWindow
from Exportar import ExportarAExcel
from  InsertarMaterias import Materia
from  InsertarAlumnos import Alumnos
from InsertarGrupos import Grupo
from InsertarCuentas import Cuentas
from EliminarAlumnos import AlumnoBorrar
from EliminarCuentas import CuentasBorrar
from EliminarMaterias import MateriasBorrar
from EliminarGrupo import GrupoBorrar
from InsertarCuentasMat import CuentasMaterias
from EliminarCuentasMat import CuentaMateriaBorrar
from InsertarUsuarios import RegistrarUsuario
from EliminarUsuario import EliminarUsuario
from ValidacionesCuentas import ValidarFecha
from ValidacionesMaterias import ValidarTrimestreMaterias
from Respaldar import RespaldarArchivoDB
import sys,sqlite3

class MainWindow(QMainWindow):
    def __init__(self,DBconnection,Name):
        super(MainWindow,self).__init__()
        uic.loadUi("../UI/Menuprincipal.ui",self) #Carga la interfaz grafica con el nombre especificado
        self.con=DBconnection
        self.createWindows()
        self.Window=None
        self.BuildUI(Name)
        self.BuildAlumnosUI()
        self.BuildMateriasUi()
        self.BuildGrupoUi()     
    
    def createWindows(self):
        self.RegistrarUsuario=RegistrarUsuario(self.con)
        self.EliminarUsuario=EliminarUsuario(self.con)
           
    def BuildUI(self,Name):
        self.actionExportar=self.findChild(QAction,"actionResult")
        self.actionExportar.triggered.connect(self.exportarTablaUsuariosMoodle)
        self.actionRespaldarBD=self.findChild(QAction,"actionRespaldarBD")
        self.actionRespaldarBD.triggered.connect(self.RespaldarDB)
        self.actionNuevoUsuario=self.findChild(QAction,"actionCrearUsuario_2")
        self.actionNuevoUsuario.triggered.connect(lambda: self.MostrarVentanas(self.RegistrarUsuario))
        self.actionEliminarUsuario=self.findChild(QAction,"actionEliminar_Usuario")
        self.actionEliminarUsuario.triggered.connect(lambda:self.MostrarVentanas(self.EliminarUsuario))
        self.menubar=self.findChild(QMenu,"menuAdmin")
        
        if Name!="Admin":
            self.menubar.menuAction().setVisible(False)
        self.buttonAlumnos=self.findChild(QPushButton,"Alumnos")
        self.buttonAlumnos.clicked.connect(self.MostrarSubMenuAlumnos)
        self.buttonAlumnos.setCheckable(True)
        self.buttonMaterias=self.findChild(QPushButton, "Materias")
        self.buttonMaterias.clicked.connect(self.MostrarSubMenuMaterias)
        self.buttonMaterias.setCheckable(True)
        self.buttonGrupos=self.findChild(QPushButton,"Grupos")
        self.buttonGrupos.clicked.connect(self.MostrarSubMenuGrupo)
        self.buttonGrupos.setCheckable(True)
        
    def BuildAlumnosUI(self):
        #construcción submenu alumnos
        self.buttonRegistrarAl=self.findChild(QPushButton,"RegistrarAl")
        self.buttonRegistrarAl.hide()
        self.buttonRegistrarAl.clicked.connect(lambda: self.MostrarVentanas( Alumnos(self.con)))
        self.buttonRegistrarCu=self.findChild(QPushButton,"RegistrarCuentas")
        self.buttonRegistrarCu.hide()
        self.buttonRegistrarCu.clicked.connect(lambda: self.MostrarVentanas(Cuentas(self.con)))
        self.buttonEliminarAl=self.findChild(QPushButton,"EliminarAl")
        self.buttonEliminarAl.hide()
        self.buttonEliminarAl.clicked.connect(lambda: self.MostrarVentanas(AlumnoBorrar(self.con)))
        self.buttonEliminarCu=self.findChild(QPushButton,"EliminarCuentas")
        self.buttonEliminarCu.hide()
        self.buttonEliminarCu.clicked.connect(lambda: self.MostrarVentanas(CuentasBorrar(self.con)))
        self.buttonCuentaMateria=self.findChild(QPushButton,"AsignarMateriasAl")
        self.buttonCuentaMateria.clicked.connect(lambda: self.MostrarVentanas(CuentasMaterias(self.con)))
        self.buttonCuentaMateria.hide()
        self.buttonCuentaMateriaB=self.findChild(QPushButton,"EliminarMateriasAl")
        self.buttonCuentaMateriaB.clicked.connect(lambda: self.MostrarVentanas(CuentaMateriaBorrar(self.con)))
        self.buttonCuentaMateriaB.hide()
     
    def BuildMateriasUi(self):   #Construcción submenu Materias
        self.buttonRegistrarMat=self.findChild(QPushButton, "RegistrarMat")
        self.buttonRegistrarMat.hide()
        self.buttonRegistrarMat.clicked.connect(lambda: self.MostrarVentanas(Materia(self.con)))
        self.buttonElimnarMat=self.findChild(QPushButton, "EliminarMat")
        self.buttonElimnarMat.hide()
        self.buttonElimnarMat.clicked.connect(lambda: self.MostrarVentanas(MateriasBorrar(self.con)))
   
    def BuildGrupoUi(self):
     #construcción submenu Grupo
        self.buttonRegistrarGpo=self.findChild(QPushButton,"RegistrarGpo")
        self.buttonRegistrarGpo.hide()
        self.buttonRegistrarGpo.clicked.connect(lambda: self.MostrarVentanas(Grupo(self.con)))
        self.buttonEliminarGpo=self.findChild(QPushButton,"EliminarGpo")
        self.buttonEliminarGpo.hide()
        self.buttonEliminarGpo.clicked.connect(lambda: self.MostrarVentanas(GrupoBorrar(self.con)))

    def MostrarSubMenuAlumnos(self):
        if self.buttonAlumnos.isChecked():
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
        if self.buttonMaterias.isChecked():
            self.buttonRegistrarMat.show()
            self.buttonElimnarMat.show()
        else:
            self.buttonRegistrarMat.hide()
            self.buttonElimnarMat.hide()
    def MostrarSubMenuGrupo(self):
        if self.buttonGrupos.isChecked():
            self.buttonRegistrarGpo.show()
            self.buttonEliminarGpo.show()
        else:
            self.buttonRegistrarGpo.hide()
            self.buttonEliminarGpo.hide()
            
    def on_popup_close(self):
        self.Window=None
            
    def MostrarVentanas(self,window):
        if self.Window is None:
            self.Window=window
            self.Window.close_signal.connect(self.on_popup_close)
            self.Window.show()
        else:
            self.Window.close()
            self.Window=None

    
    
    def exportarTablaUsuariosMoodle(self):
        MensajeError=""
        Errores=0
        cursor1=self.con.cursor()
        cursor1.execute("Pragma database_list")
        NombreDB=cursor1.fetchone()[2]
        periodo,ok=QInputDialog().getText(self,"Semestre que se quiere exportar","Semestre:",QLineEdit.Normal)
        MensajeError,Errores=ValidarFecha(periodo, MensajeError, Errores)
        Trimestre,ok=QInputDialog().getText(self,"Trimestre que se quiere exportar","Trimestre:",QLineEdit.Normal)
        MensajeError,Errores=ValidarTrimestreMaterias(Trimestre, MensajeError, Errores)
        mensaje=QMessageBox()
        if Errores ==0:
            nombre,extension=QFileDialog.getSaveFileName(self,"Nombre del archivo",filter="*.xlsx")
            if extension[1:] not in nombre:
                nombre=nombre+extension[1:]
            if nombre!="":
                self.worker=Proceso1(NombreDB,nombre,periodo,Trimestre)
                self.worker.started.connect(self.OperacionIniciada)
                self.worker.finished.connect(self.OperacionCompletada)
                self.worker.start()
            else:
                mensaje.setIcon(QtWidgets.QMessageBox.Warning)
                mensaje.setWindowTitle("Error")
                mensaje.setText("El archivo de excel debe tener un nombre")
                mensaje.exec_()
        else:
            mensaje.setIcon(QtWidgets.QMessageBox.Warning)
            mensaje.setWindowTitle("Error")
            mensaje.setText(MensajeError)
            mensaje.exec_()
    
    
    def OperacionIniciada(self):
        self.BarraProgreso=QProgressDialog("Respaldando",None, 0, 0)
        self.BarraProgreso.setWindowTitle("Iniciando operacion")
        self.BarraProgreso.setWindowTitle("Realizando operacion")
        self.BarraProgreso.show()
    def OperacionCompletada(self):
        mensaje=QMessageBox()
        mensaje.setWindowTitle("Terminando operacion")
        mensaje.setText("Operacion Completada")
        self.BarraProgreso.close()
        mensaje.exec_()
        
    
        
    def RespaldarDB(self):
         mensaje=QMessageBox()
         cursor1=self.con.cursor()
         cursor1.execute("Pragma database_list")
         NombreDB=cursor1.fetchone()[2]
         nombre,extension=QFileDialog.getSaveFileName(self,"Nombre del archivo de resplado",filter="*.db")
         if nombre!="":
            if extension[1:] not in nombre:
                 nombre=nombre+extension[1:]
            self.worker=Proceso2(NombreDB,nombre)
            self.worker.started.connect(self.OperacionIniciada)
            self.worker.finished.connect(self.OperacionCompletada)
            self.worker.start()
            
          
         else:
            mensaje.setIcon(QtWidgets.QMessageBox.Warning)
            mensaje.setWindowTitle("Error")
            mensaje.setText("no se selecciono ninguna base de datos")
            mensaje.exec_()
    
    def closeEvent(self,event):
        self.on_close()
    def on_close(self):
        self.con.close()

    
            
   

class Proceso1(QThread): #hilo auxiliar para poder ejecutar la barra de progreso mientras se realiza la exportacion a excel
    def __init__(self,DBconn:str,excel:str,periodo:str,trimestre:int):
        super().__init__()
        self.DBconnName=DBconn
        self.excel=excel
        self.periodo=periodo
        self.trimestre=trimestre
    def run(self):
        ExportarAExcel(self.DBconnName, self.excel, self.periodo,self.trimestre)

class Proceso2(QThread):#hilo auxiliar para poder ejecutar la barra de progreso mientras se realiza el respaldo la base de datos
    def __init__(self,DBName,BackupDBName):
        super().__init__()
        self.DBName=DBName
        self.BackupDBName=BackupDBName
    
    def run(self):
        RespaldarArchivoDB(self.DBName,self.BackupDBName)
        
if __name__ =="__main__":           
    if not QtWidgets.QApplication.instance():
        app=QtWidgets.QApplication(sys.argv)
    else:
        app=QtWidgets.QApplication.instance()
    con=sqlite3.connect("../DB/ESM_pruebas.db")
    Window=MainWindow(con,"Admin")
    Window.show()
    app.exec()