# Current version updated to basic ligature

import os
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from music_informations import music_informations

def __init__(self):
    self.music_info = music_informations()

def generate_music(self):
    # Multiply by 4 because of calculations on quarter-notes
    points_to_use = (self.music_info.metrum * self.music_info.tacts) * 4
    tact_space = self.music_info.metrum * 4

    file_name = "test"
    text_file = open(file_name + ".ly", 'w')
    text_file.write(self.music_info.template + "{\n")
    text_file.write(self.music_info.number_tacts + "\n")
    text_file.write(chr(92) + "time " + str(self.music_info.metrum) + "/4 ")

    while points_to_use > 0:
        note_or_pause = random.randint(0, 100)

        if tact_space <= 0:
            tact_space = self.music_info.metrum * 4

        if note_or_pause <= self.music_info.pauses_likelihood:
            index = random.randint(0, 4)
            if points_to_use >= self.music_info.rest_durations_weights[index] and tact_space >= \
                    self.music_info.rest_durations_weights[index]:
                self.music_info.melody.append(
                    self.music_info.full_scale[28] + self.music_info.rest_durations[index])
                points_to_use -= self.music_info.rest_durations_weights[index]
                tact_space -= self.music_info.rest_durations_weights[index]
        else:
            index = random.randint(0, 11)
            note_highness = random.randint(0, 27)
            is_ligature = random.randint(0, 100)
            if points_to_use >= self.music_info.durations_weights[index] and tact_space >= \
                    self.music_info.durations_weights[index]:
                if is_ligature > 40:
                    self.music_info.melody.append(
                        self.music_info.full_scale[note_highness] + self.music_info.durations[index] + "~ ")
                else:
                    self.music_info.melody.append(
                        self.music_info.full_scale[note_highness] + self.music_info.durations[index])
                points_to_use -= self.music_info.durations_weights[index]
                tact_space -= self.music_info.durations_weights[index]
            else:
                pass

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
