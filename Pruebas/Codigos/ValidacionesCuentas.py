#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re

def ValidarUsuario(Usuario:str,Mensaje:str):
    #funcion hecha en caso de que los requisitos del nombre de usuario sean distintos
    if len(Usuario)>15:
        Mensaje+="El usuario es mas grande de lo debido\n"
        
    elif re.match(r"^[a-z0-9]{1,14}$", Usuario) is None:
        Mensaje="El usuario solamente acepta letras minusculas y numeros\n"
        
    return Mensaje

def ValidarFecha(Fecha,Mensaje):
    if re.match("^20[0-9]{2}-0[1|2]$", Fecha) is None:
        Mensaje+="La fecha no es valida\n"  
    return Mensaje
    

def VerificarUsuarioCuenta(Boleta:str,Mensaje:str,DBconn): #Avisa si el alumno ya tiene una cuenta en la base de datos en el periodo indicado
    cursor=DBconn.cursor()
    verificar="""Select Alumno.NombreAlumno,Alumno.ApellidosAlumno,
    Cuenta.NombreCuenta,Cuenta.Contrasena from Alumno 
    inner join Cuenta on Alumno.CveAlumno=Cuenta.CveAlumno  and Alumno.CveAlumno=?""" 
    cursor.execute(verificar,(Boleta,))
    resultado=cursor.fetchone()
    if  len(resultado)>0:
        Mensaje+="El alumno "+ resultado[0] +" " + resultado[1]+" tiene el usuario " + resultado[2] +" con la contraseña "+ resultado[3]+"\n"
        
    return Mensaje

def VerificarBoletaCuenta(Boleta:str,Mensaje:str,DBconn):#Avisa si la boleta esta registrada en la tabla de Alumnos
    cursor=DBconn.cursor()    
    verificar="""select Alumno.CveAlumno from Alumno where CveAlumno=?
    """
    cursor.execute(verificar,(Boleta,))
    resultado =cursor.fetchone()
    if resultado is None:
        Mensaje+="La boleta no esta registrada en la tabla de alumnos\n"
        
    return Mensaje
def VerificarCuentaExista(Cuenta:str,Mensaje:str,DBconn):
    cursor=DBconn.cursor()
    verificar="select NombreCuenta from Cuenta where NombreCuenta=?"
    cursor.execute(verificar,(Cuenta,))
    resultado=cursor.fetchone()
    if resultado is None:
        Mensaje+="La cuenta no esta registrada en la tabla de cuentas de usuario\n"
        
    return Mensaje
        