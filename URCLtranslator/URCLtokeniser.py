
# read raw lines

# remove multiline comments
# remove line comments

# remove empty lines
# replace double space with single, twice

# for each line - line.split(" ")

# find @DEFINE values and resolve

# find @BITS and remove + resolve
# find @MINREG and remove + resolve
# find @MINHEAP and remove + resolve
# find @MINSTACK and remove + resolve
# find @RUN and remove

# find @HEAP and resolve
# find @MSB and resolve
# find @SMSB and resolve
# find @MAX and resolve
# find @SMAX and resolve
# find @UHALF and resolve
# find @LHALF and resolve

# find negative integers and make positive

# move DW values to end

# return URCL code list

from copy import deepcopy


def readRawURCL() -> list:
    
    name = input("Enter name of .urcl file: ")
    
    f = open(f"MPU7_Code\\URCL and B code\\{name}.urcl", "r")
    URCL = f.readlines()
    f.close()
    
    return URCL

def tokeniseURCL(URCL: list) -> list:
    
    # find and remove /**/
    for lineNumber, line in enumerate(URCL):
        if line.count("/*"):
            for lineNumber2, line2 in enumerate(URCL[lineNumber + 1: ]):
                if line2.count("*/"):
                    lineNumber2 += (lineNumber + 1)
                    break
            URCL[lineNumber] = URCL[lineNumber][: line.index("/*")]
            URCL[lineNumber2] = URCL[lineNumber2][URCL[lineNumber2].index("*/") + 2: ]
            while lineNumber < lineNumber2:
                URCL[lineNumber2] = ""
                lineNumber2 -= 1
    
    # remove //
    for lineNumber, line in enumerate(URCL):
        if line.count("//"):
            URCL[lineNumber] = URCL[lineNumber][: line.index("//")]
        elif line.count("\n"):
            URCL[lineNumber] = URCL[lineNumber].replace("\n", "")
    
    # remove [ ]
    URCL = [(line.replace("[", "")).replace("]", "") for line in URCL]
    
    # remove extra spaces
    URCL = [(line.replace("  ", " ")).replace("  ", " ") for line in URCL]
    
    # remove start and end " ":
    for lineNumber in range(len(URCL)):
        while URCL[lineNumber].endswith((" ", "\n")):
            URCL[lineNumber] = URCL[lineNumber][: -1]
        while URCL[lineNumber].startswith((" ", "\n")):
            URCL[lineNumber] = URCL[lineNumber][1: ]
    
    # remove empty lines
    oldURCL = deepcopy(URCL)
    for lineNumber, line in enumerate(oldURCL[: : -1]):
        if line in ("", " ", "\n", " \n", "\n "):
            URCL.pop(len(oldURCL) - 1 - lineNumber)
    
    # tokenise
    URCL = [line.split(" ") for line in URCL]
    
    # resolve @DEFINE
    for lineNumber, line in enumerate(URCL):
        if line[0] == "@DEFINE":
            key = line[1]
            value = line[2]
            for lineNumber2, line2 in enumerate(URCL):
                for tokenNumber, token in enumerate(line2):
                    if token == ("@" + key):
                        URCL[lineNumber2][tokenNumber] = value

    oldURCL = deepcopy(URCL)
    for lineNumber, line in enumerate(oldURCL[: : -1]):
        if line[0] == "@DEFINE":
            URCL.pop(len(oldURCL) - 1 - lineNumber)
    
    # resolve @BITS
    for lineNumber, line in enumerate(URCL):
        if line[0] == "@BITS":
            if "8" not in line:
                raise Exception("FATAL - @BITS isn't 8 in this program.")
            URCL.pop(lineNumber)
            break
    
    # find @MINREG
    MINREG = "8"
    for lineNumber, line in enumerate(URCL):
        if line[0] == "@MINREG":
            MINREG = line[1]
            URCL.pop(lineNumber)
            break

    # find @MINHEAP
    MINHEAP = "128"
    for lineNumber, line in enumerate(URCL):
        if line[0] == "@MINHEAP":
            MINHEAP = line[1]
            URCL.pop(lineNumber)
            break

    # find @MINSTACK
    MINSTACK = "128"
    for lineNumber, line in enumerate(URCL):
        if line[0] == "@MINSTACK":
            MINSTACK = line[1]
            URCL.pop(lineNumber)
            break
    
    # find @RUN
    for lineNumber, line in enumerate(URCL):
        if line[0] == "@RUN":
            URCL.pop(lineNumber)
            break

    # resolve all defined immediates
    for lineNumber, line in enumerate(URCL):
        for tokenNumber, token in enumerate(line):
            if token == "@BITS":
                URCL[lineNumber][tokenNumber] = "8"
            elif token == "@MINREG":
                URCL[lineNumber][tokenNumber] = MINREG
            elif token == "@MINHEAP":
                URCL[lineNumber][tokenNumber] = MINHEAP
            elif token == "@MINSTACK":
                URCL[lineNumber][tokenNumber] = MINSTACK
            elif token == "@HEAP":
                URCL[lineNumber][tokenNumber] = 128
            elif token == "@MSB":
                URCL[lineNumber][tokenNumber] = 128
            elif token == "@SMSB":
                URCL[lineNumber][tokenNumber] = 64
            elif token == "@MAX":
                URCL[lineNumber][tokenNumber] = 255
            elif token == "@SMAX":
                URCL[lineNumber][tokenNumber] = 127
            elif token == "@UHALF":
                URCL[lineNumber][tokenNumber] = 240
            elif token == "@LHALF":
                URCL[lineNumber][tokenNumber] = 15

    # find negative integers
    for lineNumber, line in enumerate(URCL):
        for tokenNumber, token in enumerate(line):
            if token.startswith("-"):
                number = int(token[1: ], 0)
                number = 256 - number
                URCL[lineNumber][tokenNumber] = str(number)

    # find DW values
    data = []
    lineNumber = 0
    while lineNumber < len(URCL):
        if URCL[lineNumber][0] == "DW":
            temp = []
            while URCL[lineNumber - 1][0].startswith("."):
                label = URCL[lineNumber - 1]
                temp.append(label)
                URCL.pop(lineNumber - 1)
                lineNumber -= 1
            data += temp[: : -1]
            data.append(URCL[lineNumber])
            URCL.pop(lineNumber)
        else:
            lineNumber += 1
    URCL += data
    
    # convert DW arrays into singles
    lineNumber = 0
    while lineNumber < len(URCL):
        if URCL[lineNumber][0] == "DW":
            if len(URCL[lineNumber]) > 2:
                URCL.insert(lineNumber + 1, ["DW"] + URCL[lineNumber][2: ])
                URCL[lineNumber] = URCL[lineNumber][: 2]
        lineNumber += 1
    
    return URCL

def getURCL() -> list:
    URCL = readRawURCL()
    
    URCL = tokeniseURCL(URCL)
    
    return URCL
