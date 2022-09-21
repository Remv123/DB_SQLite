#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
def RespaldarArchivoDB(DBName,DBBackupName):
    conexion=sqlite3.connect(DBName)
    conexion2=sqlite3.connect(DBBackupName)
    with conexion2:
        conexion.backup(conexion2,pages=0)
    conexion.close()
    conexion2.close()

