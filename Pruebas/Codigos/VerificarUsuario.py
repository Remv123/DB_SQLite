#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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