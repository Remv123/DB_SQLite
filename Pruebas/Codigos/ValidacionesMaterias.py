#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def ValidarMaterias(Abreviatura:str,nombre:str,semestre:str,mensaje:str):
    if len(Abreviatura)>15:
        mensaje="La abreviatura es demasiado grande\n"
    if any(c.isdigit() for c in nombre):
        mensaje+="El nombre de la materia no puede contener numeros\n"
    return mensaje

def ValidarEliminacionMaterias(Abreviatura:str,mensaje:str,Cursor):
    verificar="select NombreMateria from Materias where CveMateria=?"
    Cursor.execute(verificar,(Abreviatura,))
    resultado=Cursor.fetchone()
    if resultado is None:
        mensaje+="La materia no esta registrada en la base de datos"
       
    return mensaje

def ValidarTrimestreMaterias(Trimestre,mensaje):
    if Trimestre!="1" and Trimestre!="2":
        mensaje+="El trimestre no esta en el rango valido"
       
    return mensaje
        