#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def ValidarClaveGrupo(Grupo):
    niveles="123456789ABC"
    Mensaje=""
    if len(Grupo)>6:
        Mensaje+="El grupo excede el numero de caracteres permitidos\n"
    elif len(Grupo)==0:
        Mensaje+="El campo esta sin llenar\n"
    else:
        if niveles.find(Grupo[0]) == -1:
            Mensaje+="El nivel del grupo no es valido\n"
            
        if Grupo[1]!="C":
            Mensaje+="La segunda letra del grupo no es valida\n"
            
        if Grupo[2]!="V" and Grupo[2]!="M":
            Mensaje+="El turno del grupo no es valido\n"
            
        if Grupo[3].isdigit()==False:
            Mensaje+="El numero de grupo no es valido\n"
            
        if len(Grupo)>4:
            if Grupo[4].isdigit()==False:
                Mensaje+="El segundo numero no es valido"
            if len(Grupo)==6:
                if Grupo[5].isdigit()==False:
                    Mensaje+="El tercer numero no es valido"
                
    return Mensaje