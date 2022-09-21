#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
def ValidarUsuarioApliacion(Usuario,contrasena,Mensaje):
    expresion=r"^\w{1,20}$"
    if len(Usuario)==0 or len(contrasena)==0:
        Mensaje+="Existen campos sin llenar\n"
    else:
        if re.match(expresion,Usuario)==None:
            Mensaje+="El nombre de usuario contiene caracteres no validos\n"
        if re.match(expresion,contrasena)==None:
            Mensaje+="La contrasena contiene caracteres no validos\n"
    return Mensaje

def VerificarUsuario(name,password,connection):
    if connection!="":
        cursor=connection.cursor()
    else:
        return False
    if name=="":
        return False
    oracion="select * from Usuarios where NombreUsuario=? and Contrasena=?"
    
    cursor.execute(oracion,(name,password,))
    resultado=cursor.fetchone()
   
    if resultado is None:
        return False
    else:
        return True
    
def VerificarSoloUsuario(name,connection):
    cursor=connection.cursor()
    oracion="Select * from Usuarios where NombreUsuario=?"
    cursor.execute(oracion,(name,))
    resultado=cursor.fetchone()
    if resultado is None:
        return False
    else:
        return True
    
