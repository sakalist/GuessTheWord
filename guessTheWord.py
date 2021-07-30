# -*- coding: utf-8 -*-

""" Guess The Word
Hangman game variation

Author: Tassos Sakalis
Version 1.1
Date:  07/2021

UI created by PyQt5 UI code generator
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import random
import sys


class MyMainWindow(object):
    def __init__(self):
        self.listOfWords = []  # The list of words read from file
        self.listOfButtons = []  # The group of letter buttons
        self.listOfGames = []  # Used in continue game mode
        self.letterCount = 24  # In english lang, letterCount must be 26
        self.startLetter = "Α"  # In english lang, startLetter must be english capital A
        self.verticalButtonStep = 40  # In english lang, verticalButtonStep must be 30
        self.startingTries = 8  # Default tries to guess the word
        self.tries = self.startingTries
        self.isMultiGame = False  # Multi game flag
        self.multiGames = 0  # Number of games. Used in multi game mode
        self.load_file()
        self.word = self.listOfWords[random.randrange(len(self.listOfWords))]
        self.wordSoFar = len(self.word) * "-"
        self.buttonBackcolor = "background-color: #aaff77;"
        self.startImg = "assets/images/flower8.gif"
        self.endImg = "assets/images/flower0.gif"
        self.timer = QtCore.QTimer()
        self.minutes = 1  # Default duration (minutes)
        self.seconds = 30  # Default duration (seconds)
        self.time = QtCore.QTime(0, self.minutes, self.seconds)
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1000)  # milliseconds

    def setup_ui(self, mainWindow):
        mainWindow.setWindowTitle("Μάντεψε τη Λέξη")
        mainWindow.resize(800, 600)
        mainWindow.setStyleSheet("background-color: #f2f2d9; selection-color: #000000; "
                                 "selection-background-color: #f8f8ec")
        self.central_widget = QtWidgets.QWidget(mainWindow)

        self.lbl_title = QtWidgets.QLabel(self.central_widget)
        self.lbl_title.setGeometry(QtCore.QRect(250, 10, 461, 71))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_title.setFont(font)
        self.lbl_title.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setText("ΜΑΝΤΕΨΕ ΤΗ ΛΕΞΗ")

        self.grp_letters = QtWidgets.QGroupBox(self.central_widget)
        self.grp_letters.setGeometry(QtCore.QRect(240, 390, 491, 151))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        font.setWeight(50)
        self.grp_letters.setFont(font)
        self.grp_letters.setAutoFillBackground(False)
        self.grp_letters.setStyleSheet("background-color: rgb(240, 255, 206);")
        self.grp_letters.setTitle("Επιλέξτε γράμμα")

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
            self.listOfButtons[i].setStyleSheet(self.buttonBackcolor)
            if (i + 1) % 8 == 0:
                x = 10
                y += self.verticalButtonStep

        # Button Captions
        current_letter = ord(self.startLetter)
        for btn in self.listOfButtons:
            btn.setText(chr(current_letter))
            # Έλεγχος για το ελληνικό τελικό ς, κεφαλαίο: chr(930) ή μικρό chr(962)
            if current_letter == 929 or current_letter == 961:
                current_letter += 2
            else:
                current_letter += 1

        # Create list of Games for multi game mode (max: 10 games)
        y = 95
        for i in range(10):
            self.listOfGames.append(QtWidgets.QLabel(self.central_widget))
            self.listOfGames[i].setGeometry(QtCore.QRect(745, y, 32, 32))
            self.listOfGames[i].setPixmap(QtGui.QPixmap("assets/images/game_clear.gif"))
            self.listOfGames[i].hide()
            y += 45

        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.btn_next_game = QtWidgets.QPushButton(self.central_widget)
        self.btn_next_game.setGeometry(QtCore.QRect(720, 35, 75, 41))
        self.btn_next_game.setFont(font)
        self.btn_next_game.setStyleSheet("background-color: rgb(255, 225, 0);")
        self.btn_next_game.hide()

        self.lbl_game_over = QtWidgets.QLabel(self.central_widget)
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
        self.lbl_game_over.setText("ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ - GAME OVER")
        self.lbl_game_over.hide()

        self.img_flower = QtWidgets.QLabel(self.central_widget)
        self.img_flower.setGeometry(QtCore.QRect(30, 80, 201, 451))
        self.img_flower.setText("")
        self.img_flower.setPixmap(QtGui.QPixmap(self.startImg))

        self.grp_tries = QtWidgets.QGroupBox(self.central_widget)
        self.grp_tries.setGeometry(QtCore.QRect(260, 240, 191, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.grp_tries.setFont(font)
        self.grp_tries.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.grp_tries.setTitle("Προσπάθειες που μένουν:")

        self.lbl_tries = QtWidgets.QLabel(self.grp_tries)
        self.lbl_tries.setGeometry(QtCore.QRect(16, 19, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_tries.setFont(font)
        self.lbl_tries.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_tries.setText(str(self.tries))

        self.grp_time = QtWidgets.QGroupBox(self.central_widget)
        self.grp_time.setGeometry(QtCore.QRect(520, 240, 191, 61))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.grp_time.setFont(font)
        self.grp_time.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.grp_time.setTitle("Χρόνος που μένει:")

        self.lbl_time = QtWidgets.QLabel(self.grp_time)
        self.lbl_time.setGeometry(QtCore.QRect(10, 20, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_time.setFont(font)
        self.lbl_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_time.setText(self.time.toString("mm:ss"))

        self.frm_word = QtWidgets.QFrame(self.central_widget)
        self.frm_word.setGeometry(QtCore.QRect(250, 90, 471, 121))
        self.frm_word.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border: 2px solid rgb(150, 150, 150);\n"
                                    "border-radius: 15px;")
        self.frm_word.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_word.setFrameShadow(QtWidgets.QFrame.Raised)

        self.lbl_letters = QtWidgets.QLabel(self.frm_word)
        self.lbl_letters.setGeometry(QtCore.QRect(10, 10, 161, 21))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.lbl_letters.setFont(font)
        self.lbl_letters.setStyleSheet("border: 0;")
        self.lbl_letters.setText("Αριθμός γραμμάτων: " + str(len(self.word)))

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
        self.lbl_word.setText(self.wordSoFar)

        mainWindow.setCentralWidget(self.central_widget)

        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setTitle("Παιχνίδι")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        mainWindow.setStatusBar(self.statusbar)

        self.menu_new_game = QtWidgets.QAction(mainWindow)
        self.menu_new_game.setText("Νέο Παιχνίδι")
        self.menu_new_game.setShortcut("Ctrl+N")
        self.menu_new_game.setStatusTip("Ξεκινά ένα νέο παιχνίδι")

        self.menu_reload_file = QtWidgets.QAction(mainWindow)
        self.menu_reload_file.setText("Επαναφόρτωση Λεξικού")
        self.menu_reload_file.setShortcut("Ctrl+L")
        self.menu_reload_file.setStatusTip("Διαβάζει ξανά το λεξικό. "
                                           "Χρήσιμο αν προσθέσατε νέες λέξεις")

        self.menu_exit = QtWidgets.QAction(mainWindow)
        self.menu_exit.setText("Έξοδος")
        self.menu_exit.setShortcut("Ctrl+X")
        self.menu_exit.setStatusTip("Έξοδος από το παιχνίδι")

        self.menu.addAction(self.menu_new_game)
        self.menu.addAction(self.menu_reload_file)
        self.menu.addSeparator()
        self.menu.addAction(self.menu_exit)
        self.menubar.addAction(self.menu.menuAction())

        # Settings Dialog
        self.populate_settings_dialog()

        # Button click handler
        for index, btn in enumerate(self.listOfButtons):
            btn.clicked.connect(partial(self.letter_click, btn.text(), index))
        # Next game handler in multi game mode
        self.btn_next_game.clicked.connect(self.next_game)
        self.btn_next_game.setText("Συνέχεια")

        # Menu click handlers
        self.menu_new_game.triggered.connect(lambda: self.start_new_game())
        self.menu_reload_file.triggered.connect(lambda: self.load_file())
        self.menu_exit.triggered.connect(lambda: self.exit())

    def populate_settings_dialog(self):
        self.settings_dialog = QtWidgets.QDialog(self.central_widget)
        self.settings_dialog.setModal(True)
        self.settings_dialog.resize(700, 500)
        self.settings_dialog.setWindowTitle("Ρυθμίσεις")

        self.lbl_set_title = QtWidgets.QLabel(self.settings_dialog)
        self.lbl_set_title.setGeometry(QtCore.QRect(260, 20, 221, 20))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_set_title.setFont(font)
        self.lbl_set_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_set_title.setText("ΡΥΘΜΙΣΕΙΣ ΠΑΙΧΝΙΔΙΟΥ")

        self.lbl_img_logo = QtWidgets.QLabel(self.settings_dialog)
        self.lbl_img_logo.setGeometry(QtCore.QRect(40, 30, 128, 128))
        self.lbl_img_logo.setText("")
        self.lbl_img_logo.setPixmap(QtGui.QPixmap("assets/images/logo.gif"))

        self.lbl_max_time = QtWidgets.QLabel(self.settings_dialog)
        self.lbl_max_time.setGeometry(QtCore.QRect(200, 70, 165, 16))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.lbl_max_time.setFont(font)
        self.lbl_max_time.setText("Μέγιστος χρόνος ανά λέξη:")

        self.lbl_max_games = QtWidgets.QLabel(self.settings_dialog)
        self.lbl_max_games.setGeometry(QtCore.QRect(200, 120, 165, 16))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(10)
        self.lbl_max_games.setFont(font)
        self.lbl_max_games.setText("Συυνεχόμενα παιχνίδια:")

        self.cmb_time_min = QtWidgets.QComboBox(self.settings_dialog)
        self.cmb_time_min.setGeometry(QtCore.QRect(380, 70, 41, 22))
        self.cmb_time_min.addItem("0")
        self.cmb_time_min.addItem("1")
        self.cmb_time_min.addItem("2")
        self.cmb_time_min.addItem("3")
        self.cmb_time_min.addItem("4")
        self.cmb_time_min.addItem("5")
        self.cmb_time_min.setCurrentIndex(1)  # default 1 min

        self.cmb_time_sec = QtWidgets.QComboBox(self.settings_dialog)
        self.cmb_time_sec.setGeometry(QtCore.QRect(430, 70, 41, 22))
        self.cmb_time_sec.addItem("00")
        self.cmb_time_sec.addItem("10")
        self.cmb_time_sec.addItem("20")
        self.cmb_time_sec.addItem("30")
        self.cmb_time_sec.addItem("40")
        self.cmb_time_sec.addItem("50")
        self.cmb_time_sec.setCurrentIndex(3)  # default 30 sec

        self.cmb_games = QtWidgets.QComboBox(self.settings_dialog)
        self.cmb_games.setGeometry(QtCore.QRect(380, 120, 41, 22))
        self.cmb_games.addItem("0")
        self.cmb_games.addItem("2")
        self.cmb_games.addItem("3")
        self.cmb_games.addItem("4")
        self.cmb_games.addItem("5")
        self.cmb_games.addItem("6")
        self.cmb_games.addItem("7")
        self.cmb_games.addItem("8")
        self.cmb_games.addItem("9")
        self.cmb_games.addItem("10")

        self.label_1 = QtWidgets.QLabel(self.settings_dialog)
        self.label_1.setGeometry(QtCore.QRect(480, 70, 172, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_1.setFont(font)
        self.label_1.setText("(0:00 = Απεριόριστος χρόνος)")

        self.label_2 = QtWidgets.QLabel(self.settings_dialog)
        self.label_2.setGeometry(QtCore.QRect(430, 120, 137, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setText("(0 = Απενεργοποιημένο)")

        self.line = QtWidgets.QFrame(self.settings_dialog)
        self.line.setGeometry(QtCore.QRect(0, 170, 701, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.grp_pc = QtWidgets.QGroupBox(self.settings_dialog)
        self.grp_pc.setGeometry(QtCore.QRect(20, 190, 281, 221))
        self.grp_pc.setStyleSheet("background-color: #ffffff")
        self.grp_pc.setTitle("Λέξη από λεξικό")

        self.lbl_img_pc = QtWidgets.QLabel(self.grp_pc)
        self.lbl_img_pc.setGeometry(QtCore.QRect(50, 20, 151, 160))
        self.lbl_img_pc.setPixmap(QtGui.QPixmap("assets/images/pc.png"))

        self.grp_human = QtWidgets.QGroupBox(self.settings_dialog)
        self.grp_human.setEnabled(False)
        self.grp_human.setGeometry(QtCore.QRect(310, 190, 371, 221))
        self.grp_human.setStyleSheet("background-color: #ffffff")
        self.grp_human.setTitle("Λέξη από πληκτρολόγηση")

        self.lbl_message = QtWidgets.QLabel(self.grp_human)
        self.lbl_message.setGeometry(QtCore.QRect(10, 50, 351, 24))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(14)
        self.lbl_message.setFont(font)
        self.lbl_message.setText("Δώσε τη λέξη με ΚΕΦΑΛΑΙΑ ΕΛΛΗΝΙΚΑ")

        self.txt_pass = QtWidgets.QLineEdit(self.grp_human)
        self.txt_pass.setGeometry(QtCore.QRect(10, 100, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txt_pass.setFont(font)
        self.txt_pass.setStyleSheet("background-color: rgb(216, 234, 255);")
        self.txt_pass.setEchoMode(QtWidgets.QLineEdit.Password)

        self.btn_pass = QtWidgets.QPushButton(self.grp_human)
        self.btn_pass.setGeometry(QtCore.QRect(320, 100, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_pass.setFont(font)
        self.btn_pass.setText("?")

        self.lbl_chars = QtWidgets.QLabel(self.grp_human)
        self.lbl_chars.setGeometry(QtCore.QRect(106, 150, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_chars.setFont(font)
        self.lbl_chars.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_chars.setText("0 χαρακτήρες")

        self.button_box = QtWidgets.QDialogButtonBox(self.settings_dialog)
        self.button_box.setGeometry(QtCore.QRect(570, 450, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_box.setFont(font)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)

        self.radio_pc = QtWidgets.QRadioButton(self.settings_dialog)
        self.radio_pc.setGeometry(QtCore.QRect(90, 420, 151, 17))
        self.radio_pc.setChecked(True)
        self.radio_pc.setText("Αντίπαλος: Υπολογιστής")
        self.radio_human = QtWidgets.QRadioButton(self.settings_dialog)
        self.radio_human.setGeometry(QtCore.QRect(430, 420, 141, 17))
        self.radio_human.setText("Αντίπαλος: Άνθρωπος")

        self.btn_pass.pressed.connect(self.show_pass)
        self.btn_pass.released.connect(self.hide_pass)
        self.txt_pass.textChanged.connect(self.update_lbl_chars)

        self.radio_pc.clicked.connect(self.radio_pc_clicked)
        self.radio_human.clicked.connect(self.radio_human_clicked)

        self.button_box.accepted.connect(self.settings_dialog.accept)
        self.button_box.rejected.connect(self.settings_dialog.reject)

    def start_new_game(self):
        # Clear previous word by human
        self.txt_pass.setText("")
        # Execute settings dialog
        if self.settings_dialog.exec() == 1:  # OK pressed in settings dialog
            if self.radio_human.isChecked() and self.txt_pass.text() != "":
                # Opponent human. Pick letter from text box
                self.word = self.txt_pass.text().upper().strip()
            else:
                # Opponent PC. Pick word from dictionary
                self.word = self.listOfWords[random.randrange(len(self.listOfWords))]

            # In multi game mode show selected games and hide the rest
            self.multiGames = int(self.cmb_games.currentText())
            if self.multiGames > 0:
                self.isMultiGame = True
            else:
                self.isMultiGame = False
            self.btn_next_game.hide()
            for i in range(10):
                self.listOfGames[i].setPixmap(QtGui.QPixmap("assets/images/game_clear.gif"))
            for i in range(self.multiGames):
                self.listOfGames[i].show()
            for i in range(self.multiGames, 10):
                self.listOfGames[i].hide()

            self.play_word()

    def play_word(self):
        # Set time
        self.time = QtCore.QTime(0, int(self.cmb_time_min.currentText()), int(self.cmb_time_sec.currentText()))
        self.lbl_title.setStyleSheet("color: #000000;")
        self.lbl_title.setText("ΜΑΝΤΕΨΕ ΤΗ ΛΕΞΗ")
        self.lbl_letters.setText("Αριθμός γραμμάτων: " + str(len(self.word)))
        self.wordSoFar = len(self.word) * "-"
        self.lbl_word.setText(self.wordSoFar)
        self.tries = self.startingTries
        self.lbl_tries.setText(str(self.tries))
        self.lbl_game_over.hide()
        for button in self.listOfButtons:
            button.setStyleSheet(self.buttonBackcolor)
            button.setEnabled(True)
        self.grp_letters.setEnabled(True)
        self.img_flower.setPixmap(QtGui.QPixmap(self.startImg))
        self.lbl_time.setText(self.time.toString("mm:ss"))
        self.timer.start(1000)

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
                self.wordSoFar = self.wordSoFar[:position] + letter + self.wordSoFar[position + 1:]
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
        self.grp_letters.setDisabled(True)

        if reason == "win":
            self.lbl_title.setStyleSheet("color: rgb(0, 0, 255);")
            self.lbl_title.setText("ΜΠΡΑΒΟ! Βρήκες τη λέξη!")
            self.img_flower.setPixmap(QtGui.QPixmap(self.startImg))
            multi_game_image = "assets/images/game_win.gif"
        elif reason == "lose":
            self.lbl_title.setStyleSheet("color: rgb(255, 0, 0);")
            self.lbl_title.setText("ΛΥΠΑΜΑΙ. Δεν βρήκες τη λέξη:\n" + self.word)
            multi_game_image = "assets/images/game_lose.gif"
        else:  # Time ends
            self.lbl_title.setStyleSheet("color: rgb(255, 0, 0);")
            self.lbl_title.setText("ΤΕΛΟΣ ΧΡΟΝΟΥ. Δεν βρήκες τη λέξη:\n" + self.word)
            self.img_flower.setPixmap(QtGui.QPixmap(self.endImg))
            multi_game_image = "assets/images/game_lose.gif"

        # Check for multi game mode
        if self.isMultiGame:
            self.listOfGames[self.multiGames - 1].setPixmap(QtGui.QPixmap(multi_game_image))
            self.multiGames -= 1
            if self.multiGames > 0:
                self.btn_next_game.show()
            else:
                self.lbl_game_over.show()
        else:
            self.lbl_game_over.show()

    def next_game(self):
        self.btn_next_game.hide()
        self.word = self.listOfWords[random.randrange(len(self.listOfWords))]
        self.play_word()

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

    def update_lbl_chars(self):
        self.lbl_chars.setText(str(len(self.txt_pass.text())) + " χαρακτήρες")

    def show_pass(self):
        self.txt_pass.setEchoMode(QtWidgets.QLineEdit.Normal)

    def hide_pass(self):
        self.txt_pass.setEchoMode(QtWidgets.QLineEdit.Password)

    def radio_pc_clicked(self):
        self.cmb_games.setDisabled(False)
        self.grp_human.setEnabled(False)
        self.grp_pc.setEnabled(True)

    def radio_human_clicked(self):
        self.cmb_games.setCurrentIndex(0)
        self.cmb_games.setDisabled(True)
        self.grp_human.setEnabled(True)
        self.grp_pc.setEnabled(False)

    def exit(self):
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
