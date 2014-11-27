#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import backend
from PyQt4 import QtGui, QtCore



class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        self.lbl1 = QtGui.QLabel("Select an SBGrid Program", self)
        lbl2 = QtGui.QLabel("Program", self)
        lbl3 = QtGui.QLabel("Version", self)

        prog_sel_combo = QtGui.QComboBox(self)
        prog_sel_combo.completer()
        self.prog_dict, prog_list = backend.find_sbgrid_progs()
        for prog in prog_list:	
            prog_sel_combo.addItem(prog)

        self.ver_sel_combo = QtGui.QComboBox(self)
        self.ver_sel_combo.completer()

        self.prog_btn = QtGui.QPushButton('Run ' +prog_list[0], self)
        self.prog_btn.setToolTip('This will <b>start</b> the program selected in the dropdown')
        self.prog_btn.resize(self.prog_btn.sizeHint())
        
	#widget locations
        self.lbl1.move(25, 25)
       	lbl2.move(25, 50)
        lbl3.move(165, 50)
        prog_sel_combo.move(25, 75)
        prog_sel_combo.resize(120, 20)
        self.ver_sel_combo.move(165, 75)
        self.ver_sel_combo.resize(120, 20)
        self.prog_btn.move(25,100)


        prog_sel_combo.activated[str].connect(self.progSelected)        
        self.ver_sel_combo.activated.connect(self.verSelected)        

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QComboBox')
        self.show()
        
    def progSelected(self, prog_name):
        print prog_name
        self.prog_btn.setText('Run ' +prog_name)

        self.ver_sel_combo.clear()
        for ver in self.prog_dict[str(prog_name)]:	
            self.ver_sel_combo.addItem(ver)

    def verSelected(self, ver_num):
		print ver_num

	
                
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

    

if __name__ == '__main__':
    main()

