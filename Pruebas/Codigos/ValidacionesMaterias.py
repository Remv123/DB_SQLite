#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:26:51 2022

@author: rafael
"""

def ValidarMaterias(Abreviatura,nombre,semestre,errores,mensaje):
    if len(Abreviatura)>15:
        errores+=1
        mensaje="La abreviatura es demasiado grande\n"
    if any(c.isdigit() for c in nombre):
        errores+=1
        mensaje+="El nombre de la materia no puede contener numeros\n"
    if any(c.isalpha() for c in semestre):
        errores+=1
        mensaje+="El semestre no debe contener letras"
    if semestre.find("°")==-1:
        errores+=1
        mensaje+="El semestre debe terminar con °"
    return mensaje,errores

def ValidarEliminacionMaterias(Abreviatura,mensaje,errores,Cursor):
    verificar="select NombreMateria from Materias where CveMateria=?"
    Cursor.execute(verificar,(Abreviatura,))
    resultado=Cursor.fetchone()
    if resultado is None:
        mensaje+="La materia no esta registrada en la base de datos"
        errores+=1
    return mensaje,errores

def ValidarTrimestreMaterias(Trimestre,mensaje,errores):
    if Trimestre!="1" and Trimestre!="2":
        mensaje+="El trimestre no esta en el rango valido"
        errores+=1
    return mensaje,errores
        