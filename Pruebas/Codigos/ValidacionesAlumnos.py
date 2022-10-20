#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

def ValidarBoleta(Boleta:str,Mensaje:str):
    expresion=r"^[a-z0-9]{1,14}$"
    if len(Boleta)>14:
        Mensaje+="La Boleta del alumno excede el rango esperado\n"
       
    elif re.match(expresion, Boleta)==None:
        Mensaje+="La Boleta contiene caracteres no validos\n"
       
    return Mensaje

def ValidarNombre(Nombre:str,Mensaje:str):
    if any(char.isdigit() for char in Nombre):
         Mensaje+="El nombre no debe contener numeros\n"
        
    return Mensaje

def ValidarCorreo(Correo:str,Mensaje:str):
    if Correo.find('@')==-1 :
        Mensaje+="El correo no es valido \n"
       
    if len(Correo)<4:
        Mensaje+="El correo es demasiado corto\n"
       
    return Mensaje

def ValidarApellidos(Apellidos:str,Mensaje:str):
    expresion=r"^([a-zA-Z]{1,25})\s[a-zA-Z]{1,25}$"
    ApellidosSeparados=Apellidos.split()
    if len( ApellidosSeparados)!=2:   
        Mensaje="Deben Existir dos Apellidos en el campo\n"
    else:
        if len(ApellidosSeparados[0])>25:
            Mensaje+="El primer apellido excede el rango esperado\n"
        if   len(ApellidosSeparados[1])>25:
            Mensaje="El segundo apellido excede el rango esperado\n"
    if re.match(expresion,Apellidos)==None:
        Mensaje+="Los apellidos no pueden tener numeros \n"
       
    return Mensaje

def VerificarBoletaBaseDatos(Boleta:str,Mensaje:str,DBconnection):
    cursor=DBconnection.cursor()
    verificar="""Select CveAlumno from Alumno where CveAlumno=?"""
    cursor.execute(verificar,(Boleta,))
    if cursor.fetchone() is None:
        Mensaje+="La boleta del alumno no esta en la base de datos\n"
       
    return Mensaje
    
    
        