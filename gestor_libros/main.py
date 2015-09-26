#!/usr/bin/python
#-*-coding: utf-8-*-
 
from lector import *
from gui import *
 
 
 
def main():
  app = QtGui.QApplication(sys.argv)
  main_window = MainWindow()
  sys.exit(app.exec_())
 
if __name__ == '__main__':
  main()