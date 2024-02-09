"""
Contains constants that will be used constantly
"""

from src.music.music import Note, NoteName, NoteAccidental

# Base notes
C = Note(NoteName.C)
C_SHARP = Note(NoteName.C, NoteAccidental.SHARP)
D = Note(NoteName.D)
D_SHARP = Note(NoteName.D, NoteAccidental.SHARP)
E = Note(NoteName.E)
F = Note(NoteName.F)
F_SHARP = Note(NoteName.F, NoteAccidental.SHARP)
G = Note(NoteName.G)
G_SHARP = Note(NoteName.G, NoteAccidental.SHARP)
A = Note(NoteName.A)
A_SHARP = Note(NoteName.A, NoteAccidental.SHARP)
B = Note(NoteName.B)

# Common flats
D_FLAT = Note(NoteName.D, NoteAccidental.FLAT)
E_FLAT = Note(NoteName.E, NoteAccidental.FLAT)
G_FLAT = Note(NoteName.G, NoteAccidental.FLAT)
A_FLAT = Note(NoteName.A, NoteAccidental.FLAT)
B_FLAT = Note(NoteName.B, NoteAccidental.FLAT)

# Double sharps
C_DOUBLE_SHARP = Note(NoteName.C, NoteAccidental.DOUBLE_SHARP)
F_DOUBLE_SHARP = Note(NoteName.F, NoteAccidental.DOUBLE_SHARP)

# Other sharps
E_SHARP = Note(NoteName.E, NoteAccidental.SHARP)
B_SHARP = Note(NoteName.B, NoteAccidental.SHARP)
