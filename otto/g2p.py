import os
import subprocess
import re

from otto.settings import TMP_FOLDER

# Path for temporary g2p workspace file.
g2p_temp_file = os.path.join(TMP_FOLDER, 'g2ptemp')

PHONETISAURUS_EXECUTABLE = 'phonetisaurus-g2p'
PHONETISAURUS_MODEL = os.path.expanduser("~/phonetisaurus/g014b2b.fst")

line_reg = re.compile(r'<s> (.*) </s>')


def parseLine(line):
    return line_reg.search(line).group(1)


def parseOutput(output):
    return line_reg.findall(output)


def translateWord(word):
    out = subprocess.check_output([
        PHONETISAURUS_EXECUTABLE,
        '--model=%s' % PHONETISAURUS_MODEL,
        '--input=%s' % word,
    ])
    return parseLine(out)


def translateWords(words):
    full_text = '\n'.join(words)

    with open(g2p_temp_file, 'wb') as f:
        f.write(full_text)
        f.flush()

    output = translateFile(g2p_temp_file)
    os.remove(g2p_temp_file)

    return output


def translateFile(input_filename, output_filename=None):
    out = subprocess.check_output([
        PHONETISAURUS_EXECUTABLE,
        '--model=%s' % PHONETISAURUS_MODEL,
        '--input=%s' % input_filename,
        '--words',
        '--isfile',
    ])
    out = parseOutput(out)

    if output_filename:
        out = '\n'.join(out)

        with open(output_filename, "wb") as f:
            f.write(out)

        return None

    return out

if __name__ == "__main__":

    translateFile(os.path.expanduser("~/phonetisaurus/sentences.txt"),
                  os.path.expanduser("~/phonetisaurus/dictionary.dic"))
