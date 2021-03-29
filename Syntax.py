import re, sys
from string import punctuation
keywords = ["auto", "break", "case",
                            "char", "const", "continue",
                            "default", "do", "double",
                            "else", "enum", "extern",
                            "float", "for", "goto", "if",
                            "int", "long", "register", "return",
                            "short", "signed", "sizeof",
                            "static", "struct", "switch",
                            "typedef", "union", "unsigned",
                            "void", "volatile", "while", "asm"]
bold = "\x1b[1m"
bold_yellow = "\x1b[1m\x1b[33m"
magenta = "\x1b[35m"
green = "\x1b[32m"
red = "\x1b[31m"
cyan = "\x1b[36m"
reset = "\x1b[0m"

isKeyword = True
multiline = False
isDirective = False

inFile = sys.stdin.readlines()
for i in range(len(inFile)):
    if isDirective:
        isDirective = False
    if not isKeyword and not multiline:
        print(reset, end= '')
        isKeyword = True
    parole = re.split(r'([({\s"*})])', inFile[i])
    for i in range(len(parole)):
        if '*' in parole[i] and '/' in parole[(i-1)]:
            print(parole[i] + green, end='')
            multiline = True
            isKeyword = False
        elif '/' in parole[i]:
            if '*' in parole[(i-1)]:
                print(green + parole[(i-1)] + parole[i], end='')
                multiline = False
                isKeyword = False
            elif isDirective:
                print(cyan + parole[i], end='')
                isKeyword = False
            else:
                print(green + parole[(i-1)]+parole[i], end='')
                isKeyword = False
        # Rileva stringhe
        elif '"' in parole[i] or "'" in parole[i]:
            if isKeyword:
                print(cyan + parole[i], end='')
                isKeyword = False
            else:
                print(parole[i] + reset, end='')
        # Rileva direttive al preprocessore
        elif '#' in parole[i]:
            print(magenta + parole[i], end='')
            isKeyword = False
            isDirective = True
        elif '<' in parole[i] and isDirective:
            print(cyan + parole[i], end='')
            isDirective = False
         # Rileva punteggiatura
        elif parole[i] in punctuation:
            if multiline:
                continue
            else:
                print(red + parole[i] + reset, end='')
        elif isKeyword:
            if parole[i] in keywords:
                print(bold_yellow + parole[i] + reset, end='')
            else:
                print(parole[i], end = '')
        elif multiline:
            print(green + parole[i] + reset, end = '')
        else:
            print(parole[i], end = '')