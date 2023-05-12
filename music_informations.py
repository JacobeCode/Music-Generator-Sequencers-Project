class music_informations():
    melody = []
    tacts = 0
    metrum = 0
    title = "Default"
    subtitle = "Default"
    template = chr(92) + "version " + chr(34) + "2.22.2" + chr(34) + "\n" \
                "\header{ \n" \
                "title = " + title + "\n" \
                "subtitle = " + subtitle + "\n" \
                "} \n" \
                "\layout { \n" \
                "indent = 0\in \n" \
                "ragged-last = ##f \n" \
                "\context { \n" \
                "\Score \n" \
                "" + chr(92) + "remove Bar_number_engraver \n" \
                "} \n" \
                "} \n"