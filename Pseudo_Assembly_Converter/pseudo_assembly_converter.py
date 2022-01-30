
def convertPseudoAssembly(code: list) -> list:
    
    for lineNumber in range(len(code)):
        line = code[lineNumber]
        tokenNumber = 0
        while tokenNumber < len(code[lineNumber]):
            line = code[lineNumber]
            token = line[tokenNumber]
            
            if token == "NOP":
                newTokens = ["ADD", "(", "R0", "R0", "R0", ")"]
                code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 3: ]
                tokenNumber += 1
                
            elif token == "RST":
                newTokens = ["ADD", "(", line[tokenNumber + 2], "R0", "R0", ")"]
                code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                tokenNumber += 1
            
            elif token == "ADD":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 3:
                    tokenNumber += 1
                elif opCount == 2:
                    newTokens = ["ADD", "(", line[tokenNumber + 2], line[tokenNumber + 2], line[tokenNumber + 3], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
                
            elif token == "ADC":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 3:
                    tokenNumber += 1
                elif opCount == 2:
                    newTokens = ["ADC", "(", line[tokenNumber + 2], line[tokenNumber + 2], line[tokenNumber + 3], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "SUB":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 3:
                    newTokens = ["ADC", "(", line[tokenNumber + 2], line[tokenNumber + 3], "!" + line[tokenNumber + 4], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 6: ]
                    tokenNumber += 1
                elif opCount == 2:
                    newTokens = ["ADC", "(", line[tokenNumber + 2], line[tokenNumber + 2], "!" + line[tokenNumber + 3], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "SBB":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 3:
                    newTokens = ["ADD", "(", line[tokenNumber + 2], line[tokenNumber + 3], "!" + line[tokenNumber + 4], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 6: ]
                    tokenNumber += 1
                elif opCount == 2:
                    newTokens = ["ADD", "(", line[tokenNumber + 2], line[tokenNumber + 2], "!" + line[tokenNumber + 3], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token in ("MOV", "IMM"):
                newTokens = ["ADD", "(", line[tokenNumber + 2], line[tokenNumber + 3], "R0", ")"]
                code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                tokenNumber += 1
            
            elif token == "INC":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 2:
                    newTokens = ["ADC", "(", line[tokenNumber + 2], line[tokenNumber + 3], "R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                elif opCount == 1:
                    newTokens = ["ADC", "(", line[tokenNumber + 2], line[tokenNumber + 2], "R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "DEC":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 2:
                    newTokens = ["ADD", "(", line[tokenNumber + 2], line[tokenNumber + 3], "!R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                elif opCount == 1:
                    newTokens = ["ADD", "(", line[tokenNumber + 2], line[tokenNumber + 2], "!R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "NEG":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 2:
                    newTokens = ["ADC", "(", line[tokenNumber + 2], "!" + line[tokenNumber + 3], "R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                elif opCount == 1:
                    newTokens = ["ADC", "(", line[tokenNumber + 2], "!" + line[tokenNumber + 2], "R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "LSH":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 2:
                    newTokens = ["ADD", "(", line[tokenNumber + 2], line[tokenNumber + 3], line[tokenNumber + 3], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                elif opCount == 1:
                    newTokens = ["ADD", "(", line[tokenNumber + 2], line[tokenNumber + 2], line[tokenNumber + 2], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "LSC":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 2:
                    newTokens = ["ADC", "(", line[tokenNumber + 2], line[tokenNumber + 3], line[tokenNumber + 3], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                elif opCount == 1:
                    newTokens = ["ADC", "(", line[tokenNumber + 2], line[tokenNumber + 2], line[tokenNumber + 2], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "RSH":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 2:
                    newTokens = ["RSH", "(", line[tokenNumber + 2], line[tokenNumber + 3], "R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                elif opCount == 1:
                    newTokens = ["RSH", "(", line[tokenNumber + 2], line[tokenNumber + 2], "R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "NOR":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 3:
                    tokenNumber += 1
                elif opCount == 2:
                    newTokens = ["NOR", "(", line[tokenNumber + 2], line[tokenNumber + 2], line[tokenNumber + 3], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "AND":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 3:
                    newTokens = ["NOR", "(", line[tokenNumber + 2], "!" + line[tokenNumber + 3], "!" + line[tokenNumber + 4], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 6: ]
                    tokenNumber += 1
                elif opCount == 2:
                    newTokens = ["NOR", "(", line[tokenNumber + 2], "!" + line[tokenNumber + 2], "!" + line[tokenNumber + 3], ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "NOT":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 2:
                    newTokens = ["ADD", "(", line[tokenNumber + 2], "!" + line[tokenNumber + 3], "R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 5: ]
                    tokenNumber += 1
                elif opCount == 1:
                    newTokens = ["ADD", "(", line[tokenNumber + 2], "!" + line[tokenNumber + 2], "R0", ")"]
                    code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                    tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "SETX":
                newTokens = ["ADD", "(", "X", line[tokenNumber + 2], "R0", ")"]
                code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                tokenNumber += 1
            
            elif token == "SETY":
                newTokens = ["ADD", "(", "Y", line[tokenNumber + 2], "R0", ")"]
                code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                tokenNumber += 1
            
            elif token == "PRT":
                newTokens = ["ADD", "(", "R0", "DS", line[tokenNumber + 2], ")"]
                code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                tokenNumber += 1
                
            elif token == "STL":
                opCount = 0
                pointer = tokenNumber + 2
                while line[pointer] != ")":
                    pointer += 1
                    opCount += 1
                if opCount == 0:
                    tokenNumber += 1
                elif opCount == 1:
                    if line[tokenNumber + 2] == "RET":
                        newTokens = ["STL", "(", ")", "RET", "(", ")"]
                        code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                        tokenNumber += 1
                    else:
                        newTokens = ["STL", "(", ")", "JMP", "(", line[tokenNumber + 2], ")"]
                        code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                        tokenNumber += 1
                else:
                    raise Exception(f"FATAL - Invalid number of operands in line: {line}")
            
            elif token == "STR":
                newTokens = ["ADD", "(", "SR", line[tokenNumber + 2], "R0", ")"]
                code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                tokenNumber += 1
                
            elif token == "LOD":
                newTokens = ["ADD", "(", line[tokenNumber + 2], "SR", "R0", ")"]
                code[lineNumber] = line[: tokenNumber] + newTokens + line[tokenNumber + 4: ]
                tokenNumber += 1
            
            else:
                tokenNumber += 1
    
    # convert labels to literals
    lineNumber = 0
    labelDefinitions = []
    while lineNumber < len(code):
        if code[lineNumber][0].startswith("."):
            labelDefinitions.append([code[lineNumber][0], str(lineNumber)])
            code.pop(lineNumber)
        else:
            lineNumber += 1

    names = [i[0] for i in labelDefinitions]
    lineNumber = 0
    while lineNumber < len(code):
        tokenNumber = 0
        while tokenNumber < len(code[lineNumber]):
            if code[lineNumber][tokenNumber].startswith("."):
                number = labelDefinitions[names.index(code[lineNumber][tokenNumber])][1]
                code[lineNumber][tokenNumber] = number
            tokenNumber += 1
        lineNumber += 1
    
    return code
