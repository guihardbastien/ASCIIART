import argparse
from os import walk
import sys


# /!\ SHOULD ONLY BE CHANGED IN `main()`
# Adding characters to alphabets is ok though
app_state = {
        "max_height": 9,
        "baseline_should_be_at": 6,
        "font": "big",
        "words": None,
        "available_fonts": ["big", "mini", "small", "standard"],
        "font_uri": "./fonts/",
        "doubt":  " (ノಠ益ಠ)ノ ",
        "term-width": -1,
        "cut_opt": "none",
        "out_file": None,
        "load_acc": True,
        "dirty_alphabet": {},
        "clean_alphabet": {}
    }


def add_accents():
    """Add accent to character dict ( clean_dict )
    This function hard codes french accents cases.
    However i belive the user should be able to pass it's own list of triple
    """
    uri = app_state["font_uri"]
    try:
        with open(uri + "accents.txt", 'r') as f:
            content = f.read().split('\n')
            for x in range(0, len(content)):
                content[x] += "  "
            acute = content[0:2]
            grave = content[2:4]
            circumflex = content[4:6]
            dieresis = content[6:8]
    except FileNotFoundError:
        print("Accent file not found")
        return
    fr_acc = [('à', 'a',  acute), ('â', 'a', circumflex), ('ä', 'a', dieresis),
              ('é', 'e', acute), ('è', 'e', grave), ('ê', 'e', circumflex),
              ('ë', 'e', dieresis), ('ï', 'i', dieresis),
              ('î', 'i', circumflex), ('ô', 'o', circumflex),
              ('ö', 'o', dieresis), ('ù', 'u', grave),
              ('ü', 'u', dieresis), ('ÿ', 'y', dieresis)]
    for acc in fr_acc:
        char, init_char, accent = acc
        baseline, char_as_list = app_state["dirty_alphabet"][init_char]
        char_as_list = accent + char_as_list
        clean = clean_char(baseline + 2, char_as_list)
        app_state["clean_alphabet"][char] = clean


def clean_char(baseline, char_as_list):
    """Fills a square-ish perimeter around graphic char with spaces
    returns a list of strings with same length
    """
    bsba = app_state["baseline_should_be_at"]
    mh = app_state["max_height"]

    total_lines = len(char_as_list)
    max_length = 0
    lines_to_insert = bsba - baseline
    lines_to_append = (mh - bsba) - (total_lines - baseline)

    # find max length
    for i in range(0, len(char_as_list)):
        line = char_as_list[i]
        char_as_list[i] = line[:-1]
        if(len(line) > max_length):
            max_length = len(line)

    # add mising lines
    for x in range(0, lines_to_insert):
        char_as_list.insert(0, '')
    for y in range(0, lines_to_append):
        char_as_list.append('')

    # fill representation with spaces
    for j in range(0, len(char_as_list)):
        line = char_as_list[j]
        length = len(line)
        diff = max_length - length
        repeats = " " * (diff - 1)
        line = line + repeats
        char_as_list[j] = line
    return char_as_list


def load_char(char_file_path, char):
    """Extracts baseline etc

    This function takes a character file path and its ascii representation
    Returns its squared(clean) representation
    This function also stores a copy of a tuple made of
    the char baseline and its list representation (not cleaned aka dirty)
    """
    baseline, squared_rep = None, []
    count = 0

    with open(char_file_path, 'rt') as file:
        for line in file:
            if(line[:1] == "-"):
                baseline = count
            squared_rep.append(line[2:])
            count += 1
    bs = (baseline, squared_rep.copy())
    app_state["dirty_alphabet"][char] = bs
    squared_rep = clean_char(baseline, squared_rep)
    return squared_rep


def load_font():
    """Stores in `app_state` a dictionnary of usable letters
    """
    uri = app_state["font_uri"] + app_state["font"] + "/"
    _, _, filenames = next(walk(uri))
    for i in range(0, len(filenames)):
        char_file = filenames[i]
        char_uri = uri + char_file
        hex_string = char_file[:-4][2:]
        bytes_object = bytes.fromhex(hex_string)
        ascii_string = bytes_object.decode("ASCII")
        sqrd_char = load_char(char_uri, ascii_string)
        app_state["clean_alphabet"][ascii_string] = sqrd_char


def generate_static_char(string, char_name):
    """Helper for generating missing char placeholder or space characters
    """
    mh = app_state["max_height"]
    char = []
    for j in range(0, mh):
        char.append(string)
        app_state["clean_alphabet"][char_name] = char
    return char


def add_next_line(char_list, words):
    """Add correct return to ascii representation

    Takes an array of squared characters
    and add lines given term size and cut option.
    returns an array of arrays of squared (clean) chars
    """
    cut_opt = app_state["cut_opt"]
    term_width = app_state["term-width"]

    if (term_width is None):
        p = []
        p.append(char_list)
        return p
    paragraph = [[]]
    len_counter = 0
    current_line = 0
    for i in range(0, len(char_list)):
        char = char_list[i]
        char_length = len(char[0])
        if(cut_opt == "char"):
            if((len_counter + char_length) >= term_width):
                paragraph.append([])
                current_line += 1
                len_counter = 0

        if(cut_opt == "word"):
            if(len_counter == 0 and (words[i] == " ")):
                continue
            if(((len_counter + char_length) >= term_width)
               and (words[i] == " ")):
                paragraph.append([])
                current_line += 1
                len_counter = 0
                continue

        paragraph[current_line].append(char)
        len_counter += char_length
    return paragraph


def print_words(words):
    """Assembles a text into an ascii art string
    """
    word_length = len(words)
    mh = app_state["max_height"]

    load_font()
    add_accents()
    alphabet = app_state["clean_alphabet"]
    char_list = []
    for i in range(0, word_length):
        ascii_char = words[i]

        if(ascii_char in alphabet):
            char = alphabet[ascii_char]
        else:
            char = alphabet["doubt"]
        char_list.append(char)

    paragraph = add_next_line(char_list, words)
    art = ''
    for x in range(0, len(paragraph)):
        art_line = paragraph[x]
        line_length = len(art_line)
        for j in range(0, mh):
            line = ''
            for k in range(0, line_length):
                line = line + art_line[k][j]
            line = line + '\n'
            art = art + line
    return art


def read_from_file(filename):
    """Reads from input file
    """
    f = open(filename, "r+")
    return f.read()


def write_to_file(filename, art):
    """Write to specified file
    """
    f = open(filename, 'w+')
    f.write(art)
    f.close()


def main():
    """Handling of user arguments
    """
    arg_parser = argparse.ArgumentParser(
        description='Toilet-like script')
    arg_parser.add_argument('--words',
                            metavar='<words>',
                            type=str,
                            help='Words you want to convert to ASCII art')
    arg_parser.add_argument('--font',
                            metavar='<big|mini|small|standard>',
                            type=str,
                            help='font for your ASCII art, default big.')
    arg_parser.add_argument('--term-width',
                            metavar='<width>',
                            type=int,
                            help="Int specifying the width" +
                            " within which you'd like to print")
    arg_parser.add_argument('--cut',
                            metavar='<none|char|word>',
                            type=str,
                            help="Either none, char, word")
    arg_parser.add_argument('--input',
                            metavar='<path to in file>',
                            type=str,
                            help="text file to read from")
    arg_parser.add_argument('--output',
                            metavar='<output file path>',
                            type=str,
                            help="text file to write to")

    for arg, value in arg_parser.parse_args()._get_kwargs():
        if(arg == "words"):
            if(not(value is None)):
                app_state["words"] = value

        elif(arg == "font"):
            if (value in app_state["available_fonts"]):
                app_state["font"] = value

        elif(arg == "term_width"):
            app_state["term-width"] = value

        elif(arg == "cut"):
            if((value == "char") or (value == "word")):
                if(app_state["term-width"] is None):
                    app_state["term-width"] = 20
            app_state["cut_opt"] = value

        elif(arg == "input"):
            if(not(value is None)):
                if(app_state["words"] is None):
                    app_state["words"] = read_from_file(value)

        elif(arg == "output"):
            app_state["out_file"] = value

        else:
            print("illegal argument ' " + arg + " ' use -h option for info")

    if(app_state["words"] is None):
        print("You should provide words to print through --words " +
              "or --input option. Here si the doc: \n")
        arg_parser.print_help(sys.stderr)
        sys.exit()

    generate_static_char(app_state["doubt"], "doubt")
    generate_static_char("  ", " ")

    art = print_words(app_state["words"])
    out = app_state["out_file"]
    if (out is None):
        print(art)
    else:
        write_to_file(out, art)
        print("ascii art was written to : " + out)


main()
