#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,sqlite3

from PyQt5 import QtWidgets,QtCore

class TableViewer(QtWidgets.QWidget):
    def __init__(self,TableName:str,cursor):
        super().__init__()
        self.cursor=cursor
        self.edit=QtWidgets.QLineEdit()
        self.combo=QtWidgets.QComboBox()
        self.table=QtWidgets.QTableWidget()
        query=self.OrdenarTabla(TableName)
        layout=QtWidgets.QGridLayout(self)
        layout.addWidget(self.edit,0,0)
        layout.addWidget(self.combo,0,1)
        layout.addWidget(self.table,1,0,1,2)
        self.populate_table(query)
        self.setWindowTitle(TableName)
        self.edit.textChanged.connect(self.filter_table)
        self.show()
        
        
    def populate_table(self,query:str):
       
        self.cursor.execute(query)            
        name_of_columns=[e[0] for e in self.cursor.description]
        self.table.setColumnCount(len(name_of_columns))
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(name_of_columns)
        self.combo.clear()
        self.combo.addItems(name_of_columns)
        rows=self.cursor.fetchall()
        for i ,row_data in enumerate(rows):
            self.table.insertRow(self.table.rowCount())
            for j,value in enumerate(row_data):
                item=QtWidgets.QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole,value)
                self.table.setItem(i,j,item)
        for i in range(len(name_of_columns)):
            self.table.resizeColumnToContents(i)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    def OrdenarTabla(self,TableName):
        if TableName == "Materias":
            return """Select CveMateria as Abreviatura,NombreMateria,
        SemestreMateria as Semestre,DepartamentoMateria as Departamento,Trimestre from Materias 
        order by DepartamentoMateria,NombreMateria"""
        if TableName=="Grupo":
            return """Select CveGrupo as Grupo,GrupoSemestre as Semestre 
        from Grupo order by substr(CveGrupo,1,3),
        substr(CveGrupo,4,9)*1"""
        if TableName=="Alumno":
            return """Select CveAlumno as NoBoleta,NombreAlumno as Nombre,
        ApellidosAlumno as Apellidos,EmailAlumno as Email from Alumno"""
        if TableName=="Cuenta":
            return "select CveAlumno as Boleta,Contrasena from Cuenta"
        if TableName=="CuentasMaterias":
            return """select NombreCuenta as Usuario,NomMateria as AbreviaturaMateria,
        Cvegrupo as Grupo,SemestreCuentaMaterias as Semestre from CuentaMaterias
    """
        if TableName=="Usuarios":
            return """Select NombreUsuario as Usuario,Contrasena  from Usuarios
        """
       
   
    def filter_table(self,text):
        if text:
            filter_column=self.combo.currentIndex()
            
            for i in range(self.table.rowCount()):
                item=self.table.item(i,filter_column)
                if self.filter_row(item,text):
                    self.table.showRow(i)
                else:
                    self.table.hideRow(i)
        else:
            for i in range(self.table.rowCount()):
                self.table.showRow(i)
    def filter_row(self,item,text):
        return text in item.text()
    
   
        
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    #con=sqlite3.Connection("../DB/ESM_pruebas.db") #conexión a la base de datos
    con=sqlite3.Connection("../DB/ESM_pruebas.db")
    cursor=con.cursor() 
    window=TableViewer("Prueba",cursor)
    app.exec()
