HEB_CHARS = 'אבגדהוזחטיכלמנסעפצקרשתךםןףץ'
OTHER_CHARS = ' -_)(,.'
END_LINE_CHARS = '\r\n'
CHORDS_CHARS = 'ABCDEFGabcdefg123456789b#dim'


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


def separate_line(line: str):
    """separate line of text into chords_line, text_line"""
    chords, text_line = extract_chords(line)

    # chords = reorder_chords(chords)

    chords_line, text_line = chords_to_line(chords, text_line)

    return chords_line, text_line


def chords_to_line(chords, text_line: str):
    """
    Stringify

    index_chord: list(tuple(index:int, chord: str))
    """
    chords_line = ''
    for index, chord in chords:
        # if there's no space between the chords, add a ' ' and '-'
        if index - len(chords_line) <= 0:
            text_line = text_line[:-index] + '-' + text_line[-index:]
            chords_line += ' '

        chords_line += ' ' * (index - len(chords_line)) + chord

    return chords_line, text_line


def extract_chords(line: str):
    chords = []
    text_line = []

    chord = []
    index = 0
    for char in line:
        if char in HEB_CHARS + OTHER_CHARS + END_LINE_CHARS:
            if chord:
                chords.append((index - 1, ''.join(chord)))
                chord = []

            text_line.append(char)
            index += 1
        elif char in CHORDS_CHARS:
            chord.append(char)
        else:
            print('unknown char, debug me!! ', char)
    return chords, ''.join(text_line)


def main(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename + '.out.txt', 'w', encoding='utf-8') as out_file:
        for line in lines:
            chords_line, text_line = separate_line(line)

            out_file.write(''.join(chords_line) + '\n')
            out_file.write(''.join(text_line) + '\n')


if "__main__" == __name__:
    main('./demo.txt')
