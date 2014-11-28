#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import backend
from PyQt4 import QtGui, QtCore



class ConfigEditor(QtGui.QMainWindow):
    
    def __init__(self):
        super(ConfigEditor, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        lbl1 = QtGui.QLabel("Select an SBGrid Program", self)
        lbl1.adjustSize() 
        lbl1.resize
        lbl2 = QtGui.QLabel("Program", self)
        lbl3 = QtGui.QLabel("Version", self)
        self.lbl4 = QtGui.QLabel("Saved Overrides", self)
        self.lbl4.adjustSize()
        self.statusBar().showMessage('Ready')
   
        config_file=backend.open_config()
        self.config_header, self.config_array = backend.read_config(config_file)
        self.prog_dict, prog_list = backend.find_sbgrid_progs()

        self.prog_sel_combo = QtGui.QComboBox(self)
        self.prog_sel_combo.completer()
        for prog in prog_list:	
            self.prog_sel_combo.addItem(prog)

        self.ver_sel_combo = QtGui.QComboBox(self)
        self.ver_sel_combo.completer()

        self.add_btn = QtGui.QPushButton(self)
        self.add_btn.setIcon(QtGui.QIcon("icons/icon-plus-512.png"))
        self.add_btn.setEnabled(False)
        self.add_btn.setToolTip('Sets the selected <b>version</b> as default for this <b>program</b>. ')

        self.save_btn = QtGui.QPushButton('Save', self)
        self.save_btn.setEnabled(False)
        self.save_btn.setToolTip('Save all changes to your config file.')
        self.save_btn.resize(self.save_btn.sizeHint())

        self.table = QtGui.QTableWidget(self,)
        self.table.setColumnCount(3)
        self.table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.populate_table(self.config_array)
        
	#widget locations
        lbl1.move(25, 25)
       	lbl2.move(25, 50)
        lbl3.move(165, 50)
        self.prog_sel_combo.move(25, 75)
        self.prog_sel_combo.resize(120, 20)
        self.ver_sel_combo.move(165, 75)
        self.ver_sel_combo.resize(120, 20)
        self.add_btn.move(300,55)
        self.add_btn.resize(40,40)
        self.lbl4.move(25, 110)
        self.table.move(25,140)
        self.table.resize(315,150)
        self.save_btn.move(25,300)


        self.prog_sel_combo.activated[str].connect(self.progSelected)
        self.ver_sel_combo.activated[str].connect(self.verSelected) 
        self.add_btn.clicked.connect(lambda:    self.add_click())
        self.save_btn.clicked.connect(lambda:   self.save_click())

        self.setGeometry(300, 300, 360, 350)
        self.setFixedSize(360, 350)
        self.setWindowIcon(QtGui.QIcon('icons/gbsgrid-icon.png'))        
        self.setWindowTitle('SBGrid Version manager - GBSGrid')
        self.show()

    def populate_table(self, config_array):
        self.table.clear()        
        self.table.setRowCount(len(config_array))
        for i in range(len(config_array)):
            prog = QtGui.QTableWidgetItem(config_array[i][0])
            ver = QtGui.QTableWidgetItem(config_array[i][1])
            self.button = QtGui.QPushButton('Delete')
            self.button.clicked.connect(self.deleteButtonClicked)
            self.table.setItem(i,0,prog)
            self.table.setItem(i,1,ver)
            self.table.setCellWidget(i,2,self.button)

    def deleteButtonClicked(self):
        button = QtGui.qApp.focusWidget()
        # or button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())
            del self.config_array[index.row()]
        self.populate_table(self.config_array)
        self.save_btn.setEnabled(True)
        
    def progSelected(self, prog_name):
        print prog_name
        self.add_btn.setEnabled(True)
        self.statusBar().showMessage(prog_name+' selected, choose a version')

        self.ver_sel_combo.clear()
        for ver in self.prog_dict[str(prog_name)]:	
            self.ver_sel_combo.addItem(ver)

    def verSelected(self, ver_name):
        print ver_name
        self.statusBar().showMessage(ver_name+' selected, click <b>add</b> to store change')

    def add_click(self):
        prog = str(self.prog_sel_combo.currentText())
        ver = str(self.ver_sel_combo.currentText())
        self.config_array = backend.add_override(self.config_array, prog, ver)
        print self.config_array
        self.save_btn.setEnabled(True)
        self.populate_table(self.config_array)
        self.statusBar().showMessage(str(self.prog_sel_combo.currentText())+', version '+str(self.ver_sel_combo.currentText())+' added to change list')
        self.lbl4.setText('Unsaved Overrides')
        self.lbl4.adjustSize()
    
    def save_click(self):
        self.lbl4.setText('Saved Overrides')
        backend.write_config(self.config_header, self.config_array)
        self.statusBar().showMessage("Changes saved to ~/.sbgrid.conf")


	
                
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = ConfigEditor()
    sys.exit(app.exec_())

    

if __name__ == '__main__':
    main()

