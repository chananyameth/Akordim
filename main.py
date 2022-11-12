import re

HEB_CHARS = 'אבגדהוזחטיכלמנסעפצקרשתךםןףץ'
OTHER_CHARS = r' \-_)(,\.'
END_LINE_CHARS = '\r\n'
CHORDS_CHARS = 'ABCDEFGabcdefg123456789b#dim'


class SongLine:
    def __init__(self, pairs):
        self.pairs = pairs
        self.chords_line = ''  # will be populated
        self.text_line = ''  # will be populated

    @property
    def text_len(self):
        return len(self.text_line)

    @property
    def chords_len(self):
        return len(self.chords_line)

    def standardize_pairs(self):
        self.pairs.remove(('', ''))

        for i in range(len(self.pairs)):
            char, chord = self.pairs[i]
            if len(char) != 1:
                char = ' '
            if chord == '':
                chord = None
            self.pairs[i] = char, chord

    def build_lines(self):
        for char, chord in self.pairs:
            if chord:
                if self.chords_len == 0 or self.chords_line[-1] == ' ':
                    self.text_line += char
                    self.chords_line += chord[::-1]  # reversed
                else:
                    self.text_line += '-' * (self.chords_len - self.text_len + 1)
                    self.chords_line += ' '

                    self.text_line += char
                    self.chords_line += chord[::-1]  # reversed
            else:
                self.text_line += char
                self.chords_line += ' ' * (self.text_len - self.chords_len)

        self.text_line += ' ' * (self.chords_len - self.text_len)
        self.chords_line += ' ' * (self.text_len - self.chords_len)

        # some extra steps for the chords line
        if self.chords_line.count(' ') == len(self.chords_line):
            self.chords_line = ''
        self.chords_line = self.chords_line[::-1]  # reverse the whole line
        self.replace_chords_line_padding()  # might be needed for alignment

    def replace_chords_line_padding(self):
        """replace the starting and ending spaces for alignment"""
        l_spaces = len(self.chords_line) - len(self.chords_line.lstrip())
        r_spaces = len(self.chords_line) - len(self.chords_line.rstrip())
        self.chords_line = ' ' * r_spaces + self.chords_line.strip() + ' ' * l_spaces


def extract_pairs(line: str):
    pattern = re.compile(f'([{HEB_CHARS}{OTHER_CHARS}])?([{CHORDS_CHARS}]*)')
    pairs = re.findall(pattern, line)  # (char, chord)

    return pairs


def separate_line(line: str):
    """separate line of text into chords_line, text_line"""
    song = SongLine(extract_pairs(line))
    song.standardize_pairs()
    song.build_lines()

    return song.chords_line, song.text_line


def main(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename + '.out.txt', 'w', encoding='utf-8') as out_file:
        for line in lines:
            chords_line, text_line = separate_line(line.strip(END_LINE_CHARS))

            out_file.write(chords_line + '\n' if chords_line != '' else '')
            out_file.write(text_line + '\n')


if "__main__" == __name__:
    main('./demo.txt')
