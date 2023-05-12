class music_informations():
    melody = []
    tacts = 0
    metrum = 0
    title = "Default"
    subtitle = "Default"
    number_tacts ="\override Score.BarNumber.break-visibility = ##(#t #t #t) \n" \
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