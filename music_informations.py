class music_informations():
    melody = []
    first_note = "c,"
    last_note = "c,"
    lower_ambitus = "c,"
    higher_ambitus = "b''"
    tacts = 1
    metrum = 1
    pauses_likelihood = 10
    melody_type = "Atonic"

    how_much_1 = 1
    how_much_2m = 1
    how_much_2w = 1
    how_much_3m = 1
    how_much_3w = 1
    how_much_4 = 1
    how_much_4zm = 1
    how_much_5 = 1
    how_much_6m = 1
    how_much_6w = 1
    how_much_7m = 1
    how_much_7w = 1
    how_much_8 = 1

    interval = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]

    title = "Default"
    subtitle = "Default"

    full_scale = ["c,", "d,", "e,", "f,", "g,", "a,", "b,", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'",
                  "f'", "g'", "a'", "b'",
                  "c''", "d''", "e''", "f''", "g''", "a''", "b''", "r"]

    scale_sound = ["c", "d", "e", "f", "g", "a", "b"]
    scale_sound_score = [1, 2, 3, 4, 5, 6, 7, 0]

    chromatic_scale_end_upper = ["is", "isis", ""]
    chromatic_scale_end_lower = ["es", "eses", ""]
    chromatic_scale_end_score = [0.5, 1]

    scale_number = [",", "", "'", "''"]
    scale_number_score = [0, 7, 14, 21]

    durations = ["16", "8", "8.", "4", "4.", "4..", "2", "2.", "2..", "1", "1.", "1.."]

    durations_weights = [1, 2, 3, 4, 6, 7, 8, 12, 14, 16, 24, 28]

    rest_durations = ["16", "8", "4", "2", "1"]

    rest_durations_weights = [1, 2, 4, 8, 16]

    number_tacts = "\override Score.BarNumber.break-visibility = ##(#f #t #t) \n" \
                   "\set Score.currentBarNumber = #1 \n" \
                   "" + chr(92) + "bar " + chr(34) + chr(34) + "\n"

    template = chr(92) + "version " + chr(34) + "2.22.2" + chr(34) + "\n" \
                "\header{ \n" \
                "title = " + title + "\n" \
                "subtitle = " + subtitle + "\n" \
                "} \n" \
                "\layout { \n" \
                "indent = 0\in \n" \
                "ragged-last = ##f \n" \
                "\context { \n" \
                "} \n" \
                "} \n"
