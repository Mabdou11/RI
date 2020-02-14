# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 05:31:09 2019

@author: Moahmed AIT MEHDI
"""

from PyQt5 import QtWidgets
import sys
from interface import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
def run() :
    
   app = QtWidgets.QApplication(sys.argv)
   window = MainWindow()
   app.setStyle("Fusion")
   window.show()
   app.exec_()
    
if __name__ == '__main__':
    run()