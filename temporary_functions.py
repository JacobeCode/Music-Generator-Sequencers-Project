import os
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from music_informations import music_informations


class Ui_MainWindow(object):
    def __init__(self):
        self.music_info = music_informations()

    def generate_music(self):
        # Multiply by 4 because of calculations on quarter-notes
        points_to_use = (self.music_info.metrum * self.music_info.tacts) * 4
        tact_space = self.music_info.metrum * 4
        used_durations = []

        is_bemol = random.randint(0, 100)

        scale_range = [self.music_info.full_scale.index(self.music_info.lower_ambitus), self.music_info.full_scale.index(self.music_info.higher_ambitus)]

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
                    used_durations.append(self.music_info.rest_durations[index])
            else:
                index = random.randint(0, 11)
                note_highness = random.randint(scale_range[0], scale_range[1])
                is_ligature = random.randint(0, 100)

                val_1 = random.randint(0, self.music_info.how_much_1)
                val_2m = random.randint(0, self.music_info.how_much_2m)
                val_2w = random.randint(0, self.music_info.how_much_2w)
                val_3m = random.randint(0, self.music_info.how_much_3m)
                val_3w = random.randint(0, self.music_info.how_much_3w)
                val_4 = random.randint(0, self.music_info.how_much_4)
                val_5 = random.randint(0, self.music_info.how_much_5)
                val_6m = random.randint(0, self.music_info.how_much_6m)
                val_6w = random.randint(0, self.music_info.how_much_6w)
                val_7m = random.randint(0, self.music_info.how_much_7m)
                val_7w = random.randint(0, self.music_info.how_much_7w)
                val_8 = random.randint(0, self.music_info.how_much_8)

                interval_likelihoods = [val_1, val_2m, val_2w, val_3m, val_3w, val_4, val_5, val_6m, val_6w, val_7m, val_7w, val_8]

                where_max = interval_likelihoods.index(max(interval_likelihoods))

                if len(where_max) != 1:
                    max_random = random.randint(0, len(where_max))
                    where_max = where_max[max_random]
                else:
                    pass

                interval =

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
                    used_durations.append(self.music_info.durations[index])
                    if self.music_info.melody_type == "Chromatic":

                        halftones = random.randint(0, 2)
                        if is_bemol >= 50:
                            proper_scale = self.music_info.chromatic_scale_end_lower
                        elif is_bemol < 50:
                            proper_scale = self.music_info.chromatic_scale_end_upper

                        note_to_assign = proper_scale[halftones]
                        if is_bemol >= 50:
                            if self.music_info.melody[-1][0] == "e" or self.music_info.melody[-1][0] == "a" and halftones == 1:
                                note_to_assign = "ses"
                            elif self.music_info.melody[-1][0] == "e" or self.music_info.melody[-1][0] == "a" and halftones == 0:
                                note_to_assign = "s"
                            else:
                                pass
                        else:
                            pass

                        if len(self.music_info.melody[-1]) <= 2:
                            self.music_info.melody[-1] = self.music_info.melody[-1][0] + note_to_assign + \
                                                         used_durations[-1]
                        elif self.music_info.melody[-1][2] == "'":
                            self.music_info.melody[-1] = self.music_info.melody[-1][0] + note_to_assign + \
                                                         self.music_info.melody[-1][1] + self.music_info.melody[-1][2] + used_durations[-1]
                        elif self.music_info.melody[-1][1] == "'":
                            self.music_info.melody[-1] = self.music_info.melody[-1][0] + note_to_assign + \
                                                         self.music_info.melody[-1][1] + used_durations[-1]
                        else:
                            self.music_info.melody[-1] = self.music_info.melody[-1][0] + note_to_assign + used_durations[-1]
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
