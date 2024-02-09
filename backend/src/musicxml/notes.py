"""
The classes are for working with note-like structures in
musicxml. A note can be a pitch, an unpitched, or a rest.
"""

import os
from typing import Optional, Union
from src.music.music import NoteName, NoteType, NoteAccidental, NoteOrdering
from src.music.music import Scale as MusicalScale
from src.music.music import Note as MusicalNote
from src.musicxml.types import (
    BarLocation,
    BarStyle,
    ClefSign,
    TieType,
    StemType,
    BeamType,
    Syllabic,
)
import xml.etree.ElementTree as ET

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?><!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">"""


class Lyric:
    """
    Wrapper class for a lyric for a note from a musicxml file

    """

    def __init__(
        self,
        text: str,
        first_syllabic: Optional[Syllabic] = None,
        elision: Optional[str] = None,
        last_syllabic: Optional[Syllabic] = None,
        end_text: Optional[str] = None,
    ):
        self.text = text
        self.first_syllabic = first_syllabic
        self.elision = elision
        self.last_syllabic = last_syllabic
        self.end_text = end_text

    def to_musicxml(self):
        """
        Returns the content to a lyric in musicxml format

        Format:
          <lyric>
              <syllabic>single</syllabic>
              <text>text</text>
              <elision>elision</elision>
              <syllabic>end</syllabic>
              <text>end_text</text>
          </lyric>
        """
        if self.first_syllabic:
            first_syllabic = f"<syllabic>{self.first_syllabic.value}</syllabic>"
        else:
            first_syllabic = ""

        if self.elision:
            elision = f"<elision>{self.elision}</elision>"

        else:
            elision = ""

        if self.elision and self.last_syllabic:
            last_syllabic = f"<syllabic>{self.last_syllabic.value}</syllabic>"
        else:
            last_syllabic = ""

        if self.elision and self.end_text:
            end_text = f"<text>{self.end_text}</text>"
        else:
            end_text = ""

        return f"""<lyric>{first_syllabic}<text>{self.text}</text>{elision}{last_syllabic}{end_text}</lyric>"""

    def copy(self) -> "Lyric":
        """
        Returns a copy of this lyric
        """
        return Lyric(
            text=self.text,
            first_syllabic=self.first_syllabic,
            elision=self.elision,
            last_syllabic=self.last_syllabic,
            end_text=self.end_text,
        )


class Beam:
    """
    Wrapper class for a beam for a note from a musicxml file
    """

    def __init__(self, number: int, beam_type: BeamType):
        self.number = number
        self.beam_type = beam_type

    def to_musicxml(self):
        """
        Returns the content to a beam in musicxml format

        Format:
          <beam number="number">beam_type</beam>
        """
        return f"""<beam number="{self.number}">{self.beam_type.value}</beam>"""


class Pitch:
    """
    Wrapper class for a pitch for a note from a musicxml file
    """

    def __init__(self, step: NoteName, octave: int, alter: Optional[float] = None):
        self.step = step
        self.octave = octave
        self.alter = alter

    def to_musicxml(self):
        """
        Returns the content to a pitch in musicxml format

        Format:
          <pitch>
              <step>step</step>
              <alter>alter</alter>
              <octave>octave</octave>
          </pitch>
        """
        if self.alter:
            alter = f"<alter>{self.alter}</alter>"
        else:
            alter = ""

        return f"""<pitch><step>{self.step.name}</step>{alter}<octave>{self.octave}</octave></pitch>"""

    def copy(self) -> "Pitch":
        """
        Returns a copy of this pitch
        """
        return Pitch(step=self.step, octave=self.octave, alter=self.alter)

    def __repr__(self) -> str:
        return f"Pitch({self.step})"


class Unpitched:
    """
    Wrapper class for an unpitched for a note from a musicxml file
    """

    def __init__(
        self,
        display_step: Optional[NoteName] = None,
        display_octave: Optional[int] = None,
    ):
        self.display_step = display_step
        self.display_octave = display_octave

    def to_musicxml(self):
        """
        Returns the content to an unpitched in musicxml format

        Format:
          <unpitched>
              <display-step>display_step</display-step>
              <display-octave>display_octave</display-octave>
          </unpitched>
        """
        if self.display_step:
            display_step = f"<display-step>{self.display_step.value}</display-step>"
        else:
            display_step = ""

        if self.display_octave:
            display_octave = f"<display-octave>{self.display_octave}</display-octave>"
        else:
            display_octave = ""

        return f"""<unpitched>{display_step}{display_octave}</unpitched>"""

    def copy(self) -> "Unpitched":
        """
        Returns a copy of this unpitched
        """
        return Unpitched(
            display_step=self.display_step, display_octave=self.display_octave
        )


class Rest:
    """
    Wrapper class for a rest for a note from a musicxml file
    """

    def __init__(
        self,
        display_step: Optional[NoteName] = None,
        display_octave: Optional[int] = None,
    ):
        self.display_step = display_step
        self.display_octave = display_octave

    def to_musicxml(self):
        """
        Returns the content to a rest in musicxml format

        Format:
          <rest>
              <display-step>display_step</display-step>
              <display-octave>display_octave</display-octave>
          </rest>
        """
        if self.display_step:
            display_step = f"<display-step>{self.display_step.value}</display-step>"
        else:
            display_step = ""

        if self.display_octave:
            display_octave = f"<display-octave>{self.display_octave}</display-octave>"
        else:
            display_octave = ""

        return f"""<rest>{display_step}{display_octave}</rest>"""

    def copy(self) -> "Rest":
        """
        Returns a copy of this rest
        """
        return Rest(display_step=self.display_step, display_octave=self.display_octave)


class Note:
    """
    Wrapper class for a note from a musicxml file
    """

    def __init__(
        self,
        first_position: Union[Pitch, Unpitched, Rest],
        ties: Optional[list[TieType]] = None,  # stat
        instrument: Optional[str] = None,  # IDREF is using score-instrument
        footnote: Optional[str] = None,
        duration: Optional[int] = None,  # TODO
        level: Optional[str] = None,  # TODO
        voice: Optional[int] = None,
        note_type: Optional[NoteType] = None,
        dots: Optional[int] = None,
        accidental: Optional[NoteAccidental] = None,
        time_modification: Optional[str] = None,  # TODO
        stem: Optional[StemType] = None,
        notehead: Optional[str] = None,  # TODO
        notehead_text: Optional[str] = None,  # TODO
        staff: Optional[int] = None,  # for multi-stave parts
        beam: Optional[list[Beam]] = None,
        notations: Optional[str] = None,  # TODO
        lyric: Optional[Lyric] = None,
        play: Optional[str] = None,  # TODO
        listen: Optional[str] = None,  # TODO
    ):
        self.first_position = first_position
        self.ties = ties
        self.instrument = instrument
        self.footnote = footnote
        self.level = level
        self.voice = voice
        self.note_type = note_type
        self.dots = dots
        if accidental:
            self.accidental = accidental
        else:
            self.accidental = NoteAccidental.NATURAL
        self.time_modification = time_modification
        self.stem = stem
        self.notehead = notehead
        self.notehead_text = notehead_text
        self.staff = staff
        self.beam = beam
        self.notations = notations
        self.lyric = lyric
        self.play = play
        self.listen = listen
        self.duration = duration

    def to_musicxml(self):
        """
        Converts the note to musicxml format
        """

        if self.ties:
            ties = "".join([f"<tie type='{t.value}'/>" for t in self.ties])
        else:
            ties = ""

        if self.voice:
            voice = f"<voice>{self.voice}</voice>"
        else:
            voice = ""

        if self.duration is not None:
            duration = f"<duration>{self.duration}</duration>"
        else:
            duration = ""

        if self.note_type:
            note_type = f"<type>{self.note_type.value}</type>"
        else:
            note_type = ""

        if self.dots:
            dots = "".join(["<dot/>" for _ in range(self.dots)])
        else:
            dots = ""

        if (self.accidental) is None or self.accidental == NoteAccidental.NATURAL:
            accidental = ""
        else:
            accidental = f"<accidental>{self.accidental.value}</accidental>"

        if self.time_modification:
            time_modification = (
                f"<time-modification>{self.time_modification}</time-modification>"
            )
        else:
            time_modification = ""

        if self.stem:
            stem = f"<stem>{self.stem.value}</stem>"
        else:
            stem = ""

        if self.staff:
            staff = f"<staff>{self.staff}</staff>"
        else:
            staff = ""

        if self.beam:
            beam = "".join([b.to_musicxml() for b in self.beam])
        else:
            beam = ""

        if self.notations:
            notations = f"<notations>{self.notations}</notations>"
        else:
            notations = ""

        if self.lyric:
            lyric = self.lyric.to_musicxml()
        else:
            lyric = ""

        if self.play:
            play = f"<play>{self.play}</play>"
        else:
            play = ""

        if self.listen:
            listen = f"<listen>{self.listen}</listen>"
        else:
            listen = ""

        midsection_1 = (
            f"{ties}{voice}{duration}{note_type}{dots}{accidental}{time_modification}"
        )
        midsection_2 = f"{stem}{staff}{beam}{notations}{lyric}{play}{listen}"

        return f"""<note>{self.first_position.to_musicxml()}{midsection_1}{midsection_2}</note>"""

    def copy(self) -> "Note":
        """
        Returns a copy of this note
        """
        return Note(
            first_position=self.first_position.copy(),
            ties=self.ties,
            instrument=self.instrument,
            footnote=self.footnote,
            level=self.level,
            voice=self.voice,
            note_type=self.note_type,
            dots=self.dots,
            accidental=self.accidental,
            time_modification=self.time_modification,
            stem=self.stem,
            notehead=self.notehead,
            notehead_text=self.notehead_text,
            staff=self.staff,
            beam=self.beam.copy() if self.beam else None,
            notations=self.notations,
            lyric=self.lyric.copy() if self.lyric else None,
            play=self.play,
            listen=self.listen,
            duration=self.duration,
        )

    def __repr__(self) -> str:
        return f"XmlNote<{self.first_position}, {self.accidental}>"

    def __str__(self) -> str:
        return self.__repr__()


class Clef:
    """
    Wrapper class for a clef for a note from a musicxml file
    """

    def __init__(self, sign: ClefSign, octave_change: Optional[int] = None):
        self.sign = sign
        self.octave_change = octave_change

    def get_line_value(self):
        """
        Returns the line value for the clef
        """
        return {
            ClefSign.TREBLE: 2,
            ClefSign.BASS: 4,
            ClefSign.ALTO: 3,
            ClefSign.PERCUSSION: None,
        }[self.sign]

    def to_musicxml(self):
        """
        Converts the clef to musicxml format
        """
        octave_change = (
            f"<clef-octave-change>{self.octave_change}</clef-octave-change>"
            if self.octave_change
            else ""
        )
        line_value = self.get_line_value()
        if line_value is None:
            line = ""
        else:
            line = f"<line>{line_value}</line>"
        return f"""<clef><sign>{self.sign.value}</sign>{line}{octave_change}</clef>"""


class Attributes:
    """
    Wrapper class for attributes from a musicxml file
    """

    def __init__(
        self,
        divisions: int,
        key_fifths: int,
        beats: int,
        beat_type: int,
        clef: Optional[Clef],
    ):
        self.divisions = divisions
        self.key_fifths = key_fifths
        self.beats = beats
        self.beat_type = beat_type
        self.clef = clef

    def to_musicxml(self):
        """
        Converts the attributes to musicxml format
        """
        divisions = f"<divisions>{self.divisions}</divisions>"
        fifths = f"<key><fifths>{self.key_fifths}</fifths></key>"
        time = f"<time><beats>{self.beats}</beats><beat-type>{self.beat_type}</beat-type></time>"
        clef = self.clef.to_musicxml() if self.clef else ""
        return f"""<attributes>{divisions}{fifths}{time}{clef}</attributes>"""

    def copy(self) -> "Attributes":
        """
        Returns a copy of this attributes
        """
        return Attributes(
            divisions=self.divisions,
            key_fifths=self.key_fifths,
            beats=self.beats,
            beat_type=self.beat_type,
            clef=self.clef,
        )


class Barline:
    """
    Wrapper class for a barline from a musicxml file
    """

    def __init__(self, location: BarLocation, bar_style: BarStyle):
        self.location = location
        self.bar_style = bar_style

    def to_musicxml(self):
        """
        Converts the barline to musicxml format
        """
        return f"""<barline location="{self.location.value}"><bar-style>{self.bar_style.value}</bar-style></barline>"""

    def copy(self) -> "Barline":
        """
        Returns a copy of this barline
        """
        return Barline(location=self.location, bar_style=self.bar_style)


class Measure:
    """
    Wrapper class for a measure from a musicxml file. Only
    contains notes for now
    """

    def __init__(
        self,
        number: int,
        notes: list[Note],
        attributes: Optional[Attributes] = None,
        barline: Optional[Barline] = None,
    ):
        self.number = number
        self.notes = notes
        self.attributes = attributes
        self.barline = barline

    def to_musicxml(self):
        """
        Converts the measure to musicxml format

        Format:
            <measure number="number">
                <note>...</note>
                <note>...</note>
                ...
            </measure>
        """
        notes_xml = "".join([n.to_musicxml() for n in self.notes])
        attributes = self.attributes.to_musicxml() if self.attributes else ""
        barline = self.barline.to_musicxml() if self.barline else ""
        return f"""<measure number="{self.number}">{attributes}{notes_xml}{barline}</measure>"""

    def copy(self) -> "Measure":
        """
        Returns a copy of this measure
        """
        barline = (
            Barline(self.barline.location, self.barline.bar_style)
            if self.barline
            else None
        )
        return Measure(
            number=self.number,
            notes=[n.copy() for n in self.notes],
            attributes=self.attributes.copy() if self.attributes else None,
            barline=barline,
        )


class Part:
    """
    Wrapper class for a part from a musicxml file. Only
    """

    def __init__(self, ident: str, name: str, measures: list[Measure]):
        self.id = ident
        self.name = name
        self.measures = measures

    def to_musicxml(self):
        """
        Converts the part to musicxml format
        """
        measures_xml = "".join([m.to_musicxml() for m in self.measures])
        return f"""<part id="{self.id}">{measures_xml}</part>"""

    def copy(self) -> "Part":
        """
        Returns a copy of this part
        """
        return Part(
            ident=self.id,
            name=self.name,
            measures=[m.copy() for m in self.measures],
        )


class ScorePartwise:
    """
    Wrapper class for a score-partwise from a musicxml file.
    """

    def __init__(self, parts_list: list[Part]):
        self.parts_list = parts_list
        # self.key_fifths = key_fifths

    def to_musicxml(self):
        """
        Converts the score-partwise to musicxml format

        Format:
            <score-partwise>
                <part-list>
                    <score-part id="...">
                        <part-name>...</part-name>
                    </score-part>
                    <score-part id="...">
                        <part-name>...</part-name>
                    </score-part>
                    ...
                </part-list>
                <part id="...">...</part>
                <part id=>...</part>
                ...
            </score-partwise>
        """
        part_list_xml = "".join(
            [
                f"""<part-list><score-part id="{p.id}"><part-name>{p.name}</part-name></score-part></part-list>"""
                for p in self.parts_list
            ]
        )
        parts_xml = "".join([p.to_musicxml() for p in self.parts_list])
        return f"""<score-partwise version="4.0">{part_list_xml}{parts_xml}</score-partwise>"""

    @staticmethod
    def from_musicxml(file_path: str) -> "ScorePartwise":
        """
        Given a file path, returns a ScorePartwise object
        """
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ET.parse(file)
            root = tree.getroot()

            parts = []
            for part in root.findall("part"):
                measures = []
                for measure in part.findall("measure"):
                    notes = []
                    for note in measure.findall("note"):
                        first_position = note.find("pitch")
                        if first_position is None:
                            first_position = note.find("rest")
                            if first_position is None:
                                first_position = note.find("unpitched")
                        else:
                            first_position = Pitch(
                                step=NoteName[first_position.find("step").text],
                                octave=int(first_position.find("octave").text),
                            )
                        ties = note.find("tie")
                        if ties is not None:
                            ties = TieType[ties.get("type").upper()]
                        instrument = note.find("instrument")
                        if instrument is not None:
                            instrument = instrument.text
                        footnote = note.find("footnote")
                        if footnote is not None:
                            footnote = footnote.text
                        level = note.find("level")
                        if level is not None:
                            level = level.text
                        voice = note.find("voice")
                        if voice is not None:
                            voice = int(voice.text)
                        note_type = note.find("type")
                        if note_type is not None:
                            note_type = NoteType[note_type.text.upper()]
                        dots = note.findall("dot")
                        if dots is not None:
                            dots = len(dots)
                        duration = note.find("duration")

                        if duration is not None:
                            duration = int(duration.text)
                        accidental = note.find("accidental")

                        if accidental is not None:
                            accidental = NoteAccidental[accidental.text.upper()]
                        time_modification = note.find("time-modification")
                        if time_modification is not None:
                            time_modification = time_modification.text
                        stem = note.find("stem")
                        if stem is not None:
                            stem = StemType[stem.text.upper()]
                        notehead = note.find("notehead")
                        if notehead is not None:
                            notehead = notehead.text
                        notehead_text = note.find("notehead-text")
                        if notehead_text is not None:
                            notehead_text = notehead_text.text
                        staff = note.find("staff")
                        if staff is not None:
                            staff = int(staff.text)
                        beam = note.findall("beam")
                        if beam is not None:
                            beam = [
                                Beam(
                                    number=int(b.get("number")),
                                    beam_type=BeamType[b.text.upper()],
                                )
                                for b in beam
                            ]
                        notations = note.find("notations")
                        if notations is not None:
                            notations = notations.text

                        lyric = note.find("lyric")
                        if lyric is not None:
                            first_syllabic = lyric.find("syllabic")
                            if first_syllabic is not None:
                                first_syllabic = Syllabic[first_syllabic.text.upper()]
                            elision = lyric.find("elision")
                            if elision is not None:
                                elision = elision.text
                            last_syllabic = lyric.find("syllabic")
                            if last_syllabic is not None:
                                last_syllabic = Syllabic[last_syllabic.text.upper()]
                            end_text = lyric.find("text")
                            if end_text is not None:
                                end_text = end_text.text
                            lyric = Lyric(
                                text=lyric.find("text").text,
                                first_syllabic=first_syllabic,
                                elision=elision,
                                last_syllabic=last_syllabic,
                                end_text=end_text,
                            )

                        play = note.find("play")
                        if play is not None:
                            play = play.text
                        listen = note.find("listen")
                        if listen is not None:
                            listen = listen.text

                        attributes = measure.find("attributes")
                        if attributes is not None:
                            clef = attributes.find("clef")

                            if clef is not None:
                                octave_change = (
                                    int(clef.find("octave-change").text)
                                    if clef.find("octave-change") is not None
                                    else None
                                )
                                clef = Clef(
                                    sign=[
                                        c
                                        for c in ClefSign
                                        if c.value == clef.find("sign").text.upper()
                                    ][0],
                                    octave_change=octave_change,
                                )
                            attributes = Attributes(
                                divisions=int(attributes.find("divisions").text),
                                key_fifths=int(
                                    attributes.find("key").find("fifths").text
                                ),
                                beats=int(attributes.find("time").find("beats").text),
                                beat_type=int(
                                    attributes.find("time").find("beat-type").text
                                ),
                                clef=clef,
                            )

                        barline = measure.find("barline")
                        if barline is not None:
                            barstyle = barline.find("bar-style").text
                            location = BarLocation[barline.get("location").upper()]
                            bar_style = [b for b in BarStyle if b.value == barstyle][0]
                            barline = Barline(location=location, bar_style=bar_style)

                        note = Note(
                            first_position=first_position,
                            ties=ties,
                            instrument=instrument,
                            footnote=footnote,
                            level=level,
                            voice=voice,
                            duration=duration,
                            note_type=note_type,
                            dots=dots,
                            accidental=accidental,
                            time_modification=time_modification,
                            stem=stem,
                            notehead=notehead,
                            notehead_text=notehead_text,
                            staff=staff,
                            beam=beam,
                            notations=notations,
                            lyric=lyric,
                            play=play,
                            listen=listen,
                        )
                        notes.append(note)

                    measures.append(
                        Measure(
                            number=int(measure.get("number")),
                            notes=notes,
                            attributes=attributes,
                            barline=barline,
                        )
                    )

                score_parts = root.find("part-list").findall("score-part")
                part_name = ""
                for score_part in score_parts:
                    if (
                        score_part.get("id") == part.get("id")
                        and score_part.find("part-name") is not None
                    ):
                        part_name = score_part.find("part-name").text
                        break

                parts.append(
                    Part(
                        ident=part.get("id"),
                        name=part_name,
                        measures=measures,
                    )
                )

            return ScorePartwise(parts_list=parts)

    def copy(self) -> "ScorePartwise":
        """
        Returns a copy of this score-partwise
        """
        return ScorePartwise(parts_list=[p.copy() for p in self.parts_list])


class TransposerHelper:
    """
    Helper for extracting the information from musicxml files,
    and then transposing the notes
    """

    @staticmethod
    def get_scale_from_score(score: ScorePartwise) -> MusicalScale:
        """
        Returns the scale of the score
        """
        try:
            key_fifths = score.parts_list[0].measures[0].attributes.key_fifths
        except Exception:
            key_fifths = 0
        natural_order = NoteOrdering.get_default_order()
        return MusicalScale(natural_order[key_fifths % len(natural_order)])

    @staticmethod
    def get_scale_key_fifths(scale: MusicalScale) -> int:
        """
        Returns the numbers of fifths from c for a scale
        """
        home_note = scale.start_note
        natural_order = NoteOrdering.get_default_order()
        return natural_order.index(home_note)

    @staticmethod
    def convert_notes(notes: list[Note]) -> list[MusicalNote]:
        """
        Converts a musicxml note into a musical note
        """
        new_notes: list[MusicalNote] = []

        for xml_note in notes:
            accidental: str = xml_note.accidental or NoteAccidental.NATURAL

            if isinstance(xml_note.first_position, Pitch):
                note_name = xml_note.first_position.step
                new_notes.append(
                    MusicalNote(
                        note_name,
                        accidental,
                    )
                )

        return new_notes

    @staticmethod
    def transpose_measure(
        measure: Measure, new_scale: MusicalScale, original_scale: MusicalScale
    ) -> Measure:
        """
        Transposes the measure from the original scale to the new scale
        """
        new_measure = measure.copy()
        musical_notes = TransposerHelper.convert_notes(measure.notes)
        new_musical_notes: list[MusicalNote] = new_scale.transpose_notes_from(
            original_scale, musical_notes
        )
        new_notes = [note.copy() for note in measure.notes]
        for i, new_note in enumerate(new_musical_notes):
            new_notes[i].first_position.step = new_note.note_name
            new_notes[i].accidental = new_note.accidental

        new_attributes = None
        if measure.attributes is not None:
            new_attributes = measure.attributes.copy()
            new_attributes.key_fifths = TransposerHelper.get_scale_key_fifths(new_scale)

        new_measure.attributes = new_attributes
        new_measure.notes = new_notes
        return new_measure

    @staticmethod
    def transpose_part(
        part: Part, new_scale: MusicalScale, original_scale: MusicalScale
    ) -> Part:
        """
        Transposes the part from the original scale to the new scale
        """
        new_part = part.copy()
        transposed_measures = []
        for measure in part.measures:
            new_measure = TransposerHelper.transpose_measure(
                measure, new_scale, original_scale
            )
            transposed_measures.append(new_measure)

        part.measures = transposed_measures
        return new_part

    @staticmethod
    def transpose_score(
        score: ScorePartwise,
        new_scale: MusicalScale,
        original_scale: Optional[MusicalScale] = None,
    ) -> ScorePartwise:
        """
        Transposes the score from the original scale to the new scale
        """
        transposed_parts = []
        if not original_scale:
            start_scale = TransposerHelper.get_scale_from_score(score)
        else:
            start_scale = original_scale

        for part in score.parts_list:
            new_part = TransposerHelper.transpose_part(part, new_scale, start_scale)
            transposed_parts.append(new_part)

        return ScorePartwise(transposed_parts)


class MusicXmlGenerator:
    """
    Given a score partwise, generates a MusicXML file
    """

    def __init__(self, score: ScorePartwise):
        self.score = score

    def to_musicxml(self) -> str:
        """
        Returns the MusicXML representation of the score
        """
        return f"{HEADER}{self.score.to_musicxml()}"


def build_twinkles():
    """
    Generates a folder of all twinkle twinkle little stars in each key
    """
    original_score = ScorePartwise.from_musicxml(
        "./sample_files/Twinkle_Twinkle_Little_Star_Complete.musicxml"
    )
    original_scale = TransposerHelper.get_scale_from_score(original_score)

    for note in NoteOrdering.get_default_order():
        print("Transposing key", str(note) + "...")
        new_scale = MusicalScale(note)
        new_score = TransposerHelper.transpose_score(
            original_score, new_scale, original_scale
        )

        generator = MusicXmlGenerator(new_score)
        musicxml = generator.to_musicxml()
        with open(
            f"./sample_files/twinkles/twink_twink_little_star_{note}.musicxml",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(musicxml)

    print("done")


if __name__ == "__main__":
    build_twinkles()
