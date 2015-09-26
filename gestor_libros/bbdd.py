#!/usr/bin/python
#-*-coding: utf-8-*-
import MySQLdb
 
class BaseDeDatos():
   
  '''def getBBDD(self):
    cxn = MySQLdb.connect(user='root', passwd='anita90', db='libros')
    return cxn'''
   
  def addRow(self, isbn, autor, titulo, precio, numero):
    params = (isbn, autor, titulo, precio, numero)
    cxn = MySQLdb.connect(user='root', passwd='anita90', db='libros')
    cur = cxn.cursor()
    #cur.execute("INSERT INTO stock VALUES(%d, %s, %s, %d, %d)", params)
    cur.execute("INSERT INTO stock VALUES(%s, %s, %s, %s, %s)", params)
    cur.close()
    cxn.commit()
    cxn.close()
   
  def showByISBN(self, isbn):
    params = isbn
    cxn = MySQLdb.connect(user='root', passwd='anita90', db='libros')
    cur = cxn.cursor()
    cur.execute("SELECT * FROM stock WHERE isbn LIKE %d", params)
     
    for data in cur.fetchall():
      print '%s\t%s\t%s\t%s\t%s' % data
     
    cur.close()
    cxn.commit()
    cxn.close()
   
  def showAll(self):
    cxn = MySQLdb.connect(user='root', passwd='anita90', db='libros')
    cur = cxn.cursor()
    cur.execute("SELECT * FROM stock")
     
    libros = ''
    for data in cur.fetchall():
      aux = '%s\t%s\t%s\t%s\t%s\n' % data
      libros = libros + aux
     
    cur.close()
    cxn.commit()
    cxn.close()
     
    return libros