#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:16:48 2022

@author: rafael
"""
from pysqlcipher3 import dbapi2 as sqlite
def GenerarCursor(DBconn,password):
    cursor=DBconn.cursor()
    cursor.execute("Pragma key=""'"+password+"'")
    cursor.execute("PRAGMA cipher_compatibility = 3")

    return cursor
