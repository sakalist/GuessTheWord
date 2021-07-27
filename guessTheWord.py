# -*- coding: utf-8 -*-

""" Guess The Word
Hangman game variation

Author: Tassos Sakalis
Version 1.0
Date:  07/2021

UI created by PyQt5 UI code generator
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import random
import sys


class MyMainWindow(object):
    def __init__(self):
        self.listOfWords = []   # The list of words read from file
        self.listOfButtons = []  # The group of letter buttons
        self.letterCount = 24  # In english lang, letterCount must be 26
        self.startLetter = "Α"  # In english lang, startLetter must be english capital A
        self.verticalButtonStep = 40  # In english lang, verticalButtonStep must be 30
        self.starting_tries = 8
        self.tries = self.starting_tries
        self.load_file()
        self.word = self.listOfWords[random.randrange(len(self.listOfWords))]
        self.wordSoFar = len(self.word) * "-"
        self.button_backcolor = "background-color: #aaff77;"
        self.start_img = "assets/images/flower8.gif"
        self.end_img = "assets/images/flower0.gif"
        self.timer = QtCore.QTimer()
        self.minutes = 1  # Duration (minutes)
        self.seconds = 30  # Duration (seconds)
        self.time = QtCore.QTime(0, self.minutes, self.seconds)
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1000)  # milliseconds

    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        main_window.setStyleSheet("background-color: #f2f2d9; selection-color: #000000; "
                                  "selection-background-color: #f8f8ec")
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        self.grp_letters = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_letters.setGeometry(QtCore.QRect(240, 390, 491, 151))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        font.setWeight(50)
        self.grp_letters.setFont(font)
        self.grp_letters.setAutoFillBackground(False)
        self.grp_letters.setStyleSheet("background-color: rgb(240, 255, 206);")
        self.grp_letters.setObjectName("grp_letters")

        # Create list of letter buttons
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        x = 10  # x position of first button
        y = 30  # y position of first button
        for i in range(self.letterCount):
            self.listOfButtons.append(QtWidgets.QPushButton(self.grp_letters))
            self.listOfButtons[i].setGeometry(QtCore.QRect(x, y, 45, 30))
            x += 60
            self.listOfButtons[i].setFont(font)
            self.listOfButtons[i].setStyleSheet(self.button_backcolor)
            self.listOfButtons[i].setObjectName("btn_" + str(i))
            if (i+1) % 8 == 0:
                x = 10
                y += self.verticalButtonStep

        self.lbl_game_over = QtWidgets.QLabel(self.centralwidget)
        self.lbl_game_over.setGeometry(QtCore.QRect(260, 330, 451, 31))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_game_over.setFont(font)
        self.lbl_game_over.setStyleSheet("background-color: rgb(170, 255, 127);")
        self.lbl_game_over.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_game_over.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_game_over.setObjectName("lbl_game_over")
        self.lbl_game_over.hide()

        self.img_flower = QtWidgets.QLabel(self.centralwidget)
        self.img_flower.setGeometry(QtCore.QRect(30, 80, 201, 451))
        self.img_flower.setText("")
        self.img_flower.setPixmap(QtGui.QPixmap(self.start_img))
        self.img_flower.setObjectName("img_flower")

        self.grp_tries = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_tries.setGeometry(QtCore.QRect(260, 240, 191, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.grp_tries.setFont(font)
        self.grp_tries.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.grp_tries.setObjectName("grp_tries")

        self.lbl_tries = QtWidgets.QLabel(self.grp_tries)
        self.lbl_tries.setGeometry(QtCore.QRect(16, 19, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_tries.setFont(font)
        self.lbl_tries.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_tries.setObjectName("lbl_tries")

        self.grp_time = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_time.setGeometry(QtCore.QRect(520, 240, 191, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.grp_time.setFont(font)
        self.grp_time.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.grp_time.setObjectName("grp_time")

        self.lbl_time = QtWidgets.QLabel(self.grp_time)
        self.lbl_time.setGeometry(QtCore.QRect(10, 20, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_time.setFont(font)
        self.lbl_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_time.setObjectName("lbl_time")

        self.frm_word = QtWidgets.QFrame(self.centralwidget)
        self.frm_word.setGeometry(QtCore.QRect(250, 90, 471, 121))
        self.frm_word.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border: 2px solid rgb(150, 150, 150);\n"
                                    "border-radius: 15px;")
        self.frm_word.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_word.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_word.setObjectName("frm_word")

        self.lbl_letters = QtWidgets.QLabel(self.frm_word)
        self.lbl_letters.setGeometry(QtCore.QRect(10, 10, 161, 21))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_letters.setFont(font)
        self.lbl_letters.setStyleSheet("border: 0;")
        self.lbl_letters.setObjectName("lbl_letters")

        self.lbl_word = QtWidgets.QLabel(self.frm_word)
        self.lbl_word.setGeometry(QtCore.QRect(6, 50, 461, 41))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_word.setFont(font)
        self.lbl_word.setStyleSheet("border: 0;")
        self.lbl_word.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_word.setObjectName("lbl_word")

        self.lbl_title = QtWidgets.QLabel(self.centralwidget)
        self.lbl_title.setGeometry(QtCore.QRect(250, 10, 461, 71))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_title.setFont(font)
        self.lbl_title.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setObjectName("lbl_title")
        self.lbl_title.setWordWrap(True)

        main_window.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        main_window.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.menu_new_game = QtWidgets.QAction(main_window)
        self.menu_new_game.setObjectName("menu_new_game")
        self.menu_reload_file = QtWidgets.QAction(main_window)
        self.menu_reload_file.setObjectName("menu_reload_file")
        self.menu_exit = QtWidgets.QAction(main_window)
        self.menu_exit.setObjectName("menu_exit")

        self.menu.addAction(self.menu_new_game)
        self.menu.addAction(self.menu_reload_file)
        self.menu.addSeparator()
        self.menu.addAction(self.menu_exit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(main_window)

        # Button click handler
        for index, btn in enumerate(self.listOfButtons):
            btn.clicked.connect(partial(self.letter_click, btn.text(), index))
        # Menu click handlers
        self.menu_new_game.triggered.connect(lambda: self.start_new_game())
        self.menu_reload_file.triggered.connect(lambda: self.load_file())
        self.menu_exit.triggered.connect(lambda: self.exit())

        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Μάντεψε τη Λέξη"))
        self.lbl_game_over.setText(_translate("main_window", "ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ - GAME OVER"))
        self.grp_tries.setTitle(_translate("main_window", "Προσπάθειες που μένουν:"))
        self.lbl_tries.setText(_translate("main_window", str(self.tries)))
        self.grp_time.setTitle(_translate("main_window", "Χρόνος που μένει:"))
        self.lbl_time.setText(_translate("main_window", self.time.toString("mm:ss")))
        self.lbl_letters.setText(_translate("main_window", "Αριθμός γραμμάτων: " + str(len(self.word))))
        self.lbl_word.setText(_translate("main_window", self.wordSoFar))
        self.lbl_title.setText(_translate("main_window", "ΜΑΝΤΕΨΕ ΤΗ ΛΕΞΗ"))

        self.menu.setTitle(_translate("main_window", "Παιχνίδι"))
        self.menu_new_game.setText(_translate("main_window", "Νέο Παιχνίδι"))
        self.menu_new_game.setShortcut(_translate("main_window", "Ctrl+N"))
        self.menu_new_game.setStatusTip(_translate("main_window", "Ξεκινά ένα νέο παιχνίδι"))
        self.menu_reload_file.setText(_translate("main_window", "Επαναφόρτωση Λεξικού"))
        self.menu_reload_file.setShortcut(_translate("main_window", "Ctrl+L"))
        self.menu_reload_file.setStatusTip(_translate("main_window", "Διαβάζει ξανά το λεξικό. "
                                                                    "Χρήσιμο αν προσθέσατε νέες λέξεις"))
        self.menu_exit.setText(_translate("main_window", "Έξοδος"))
        self.menu_exit.setShortcut(_translate("main_window", "Ctrl+X"))
        self.menu_exit.setStatusTip(_translate("main_window", "Έξοδος από το παιχνίδι"))

        self.grp_letters.setTitle(_translate("main_window", "Επιλέξτε γράμμα"))
        current_letter = ord(self.startLetter)

        # Button Captions
        for btn in self.listOfButtons:
            btn.setText(_translate("main_window", chr(current_letter)))
            # Έλεγχος για το ελληνικό τελικό ς, κεφαλαίο: chr(930) ή μικρό chr(962)
            if current_letter == 929 or current_letter == 961:
                current_letter += 2
            else:
                current_letter += 1

    def letter_click(self, letter, idx):
        # Disable clicked letter
        self.listOfButtons[idx].setEnabled(False)
        self.listOfButtons[idx].setStyleSheet("background-color: rgb(240, 255, 206);")

        # Check if letter found
        if letter in self.word:
            # Letter found in word
            # Replace every occurrence of letter in wordSoFar
            position = self.word.find(letter, 0)
            while position != -1:  # -1 means not found
                # Place letter in position
                self.wordSoFar = self.wordSoFar[:position] + letter + self.wordSoFar[position+1:]
                # Search for next occurrence
                position = self.word.find(letter, position + 1)
            # Display word found so far
            self.lbl_word.setText(self.wordSoFar)
            # Check if word completed
            if self.wordSoFar == self.word:
                self.game_over("win")
        else:
            # Letter not found in word
            # Update and display tries
            self.tries -= 1
            self.lbl_tries.setText(str(self.tries))
            # Update image
            # If tries > 8 show image number 8
            number = 8 if self.tries > 8 else self.tries
            img = "assets/images/flower" + str(number) + ".gif"
            self.img_flower.setPixmap(QtGui.QPixmap(img))
            # Check for game over
            if self.tries == 0:
                self.game_over("lose")

    def game_over(self, reason):
        self.timer.stop()
        self.lbl_game_over.show()
        self.grp_letters.setDisabled(True)

        if reason == "win":
            self.lbl_title.setStyleSheet("color: rgb(0, 0, 255);")
            self.lbl_title.setText("ΜΠΡΑΒΟ! Βρήκες τη λέξη!")
            self.img_flower.setPixmap(QtGui.QPixmap(self.start_img))
        elif reason == "lose":
            self.lbl_title.setStyleSheet("color: rgb(255, 0, 0);")
            self.lbl_title.setText("ΛΥΠΑΜΑΙ. Δεν βρήκες τη λέξη:\n" + self.word)
        else:  # Time ends
            self.lbl_title.setStyleSheet("color: rgb(255, 0, 0);")
            self.lbl_title.setText("ΤΕΛΟΣ ΧΡΟΝΟΥ. Δεν βρήκες τη λέξη:\n" + self.word)
            self.img_flower.setPixmap(QtGui.QPixmap(self.end_img))

    def start_new_game(self):
        # Initialize game parameters
        self.lbl_title.setStyleSheet("color: #000000;")
        self.lbl_title.setText("ΜΑΝΤΕΨΕ ΤΗ ΛΕΞΗ")
        self.word = self.listOfWords[random.randrange(len(self.listOfWords))]
        self.lbl_letters.setText("Αριθμός γραμμάτων: " + str(len(self.word)))
        self.wordSoFar = len(self.word) * "-"
        self.lbl_word.setText(self.wordSoFar)
        self.tries = self.starting_tries
        self.lbl_tries.setText(str(self.tries))
        self.lbl_game_over.hide()
        for button in self.listOfButtons:
            button.setStyleSheet(self.button_backcolor)
            button.setEnabled(True)
        self.grp_letters.setEnabled(True)
        self.img_flower.setPixmap(QtGui.QPixmap(self.start_img))
        self.time = QtCore.QTime(0, self.minutes, self.seconds)
        self.lbl_time.setText(self.time.toString("mm:ss"))
        self.timer.start(1000)

    def load_file(self):
        # Read dictionary file and fill listOfWords
        self.listOfWords = []
        with open('assets/dict.txt') as f:
            for line in f:
                # Strip word and convert to uppercase
                word = line.upper().strip()
                if word:  # Add only non empty lines
                    self.listOfWords.append(word)

    def timer_event(self):
        # Add one second
        self.time = self.time.addSecs(-1)
        # Display elapsed time
        self.lbl_time.setText(self.time.toString("mm:ss"))
        # Check for time limit
        if int(self.time.toString("mm")) == 0 and int(self.time.toString("ss")) == 0:
            self.game_over("time")

    def exit(self):
        sys.exit()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
