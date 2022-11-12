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


def override_spaces_with_chords(chords, spaces):
    for i in range(len(chords)):
        spaces[i + 1] = spaces[i + 1] - len(chords[i])


def chords_to_line_1(spaces, chords):
    line = ''
    for i in range(len(chords)):
        line += ' ' * spaces[i] + chords[i]
    line += ' ' * spaces[-1]
    return line


def space_out_chords(chords, spaces, text_line):
    if spaces[0] == 0:
        spaces[0] = 1
        text_line = ' ' + text_line

    accumulate = 0
    for i in range(len(chords)):
        accumulate += spaces[i] + len(chords[i])
        if (diff := len(chords[i]) + 1 - spaces[i + 1]) > 0:
            spaces[i + 1] += diff
            text_line = text_line[:accumulate] + '-' * diff + text_line[accumulate:]


def extract_chords(line: str):
    chords = []
    spaces = []
    text_line = []

    chord = []
    counter = 0
    for char in line:
        if char in HEB_CHARS + OTHER_CHARS + END_LINE_CHARS:
            if chord:
                spaces.append(counter - 1)
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
    chords, spaces, text_line = extract_chords(line)

    space_out_chords(chords, spaces, text_line)
    override_spaces_with_chords(chords, spaces)

    chords.reverse()
    # spaces.reverse()

    chords_line = chords_to_line_1(spaces, chords)
    # chords_line, text_line = chords_to_line(chords, text_line)

    text_line += ' ' * (len(text_line) - len(chords_line))

    return chords_line, text_line


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
