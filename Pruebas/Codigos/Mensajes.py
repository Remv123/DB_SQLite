#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

def MostrarErroresInsercion(Errores):
    msg=QtWidgets.QMessageBox()
    msg.setWindowTitle("Error")
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText("Error en la inscerción de datos")
    msg.setDetailedText(Errores)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setEscapeButton(QtWidgets.QMessageBox.Ok)
    msg.exec()
    
def MostrarExito():
    msg=QtWidgets.QMessageBox()
    msg.setWindowTitle("Notificación")
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Los datos se ingresaron de manera correcta")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setEscapeButton(QtWidgets.QMessageBox.Ok)
    msg.exec()

def MostrarExitoBorrar():
    msg=QtWidgets.QMessageBox()
    msg.setWindowTitle("Notificación")
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Los datos se borraron de manera correcta")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setEscapeButton(QtWidgets.QMessageBox.Ok)
    msg.exec()

def MostrarErroresBorrar(Errores):
    msg=QtWidgets.QMessageBox()
    msg.setWindowTitle("Error")
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText("Error en la eliminación de datos")
    msg.setDetailedText(Errores)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setEscapeButton(QtWidgets.QMessageBox.Ok)
    msg.exec()
    
