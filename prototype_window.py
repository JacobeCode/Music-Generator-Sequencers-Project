# Prototype window contains older version of algorithm for generating melody

import os
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from music_informations import music_informations


class Ui_MainWindow(object):
    def __init__(self):
        self.music_info = music_informations()

    def generate_music(self):
        # Multiply by 4 because of calculations on quarter-notes
        # This part is used for proper calculations for tact and whole song duration
        points_to_use = (self.music_info.metrum * self.music_info.tacts) * 4
        tact_space = self.music_info.metrum * 4
        used_durations = []

        # Calculation of score range dependent on lower border of ambitus
        lower_score = int(self.music_info.scale_sound.index(self.music_info.lower_ambitus[0])) + 1
        if self.music_info.lower_ambitus[1] == ",":
            pass
        elif self.music_info.lower_ambitus[1] == "":
            lower_score += 7
        elif self.music_info.lower_ambitus[1] == "'":
            lower_score += 14
        else:
            lower_score += 21

        # Calculation of score range dependent on higher border of ambitus
        higher_score = int(self.music_info.scale_sound.index(self.music_info.higher_ambitus[0])) + 1
        if self.music_info.higher_ambitus[1] == ",":
            pass
        elif self.music_info.higher_ambitus[1] == "":
            higher_score += 7
        elif self.music_info.higher_ambitus[1] == "'":
            higher_score += 14
        else:
            higher_score += 21

        # Scale score range calculated above
        scale_range = [lower_score, higher_score]

        # Control for checking calculations
        print("CHECK_01")
        print(scale_range)

        # Setting up proper file_name and starting writing to file with template and metrum
        file_name = "temp"
        text_file = open(file_name + ".ly", 'w')
        text_file.write(self.music_info.template + "{\n")
        text_file.write(self.music_info.number_tacts + "\n")
        text_file.write(chr(92) + "time " + str(self.music_info.metrum) + "/4 ")

        is_bemol = random.randint(0, 100)

        # Loop for melody creation on score_based system
        while points_to_use > 0:
            note_or_pause = random.randint(0, 100)

            if tact_space <= 0:
                tact_space = self.music_info.metrum * 4

            if note_or_pause <= self.music_info.pauses_likelihood:
                index = random.randint(0, 4)
                if points_to_use >= self.music_info.rest_durations_weights[index] and tact_space >= \
                        self.music_info.rest_durations_weights[index]:
                    self.music_info.melody.append(
                        self.music_info.scale_sound[7] + self.music_info.rest_durations[index])
                    points_to_use -= self.music_info.rest_durations_weights[index]
                    tact_space -= self.music_info.rest_durations_weights[index]
                    used_durations.append(self.music_info.rest_durations[index])
                else:
                    index = random.randint(0, 11)



                    note = random.randint(0, 6)
                    scale = random.randint(0, 3)

                    note_full_score = self.music_info.scale_sound_score[note] + self.music_info.scale_sound_score[scale]

                    if self.music_info.melody_type == "Random":
                        is_chromatic = random.randint(0, 100)

                    if self.music_info.melody_type == "Chromatic" or is_chromatic >= 50:
                        halftones = random.randint(0, 1)
                        note_full_score += self.music_info.chromatic_scale_end_score[halftones]

                    is_ligature = random.randint(0, 100)

                    if points_to_use >= note_full_score and tact_space >= note_full_score:
                        if self.music_info.melody_type == "Chromatic" or is_chromatic >= 50:
                            if is_ligature > 40:
                                if is_bemol >= 50:
                                    self.music_info.melody.append(
                                        self.music_info.scale_sound[note] + self.music_info.chromatic_scale_end_lower[halftones] + self.music_info.scale_number[scale] + self.music_info.durations[index] + "~ ")
                                else:
                                    self.music_info.melody.append(
                                        self.music_info.scale_sound[note] + self.music_info.chromatic_scale_end_upper[halftones] + self.music_info.scale_number[scale] + self.music_info.durations[index] + "~ ")
                            else:
                                if is_bemol >= 50:
                                    self.music_info.melody.append(
                                        self.music_info.scale_sound[note] +
                                        self.music_info.chromatic_scale_end_lower[halftones] + self.music_info.scale_number[scale] + self.music_info.durations[index])
                                else:
                                    self.music_info.melody.append(
                                        self.music_info.scale_sound[note] +
                                        self.music_info.chromatic_scale_end_upper[halftones] + self.music_info.scale_number[scale] + self.music_info.durations[index])
                            points_to_use -= note_full_score
                            tact_space -= note_full_score
                            used_durations.append(self.music_info.durations[index])
                        else:
                            if is_ligature > 40:
                                self.music_info.melody.append(
                                    self.music_info.scale_sound[note] + self.music_info.scale_number[scale] + self.music_info.durations[index] + "~ ")
                            else:
                                self.music_info.melody.append(
                                    self.music_info.scale_sound[note] + self.music_info.scale_number[scale] + self.music_info.durations[index])
                            points_to_use -= note_full_score
                            tact_space -= note_full_score
                            used_durations.append(self.music_info.durations[index])
                    else:
                        pass

                    self.music_info.melody[0] = self.music_info.first_note + used_durations[0]
                    self.music_info.melody[-1] = self.music_info.last_note + used_durations[0]

                    for note in self.music_info.melody:
                        text_file.write(note + " ")

                    # Closing file and setting proper bars
                    text_file.write("\n" + chr(92) + "bar " + chr(34) + "||" + chr(34) + "}")
                    text_file.close()

                    self.music_info.melody = []

                    os.system("lilypond --pdf " + file_name + ".ly")
                    os.system(file_name + ".pdf")
    def change_metrum(self):
        if self.metrum_insert.toPlainText() == "":
            pass
        else:
            self.music_info.metrum = int(self.metrum_insert.toPlainText())

    def change_tacts(self):
        if self.tacts_insert.toPlainText() == "":
            pass
        else:
            self.music_info.tacts = int(self.tacts_insert.toPlainText())

    def change_likelihood_pauses(self):
        if self.pauses_insert.toPlainText() == "":
            pass
        else:
            self.music_info.pauses_likelihood = int(self.pauses_insert.toPlainText())

    def change_first_note(self):
        note = self.note_first_input.currentText()
        scale = self.scale_first_note_input.currentText()

        self.music_info.first_note = note.lower()

        if scale == "Wielkie":
            self.music_info.first_note = self.music_info.first_note + ","
        elif scale == "Małe":
            pass
        elif scale == "Razkreślne":
            self.music_info.first_note = self.music_info.first_note + "'"
        elif scale == "Dwukreślne":
            self.music_info.first_note = self.music_info.first_note + "''"

    def change_last_note(self):
        note = self.note_last_input.currentText()
        scale = self.scale_last_note_input.currentText()

        if scale != "Wielkie":
            self.music_info.last_note = note.lower()
        else:
            self.music_info.last_note = note

        if scale == "Wielkie":
            self.music_info.last_note = self.music_info.last_note + ","
        elif scale == "Małe":
            pass
        elif scale == "Razkreślne":
            self.music_info.last_note = self.music_info.last_note + "'"
        elif scale == "Dwukreślne":
            self.music_info.last_note = self.music_info.last_note + "''"

    def change_lower_border(self):
        note = self.note_lower_ambitus_input.currentText()
        scale = self.scale_lower_ambitus_input.currentText()

        if scale != "Wielkie":
            self.music_info.lower_ambitus = note.lower()
        else:
            self.music_info.lower_ambitus = note

        if scale == "Wielkie":
            self.music_info.lower_ambitus = self.music_info.lower_ambitus + ","
        elif scale == "Małe":
            pass
        elif scale == "Razkreślne":
            self.music_info.lower_ambitus = self.music_info.lower_ambitus + "'"
        elif scale == "Dwukreślne":
            self.music_info.lower_ambitus = self.music_info.lower_ambitus + "''"

    def change_higher_border(self):
        note = self.note_higher_ambitus_input.currentText()
        scale = self.scale_higher_ambitus_input.currentText()

        if scale != "Wielkie":
            self.music_info.higher_ambitus = note.lower()
        else:
            self.music_info.higher_ambitus = note

        if scale == "Wielkie":
            self.music_info.higher_ambitus = self.music_info.higher_ambitus + ","
        elif scale == "Małe":
            pass
        elif scale == "Razkreślne":
            self.music_info.higher_ambitus = self.music_info.higher_ambitus + "'"
        elif scale == "Dwukreślne":
            self.music_info.higher_ambitus = self.music_info.higher_ambitus + "''"

    def change_interval_likelihood(self):
        self.music_info.how_much_1 = self.input_1.value()
        self.music_info.how_much_2m = self.input_2m.value()
        self.music_info.how_much_2w = self.input_2w.value()
        self.music_info.how_much_3m = self.input_3m.value()
        self.music_info.how_much_3w = self.input_3w.value()
        self.music_info.how_much_4 = self.input_4.value()
        self.music_info.how_much_5 = self.input_5.value()
        self.music_info.how_much_6m = self.input_6m.value()
        self.music_info.how_much_6w = self.input_6w.value()
        self.music_info.how_much_7m = self.input_7m.value()
        self.music_info.how_much_7w = self.input_7w.value()
        self.music_info.how_much_8 = self.input_8.value()

    def change_melody_type(self):
        self.music_info.melody_type = self.melody_type_input.currentText()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 623)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.program_info_text_edit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.program_info_text_edit.setGeometry(QtCore.QRect(420, 150, 201, 371))
        self.program_info_text_edit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.program_info_text_edit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.program_info_text_edit.setReadOnly(True)
        self.program_info_text_edit.setObjectName("program_info_text_edit")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 550, 361, 23))
        self.progressBar.setProperty("value", 21)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.settings_tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.settings_tabs.setGeometry(QtCore.QRect(10, 100, 401, 441))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.settings_tabs.setFont(font)
        self.settings_tabs.setObjectName("settings_tabs")
        self.basic_settings = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.basic_settings.setFont(font)
        self.basic_settings.setObjectName("basic_settings")
        self.metrum_info = QtWidgets.QTextEdit(self.basic_settings)
        self.metrum_info.setGeometry(QtCore.QRect(20, 20, 231, 31))
        self.metrum_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.metrum_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.metrum_info.setLineWidth(0)
        self.metrum_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_info.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.metrum_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.metrum_info.setObjectName("metrum_info")
        self.metrum_insert = QtWidgets.QTextEdit(self.basic_settings)
        self.metrum_insert.setGeometry(QtCore.QRect(250, 20, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.metrum_insert.setFont(font)
        self.metrum_insert.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.metrum_insert.setFrameShadow(QtWidgets.QFrame.Raised)
        self.metrum_insert.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_insert.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_insert.setObjectName("metrum_insert")
        self.metrum_div = QtWidgets.QTextEdit(self.basic_settings)
        self.metrum_div.setGeometry(QtCore.QRect(310, 20, 61, 31))
        self.metrum_div.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.metrum_div.setFrameShadow(QtWidgets.QFrame.Raised)
        self.metrum_div.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_div.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_div.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.metrum_div.setObjectName("metrum_div")
        self.tacts_info = QtWidgets.QTextEdit(self.basic_settings)
        self.tacts_info.setGeometry(QtCore.QRect(20, 70, 231, 31))
        self.tacts_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tacts_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tacts_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tacts_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tacts_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.tacts_info.setObjectName("tacts_info")
        self.tacts_insert = QtWidgets.QTextEdit(self.basic_settings)
        self.tacts_insert.setGeometry(QtCore.QRect(250, 70, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.tacts_insert.setFont(font)
        self.tacts_insert.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tacts_insert.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tacts_insert.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tacts_insert.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tacts_insert.setObjectName("tacts_insert")
        self.pauses_info = QtWidgets.QTextEdit(self.basic_settings)
        self.pauses_info.setGeometry(QtCore.QRect(20, 120, 231, 31))
        self.pauses_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pauses_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.pauses_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pauses_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pauses_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.pauses_info.setObjectName("pauses_info")
        self.pauses_insert = QtWidgets.QTextEdit(self.basic_settings)
        self.pauses_insert.setGeometry(QtCore.QRect(250, 120, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pauses_insert.setFont(font)
        self.pauses_insert.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pauses_insert.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pauses_insert.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pauses_insert.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pauses_insert.setObjectName("pauses_insert")
        self.first_note_info = QtWidgets.QTextEdit(self.basic_settings)
        self.first_note_info.setGeometry(QtCore.QRect(20, 170, 171, 31))
        self.first_note_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.first_note_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.first_note_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.first_note_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.first_note_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.first_note_info.setObjectName("first_note_info")
        self.last_note_info = QtWidgets.QTextEdit(self.basic_settings)
        self.last_note_info.setGeometry(QtCore.QRect(20, 220, 171, 31))
        self.last_note_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.last_note_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.last_note_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.last_note_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.last_note_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.last_note_info.setObjectName("last_note_info")
        self.ambitus_low_info = QtWidgets.QTextEdit(self.basic_settings)
        self.ambitus_low_info.setGeometry(QtCore.QRect(20, 270, 171, 31))
        self.ambitus_low_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ambitus_low_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.ambitus_low_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ambitus_low_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ambitus_low_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.ambitus_low_info.setObjectName("ambitus_low_info")
        self.ambitus_high_info = QtWidgets.QTextEdit(self.basic_settings)
        self.ambitus_high_info.setGeometry(QtCore.QRect(20, 320, 171, 31))
        self.ambitus_high_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ambitus_high_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.ambitus_high_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ambitus_high_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ambitus_high_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.ambitus_high_info.setObjectName("ambitus_high_info")
        self.line = QtWidgets.QFrame(self.basic_settings)
        self.line.setGeometry(QtCore.QRect(-13, 0, 431, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.basic_settings)
        self.line_2.setGeometry(QtCore.QRect(0, 50, 401, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.basic_settings)
        self.line_3.setGeometry(QtCore.QRect(0, 100, 401, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.basic_settings)
        self.line_4.setGeometry(QtCore.QRect(0, 150, 401, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.basic_settings)
        self.line_5.setGeometry(QtCore.QRect(0, 200, 401, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.basic_settings)
        self.line_6.setGeometry(QtCore.QRect(0, 250, 411, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(self.basic_settings)
        self.line_7.setGeometry(QtCore.QRect(0, 300, 411, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self.basic_settings)
        self.line_8.setGeometry(QtCore.QRect(0, 350, 421, 20))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.note_first_input = QtWidgets.QComboBox(self.basic_settings)
        self.note_first_input.setGeometry(QtCore.QRect(200, 170, 41, 31))
        self.note_first_input.setObjectName("note_first_input")
        self.note_first_input.addItem("")
        self.note_first_input.addItem("")
        self.note_first_input.addItem("")
        self.note_first_input.addItem("")
        self.note_first_input.addItem("")
        self.note_first_input.addItem("")
        self.note_first_input.addItem("")
        self.scale_first_note_input = QtWidgets.QComboBox(self.basic_settings)
        self.scale_first_note_input.setGeometry(QtCore.QRect(250, 170, 121, 31))
        self.scale_first_note_input.setObjectName("scale_first_note_input")
        self.scale_first_note_input.addItem("")
        self.scale_first_note_input.addItem("")
        self.scale_first_note_input.addItem("")
        self.scale_first_note_input.addItem("")
        self.note_last_input = QtWidgets.QComboBox(self.basic_settings)
        self.note_last_input.setGeometry(QtCore.QRect(200, 220, 41, 31))
        self.note_last_input.setObjectName("note_last_input")
        self.note_last_input.addItem("")
        self.note_last_input.addItem("")
        self.note_last_input.addItem("")
        self.note_last_input.addItem("")
        self.note_last_input.addItem("")
        self.note_last_input.addItem("")
        self.note_last_input.addItem("")
        self.scale_last_note_input = QtWidgets.QComboBox(self.basic_settings)
        self.scale_last_note_input.setGeometry(QtCore.QRect(250, 220, 121, 31))
        self.scale_last_note_input.setObjectName("scale_last_note_input")
        self.scale_last_note_input.addItem("")
        self.scale_last_note_input.addItem("")
        self.scale_last_note_input.addItem("")
        self.scale_last_note_input.addItem("")
        self.note_lower_ambitus_input = QtWidgets.QComboBox(self.basic_settings)
        self.note_lower_ambitus_input.setGeometry(QtCore.QRect(200, 270, 41, 31))
        self.note_lower_ambitus_input.setObjectName("note_lower_ambitus_input")
        self.note_lower_ambitus_input.addItem("")
        self.note_lower_ambitus_input.addItem("")
        self.note_lower_ambitus_input.addItem("")
        self.note_lower_ambitus_input.addItem("")
        self.note_lower_ambitus_input.addItem("")
        self.note_lower_ambitus_input.addItem("")
        self.note_lower_ambitus_input.addItem("")
        self.scale_lower_ambitus_input = QtWidgets.QComboBox(self.basic_settings)
        self.scale_lower_ambitus_input.setGeometry(QtCore.QRect(250, 270, 121, 31))
        self.scale_lower_ambitus_input.setObjectName("scale_lower_ambitus_input")
        self.scale_lower_ambitus_input.addItem("")
        self.scale_lower_ambitus_input.addItem("")
        self.scale_lower_ambitus_input.addItem("")
        self.scale_lower_ambitus_input.addItem("")
        self.note_higher_ambitus_input = QtWidgets.QComboBox(self.basic_settings)
        self.note_higher_ambitus_input.setGeometry(QtCore.QRect(200, 320, 41, 31))
        self.note_higher_ambitus_input.setObjectName("note_higher_ambitus_input")
        self.note_higher_ambitus_input.addItem("")
        self.note_higher_ambitus_input.addItem("")
        self.note_higher_ambitus_input.addItem("")
        self.note_higher_ambitus_input.addItem("")
        self.note_higher_ambitus_input.addItem("")
        self.note_higher_ambitus_input.addItem("")
        self.note_higher_ambitus_input.addItem("")
        self.scale_higher_ambitus_input = QtWidgets.QComboBox(self.basic_settings)
        self.scale_higher_ambitus_input.setGeometry(QtCore.QRect(250, 320, 121, 31))
        self.scale_higher_ambitus_input.setObjectName("scale_higher_ambitus_input")
        self.scale_higher_ambitus_input.addItem("")
        self.scale_higher_ambitus_input.addItem("")
        self.scale_higher_ambitus_input.addItem("")
        self.scale_higher_ambitus_input.addItem("")
        self.melody_type_info = QtWidgets.QTextEdit(self.basic_settings)
        self.melody_type_info.setGeometry(QtCore.QRect(20, 370, 171, 31))
        self.melody_type_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.melody_type_info.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.melody_type_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.melody_type_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.melody_type_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.melody_type_info.setObjectName("melody_type_info")
        self.melody_type_input = QtWidgets.QComboBox(self.basic_settings)
        self.melody_type_input.setGeometry(QtCore.QRect(200, 370, 171, 31))
        self.melody_type_input.setObjectName("melody_type_input")
        self.melody_type_input.addItem("")
        self.melody_type_input.addItem("")
        self.melody_type_input.addItem("")
        self.line_9 = QtWidgets.QFrame(self.basic_settings)
        self.line_9.setGeometry(QtCore.QRect(0, -20, 20, 451))
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.line_10 = QtWidgets.QFrame(self.basic_settings)
        self.line_10.setGeometry(QtCore.QRect(0, 400, 401, 20))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.line_11 = QtWidgets.QFrame(self.basic_settings)
        self.line_11.setGeometry(QtCore.QRect(370, -20, 20, 451))
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.metrum_insert.raise_()
        self.metrum_info.raise_()
        self.metrum_div.raise_()
        self.tacts_info.raise_()
        self.tacts_insert.raise_()
        self.pauses_info.raise_()
        self.pauses_insert.raise_()
        self.first_note_info.raise_()
        self.last_note_info.raise_()
        self.ambitus_low_info.raise_()
        self.ambitus_high_info.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
        self.line_4.raise_()
        self.line_5.raise_()
        self.line_6.raise_()
        self.line_7.raise_()
        self.line_8.raise_()
        self.note_first_input.raise_()
        self.scale_first_note_input.raise_()
        self.note_last_input.raise_()
        self.scale_last_note_input.raise_()
        self.note_lower_ambitus_input.raise_()
        self.scale_lower_ambitus_input.raise_()
        self.note_higher_ambitus_input.raise_()
        self.scale_higher_ambitus_input.raise_()
        self.melody_type_info.raise_()
        self.melody_type_input.raise_()
        self.line_9.raise_()
        self.line_10.raise_()
        self.line_11.raise_()
        self.settings_tabs.addTab(self.basic_settings, "")
        self.Interval_settings = QtWidgets.QWidget()
        self.Interval_settings.setObjectName("Interval_settings")
        self.input_4 = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_4.setGeometry(QtCore.QRect(100, 330, 42, 31))
        self.input_4.setMaximum(100000)
        self.input_4.setProperty("value", 1)
        self.input_4.setObjectName("input_4")
        self.input_1 = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_1.setGeometry(QtCore.QRect(100, 30, 42, 31))
        self.input_1.setMaximum(10000)
        self.input_1.setProperty("value", 1)
        self.input_1.setObjectName("input_1")
        self.input_6m = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_6m.setGeometry(QtCore.QRect(290, 90, 42, 31))
        self.input_6m.setMaximum(100000)
        self.input_6m.setProperty("value", 1)
        self.input_6m.setObjectName("input_6m")
        self.input_7w = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_7w.setGeometry(QtCore.QRect(290, 271, 42, 31))
        self.input_7w.setMaximum(100000)
        self.input_7w.setProperty("value", 1)
        self.input_7w.setObjectName("input_7w")
        self.input_5 = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_5.setGeometry(QtCore.QRect(290, 30, 42, 31))
        self.input_5.setMaximum(100000)
        self.input_5.setProperty("value", 1)
        self.input_5.setObjectName("input_5")
        self.input_2m = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_2m.setGeometry(QtCore.QRect(100, 90, 42, 31))
        self.input_2m.setMaximum(100000)
        self.input_2m.setProperty("value", 1)
        self.input_2m.setObjectName("input_2m")
        self.input_3w = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_3w.setGeometry(QtCore.QRect(100, 270, 42, 31))
        self.input_3w.setMaximum(100000)
        self.input_3w.setProperty("value", 1)
        self.input_3w.setObjectName("input_3w")
        self.input_2w = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_2w.setGeometry(QtCore.QRect(100, 150, 42, 31))
        self.input_2w.setMaximum(100000)
        self.input_2w.setProperty("value", 1)
        self.input_2w.setObjectName("input_2w")
        self.input_3m = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_3m.setGeometry(QtCore.QRect(100, 210, 42, 31))
        self.input_3m.setMaximum(100000)
        self.input_3m.setProperty("value", 1)
        self.input_3m.setObjectName("input_3m")
        self.input_7m = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_7m.setGeometry(QtCore.QRect(290, 211, 42, 31))
        self.input_7m.setMaximum(100000)
        self.input_7m.setProperty("value", 1)
        self.input_7m.setObjectName("input_7m")
        self.input_8 = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_8.setGeometry(QtCore.QRect(290, 331, 42, 31))
        self.input_8.setMaximum(100000)
        self.input_8.setProperty("value", 1)
        self.input_8.setObjectName("input_8")
        self.input_6w = QtWidgets.QSpinBox(self.Interval_settings)
        self.input_6w.setGeometry(QtCore.QRect(290, 151, 42, 31))
        self.input_6w.setMaximum(100000)
        self.input_6w.setProperty("value", 1)
        self.input_6w.setObjectName("input_6w")
        self._info = QtWidgets.QTextEdit(self.Interval_settings)
        self._info.setGeometry(QtCore.QRect(60, 30, 31, 31))
        self._info.setFrameShadow(QtWidgets.QFrame.Raised)
        self._info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._info.setReadOnly(True)
        self._info.setObjectName("_info")
        self.info_2m = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_2m.setGeometry(QtCore.QRect(60, 90, 31, 31))
        self.info_2m.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_2m.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_2m.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_2m.setReadOnly(True)
        self.info_2m.setObjectName("info_2m")
        self.info_3m = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_3m.setGeometry(QtCore.QRect(60, 210, 31, 31))
        self.info_3m.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_3m.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_3m.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_3m.setReadOnly(True)
        self.info_3m.setObjectName("info_3m")
        self.info_2w = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_2w.setGeometry(QtCore.QRect(60, 150, 31, 31))
        self.info_2w.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_2w.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_2w.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_2w.setReadOnly(True)
        self.info_2w.setObjectName("info_2w")
        self.info_4 = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_4.setGeometry(QtCore.QRect(60, 330, 31, 31))
        self.info_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_4.setReadOnly(True)
        self.info_4.setObjectName("info_4")
        self.info_6m = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_6m.setGeometry(QtCore.QRect(250, 90, 31, 31))
        self.info_6m.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_6m.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_6m.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_6m.setReadOnly(True)
        self.info_6m.setObjectName("info_6m")
        self.info_5 = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_5.setGeometry(QtCore.QRect(250, 30, 31, 31))
        self.info_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_5.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_5.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_5.setReadOnly(True)
        self.info_5.setObjectName("info_5")
        self.info_3w = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_3w.setGeometry(QtCore.QRect(60, 270, 31, 31))
        self.info_3w.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_3w.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_3w.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_3w.setReadOnly(True)
        self.info_3w.setObjectName("info_3w")
        self.info_7 = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_7.setGeometry(QtCore.QRect(250, 210, 31, 31))
        self.info_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_7.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_7.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_7.setReadOnly(True)
        self.info_7.setObjectName("info_7")
        self.info_8 = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_8.setGeometry(QtCore.QRect(250, 330, 31, 31))
        self.info_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_8.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_8.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_8.setReadOnly(True)
        self.info_8.setObjectName("info_8")
        self.info_7w = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_7w.setGeometry(QtCore.QRect(250, 270, 31, 31))
        self.info_7w.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_7w.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_7w.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_7w.setReadOnly(True)
        self.info_7w.setObjectName("info_7w")
        self.info_6w = QtWidgets.QTextEdit(self.Interval_settings)
        self.info_6w.setGeometry(QtCore.QRect(250, 150, 31, 31))
        self.info_6w.setFrameShadow(QtWidgets.QFrame.Raised)
        self.info_6w.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_6w.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info_6w.setReadOnly(True)
        self.info_6w.setObjectName("info_6w")
        self.line_17 = QtWidgets.QFrame(self.Interval_settings)
        self.line_17.setGeometry(QtCore.QRect(-30, 0, 441, 20))
        self.line_17.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.line_18 = QtWidgets.QFrame(self.Interval_settings)
        self.line_18.setGeometry(QtCore.QRect(-50, 400, 461, 20))
        self.line_18.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_18.setObjectName("line_18")
        self.line_19 = QtWidgets.QFrame(self.Interval_settings)
        self.line_19.setGeometry(QtCore.QRect(0, -30, 20, 481))
        self.line_19.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.line_20 = QtWidgets.QFrame(self.Interval_settings)
        self.line_20.setGeometry(QtCore.QRect(370, -30, 20, 481))
        self.line_20.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.line_21 = QtWidgets.QFrame(self.Interval_settings)
        self.line_21.setGeometry(QtCore.QRect(0, 60, 441, 20))
        self.line_21.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.line_22 = QtWidgets.QFrame(self.Interval_settings)
        self.line_22.setGeometry(QtCore.QRect(-10, 120, 441, 20))
        self.line_22.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.line_23 = QtWidgets.QFrame(self.Interval_settings)
        self.line_23.setGeometry(QtCore.QRect(0, 180, 441, 20))
        self.line_23.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.line_24 = QtWidgets.QFrame(self.Interval_settings)
        self.line_24.setGeometry(QtCore.QRect(-10, 240, 441, 20))
        self.line_24.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_24.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_24.setObjectName("line_24")
        self.line_25 = QtWidgets.QFrame(self.Interval_settings)
        self.line_25.setGeometry(QtCore.QRect(-10, 300, 441, 20))
        self.line_25.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_25.setObjectName("line_25")
        self.line_26 = QtWidgets.QFrame(self.Interval_settings)
        self.line_26.setGeometry(QtCore.QRect(-10, 390, 461, 20))
        self.line_26.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_26.setObjectName("line_26")
        self.line_27 = QtWidgets.QFrame(self.Interval_settings)
        self.line_27.setGeometry(QtCore.QRect(-20, 380, 461, 20))
        self.line_27.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_27.setObjectName("line_27")
        self.line_28 = QtWidgets.QFrame(self.Interval_settings)
        self.line_28.setGeometry(QtCore.QRect(-10, 370, 461, 20))
        self.line_28.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_28.setObjectName("line_28")
        self.line_29 = QtWidgets.QFrame(self.Interval_settings)
        self.line_29.setGeometry(QtCore.QRect(-10, 360, 461, 20))
        self.line_29.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_29.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_29.setObjectName("line_29")
        self.line_30 = QtWidgets.QFrame(self.Interval_settings)
        self.line_30.setGeometry(QtCore.QRect(10, -20, 20, 481))
        self.line_30.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_30.setObjectName("line_30")
        self.line_31 = QtWidgets.QFrame(self.Interval_settings)
        self.line_31.setGeometry(QtCore.QRect(360, -40, 20, 481))
        self.line_31.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_31.setObjectName("line_31")
        self.line_32 = QtWidgets.QFrame(self.Interval_settings)
        self.line_32.setGeometry(QtCore.QRect(180, -10, 20, 481))
        self.line_32.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_32.setObjectName("line_32")
        self.line_33 = QtWidgets.QFrame(self.Interval_settings)
        self.line_33.setGeometry(QtCore.QRect(190, -20, 20, 481))
        self.line_33.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_33.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_33.setObjectName("line_33")
        self.settings_tabs.addTab(self.Interval_settings, "")
        self.generate_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_button.setGeometry(QtCore.QRect(420, 550, 201, 21))
        self.generate_button.setObjectName("generate_button")
        self.command_line_window = QtWidgets.QTextEdit(self.centralwidget)
        self.command_line_window.setEnabled(True)
        self.command_line_window.setGeometry(QtCore.QRect(20, 10, 591, 81))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.command_line_window.setFont(font)
        self.command_line_window.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.command_line_window.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.command_line_window.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.command_line_window.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.command_line_window.setObjectName("command_line_window")
        self.line_12 = QtWidgets.QFrame(self.centralwidget)
        self.line_12.setGeometry(QtCore.QRect(10, 540, 20, 91))
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.line_13 = QtWidgets.QFrame(self.centralwidget)
        self.line_13.setGeometry(QtCore.QRect(380, 540, 20, 91))
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.line_14 = QtWidgets.QFrame(self.centralwidget)
        self.line_14.setGeometry(QtCore.QRect(410, 530, 241, 16))
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.line_15 = QtWidgets.QFrame(self.centralwidget)
        self.line_15.setGeometry(QtCore.QRect(410, 130, 241, 16))
        self.line_15.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.line_16 = QtWidgets.QFrame(self.centralwidget)
        self.line_16.setGeometry(QtCore.QRect(380, 90, 20, 31))
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.settings_tabs.setCurrentIndex(0)
        self.note_higher_ambitus_input.setCurrentIndex(6)
        self.scale_higher_ambitus_input.setCurrentIndex(3)
        self.pauses_insert.textChanged.connect(MainWindow.change_likelihood_pauses)  # type: ignore
        self.tacts_insert.textChanged.connect(MainWindow.change_tacts)  # type: ignore
        self.metrum_insert.textChanged.connect(MainWindow.change_metrum)  # type: ignore
        self.generate_button.clicked.connect(MainWindow.generate_music)  # type: ignore
        self.note_first_input.currentTextChanged['QString'].connect(MainWindow.change_first_note)  # type: ignore
        self.scale_first_note_input.currentTextChanged['QString'].connect(MainWindow.change_first_note)  # type: ignore
        self.note_last_input.currentTextChanged['QString'].connect(MainWindow.change_last_note)  # type: ignore
        self.scale_last_note_input.currentTextChanged['QString'].connect(MainWindow.change_last_note)  # type: ignore
        self.note_lower_ambitus_input.currentTextChanged['QString'].connect(
            MainWindow.change_lower_border)  # type: ignore
        self.scale_lower_ambitus_input.currentTextChanged['QString'].connect(
            MainWindow.change_lower_border)  # type: ignore
        self.note_higher_ambitus_input.currentTextChanged['QString'].connect(
            MainWindow.change_higher_border)  # type: ignore
        self.scale_higher_ambitus_input.currentTextChanged['QString'].connect(
            MainWindow.change_higher_border)  # type: ignore
        self.melody_type_input.currentTextChanged['QString'].connect(MainWindow.change_melody_type)  # type: ignore
        self.input_1.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_2m.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_2w.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_3m.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_3w.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_4.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_5.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_6m.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_6w.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_7m.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_7w.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        self.input_8.valueChanged['int'].connect(MainWindow.change_interval_likelihood)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.metrum_info.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">Requested metrum (n/4)</span></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-style:italic;\"><br /></p></body></html>"))
        self.metrum_insert.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">1</span></p></body></html>"))
        self.metrum_div.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                           "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">/4</span></p></body></html>"))
        self.tacts_info.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                           "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">Number of tacts</span></p></body></html>"))
        self.tacts_insert.setHtml(_translate("MainWindow",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">1</span></p></body></html>"))
        self.pauses_info.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">Likelihood of pauses [%]</span></p>\n"
                                            "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-style:italic;\"><br /></p></body></html>"))
        self.pauses_insert.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">10</span></p></body></html>"))
        self.first_note_info.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">Requested first note</span></p></body></html>"))
        self.last_note_info.setHtml(_translate("MainWindow",
                                               "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                               "p, li { white-space: pre-wrap; }\n"
                                               "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                               "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">Requested last note</span></p>\n"
                                               "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-style:italic;\"><br /></p></body></html>"))
        self.ambitus_low_info.setHtml(_translate("MainWindow",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                                 "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-style:italic;\">Lower border of ambitus</span></p>\n"
                                                 "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt; font-style:italic;\"><br /></p>\n"
                                                 "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt; font-style:italic;\"><br /></p>\n"
                                                 "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt; font-style:italic;\"><br /></p>\n"
                                                 "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt; font-style:italic;\"><br /></p></body></html>"))
        self.ambitus_high_info.setHtml(_translate("MainWindow",
                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "p, li { white-space: pre-wrap; }\n"
                                                  "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                                  "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-style:italic;\">Higher border of ambitus</span></p></body></html>"))
        self.note_first_input.setItemText(0, _translate("MainWindow", "C"))
        self.note_first_input.setItemText(1, _translate("MainWindow", "D"))
        self.note_first_input.setItemText(2, _translate("MainWindow", "E"))
        self.note_first_input.setItemText(3, _translate("MainWindow", "F"))
        self.note_first_input.setItemText(4, _translate("MainWindow", "G"))
        self.note_first_input.setItemText(5, _translate("MainWindow", "A"))
        self.note_first_input.setItemText(6, _translate("MainWindow", "B"))
        self.scale_first_note_input.setItemText(0, _translate("MainWindow", "Wielkie"))
        self.scale_first_note_input.setItemText(1, _translate("MainWindow", "Małe"))
        self.scale_first_note_input.setItemText(2, _translate("MainWindow", "Razkreślne"))
        self.scale_first_note_input.setItemText(3, _translate("MainWindow", "Dwukreślne"))
        self.note_last_input.setItemText(0, _translate("MainWindow", "C"))
        self.note_last_input.setItemText(1, _translate("MainWindow", "D"))
        self.note_last_input.setItemText(2, _translate("MainWindow", "E"))
        self.note_last_input.setItemText(3, _translate("MainWindow", "F"))
        self.note_last_input.setItemText(4, _translate("MainWindow", "G"))
        self.note_last_input.setItemText(5, _translate("MainWindow", "A"))
        self.note_last_input.setItemText(6, _translate("MainWindow", "B"))
        self.scale_last_note_input.setItemText(0, _translate("MainWindow", "Wielkie"))
        self.scale_last_note_input.setItemText(1, _translate("MainWindow", "Małe"))
        self.scale_last_note_input.setItemText(2, _translate("MainWindow", "Razkreślne"))
        self.scale_last_note_input.setItemText(3, _translate("MainWindow", "Dwukreślne"))
        self.note_lower_ambitus_input.setItemText(0, _translate("MainWindow", "C"))
        self.note_lower_ambitus_input.setItemText(1, _translate("MainWindow", "D"))
        self.note_lower_ambitus_input.setItemText(2, _translate("MainWindow", "E"))
        self.note_lower_ambitus_input.setItemText(3, _translate("MainWindow", "F"))
        self.note_lower_ambitus_input.setItemText(4, _translate("MainWindow", "G"))
        self.note_lower_ambitus_input.setItemText(5, _translate("MainWindow", "A"))
        self.note_lower_ambitus_input.setItemText(6, _translate("MainWindow", "B"))
        self.scale_lower_ambitus_input.setItemText(0, _translate("MainWindow", "Wielkie"))
        self.scale_lower_ambitus_input.setItemText(1, _translate("MainWindow", "Małe"))
        self.scale_lower_ambitus_input.setItemText(2, _translate("MainWindow", "Razkreślne"))
        self.scale_lower_ambitus_input.setItemText(3, _translate("MainWindow", "Dwukreślne"))
        self.note_higher_ambitus_input.setItemText(0, _translate("MainWindow", "C"))
        self.note_higher_ambitus_input.setItemText(1, _translate("MainWindow", "D"))
        self.note_higher_ambitus_input.setItemText(2, _translate("MainWindow", "E"))
        self.note_higher_ambitus_input.setItemText(3, _translate("MainWindow", "F"))
        self.note_higher_ambitus_input.setItemText(4, _translate("MainWindow", "G"))
        self.note_higher_ambitus_input.setItemText(5, _translate("MainWindow", "A"))
        self.note_higher_ambitus_input.setItemText(6, _translate("MainWindow", "B"))
        self.scale_higher_ambitus_input.setItemText(0, _translate("MainWindow", "Wielkie"))
        self.scale_higher_ambitus_input.setItemText(1, _translate("MainWindow", "Małe"))
        self.scale_higher_ambitus_input.setItemText(2, _translate("MainWindow", "Razkreślne"))
        self.scale_higher_ambitus_input.setItemText(3, _translate("MainWindow", "Dwukreślne"))
        self.melody_type_info.setHtml(_translate("MainWindow",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                                 "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-style:italic;\">Melody Type</span></p>\n"
                                                 "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt; font-style:italic;\"><br /></p></body></html>"))
        self.melody_type_input.setItemText(0, _translate("MainWindow", "Atonic"))
        self.melody_type_input.setItemText(1, _translate("MainWindow", "Chromatic"))
        self.melody_type_input.setItemText(2, _translate("MainWindow", "Random"))
        self.settings_tabs.setTabText(self.settings_tabs.indexOf(self.basic_settings),
                                      _translate("MainWindow", "Basic_Settings"))
        self._info.setHtml(_translate("MainWindow",
                                      "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                      "p, li { white-space: pre-wrap; }\n"
                                      "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                      "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">1</span></p></body></html>"))
        self.info_2m.setHtml(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">2&gt;</span></p></body></html>"))
        self.info_3m.setHtml(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">3&gt;</span></p></body></html>"))
        self.info_2w.setHtml(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">2&lt;</span></p></body></html>"))
        self.info_4.setHtml(_translate("MainWindow",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">4</span></p></body></html>"))
        self.info_6m.setHtml(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">6&lt;</span></p></body></html>"))
        self.info_5.setHtml(_translate("MainWindow",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">5</span></p></body></html>"))
        self.info_3w.setHtml(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">3&lt;</span></p></body></html>"))
        self.info_7.setHtml(_translate("MainWindow",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">7</span></p></body></html>"))
        self.info_8.setHtml(_translate("MainWindow",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                       "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">8</span></p></body></html>"))
        self.info_7w.setHtml(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">7&lt;</span></p></body></html>"))
        self.info_6w.setHtml(_translate("MainWindow",
                                        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-style:italic;\">6&gt;</span></p></body></html>"))
        self.settings_tabs.setTabText(self.settings_tabs.indexOf(self.Interval_settings),
                                      _translate("MainWindow", "Interval_settings"))
        self.generate_button.setText(_translate("MainWindow", "Generate"))
        self.command_line_window.setHtml(_translate("MainWindow",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:600; font-style:italic;\">\n"
                                                    "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\';\">Welcome in the program for basic, algorithmic music generation !</span></p></body></html>"))
