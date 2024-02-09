# pylint: disable=line-too-long,missing-docstring
import unittest
from src.music.music import NoteAccidental, NoteName
from src.musicxml.notes import (
    Note,
    Pitch,
    Unpitched,
    Rest,
    NoteType,
    Beam,
    BeamType,
    TieType,
    Lyric,
    Syllabic,
    Measure,
    Attributes,
    Clef,
    ClefSign,
    Barline,
    BarLocation,
    BarStyle,
    Part,
    ScorePartwise,
)


class TestNote(unittest.TestCase):
    def setUp(self):
        self.pitch = Pitch(NoteName.G, 4)
        self.unpitched = Unpitched(display_step=NoteName.C, display_octave=4)
        self.rest = Rest()

        self.note_pitch = Note(
            first_position=self.pitch,
            ties=[TieType.START],
            voice=1,
            note_type=NoteType.QUARTER,
            dots=2,
            accidental=NoteAccidental.NATURAL,
            beam=[Beam(1, BeamType.BEGIN)],
            lyric=Lyric("twink", first_syllabic=Syllabic.BEGIN),
        )
        self.note_mid = Note(
            first_position=Pitch(NoteName.C, 4),
            ties=[TieType.START, TieType.STOP],
            note_type=NoteType.QUARTER,
            beam=[Beam(1, BeamType.CONTINUE), Beam(2, BeamType.BEGIN)],
            lyric=Lyric("le", first_syllabic=Syllabic.END),
        )

    def test_to_musicxml(self):
        self.assertEqual(
            self.note_pitch.to_musicxml(),
            """<note><pitch><step>G</step><octave>4</octave></pitch><tie type='start'/><voice>1</voice><type>quarter</type><dot/><dot/><beam number="1">begin</beam><lyric><syllabic>begin</syllabic><text>twink</text></lyric></note>""",
        )
        self.assertEqual(
            self.note_mid.to_musicxml(),
            """<note><pitch><step>C</step><octave>4</octave></pitch><tie type='start'/><tie type='stop'/><type>quarter</type><beam number="1">continue</beam><beam number="2">begin</beam><lyric><syllabic>end</syllabic><text>le</text></lyric></note>""",
        )

class TestMeasure(unittest.TestCase):
    def setUp(self):
        self.note = Note(
            first_position=Pitch(NoteName.C, 4),
            ties=[TieType.START, TieType.STOP],
            note_type=NoteType.QUARTER,
            lyric=Lyric("twink", first_syllabic=Syllabic.BEGIN),
        )
        self.other_note = Note(
            first_position=Pitch(NoteName.G, 4),
            lyric=Lyric("le", first_syllabic=Syllabic.END),
        )
        self.measure = Measure(1, [self.note, self.other_note])
        self.special_measure = Measure(
            1,
            [self.note, self.other_note],
            attributes=Attributes(1, 0, 4, 4, Clef(ClefSign.TREBLE)),
            barline=Barline(BarLocation.RIGHT, BarStyle.HEAVY_HEAVY),
        )

    def test_to_musicxml(self):
        self.assertEqual(
            self.measure.to_musicxml(),
            """<measure number="1"><note><pitch><step>C</step><octave>4</octave></pitch><tie type='start'/><tie type='stop'/><type>quarter</type><lyric><syllabic>begin</syllabic><text>twink</text></lyric></note><note><pitch><step>G</step><octave>4</octave></pitch><lyric><syllabic>end</syllabic><text>le</text></lyric></note></measure>""",
        )

    def test_special_measure(self):
        self.assertEqual(
            self.special_measure.to_musicxml(),
            """<measure number="1"><attributes><divisions>1</divisions><key><fifths>0</fifths></key><time><beats>4</beats><beat-type>4</beat-type></time><clef><sign>G</sign><line>2</line></clef></attributes><note><pitch><step>C</step><octave>4</octave></pitch><tie type='start'/><tie type='stop'/><type>quarter</type><lyric><syllabic>begin</syllabic><text>twink</text></lyric></note><note><pitch><step>G</step><octave>4</octave></pitch><lyric><syllabic>end</syllabic><text>le</text></lyric></note><barline location="right"><bar-style>heavy-heavy</bar-style></barline></measure>""",
        )


class TestScorePartwise(unittest.TestCase):
    def setUp(self):
        self.measure = Measure(
            1, [Note(Pitch(NoteName.C, 4), accidental=NoteAccidental.SHARP)]
        )
        self.part = Part(ident="P1", name="Music", measures=[self.measure])
        self.score_partwise = ScorePartwise([self.part])

    def test_to_musicxml(self):
        self.assertEqual(
            self.score_partwise.to_musicxml(),
            """<score-partwise version="4.0"><part-list><score-part id="P1"><part-name>Music</part-name></score-part></part-list><part id="P1"><measure number="1"><note><pitch><step>C</step><octave>4</octave></pitch><accidental>sharp</accidental></note></measure></part></score-partwise>""",
        )


if __name__ == "__main__":
    unittest.main()
