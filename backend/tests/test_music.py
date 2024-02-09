# pylint: disable=line-too-long,missing-docstring
import unittest

from src.music.music import Note, NoteName, Scale, ScaleType
from src.music.notes import *


class TestNote(unittest.TestCase):
    def setUp(self):
        self.note = C

    def test_get_next_note_name(self):
        next_note = self.note.get_next_note_name()

        self.assertEqual(next_note, NoteName.D)
        self.assertEqual(Note(NoteName.G).get_next_note_name(), NoteName.A)

    def test_get_root_note(self):
        self.assertEqual(self.note.get_root_note(), self.note)
        self.assertEqual(F_DOUBLE_SHARP.get_root_note(), G)
        self.assertEqual(D_FLAT.get_root_note(), C_SHARP)
        self.assertEqual(E_SHARP.get_root_note(), F)

    def test_get_note_n_steps_away(self):
        self.assertEqual(self.note.get_note_n_steps_away(1), C_SHARP)
        self.assertEqual(self.note.get_note_n_steps_away(2), D)
        self.assertEqual(self.note.get_note_n_steps_away(7), G)
        self.assertEqual(self.note.get_note_n_steps_away(8), G_SHARP)
        self.assertEqual(self.note.get_note_n_steps_away(9), A)
        self.assertEqual(self.note.get_note_n_steps_away(12), C)

    def test_copy(self):
        copy = self.note.copy()
        self.assertEqual(copy, self.note)
        self.assertEqual(copy, C)
        self.assertEqual(copy.note_name, self.note.note_name)
        self.assertEqual(copy.accidental, self.note.accidental)

    def test_str(self):
        self.assertEqual(str(self.note), "C")
        self.assertEqual(str(C_SHARP), "C#")
        self.assertEqual(str(D_FLAT), "Db")
        self.assertEqual(str(F_DOUBLE_SHARP), "Fx")
        self.assertEqual(str(E_SHARP), "E#")
        self.assertEqual(str(B_SHARP), "B#")
        self.assertEqual(str(G_FLAT), "Gb")

    def test_eq(self):
        self.assertEqual(self.note, C)
        self.assertEqual(self.note, Note(NoteName.C))
        self.assertEqual(self.note, B_SHARP)
        self.assertEqual(self.note, B_SHARP.get_root_note())


        self.assertNotEqual(self.note, D)
        self.assertNotEqual(self.note, C_SHARP)
        self.assertNotEqual(self.note, E_FLAT)
        self.assertNotEqual(self.note, G_FLAT)

        self.assertEqual(F_DOUBLE_SHARP, G)
        self.assertEqual(D_FLAT, C_SHARP)

class TestScale(unittest.TestCase):
    def setUp(self):
        self.scale = Scale(C)
        self.other_scale = Scale(G_SHARP)
        self.aoelion = Scale(A, scale_type=ScaleType.AEOLIAN)

    def test_get_scale_formula(self):
        self.assertEqual(self.scale.get_scale_formula(), [0, 2, 2, 1, 2, 2, 2])
        self.assertEqual(self.other_scale.get_scale_formula(), [0, 2, 2, 1, 2, 2, 2])
        self.assertEqual(self.aoelion.get_scale_formula(), [0, 2, 1, 2, 2, 1, 2])

    def test_get_scale_formula_cumulative(self):
        self.assertEqual(self.scale.get_scale_formula_cum_sum(), [0, 2, 4, 5, 7, 9, 11])
        self.assertEqual(self.other_scale.get_scale_formula_cum_sum(), [0, 2, 4, 5, 7, 9, 11])
        self.assertEqual(self.aoelion.get_scale_formula_cum_sum(), [0, 2, 3, 5, 7, 8, 10])

    def test_get_scale_note_ordering(self):
        self.assertEqual(self.scale.get_scale_note_ordering(), [C, C_SHARP, D, D_SHARP, E, F, F_SHARP, G, G_SHARP, A, A_SHARP, B])
        self.assertEqual(self.other_scale.get_scale_note_ordering(), [G_SHARP, A, A_SHARP, B, C, C_SHARP, D, D_SHARP, E, F, F_SHARP, G])

    def test_get_basic_scale(self):
        self.assertEqual(self.scale.get_basic_scale(), [C, D, E, F, G, A, B])
        self.assertEqual(self.other_scale.get_basic_scale(), [G_SHARP, A_SHARP, C, C_SHARP, D_SHARP, F, G])

    def test_get_scale(self):
        self.assertEqual(self.scale.get_scale(), [C, D, E, F, G, A, B])
        self.assertEqual(self.other_scale.get_scale(), [G_SHARP, A_SHARP, B_SHARP, C_SHARP, D_SHARP, E_SHARP, F_DOUBLE_SHARP])
        self.assertEqual(Scale(C_SHARP).get_scale(), [C_SHARP, D_SHARP, E_SHARP, F_SHARP, G_SHARP, A_SHARP, B_SHARP])

    def test_get_transpose(self):
        self.assertEqual(self.scale.get_transpose(self.other_scale), {
            C: G_SHARP,
            D: A_SHARP,
            E: B_SHARP,
            F: C_SHARP,
            G: D_SHARP,
            A: E_SHARP,
            B: F_DOUBLE_SHARP,
        })

        self.assertEqual(self.scale.get_transpose(Scale(G)), {
            C: G,
            D: A,
            E: B,
            F: C,
            G: D,
            A: E,
            B: F_SHARP,
        })

    def test_transpose_notes_from(self):
        self.assertEqual(self.scale.transpose_notes_from(Scale(G), [C, G, C_SHARP]), [F, C, F_SHARP])
