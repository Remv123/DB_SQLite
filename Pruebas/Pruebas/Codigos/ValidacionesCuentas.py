#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 18:19:46 2022

@author: rafael
"""
import string,re

def ValidarUsuario(Usuario,Mensaje,Errores):
    letras=string.ascii_letters
    digitos=string.digits
    numeros=0
    Letras=0
    for elem in Usuario:
        if elem in letras:
            Letras+=1
        if elem in digitos:
            numeros+=1 
    if Letras!=2:
        Mensaje+="El usuario no cumple con el numero requerido de letras\n"
        Errores+=1 
    if numeros!=10:
        Mensaje+="El usuario no cumple con el numero requerido de numeros\n"
        Errores+=1 
    return Mensaje,Errores

def ValidarFecha(Fecha,Mensaje,errores):
    if re.match("^20[0-9]{2}-0[1|2]$", Fecha) is None:
        Mensaje+="La fecha no es valida\n"
        errores+=1
    return Mensaje,errores
    

def VerificarUsuarioCuenta(Boleta,Fecha,Mensaje,errores,DBconn): #Avisa si el alumno ya tiene una cuenta en la base de datos en el periodo indicado
    cursor=DBconn.cursor()
    verificar="""Select Alumno.NombreAlumno,Alumno.ApellidosAlumno,
    Cuenta.NombreCuenta,Cuenta.Contrasena from Alumno 
    inner join Cuenta on Alumno.CveAlumno=Cuenta.CveAlumno where Cuenta.Semestre=? and Alumno.CveAlumno=?""" 
    cursor.execute(verificar,(Fecha,Boleta))
    resultado=cursor.fetchall()
    if  len(resultado)>0:
        Mensaje+="El alumno "+ resultado[0][0] +" " + resultado[0][1]+" tiene el usuario " + resultado[0][2] +" con la contraseña "+ resultado[0][3]+"\n"
        errores+=1
    return Mensaje, errores

def VerificarBoletaCuenta(Boleta,Mensaje,errores,DBconn):#Avisa si la boleta esta registrada en la tabla de Alumnos
    cursor=DBconn.cursor()    
    verificar="""select Alumno.CveAlumno from Alumno where CveAlumno=?
    """
    cursor.execute(verificar,(Boleta,))
    resultado =cursor.fetchone()
    if resultado is None:
        Mensaje+="La boleta no esta registrada en la tabla de alumnos\n"
        errores+=1
    return Mensaje, errores

def VerificarCuentaExista(Cuenta,Mensaje,errores,DBconn):
    cursor=DBconn.cursor()
    verificar="select NombreCuenta from Cuenta where NombreCuenta=?"
    cursor.execute(verificar,(Cuenta,))
    resultado=cursor.fetchone()
    if resultado is None:
        Mensaje+="La cuenta no esta registrada en la tabla de cuentas de usuario\n"
        errores+=1
    return Mensaje,errores
        