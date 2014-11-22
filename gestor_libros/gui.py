#!/usr/bin/python

from PySide import QtGui, QtCore
import sys
from lector import * 
import os

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
    
    #bot_osciloscopio.clicked.connect(lambda: self.init_ventana_osc())
    #bot_med_pot.clicked.connect(lambda: self.init_ventana_pot())
    
    self.setLayout(grid)        
    self.setGeometry(100, 100, 500, 500)
    self.setWindowTitle('Ventana principal')
    self.showMaximized()
    
  def init_lector(self):
    v = Lector()
    isbn = v.getBarCode()
    iberlibro = "http://www.iberlibro.com/servlet/SearchResults?isbn=" + str(isbn)
    pagina = os.popen("curl " + iberlibro)
    pagina = pagina.read()
    
    patron_nombre = '<meta itemprop="name" content="'
    patron_autor = '<meta itemprop="author" content="'
    patron_fecha = '<meta itemprop="datePublished" content="'
    patron_precio = '<meta itemprop="price" content="'
    patron_fin = '" />'
    
    len_nombre = len(patron_nombre)
    len_autor = len(patron_autor)
    len_fecha = len(patron_fecha)
    len_precio = len(patron_precio)

    index1 = pagina.find(patron_nombre)
    index2 = pagina.find(patron_fin, index1)
    titulo = pagina[index1+len_nombre:index2]
    
    index1 = pagina.find(patron_autor, index2)
    index2 = pagina.find(patron_fin, index1)
    autor = pagina[index1+len_autor:index2]

    index1 = pagina.find(patron_fecha, index2)
    index2 = pagina.find(patron_fin, index1)
    fecha = pagina[index1+len_fecha:index2]
    
    index1 = pagina.find(patron_precio, index2)
    index2 = pagina.find(patron_fin, index1)
    precio = pagina[index1+len_precio:index2]
    
    string = "Titulo: " + titulo + "\nAutor: " + autor + "\nFecha de publicacion: " + fecha + '\nPrecio(Iberlibro): ' + precio + ' EUR'

    info = VentanaInfo(string)

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
    win.setInformativeText(texto)
    #win.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    win.exec_()
    
