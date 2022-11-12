HEB_CHARS = 'אבגדהוזחטיכלמנסעפצקרשתךםןףץ'
OTHER_CHARS = ' -_)(,.'
END_LINE_CHARS = '\r\n'
CHORDS_CHARS = 'ABCDEFGabcdefg123456789b#dim'


class SongLine:
    def __init__(self, chords, spaces, text_line):
        self.chords = chords
        self.spaces = spaces
        self.text_line = text_line
        self.chords_line = ''  # will be populated

    def insert_text_at(self, text, where):
        self.text_line = self.text_line[:where] + text + self.text_line[where:]

    @property
    def text_len(self):
        return len(self.text_line)


def reorder_chords(index_chord: list):
    """
    reverse chords in line, keep spaces the same

    index_chord: list(tuple(index:int, chord:str))
    """
    indexes = []
    chords = []
    for index, chord in index_chord:
        indexes.append(index)
        chords.append(chord)

    return zip(indexes, reversed(chords))


def override_spaces_with_chords(song):
    for i in range(len(song.chords)):
        song.spaces[i + 1] = song.spaces[i + 1] - len(song.chords[i])


def chords_to_line_1(song):
    line = ''
    for i in range(len(song.chords)):
        line += song.chords[i].rjust(song.spaces[i])
    line += ' ' * song.spaces[-1]
    return line


def space_out_chords(song):
    """each space must be at least 1 more than its chord (in length)"""
    if song.spaces[0] == 0:
        song.spaces[0] = 1
        song.text_line = ' ' + song.text_line

    accumulate = 0
    for i in range(len(song.chords)):
        accumulate += song.spaces[i]
        if (diff := (len(song.chords[i]) + 1) - song.spaces[i + 1]) > 0:
            song.spaces[i + 1] += diff
            song.insert_text_at('-' * diff, accumulate)


def widen_spaces(song):
    accumulate = 0
    for i in range(len(song.chords) - 1, 0, -1):
        if (diff := len(song.chords[i]) + 1 - song.spaces[i]) > 0:
            song.spaces[i] += diff
            song.insert_text_at('-' * diff, accumulate)
        accumulate += song.spaces[i]


def extract_chords(line: str):
    chords = []
    spaces = []
    text_line = []

    chord = []
    counter = 0
    for char in line:
        if char in HEB_CHARS + OTHER_CHARS + END_LINE_CHARS:
            if chord:
                spaces.append(counter)
                counter = 0
                chords.append(''.join(chord))
                chord = []

            text_line.append(char)
            counter += 1
        elif char in CHORDS_CHARS:
            chord.append(char)
        else:
            print('unknown char, debug me!! ', char)

    if chord:
        spaces.append(counter)
        counter = 0
        chords.append(''.join(chord))

    spaces.append(counter)

    return chords, spaces, ''.join(text_line)


def separate_line(line: str):
    """separate line of text into chords_line, text_line"""
    song = SongLine(*extract_chords(line))

    song.chords.reverse()
    song.spaces.reverse()

    widen_spaces(song)
    # space_out_chords(song)
    # override_spaces_with_chords(song)

    song.chords_line = chords_to_line_1(song)
    # song.chords_line, text_line = chords_to_line(chords, text_line)

    song.text_line += ' ' * (len(song.text_line) - len(song.chords_line))

    return song.chords_line, song.text_line


def main(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename + '.out.txt', 'w', encoding='utf-8') as out_file:
        for line in lines:
            chords_line, text_line = separate_line(line[:-1])

            out_file.write(''.join(chords_line) + '\n')
            out_file.write(''.join(text_line) + '\n')


if "__main__" == __name__:
    main('./demo.txt')
