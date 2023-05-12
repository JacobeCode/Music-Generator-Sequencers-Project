import os

from PyQt5 import QtCore, QtGui, QtWidgets
from music_informations import music_informations

def __init__(self):
    self.music_info = music_informations()
def generate_music(self):
    file_name = "test"
    text_file = open(file_name + ".ly", 'w')
    text_file.write(self.music_info.template + "{\n")
    for note in self.music_info.melody:
        text_file.write(note + " ")
    text_file.write("}\n")
    text_file.close()
    os.system("lilypond --pdf " + file_name + ".ly")
    os.system(file_name + ".pdf")
def change_metrum(self):
    self.music_info.metrum = int(self.metrum_insert.toPlainText())
    print(str(self.music_info.metrum))

def change_tacts(self):
    self.music_info.tacts = int(self.tacts_insert.toPlainText())
    print(str(self.music_info.tacts))
