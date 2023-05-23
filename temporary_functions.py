# Main GUI window file created with help of PyQt5 Designer

# Issue:
#   - First note must be in ambitus in case to program work properly
#   - Likelihood on 0 level works not good enough
#   - Last note is not included in ambitus

import os
import random
import numpy

from PyQt5 import QtCore, QtGui, QtWidgets
from music_informations import music_informations


class Ui_MainWindow(object):
    def __init__(self):
        self.music_info = music_informations()

    def generate_music(self):
        # Initial values - scores for certain parts
        # Multiply by 4 because of calculations on quarter-notes
        # Calculation of score that is available in certain melody
        points_to_use = (self.music_info.metrum * self.music_info.tacts) * 4
        # Tact points used to control tact notes
        tact_space = self.music_info.metrum * 4
        # Storage for used durations of notes - used in replacing notes and pauses
        used_durations = []
        # Value used to draw sharp or be-mol notation in "Chromatic" mode
        is_bemol = random.randint(0, 100)
        # Value for controlling clef - Treble = True - Bass = False
        clef = True

        # Score for first initial note
        first_note_score = self.music_info.scale_sound_score[
            self.music_info.scale_sound.index(self.music_info.first_note[0])]
        if self.scale_first_note_input.currentText() == "Wielkie":
            pass
        elif self.scale_first_note_input.currentText() == "Małe":
            first_note_score += 7
        elif self.scale_first_note_input.currentText() == "Razkreślne":
            first_note_score += 14
        elif self.scale_first_note_input.currentText() == "Dwukreślne":
            first_note_score += 21

        # Calculation of score range dependent on lower border of ambitus
        lower_score = int(self.music_info.scale_sound.index(self.music_info.lower_ambitus[0])) + 1
        if self.scale_lower_ambitus_input.currentText() == "Wielkie":
            pass
        elif self.scale_lower_ambitus_input.currentText() == "Małe":
            lower_score += 7
        elif self.scale_lower_ambitus_input.currentText() == "Razkreślne":
            lower_score += 14
        elif self.scale_lower_ambitus_input.currentText() == "Dwukreślne":
            lower_score += 21

        # Calculation of score range dependent on higher border of ambitus
        higher_score = int(self.music_info.scale_sound.index(self.music_info.higher_ambitus[0])) + 1
        if self.scale_higher_ambitus_input.currentText() == "Wielkie":
            pass
        elif self.scale_higher_ambitus_input.currentText() == "Małe":
            higher_score += 7
        elif self.scale_higher_ambitus_input.currentText() == "Razkreślne":
            higher_score += 14
        elif self.scale_higher_ambitus_input.currentText() == "Dwukreślne":
            higher_score += 21

        # Setting up current note as first one for initial conditions
        current_note = first_note_score

        # Scale score range calculated above
        scale_range = [lower_score, higher_score]

        # Beginning of writing to file - template + metrum
        file_name = "test"
        text_file = open(file_name + ".ly", 'w')
        text_file.write(self.music_info.template + "{\n")
        text_file.write(self.music_info.number_tacts + "\n")
        text_file.write(chr(92) + "time " + str(self.music_info.metrum) + "/4 ")

        # Control for first iteration
        first_iteration = True

        # Loop for creating music
        while points_to_use > 0:
            # Drawing value for decision if next element will be note or pause
            note_or_pause = random.randint(0, 100)

            # Checking tact space (in case of 0 - ending tact and writing new one)
            if tact_space <= 0:
                tact_space = self.music_info.metrum * 4

            # Drawing value for duration of note
            index = random.randint(0, 11)

            if first_iteration:
                # Writing first note selected in GUI
                self.music_info.melody.append(self.music_info.first_note + self.music_info.durations[index])
                # Scheme is constructed to verify whole score for melody, small score for tacts and verifying them through array with used durations
                points_to_use -= self.music_info.durations_weights[index]
                tact_space -= self.music_info.durations_weights[index]
                used_durations.append(self.music_info.durations[index])
                first_iteration = False
            elif note_or_pause <= self.music_info.pauses_likelihood:
                # If for writing pauses - likelihood is controlled through movable border of condition above
                # Picking up pause duration
                index = random.randint(0, 4)
                # Checking if pause can be inserted in tact and melody
                if points_to_use >= self.music_info.rest_durations_weights[index] and tact_space >= \
                        self.music_info.rest_durations_weights[index]:
                    self.music_info.melody.append(
                        "r" + self.music_info.rest_durations[index])
                    # Veryfing score
                    points_to_use -= self.music_info.rest_durations_weights[index]
                    tact_space -= self.music_info.rest_durations_weights[index]
                    used_durations.append(self.music_info.rest_durations[index])
            else:
                # Else write classic note - note_highness_score controlled with ambitus score calculated at start
                note_highness_score = random.randint(scale_range[0], scale_range[1])
                # Drawing if note chosen above, have chance for ligature
                is_ligature = random.randint(0, 100)

                # Init for likelihoods
                val_1 = 0
                val_2m = 0
                val_2w = 0
                val_3m = 0
                val_3w = 0
                val_4 = 0
                val_4zm = 0
                val_5 = 0
                val_6m = 0
                val_6w = 0
                val_7m = 0
                val_7w = 0
                val_8 = 0

                # First option for Atonic music
                if self.music_info.melody_type == "Atonic":
                    # Grabbing information about interval probabilities - halftones are disabled
                    # System works similar to pauses likelihood
                    # 0 - is disabled
                    # 1<= - is active, the higher the value, the higher probability
                    # Drawing number for every interval - the highest score wins
                    if self.input_1.value() == 0:
                        val_1 = 0
                    else:
                        val_1 = random.randint(1, self.input_1.value())
                    val_2m = 0
                    if self.input_2w.value() == 0:
                        val_2w = 0
                    else:
                        val_2w = random.randint(1, self.input_2w.value())
                    val_3m = 0
                    if self.input_3w.value() == 0:
                        val_3w = 0
                    else:
                        val_3w = random.randint(1, self.input_3w.value())
                    val_4 = 0
                    if self.input_4zm.value() == 0:
                        val4zm = 0
                    else:
                        val4zm = random.randint(1, self.input_4zm.value())
                    val_5 = 0
                    if self.input_6m.value() == 0:
                        val_6m = 0
                    else:
                        val_6m = random.randint(1, self.input_6m.value())
                    val_6w = 0
                    if self.input_7m.value() == 0:
                        val_7m = 0
                    else:
                        val_7m = random.randint(1, self.input_7m.value())
                    val_7w = 0
                    if self.input_8.value() == 0:
                        val_8 = 0
                    else:
                        val_8 = random.randint(1, self.input_8.value())
                # Same algorithm for "Chromatic" and "Random" modes - with halftones
                elif self.music_info.melody_type == "Chromatic" or self.music_info.melody_type == "Random":
                    if self.input_1.value() == 0:
                        val_1 = 0
                    else:
                        val_1 = random.randint(1, self.input_1.value())
                    if self.input_2m.value() == 0:
                        val_2m = 0
                    else:
                        val_2m = random.randint(1, self.input_2m.value())
                    if self.input_2w.value() == 0:
                        val_2w = 0
                    else:
                        val_2w = random.randint(1, self.input_2w.value())
                    if self.input_3m.value() == 0:
                        val_3m = 0
                    else:
                        val_3m = random.randint(1, self.input_3m.value())
                    if self.input_3w.value() == 0:
                        val_3w = 0
                    else:
                        val_3w = random.randint(1, self.input_3w.value())
                    if self.input_4.value() == 0:
                        val_4 = 0
                    else:
                        val_4 = random.randint(1, self.input_4.value())
                    if self.input_4zm.value() == 0:
                        val_4zm = 0
                    else:
                        val_4zm = random.randint(1, self.input_4zm.value())
                    if self.input_5.value() == 0:
                        val_5 = 0
                    else:
                        val_5 = random.randint(1, self.input_5.value())
                    if self.input_6m.value() == 0:
                        val_6m = 0
                    else:
                        val_6m = random.randint(1, self.input_6m.value())
                    if self.input_6w.value() == 0:
                        val_6w = 0
                    else:
                        val_6w = random.randint(1, self.input_6w.value())
                    if self.input_7m.value() == 0:
                        val_7m = 0
                    else:
                        val_7m = random.randint(1, self.input_7m.value())
                    if self.input_7w.value() == 0:
                        val_7w = 0
                    else:
                        val_7w = random.randint(1, self.input_7w.value())
                    if self.input_8.value() == 0:
                        val_8 = 0
                    else:
                        val_8 = random.randint(1, self.input_8.value())

                # Array with likelihood scores
                interval_likelihoods = numpy.array(
                    [val_1, val_2m, val_2w, val_3m, val_3w, val_4, val_4zm, val_5, val_6m, val_6w, val_7m, val_7w,
                     val_8])

                # Searching for maximum in likelihood array
                maximum = interval_likelihoods.max()

                # Extracting index of maximum
                where_max = numpy.where(interval_likelihoods == maximum)[0]

                # If there are equal scores - drawing for interval
                if len(where_max) != 1:
                    max_random = random.randint(0, len(where_max) - 1)
                    max_location = where_max[max_random]
                else:
                    max_location = where_max[0]

                # Extracting interval from pre-prepared array
                interval = self.music_info.interval[max_location]

                # Decision if the interval will be used to add or subtract halftones
                up_or_down = random.randint(0, 100)

                if up_or_down >= 50:
                    pass
                else:
                    interval = interval * -1

                # Creating temporary note for validation
                temporary_note = current_note + interval

                # Checking if note is in ambitus range - if not try the other way - if not pass
                positive = True
                if temporary_note < lower_score or temporary_note > higher_score:
                    interval = interval * -1
                    temporary_note = current_note + interval
                    if temporary_note < lower_score or temporary_note > higher_score:
                        positive = False
                    else:
                        current_note = temporary_note
                else:
                    current_note = temporary_note

                # If interval is possible current note if overwritten and operation note is used below
                operation_note = current_note

                # If note is in ambitus continue, else pass
                if positive is True:
                    # Deciding about halftones - Chromatic using only be-mol or sharp value - Random using all of them
                    halftone = ""
                    proper_scale = []
                    if self.music_info.melody_type == "Chromatic":
                        chromatic_sign = random.randint(0, 2)
                        if is_bemol >= 40:
                            proper_scale = self.music_info.chromatic_scale_end_lower
                        elif is_bemol < 40:
                            proper_scale = self.music_info.chromatic_scale_end_upper

                        # After drawing scale - assigning proper scale to connect good halftone
                        halftone = proper_scale[chromatic_sign]
                        # Special cases for a and e
                        if is_bemol >= 50:
                            if self.music_info.melody[-1][0] == "e" or self.music_info.melody[-1][
                                0] == "a" and chromatic_sign == 1:
                                halftone = "ses"
                            elif self.music_info.melody[-1][0] == "e" or self.music_info.melody[-1][
                                0] == "a" and chromatic_sign == 0:
                                halftone = "s"
                            else:
                                pass
                        else:
                            pass

                    # Construction of melody for random option with whole drawing for each note and halftone
                    # Likelihood of normal note is a little higher
                    # Special cases included
                    if self.music_info.melody_type == "Random":
                        if current_note % 1 == 0:
                            variant = random.randint(0, 120)
                            if variant <= 30 and operation_note != 1:
                                operation_note -= 1
                                halftone = "isis"
                            elif variant <= 90:
                                pass
                            elif variant <= 120 and operation_note != 28:
                                operation_note += 1
                                halftone = "eses"
                        elif current_note % 1 != 0:
                            variant = random.randint(0, 100)
                            if variant <= 50 and operation_note > 1:
                                operation_note -= 0.5
                                halftone = "is"
                            elif variant <= 100 and operation_note < 28:
                                operation_note += 0.5
                                halftone = "es"

                    # Proper construction of melody array - scoring points and assigning proper signs
                    decryption_note = ""
                    if self.music_info.melody_type == "Atonic":
                        if operation_note <= 7:
                            decryption_note = str(self.music_info.scale_sound[operation_note - 1]) + "," + \
                                              self.music_info.durations[index]
                        elif operation_note <= 14:
                            decryption_note = str(self.music_info.scale_sound[operation_note - 8]) + \
                                              self.music_info.durations[index]
                        elif operation_note <= 21:
                            decryption_note = str(self.music_info.scale_sound[operation_note - 15]) + "'" + \
                                              self.music_info.durations[index]
                        elif operation_note <= 28:
                            decryption_note = str(self.music_info.scale_sound[operation_note - 22]) + "''" + \
                                              self.music_info.durations[index]
                    # Random / Chromatic variant
                    elif self.music_info.melody_type == "Random" or self.music_info.melody_type == "Chromatic":
                        decryption_note = ""
                        if operation_note <= 7:
                            decryption_note = str(self.music_info.scale_sound[int(operation_note) - 1]) + str(
                                halftone) + "," + self.music_info.durations[index]
                        elif operation_note <= 14:
                            decryption_note = str(self.music_info.scale_sound[int(operation_note) - 8]) + str(
                                halftone) + \
                                              self.music_info.durations[index]
                        elif operation_note <= 21:
                            decryption_note = str(self.music_info.scale_sound[int(operation_note) - 15]) + str(
                                halftone) + "'" + self.music_info.durations[index]
                        elif operation_note <= 28:
                            decryption_note = str(self.music_info.scale_sound[int(operation_note) - 22]) + str(
                                halftone) + "''" + self.music_info.durations[index]

                    # Controlling clef - if note is too low - bass
                    if operation_note >= 14 and clef is False:
                        self.music_info.melody.append("\n" + chr(92) + "clef " + chr(32) + "treble" + chr(32) + "\n")
                        clef = True
                    elif operation_note < 14 and clef is True:
                        self.music_info.melody.append("\n" + chr(92) + "clef " + chr(32) + "bass" + chr(32) + "\n")
                        clef = False

                    # Finally ligature drawing or simple note with signs appending
                    if points_to_use >= self.music_info.durations_weights[index] and tact_space >= \
                            self.music_info.durations_weights[index]:
                        if is_ligature > 70:
                            self.music_info.melody.append(decryption_note + "~ ")
                        else:
                            self.music_info.melody.append(decryption_note)
                        # Scoring
                        points_to_use -= self.music_info.durations_weights[index]
                        tact_space -= self.music_info.durations_weights[index]
                        used_durations.append(self.music_info.durations[index])
                    else:
                        pass
                else:
                    pass

        # Substitution of last note
        self.music_info.melody[-1] = self.music_info.last_note + used_durations[0]

        # Writing melody
        for note in self.music_info.melody:
            text_file.write(note + " ")

        # Closing file and setting proper bars
        text_file.write("\n" + chr(92) + "bar " + chr(34) + "||" + chr(34) + "}")
        text_file.close()

        # Cleaning up the melody array for next active cases
        self.music_info.melody = []

        # Opening pdf with generated melody
        os.system("lilypond --pdf " + file_name + ".ly")
        os.system(file_name + ".pdf")

    # Below are written functions for controlling changes of values in GUI
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

        if scale == "Wielkie":
            self.music_info.lower_ambitus = note.lower() + ","
        elif scale == "Małe":
            self.music_info.lower_ambitus = note.lower()
        elif scale == "Razkreślne":
            self.music_info.lower_ambitus = note.lower() + "'"
        elif scale == "Dwukreślne":
            self.music_info.lower_ambitus = note.lower() + "''"

        print(self.music_info.lower_ambitus)

    def change_higher_border(self):
        note = self.note_higher_ambitus_input.currentText()
        scale = self.scale_higher_ambitus_input.currentText()

        if scale == "Wielkie":
            self.music_info.higher_ambitus = note.lower() + ","
        elif scale == "Małe":
            self.music_info.higher_ambitus = note.lower()
        elif scale == "Razkreślne":
            self.music_info.higher_ambitus = note.lower() + "'"
        elif scale == "Dwukreślne":
            self.music_info.higher_ambitus = note.lower() + "''"

    def change_interval_likelihood(self):
        self.music_info.how_much_1 = self.input_1.value()
        self.music_info.how_much_2m = self.input_2m.value()
        self.music_info.how_much_2w = self.input_2w.value()
        self.music_info.how_much_3m = self.input_3m.value()
        self.music_info.how_much_3w = self.input_3w.value()
        self.music_info.how_much_4 = self.input_4.value()
        self.music_info.how_much_4zm = self.input_4zm.value()
        self.music_info.how_much_5 = self.input_5.value()
        self.music_info.how_much_6m = self.input_6m.value()
        self.music_info.how_much_6w = self.input_6w.value()
        self.music_info.how_much_7m = self.input_7m.value()
        self.music_info.how_much_7w = self.input_7w.value()
        self.music_info.how_much_8 = self.input_8.value()

    def change_melody_type(self):
        self.music_info.melody_type = self.melody_type_input.currentText()
