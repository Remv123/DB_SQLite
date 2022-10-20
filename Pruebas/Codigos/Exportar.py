#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from pandas import ExcelWriter
import sqlite3

def ExportarAExcel(conexion,excel,periodo,trimestre):

    con=sqlite3.connect(conexion)
    sql="""select Cuenta.NombreCuenta as username,Contrasena as password ,NombreAlumno as firstname,ApellidosAlumno as lastname,
    EmailAlumno as email,NombreMateria as course,CveGrupo as 'group',Trimestre
    from CuentaMaterias  inner join Cuenta on CuentaMaterias.NombreCuenta=Cuenta.NombreCuenta inner join Alumno
     on Cuenta.CveAlumno=Alumno.CveAlumno inner join Materias on CuentaMaterias.NomMateria=Materias.CveMateria 
     where CuentaMaterias.SemestreCuentaMaterias=? and (Trimestre=? or Trimestre is NULL) 
     """
    
    
    data=pd.read_sql(sql,con,params=[periodo,trimestre])
    data['idx']=data.groupby("username").cumcount()+1
    a=data.pivot_table(index=["username","password","firstname","lastname","email"],columns="idx",values=["group","course"],aggfunc='first')
    a.sort_index(axis=1,level=1,inplace=True)
    columnas=list(a.columns)
    columnas=[str(x+str(y)) for x,y in columnas]
    columnas.sort(key=lambda x:(int(x[-1])))
    a.columns=columnas
    a.reset_index(inplace=True)
    a.to_string(index=False)
    a.to_excel(excel,index=False)
    con.close()
    
