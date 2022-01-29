
def tokenise(rawCode: str) -> list:
    
    # remove multiline comments
    while rawCode.count("/*") > 0:
        index1 = rawCode.index("/*")
        index2 = rawCode.index("*/") + 2
        rawCode = rawCode[: index1] + rawCode[index2: ]
    
    # convert code to list of lines
    code = rawCode.split("\n")
    
    # remove line comments
    for line in code:
        if line.count("//") > 0:
            line = line[line.index("//"): ]
    
    # remove empty lines
    iteration = 0
    while iteration < len(code):
        if not code[iteration]:
            code.pop(iteration)
        else:
            iteration += 1
        
    # tokenise each line
    answer = []
    for line in code:
        lineAnswer = []
        char = 0
        while char < len(line):
            if line[char].isalnum() or line[char] in ("@", "~", "-", "+", "'", ".", "!"): # .startswith(("NOP", "RST", "ADD", "ADC", "SUB", "SBB", "MOV", "IMM", "INC", "DEC", "NEG", "LSH", "LSC", "RSH", "NOR", "AND", "NOT", "FLG", "SETX", "SETY", "PRT", "VSH", "SPT", "RPT", "HLT", "JMP", "RET", "STL", "FFG", "CLR", "STR", "LOD")):
                text = line[char]
                char += 1
                while line[char].isalnum() or line[char] in ("+", "-"):
                    text += line[char]
                    char += 1
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
                        while code[pointer].startswith("."):
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
                        while code[pointer].startswith("."):
                            pointer -= 1
                        number -= 1
                    code[lineNumber][tokenNumber] = f".relativeLabel{uniqueNumber}"
                    code.insert(pointer, [f".relativeLabel{uniqueNumber}"])
                    return convertRelativesToLabels(code, uniqueNumber + 1)
        return code
    
    answer = convertRelativesToLabels(answer)
    
    return answer
