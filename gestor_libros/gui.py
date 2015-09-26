#!/usr/bin/python
#-*-coding: utf-8-*-
 
from PySide import QtGui, QtCore
import sys
from lector import *
import os
from bbdd import *
 
 
class MainWindow(QtGui.QWidget):
   
  def __init__(self):
    super(MainWindow, self).__init__()
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
     
    bot_nuevo = QtGui.QPushButton('Introducir nuevo libro', self)
    bot_consultar = QtGui.QPushButton('Consultar libros', self)
    bot_sacar = QtGui.QPushButton('Sacar libros', self)
    bot_salir = QtGui.QPushButton('Salir', self)
     
    grid.addWidget(bot_nuevo, 1, 1)
    grid.addWidget(bot_consultar, 2, 1)
    grid.addWidget(bot_sacar, 3, 1)
    grid.addWidget(bot_salir, 4, 2)
     
    bot_salir.clicked.connect(QtCore.QCoreApplication.instance().quit)
    bot_nuevo.clicked.connect(lambda : self.init_lector())
    bot_consultar.clicked.connect(lambda : self.imprime_libros())
     
    #bot_osciloscopio.clicked.connect(lambda: self.init_ventana_osc())
    #bot_med_pot.clicked.connect(lambda: self.init_ventana_pot())
     
    self.setLayout(grid)        
    self.setGeometry(100, 100, 500, 500)
    self.setWindowTitle('Ventana principal')
    self.showMaximized()
     
  def imprime_libros(self):
    base = BaseDeDatos()
    libros = base.showAll()
    info = VentanaInfo(libros)
   
  def init_lector(self):
    diccionario = {'&Aacute;':'Á', '&Eacute;':'É', '&Iacute;':'Í', '&Oacute;':'Ó', '&Uacute;':'Ú', '&aacute;':'á', '&eacute;':'é', '&iacute;':'í', '&oacute;':'ó', '&uacute;':'ú', '&Ntilde;':'Ñ', '&ntilde;':'ñ'}
    v = Lector()
    isbn = v.getBarCode()
    iberlibro = "http://www.iberlibro.com/servlet/SearchResults?isbn=" + str(isbn)
    pagina = os.popen("curl " + iberlibro)
    pagina = pagina.read()
     
    titulo, autor, fecha, precio = self.getData(pagina)
     
    # Cambiamos la codificacion
    for key in diccionario:
      titulo = titulo.replace(key, diccionario[key])
      autor = autor.replace(key, diccionario[key])
     
    string = "Título: " + titulo + "\nAutor: " + autor + "\nFecha de publicación: " + fecha + '\nPrecio(Iberlibro): ' + precio + ' EUR'
     
    info = VentanaInfo(string)
     
    base = BaseDeDatos()
    base.addRow(isbn, autor, titulo, precio, 1)
     
  def getData(self, pagina):
    patron_nombre = '<meta itemprop="name" content="'
    patron_autor = '<meta itemprop="author" content="'
    patron_fecha = '<meta itemprop="datePublished" content="'
    patron_precio = '<meta itemprop="price" content="'
    patron_fin = '" />'
     
    len_nombre = len(patron_nombre)
    len_autor = len(patron_autor)
    len_fecha = len(patron_fecha)
    len_precio = len(patron_precio)
     
    index1_t = pagina.find(patron_nombre)
    index2_t = pagina.find(patron_fin, index1_t)
    if index1_t == -1:
      index1_t = 0
      index2_t = index1_t
     
    index1_a = pagina.find(patron_autor, index2_t)
    index2_a = pagina.find(patron_fin, index1_a)
    if index1_a == -1:
      index1_a = index2_t
      index2_a = index1_a
     
    index1_f = pagina.find(patron_fecha, index2_a)
    index2_f = pagina.find(patron_fin, index1_f)
    if index1_f == -1:
      index1_f = index2_a
      index2_f = index1_f
     
    index1_p = pagina.find(patron_precio, index2_f)
    index2_p = pagina.find(patron_fin, index1_p)
    if index1_p == -1:
      index1_p = index2_f
      index2_p = index1_p
     
    titulo = pagina[index1_t+len_nombre:index2_t]
    autor = pagina[index1_a+len_autor:index2_a]
    fecha = pagina[index1_f+len_fecha:index2_f]
    precio = pagina[index1_p+len_precio:index2_p]
 
    return titulo, autor, fecha, precio
 
class VentanaInfo(QtGui.QWidget):
   
  def __init__(self, texto):
    '''Constructor de una ventana de informacion
     
    Parametros:
      texto: Texto que mostrar'a la ventana
     
    '''
    super(VentanaInfo, self).__init__()
    self.inicializa(texto)
   
  def inicializa(self, texto):
    win = QtGui.QMessageBox()
     
    # Lo ponemos para que lo entienda PySide
    codec = QtCore.QTextCodec.codecForName("UTF-8")
    texto = codec.toUnicode(texto)
     
    win.setInformativeText(texto)
    #win.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    win.exec_()