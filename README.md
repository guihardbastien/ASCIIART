# ASCIIART

## Description

Turns a string into a neat ascii art string.

Example:

```bash
python ascii_art.py --cut char --font mini --words "HelloWorld"


|_| _ || _ \    / _ ._| _|
| |(/_||(_) \/\/ (_)| |(_|

```
## Overview

### Directory structure

```bash
.
├── CHANGELOG.md
├── README.md
├── ascii_art.py
├── fonts
│   ├── accents.txt
│   ├── big
│   │   ├── 0x21.txt
│   │   ├── ...
│   │   └── 0x7e.txt
│   ├── mini
│   │   ├── 0x21.txt
│   │   ├── ...
│   │   └── 0x7e.txt
│   ├── small
│   │   ├── 0x21.txt
│   │   ├── ...
│   │   └── 0x7e.txt
│   └── standard
│       ├── 0x21.txt
│       ├── ...
│       └── 0x7e.txt
├── in.txt
├── out.txt
└── tests
    └── tests_v1_tp3.md
```

### Features
**Help:**
```bash
python ascii_art.py --h
```

```bash
  -h, --help            show this help message and exit
  --words <words>       Words you want to convert to ASCII art
  --font <big|mini|small|standard>
                        font for your ASCII art, default big.
  --term-width <width>  Int specifying the width within which you\'d like to
                        print
  --cut <none|char|word>
                        Either none, char, word
  --input <path to in file>
                        text file to read from
  --output <output file path>
                        text file to write to
```

### How to use ?
```bash
python ascii_art.py --cut word --term-width 20 --font mini --words bordel
# or
python ascii_art.py --cut char --font mini  --input in.txt
```

## Other/Optional considerations

Please follow the folowing template for tests:

```
 # Report X

 ## Id: #X

 **Title:** Template

 **Version:** VX.X

 **Category:** XXX XXX

 **Priority:** [1, 2, 3, 4]

 **Description:** Lorem ipsum

 -------------------------------------------------------------------------------
```

## Ressources

- TBA 

