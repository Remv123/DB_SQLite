#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QInputDialog,QProgressDialog
from PyQt5.QtWidgets import QFileDialog,QMenu,QMessageBox,QAction,QLineEdit,QPushButton,QMainWindow
from ValidacionesUsuario import VerificarUsuario
from Conexion import ConexionDB
from Menu import MainWindow
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
from ValidacionesAlumnos import ValidarBoleta,VerificarBoletaBaseDatos
from ValidacionesCuentas import ValidarUsuario,ValidarFecha,VerificarBoletaCuenta,VerificarUsuarioCuenta,VerificarCuentaExista
from ValidacionesUsuario import VerificarSoloUsuario,ValidarUsuarioApliacion
from ValidacionesMaterias import ValidarMaterias
from ValidacionesGrupo import ValidarClaveGrupo
from CustomTableView import TableViewer
from ResourcePath import resource_path
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import sys,sqlite3

if __name__=="__main__":
    if not QtWidgets.QApplication.instance():
        app=QtWidgets.QApplication(sys.argv)
    else:
        app=QtWidgets.QApplication.instance()
    Window=ConexionDB()
    Window.show()
    app.exec()
        