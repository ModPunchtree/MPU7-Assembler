
def tokenise(rawCode: str) -> list:
    
    # remove multiline comments
    while rawCode.count("/*") > 0:
        index1 = rawCode.index("/*")
        index2 = rawCode.index("*/") + 2
        rawCode = rawCode[: index1] + rawCode[index2: ]
    
    # convert code to list of lines
    code = rawCode.split("\n")
    
    # remove line comments
    for lineNumber in range(len(code)):
        if code[lineNumber].count("//") > 0:
            code[lineNumber] = code[lineNumber][: code[lineNumber].index("//")]
    
    # remove empty lines
    iteration = 0
    while iteration < len(code):
        if (not code[iteration]) or (code[iteration].count(" ") == len(code[iteration])):
            code.pop(iteration)
        else:
            iteration += 1
        
    # tokenise each line
    answer = []
    for line in code:
        lineAnswer = []
        char = 0
        while char < len(line):
            if line[char].isalnum() or line[char] in ("@", "~", "-", "+", "'", ".", "!", "_"): # .startswith(("NOP", "RST", "ADD", "ADC", "SUB", "SBB", "MOV", "IMM", "INC", "DEC", "NEG", "LSH", "LSC", "RSH", "NOR", "AND", "NOT", "FLG", "SETX", "SETY", "PRT", "VSH", "SPT", "RPT", "HLT", "JMP", "RET", "STL", "FFG", "CLR", "STR", "LOD")):
                text = line[char]
                char += 1
                if char < len(line):
                    if (text == "'") and (line[char] in (" ", "!", ":", ";", "%", "#", "'", "~", "(", ")", "{", "}", "[", "]", "<", ">", "?", "/", "\\", "£", "$", "€", "^", "&", "=", "_", "|", "@")):
                        text += line[char]
                        char += 1
                    while line[char].isalnum() or line[char] in ("+", "-", "'", "_", ".", "*", "/"):
                        text += line[char]
                        char += 1
                        if char >= len(line):
                            break
                lineAnswer.append(text)
            elif line[char] in ("(", ")", ";"):
                lineAnswer.append(line[char])
                char += 1
            elif line[char] in (" ", ","):
                char += 1
            else:
                raise Exception(f"FATAL - Unrecognised character: {line[char]}")
        answer.append(lineAnswer)
    
    # convert relatives to labels
    def convertRelativesToLabels(code: list, uniqueNumber: int = 0) -> list:
        for lineNumber in range(len(code)):
            for tokenNumber, token in enumerate(code[lineNumber]):
                if token.startswith("~+"):
                    number = int(token[2: ], 0)
                    pointer = lineNumber
                    while number > 0:
                        pointer += 1
                        while code[pointer][0].startswith("."):
                            pointer += 1
                        number -= 1
                    code[lineNumber][tokenNumber] = f".relativeLabel{uniqueNumber}"
                    code.insert(pointer, [f".relativeLabel{uniqueNumber}"])
                    return convertRelativesToLabels(code, uniqueNumber + 1)
                elif token.startswith("~-"):
                    number = int(token[2: ], 0)
                    pointer = lineNumber
                    while number > 0:
                        pointer -= 1
                        while code[pointer][0].startswith("."):
                            pointer -= 1
                        number -= 1
                    code[lineNumber][tokenNumber] = f".relativeLabel{uniqueNumber}"
                    code.insert(pointer, [f".relativeLabel{uniqueNumber}"])
                    return convertRelativesToLabels(code, uniqueNumber + 1)
        return code
    
    answer = convertRelativesToLabels(answer)
    
    def convertChar(char: str) -> str:
        if char == "0":
            return "0"
        if char == "1":
            return "1"
        if char == "2":
            return "2"
        if char == "3":
            return "3"
        if char == "4":
            return "4"
        if char == "5":
            return "5"
        if char == "6":
            return "6"
        if char == "7":
            return "7"
        if char == "8":
            return "8"
        if char == "9":
            return "9"
        if char == "A":
            return "10"
        if char == "B":
            return "11"
        if char == "C":
            return "12"
        if char == "D":
            return "13"
        if char == "E":
            return "14"
        if char == "F":
            return "15"
        if char == "G":
            return "16"
        if char == "H":
            return "17"
        if char == "I":
            return "18"
        if char == "J":
            return "19"
        if char == "K":
            return "20"
        if char == "L":
            return "21"
        if char == "M0":
            return "22"
        if char == "M1":
            return "23"
        if char == "N0":
            return "24"
        if char == "N1":
            return "25"
        if char == "O":
            return "26"
        if char == "P":
            return "27"
        if char == "Q":
            return "28"
        if char == "R":
            return "29"
        if char == "S":
            return "30"
        if char == "T":
            return "31"
        if char == "U":
            return "32"
        if char == "V":
            return "33"
        if char == "W0":
            return "34"
        if char == "W1":
            return "35"
        if char == "X":
            return "36"
        if char == "Y":
            return "37"
        if char == "Z":
            return "38"
        if char == "a":
            return "39"
        if char == "b":
            return "40"
        if char == "c":
            return "41"
        if char == "d":
            return "42"
        if char == "e":
            return "43"
        if char == "f":
            return "44"
        if char == "g":
            return "45"
        if char == "h":
            return "46"
        if char == "i":
            return "47"
        if char == "j":
            return "48"
        if char == "k":
            return "49"
        if char == "l":
            return "50"
        if char == "m0":
            return "51"
        if char == "m1":
            return "52"
        if char == "n":
            return "53"
        if char == "o":
            return "54"
        if char == "p":
            return "55"
        if char == "q":
            return "56"
        if char == "r":
            return "57"
        if char == "s":
            return "58"
        if char == "t":
            return "59"
        if char == "u":
            return "60"
        if char == "v":
            return "61"
        if char == "w0":
            return "62"
        if char == "w1":
            return "63"
        if char == "x":
            return "64"
        if char == "y":
            return "65"
        if char == "z":
            return "66"
        if char == "+":
            return "67"
        if char == "-":
            return "68"
        if char == "*":
            return "69"
        if char == "/":
            return "70"
        if char == "=":
            return "71"
        if char == "!":
            return "72"
        if char == "?":
            return "73"
        if char == ":":
            return "74"
        if char == ";":
            return "75"
        if char == "'":
            return "76"
        if char == "_":
            return "77"
        if char == '"':
            return "78"
        if char == "%":
            return "79"
        if char == "^":
            return "80"
        if char == "(":
            return "81"
        if char == ")":
            return "82"
        if char == "[":
            return "83"
        if char == "]":
            return "84"
        if char == "{":
            return "85"
        if char == "}":
            return "86"
        if char == "\\":
            return "87"
        if char == "|":
            return "88"
        if char == "||":
            return "89"
        if char == "<":
            return "90"
        if char == ">":
            return "91"
        if char == "<=":
            return "92"
        if char == ">=":
            return "93"
        if char == ".":
            return "94"
        if char == ",":
            return "95"
        if char == "¬":
            return "96"
        if char == "divison":
            return "97"
        if char == "integral":
            return "98"
        if char in ("sum", "Sigma"):
            return "99"
        if char == "rad":
            return "100"
        if char == "pi":
            return "101"
        if char == "mu":
            return "102"
        if char == "degree":
            return "103"
        if char == "theta":
            return "104"
        if char == "Delta":
            return "105"
        if char == "delta":
            return "106"
        if char in ("Xi", "==", "==="):
            return "107"
        if char == "€":
            return "108"
        if char == "~0":
            return "109"
        if char == "~1":
            return "110"
        if char == "multiply":
            return "111"
        if char in ("dot", "bullet"):
            return "112"
        if char == "lambda":
            return "113"
        if char == "$":
            return "114"
        if char == "£":
            return "115"
        if char == "p0":
            return "116"
        if char == "p1":
            return "117"
        if char == "p2":
            return "118"
        if char == "p3":
            return "119"
        if char == "p4":
            return "120"
        if char == "p5":
            return "121"
        if char == "p6":
            return "122"
        if char == "p7":
            return "123"
        if char == "P0":
            return "124"
        if char == "P1":
            return "125"
        if char == "P2":
            return "126"
        if (char == " ") or (char == ""):
            return "127"
        raise Exception(f"FATAL - Unrecognised char: {char}")
    
    for lineNumber, line in enumerate(answer):
        for tokenNumber, token in enumerate(line):
            if token.startswith("'"):
                char = token[1: -1]
                number = convertChar(char)
                answer[lineNumber][tokenNumber] = number
    
    for line in answer:
        if line[0] == "@DEFINE":
            key = "@" + line[1]
            value = line[2]
            for lineNumber, line2 in enumerate(answer):
                for tokenNumber, token in enumerate(line2):
                    if token == key:
                        answer[lineNumber][tokenNumber] = value
    
    temp = 0
    while temp < len(answer):
        if answer[temp][0] == "@DEFINE":
            answer.pop(temp)
        else:
            temp += 1
    
    return answer
