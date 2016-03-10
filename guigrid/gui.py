#!/usr/bin/python
# -*- coding: utf-8 -*-

import signal
import sys
import parser
from PyQt4 import QtGui, QtCore

__version__ = "0.0.9"

class ConfigEditor(QtGui.QMainWindow):
    
    def __init__(self):
        super(ConfigEditor, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        
        #Initialise the backend and scrape required info/configs
        branch = parser.detect_branch()
        try:
            progs_list = parser.ls_progs(branch['folder'])
        except KeyError:
            error_msg = "No SBgrid installation found at '/programs/'"
            QtGui.QMessageBox.information(None, 'Fatal Error', error_msg)
        self.progs_dict = parser.scrape_all_progs(branch, progs_list)

        config_file=parser.open_config()
        self.config_header, self.config_array = parser.read_config(config_file)

        #spawn labels and status bar
        lbl1 = QtGui.QLabel("Select an SBGrid Program", self)
        lbl1.adjustSize() 
        lbl1.resize
        lbl2 = QtGui.QLabel("Program", self)
        lbl3 = QtGui.QLabel("Version", self)
        self.lbl4 = QtGui.QLabel("Saved Overrides", self)
        self.lbl4.adjustSize()
        self.statusBar().showMessage('Ready (ver: ' + __version__ + ')')
   
        #spawn/populate program select box
        self.prog_sel_combo = QtGui.QComboBox(self)
        self.prog_sel_combo.completer()
        for prog in progs_list:	
            self.prog_sel_combo.addItem(prog)
        #spawn/populate version select box
        self.ver_sel_combo = QtGui.QComboBox(self)
        self.ver_sel_combo.completer()
        for ver in self.progs_dict[str(progs_list[0])]["allver"]:	
            self.ver_sel_combo.addItem(ver)
        #spawn add button
	self.add_btn = QtGui.QPushButton('+',self)
        self.add_btn.setStyleSheet('QPushButton {font-size: 24pt; font-weight: bold}')
        self.add_btn.setToolTip('Sets the selected <b>version</b> as default for this <b>program</b>. ')
        #spawn save button
        self.save_btn = QtGui.QPushButton('Save', self)
        self.save_btn.setEnabled(False)
        self.save_btn.setToolTip('Save all changes to your config file.')
        self.save_btn.resize(self.save_btn.sizeHint())
        #spawn/populate overrides info table
        self.table = QtGui.QTableWidget(self,)
        self.table.setHorizontalHeaderLabels(["Program","Version","Reset"])
        self.table.setColumnCount(3)
        self.table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.populate_table()
    	#set static widget locations
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

        #linking clicks to event functions
        self.prog_sel_combo.activated[str].connect(self.prog_selected)
        self.ver_sel_combo.activated[str].connect(self.ver_selected) 
        self.add_btn.clicked.connect(lambda:    self.add_click())
        self.save_btn.clicked.connect(lambda:   self.save_click())
        #setup window and show it
        self.setGeometry(300, 300, 360, 350)
        self.setFixedSize(360, 350)
        self.setWindowIcon(QtGui.QIcon('icons/gbsgrid-icon.png'))        
        self.setWindowTitle('SBGrid Version manager - GUIGrid')
        self.show()

    def populate_table(self):
        """Clears the overrides information table and repopulates it"""
        self.table.clear()
        self.table.setHorizontalHeaderLabels(["Program","Version"," "])        
        self.table.setRowCount(len(self.config_array))
        for i in range(len(self.config_array)):
            prog = QtGui.QTableWidgetItem(self.config_array[i][0])
            ver = QtGui.QTableWidgetItem(self.config_array[i][1])
            self.reset_btn = QtGui.QPushButton('Reset')
            self.reset_btn.setToolTip('<b>Removes an override entry</b>, resetting the version to the SBGrid default')
            self.reset_btn.clicked.connect(self.reset_button_clicked)
            self.table.setItem(i,0,prog)
            self.table.setItem(i,1,ver)
            self.table.setCellWidget(i,2,self.reset_btn)

    def reset_button_clicked(self):
        """Resets the progs override to the default version"""
        button = QtGui.qApp.focusWidget()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            del self.config_array[index.row()]
        self.populate_table()
        self.save_btn.setEnabled(True)
        
    def prog_selected(self, prog_name):
        """Populates the version select dropdown""" 
        self.statusBar().showMessage(prog_name+' selected, choose a version')

        self.ver_sel_combo.clear()
        for ver in self.progs_dict[str(prog_name)]["allver"]:	
            self.ver_sel_combo.addItem(ver)

    def ver_selected(self, ver_name):
        self.statusBar().showMessage(ver_name+' selected, click <b>add</b> to store change')

    def add_click(self):
        """Adds entry to config_array, refreshes UI"""
        prog = str(self.prog_sel_combo.currentText())
        ver = str(self.ver_sel_combo.currentText())
        self.config_array = parser.add_override(self.config_array, prog, ver, self.progs_dict)
        #print self.config_array
        self.save_btn.setEnabled(True)
        self.populate_table()
        self.statusBar().showMessage(str(self.prog_sel_combo.currentText())+', version '+str(self.ver_sel_combo.currentText())+' added to change list')
        self.lbl4.setText('Unsaved Overrides')
        self.lbl4.adjustSize()
 
    def save_click(self):
        """Calls to the backend to store staged override changes in the file"""
        self.lbl4.setText('Saved Overrides')
        try:
            parser.write_config(self.config_header, self.config_array)
        except IOError:
            print("Can't write to file, please check you have permission for ~/.sbgrid.conf")
        else:
            save_msg = "Changes saved to ~/.sbgrid.conf, to load new versions you must <b>start a new terminal session</b>"
            self.statusBar().showMessage(save_msg)
            self.save_btn.setEnabled(False)
            QtGui.QMessageBox.information(None, 'Changes Succesfully Saved', save_msg)

    def closeEvent(self, event):
        """Warns user when closing the program with unsaved changes"""
        if self.save_btn.isEnabled():
            reply = QtGui.QMessageBox.question(self, 'Message',
                "You have unsaved override changes, are you sure to quit?", QtGui.QMessageBox.Yes | 
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QtGui.QApplication.quit()    

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)    
    app = QtGui.QApplication(sys.argv)
    timer = QtCore.QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)
    ex = ConfigEditor()
    sys.exit(app.exec_())

