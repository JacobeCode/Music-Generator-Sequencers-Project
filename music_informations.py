class music_informations():
    melody = []
    tacts = 0
    metrum = 0
    pauses_likelihood = 0

    title = "Default"
    subtitle = "Default"

    full_scale = ["c,", "d,", "e,", "f,", "g,", "a,", "b,", "c", "d", "e", "f", "g", "a", "b", "c'", "d'", "e'",
                  "f'", "g'", "a'", "b'",
                  "c''", "d''", "e''", "f''", "g''", "a''", "b''", "r"]

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
