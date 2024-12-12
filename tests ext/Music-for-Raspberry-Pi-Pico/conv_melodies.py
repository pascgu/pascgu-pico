from melodies import *  # import melodies.py
from notes import *     # import notes.py


conv_notes = {
"REST": "silence",
"NOTE_B0": "si_-1",
"NOTE_C1": "do_0",
"NOTE_CS1": "do#_0",
"NOTE_D1": "re_0",
"NOTE_DS1": "re#_0",
"NOTE_E1": "mi_0",
"NOTE_F1": "fa_0",
"NOTE_FS1": "fa#_0",
"NOTE_G1": "sol_0",
"NOTE_GS1": "sol#_0",
"NOTE_A1": "la_0",
"NOTE_AS1": "la#_0",
"NOTE_B1": "si_0",
"NOTE_C2": "do_1",
"NOTE_CS2": "do#_1",
"NOTE_D2": "re_1",
"NOTE_DS2": "re#_1",
"NOTE_E2": "mi_1",
"NOTE_F2": "fa_1",
"NOTE_FS2": "fa#_1",
"NOTE_G2": "sol_1",
"NOTE_GS2": "sol#_1",
"NOTE_A2": "la_1",
"NOTE_AS2": "la#_1",
"NOTE_B2": "si_1",
"NOTE_C3": "do_2",
"NOTE_CS3": "do#_2",
"NOTE_D3": "re_2",
"NOTE_DS3": "re#_2",
"NOTE_E3": "mi_2",
"NOTE_F3": "fa_2",
"NOTE_FS3": "fa#_2",
"NOTE_G3": "sol_2",
"NOTE_GS3": "sol#_2",
"NOTE_A3": "la_2",
"NOTE_AS3": "la#_2",
"NOTE_B3": "si_2",
"NOTE_C4": "do_3",
"NOTE_CS4": "do#_3",
"NOTE_D4": "re_3",
"NOTE_DS4": "re#_3",
"NOTE_E4": "mi_3",
"NOTE_F4": "fa_3",
"NOTE_FS4": "fa#_3",
"NOTE_G4": "sol_3",
"NOTE_GS4": "sol#_3",
"NOTE_A4": "la_3",
"NOTE_AS4": "la#_3",
"NOTE_B4": "si_3",
"NOTE_C5": "do_4",
"NOTE_CS5": "do#_4",
"NOTE_D5": "re_4",
"NOTE_DS5": "re#_4",
"NOTE_E5": "mi_4",
"NOTE_F5": "fa_4",
"NOTE_FS5": "fa#_4",
"NOTE_G5": "sol_4",
"NOTE_GS5": "sol#_4",
"NOTE_A5": "la_4",
"NOTE_AS5": "la#_4",
"NOTE_B5": "si_4",
"NOTE_C6": "do_5",
"NOTE_CS6": "do#_5",
"NOTE_D6": "re_5",
"NOTE_DS6": "re#_5",
"NOTE_E6": "mi_5",
"NOTE_F6": "fa_5",
"NOTE_FS6": "fa#_5",
"NOTE_G6": "sol_5",
"NOTE_GS6": "sol#_5",
"NOTE_A6": "la_5",
"NOTE_AS6": "la#_5",
"NOTE_B6": "si_5",
"NOTE_C7": "do_6",
"NOTE_CS7": "do#_6",
"NOTE_D7": "re_6",
"NOTE_DS7": "re#_6",
"NOTE_E7": "mi_6",
"NOTE_F7": "fa_6",
"NOTE_FS7": "fa#_6",
"NOTE_G7": "sol_6",
"NOTE_GS7": "sol#_6",
"NOTE_A7": "la_6",
"NOTE_AS7": "la#_6",
"NOTE_B7": "si_6",
"NOTE_C8": "do_7",
"NOTE_CS8": "do#_7",
"NOTE_D8": "re_7",
"NOTE_DS8": "re#_7"
}


# temps des notes
D = 0.25 # double croche
C = 0.5 # croche
Cpt = 0.75 # croche pointée
N = 1 # noire
Npt = 1.5 # noire pointée
B = 2 # blanche
Bpt = 3 # blanche pointée
R = 4 # ronde
Rpt = 6 # ronde pointée

conv_t = {
    "4": "N",
    "-4": "Npt",
    "8": "B",
    "-8": "Bpt",
    "16": "R",
    "-16": "Rpt",
    "2": "C",
    "1": "D"
}
conv_t = {
    "4": "N",
    "04": "N",
    "-4": "Npt",
    "8": "C",
    "-8": "Cpt",
    "16": "D",
    "-16": "Dpt",
    "32": "T",
    "-32": "Tpt",
    "2": "B",
    "-2": "Bpt",
    "1": "R",
    "-1": "Rpt"
}

for i,mel in enumerate(melody):
    #if i!=6: continue #TEMP
    titre = mel[0]
    titre = titre.replace('ü','u')
    name = titre
    name = name.replace(' ','_')
    for c in "()'\"-,":
        name = name.replace(c,'')
    name = name.replace('__','_')
    titre = titre.replace("'","\\'")
    tempo = mel[1]
    print(f"{name} = {{'titre':'{titre}', 'tempo':{tempo},")
    print(f"    'notes':[ ", end='')
    for note,t in zip(mel[2::2],mel[3::2]):
        if not note in conv_notes:
            raise ValueError(f"note {note} unknown")
        if not t in conv_t:
            raise ValueError(f"t {t} unknown")
        new_note = conv_notes[note]
        new_t = conv_t[t]
        print(f"('{new_note}',{new_t}),", end='')
    print("] }")