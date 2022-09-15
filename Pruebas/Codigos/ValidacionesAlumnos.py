#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def ValidarBoleta(Boleta,Mensaje,contador):
    if len(Boleta)>14:
        Mensaje+="La Boleta del alumno excede el rango esperado\n"
        contador+=1
    return Mensaje,contador

def ValidarNombre(Nombre,Mensaje,contador):
    if any(char.isdigit() for char in Nombre):
         Mensaje+="El nombre no debe contener numeros\n"
         contador+=1
    return Mensaje,contador

def ValidarCorreo(Correo,Mensaje,contador):
    if Correo.find('@')==-1:
        Mensaje+="El correo no es valido \n"
        contador+=1
    if len(Correo)<4:
        Mensaje+="El correo es demasiado corto\n"
        contador+=1
    return Mensaje,contador

def ValidarApellidos(Apellidos,Mensaje,contador):
    if any(char.isdigit() for char in Apellidos):
        Mensaje+="Los apellidos no pueden tener numeros\n"
        contador+=1
    return Mensaje,contador

def VerificarBoletaBaseDatos(Boleta,Mensaje,contador,DBconnection):
    cursor=DBconnection.cursor()
    verificar="""Select CveAlumno from Alumno where CveAlumno=?"""
    cursor.execute(verificar,(Boleta,))
    if cursor.fetchone() is None:
        Mensaje+="La boleta del alumno no esta en la base de datos\n"
        contador+=1
    return Mensaje,contador
    
    
        