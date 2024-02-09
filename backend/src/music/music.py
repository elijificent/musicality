"""
Operations on notes on scales, seperate from musicxml logic,
but with it in mind. It is, for example, why a note has it's
two parts split into two parameters (NoteName and NoteAccidental),
but want to avoid "polymorphic issues" that may arise from treating
the music concept of a scale with it's musicxml conterpart.
"""

from enum import Enum

NOTES_IN_SCALE = 7
NOTES_IN_OCTAVE = 12


class NoteName(Enum):
    """
    A enum for the names of notes
    """

    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


class NoteAccidental(Enum):
    """
    A enum for types of note accidentals
    """

    FLAT = "flat"
    NATURAL = "natural"
    SHARP = "sharp"
    DOUBLE_SHARP = "double-sharp"
    # Add all the accidentals here

    def __repr__(self):
        return {
            "flat": "b",
            "natural": "",
            "sharp": "#",
            "double-sharp": "x",
        }[self.value]

    def __str__(self):
        return self.__repr__()


class NoteType(Enum):
    """
    Wrapper class for a note type for a note from a musicxml file
    """

    WHOLE = "whole"
    HALF = "half"
    QUARTER = "quarter"
    EIGHTH = "eighth"
    SIXTEENTH = "sixteenth"


class Note:
    """
    A class for working with individual notes, with musicxml in mind
    """

    def __init__(
        self,
        note_name: NoteName,
        accidental: NoteAccidental = NoteAccidental.NATURAL,
        note_type: NoteType = None,
    ):
        self.note_name = note_name
        self.accidental = accidental
        self.note_type = note_type

    def get_next_note_name(self) -> NoteName:
        """
        Returns the next note name
        """
        return NoteName(self.note_name.value + 1 if self.note_name.value < 7 else 1)

    def get_root_note(self) -> "Note":
        """
        Returns the name of the note that would appear on a keyboard.
        This is useful for determining the difference between note notation,
        and it's actuality. Fx, for example being equivalent to G in a
        mathematical sense, but not in a musical sense.
        """
        if self.accidental == NoteAccidental.NATURAL:
            return Note(self.note_name, NoteAccidental.NATURAL)

        if self.accidental == NoteAccidental.FLAT:
            return Note(
                NoteName(self.note_name.value - 1 if self.note_name.value > 1 else 7),
                NoteAccidental.SHARP,
            )

        if self.accidental == NoteAccidental.SHARP:
            if self.note_name in [NoteName.B, NoteName.E]:
                return Note(
                    NoteName(
                        self.note_name.value + 1 if self.note_name.value < 7 else 1
                    ),
                    NoteAccidental.NATURAL,
                )
            else:
                return Note(self.note_name, NoteAccidental.SHARP)

        if self.accidental == NoteAccidental.DOUBLE_SHARP:
            return Note(
                NoteName(self.note_name.value + 1 if self.note_name.value < 7 else 1),
                NoteAccidental.NATURAL,
            )

        raise ValueError("Do not know how to transform note")

    def get_note_n_steps_away(self, n: int, ordering: list["Note"] = None) -> "Note":
        """
        Returns the Note n steps away from this note
        """
        if ordering is None:
            order = NoteOrdering.get_alphabet_ordering()
        else:
            order = ordering
        root_note = self.get_root_note()
        root_note_index = order.index(root_note)
        new_note_index = (root_note_index + n) % len(order)
        return order[new_note_index]

    def get_steps_from(self, other_note: "Note", ordering: list["Note"] = None) -> int:
        """
        Returns how many steps away tthe other note is from this note
        """
        if ordering is None:
            order = NoteOrdering.get_alphabet_ordering()
        else:
            order = ordering

        root_note = self.get_root_note()
        other_root_note = other_note.get_root_note()
        return (order.index(other_root_note) - order.index(root_note)) % len(order)

    def copy(self) -> "Note":
        """
        Returns a copy of the note
        """
        return Note(self.note_name, self.accidental)

    def __repr__(self):
        return f"{self.note_name}{self.accidental}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other: "Note"):
        if not isinstance(other, Note):
            return False

        root_note = self.get_root_note()
        other_root_note = other.get_root_note()
        return (
            root_note.note_name == other_root_note.note_name
            and root_note.accidental == other_root_note.accidental
        )

    def __hash__(self):
        return hash((self.note_name, self.accidental))


class NoteOrdering:
    """
    Gives useful "ordering" of notes
    """

    @staticmethod
    def get_alphabet_ordering() -> list[Note]:
        """
        Returns the ordering of notes on a piano
        """
        return [
            Note(NoteName.A, NoteAccidental.NATURAL),
            Note(NoteName.A, NoteAccidental.SHARP),
            Note(NoteName.B, NoteAccidental.NATURAL),
            Note(NoteName.C, NoteAccidental.NATURAL),
            Note(NoteName.C, NoteAccidental.SHARP),
            Note(NoteName.D, NoteAccidental.NATURAL),
            Note(NoteName.D, NoteAccidental.SHARP),
            Note(NoteName.E, NoteAccidental.NATURAL),
            Note(NoteName.F, NoteAccidental.NATURAL),
            Note(NoteName.F, NoteAccidental.SHARP),
            Note(NoteName.G, NoteAccidental.NATURAL),
            Note(NoteName.G, NoteAccidental.SHARP),
        ]

    @staticmethod
    def get_default_order() -> list[Note]:
        """
        Returns them in the order they are in the octave,
        starting from C, flats after sharps
        """
        return [
            Note(NoteName.C, NoteAccidental.NATURAL),
            Note(NoteName.C, NoteAccidental.SHARP),
            Note(NoteName.D, NoteAccidental.FLAT),
            Note(NoteName.D, NoteAccidental.NATURAL),
            Note(NoteName.D, NoteAccidental.SHARP),
            Note(NoteName.E, NoteAccidental.FLAT),
            Note(NoteName.E, NoteAccidental.NATURAL),
            Note(NoteName.F, NoteAccidental.NATURAL),
            Note(NoteName.F, NoteAccidental.SHARP),
            Note(NoteName.G, NoteAccidental.FLAT),
            Note(NoteName.G, NoteAccidental.NATURAL),
            Note(NoteName.G, NoteAccidental.SHARP),
            Note(NoteName.A, NoteAccidental.FLAT),
            Note(NoteName.A, NoteAccidental.NATURAL),
            Note(NoteName.A, NoteAccidental.SHARP),
            Note(NoteName.B, NoteAccidental.FLAT),
            Note(NoteName.B, NoteAccidental.NATURAL),
        ]


class ScaleType(Enum):
    """
    Wrapper class for a scale type
    """

    IONIAN = 1
    AEOLIAN = 2


class Scale:
    """
    A class for working with a musical scale, given the start key and
    the scale type

    Args:
        start_note (Note): The note that the scale starts on
        scale_type (ScaleType): The type of scale that we are working with
    """

    def __init__(self, start_note: Note, scale_type: ScaleType = ScaleType.IONIAN):
        self.start_note = start_note
        self.scale_type = scale_type

    def get_scale_formula(self) -> list[int]:
        """
        Returns the steps needed to form the scale
        """
        if self.scale_type == ScaleType.IONIAN:
            return [0, 2, 2, 1, 2, 2, 2]
        elif self.scale_type == ScaleType.AEOLIAN:
            return [0, 2, 1, 2, 2, 1, 2]
        else:
            raise ValueError("Invalid scale type")

    def get_scale_formula_cum_sum(self) -> list[int]:
        """
        Returns the cumulative sum for the steps to get to each
        note in the scale
        """
        return [sum(self.get_scale_formula()[: i + 1]) for i in range(NOTES_IN_SCALE)]

    def get_scale_note_ordering(self) -> list[Note]:
        """
        Returns the ordering of notes in the scale
        """
        return [
            self.start_note.get_note_n_steps_away(step)
            for step in range(NOTES_IN_OCTAVE)
        ]

    def get_basic_scale(self) -> list[Note]:
        """
        Returns the what the scale would be if we used
        the natural note that would be selected, given the
        start note and the scale formula.
        """
        return [
            self.start_note.get_note_n_steps_away(step)
            for step in self.get_scale_formula_cum_sum()
        ]

    def get_scale(self) -> list[Note]:
        """
        Returns the notes that are considered part of the scale
        """
        notes = [self.start_note.copy()]
        basic_scale = self.get_basic_scale()
        for scale_degree in range(1, NOTES_IN_SCALE):
            prev_note = notes[-1]
            curr_note = basic_scale[scale_degree]
            should_be_note_name = prev_note.get_next_note_name()

            if curr_note.note_name == should_be_note_name:
                notes.append(curr_note)
            else:
                if should_be_note_name.value < curr_note.note_name.value:
                    if should_be_note_name == NoteName.F and prev_note == Note(
                        NoteName.E, NoteAccidental.SHARP
                    ):
                        notes.append(Note(NoteName.F, NoteAccidental.DOUBLE_SHARP))

                    elif should_be_note_name == NoteName.C and prev_note == Note(
                        NoteName.B, NoteAccidental.SHARP
                    ):
                        notes.append(Note(NoteName.C, NoteAccidental.DOUBLE_SHARP))
                    else:
                        notes.append(Note(should_be_note_name, NoteAccidental.SHARP))
                else:
                    notes.append(Note(should_be_note_name, NoteAccidental.FLAT))
        return notes

    def get_transpose(self, other_scale: "Scale") -> dict[str, str]:
        """
        Returns a dictionary that maps the notes in this scale to the notes in the other scale
        """
        if self.scale_type != other_scale.scale_type:
            raise ValueError("Cannot transpose scales of different types")

        self_scale_order = self.get_scale()
        other_scale_order = other_scale.get_scale()

        return {
            self_scale_order[i]: other_scale_order[i] for i in range(NOTES_IN_SCALE)
        }

    def transpose_notes_from(
        self, original_scale: "Scale", notes: list[Note]
    ) -> list[Note]:
        """
        Transposes the notes from the original scale to the current scale
        """
        if original_scale.scale_type != self.scale_type:
            raise ValueError("Cannot transpose scales of different types")

        transposed = []
        for note in notes:
            steps_from_home_note = original_scale.start_note.get_steps_from(note)
            transposed_note = self.start_note.get_note_n_steps_away(
                steps_from_home_note
            )
            transposed.append(transposed_note)

        return transposed
