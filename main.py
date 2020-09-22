from PyQt5 import QtWidgets, QtMultimediaWidgets, QtMultimedia, QtCore, QtGui, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox
import sys, random

""" 
A program for research at the University of Chicago: Data Formatting, visualization, & summarization for numeric data.
"""

class UCAnalysisGUI(QMainWindow):
    def __init__(self):
        """The __init__ method of UCAnalysisGUI class prepares GUI by inheriting QMainWindow from PyQt5. It adds meta
        information, defines screen size & placement and calls the sub-methods responsible for populating the GUI
        with widgets and widget functionality."""
        super().__init__()
        # creates a full-screen application with coordinates (0, 0)
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('Data Analysis & Visualization for UC')
        # Call method that adds content to main window
        self.initialize_content()
        # Call method that adds interactivity/widget functionality to GUI
        self.initialize_interactive_methods()

    def initialize_content(self):
        """All widgets are created, styled, and positioned on the GUI window in this method. The UCAnalysisGUI class
        calls this method during the execution of it's __init__ method, populating the GUI with content."""
        pass

    def initialize_interactive_methods(self):
        """All widget functions activated by user interaction are defined in this method. The UCAnalysisGUI class
        calls this method during the execution of it's __init__ method"""
        pass


# Run Application
def launch_GUI():
    app_configuration = QApplication(sys.argv)   # Creates a QApplication that configures the PyQt5 program
    application = UCAnalysisGUI()                # Instantiates our GUI class
    application.show()                           # Show the application on local machine's screen
    sys.exit(app_configuration.exec_())          # Instructs program to terminate when user closes the GUI


launch_GUI()                                     # Run the program