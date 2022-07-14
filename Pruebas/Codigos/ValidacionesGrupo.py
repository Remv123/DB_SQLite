#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 19:47:30 2022

@author: rafael
"""

def ValidarClaveGrupo(Grupo):
    niveles="123456789ABC"
    Mensaje=""
    Errores=0
    if len(Grupo)==0:
        Mensaje+="El campo esta sin llenar\n"
        Errores+=1
    else:
        if niveles.find(Grupo[0]) == -1:
            Mensaje+="El nivel del grupo no es valido\n"
            Errores+=1
        if Grupo[1]!="C":
            Mensaje+="La segunda letra del grupo no es valida\n"
            Errores+=1
        if Grupo[2]!="V" and Grupo[2]!="M":
            Mensaje+="El turno del grupo no es valido\n"
            Errores+=1
        if Grupo[3].isdigit()==False:
            Mensaje+="El numero de grupo no es valido\n"
            Errores+=1
        if len(Grupo)==5:
            if Grupo[4].isdigit()==False:
                Mensaje+="El segundo numero no es valido"
                Errores+=1
    return Mensaje,Errores