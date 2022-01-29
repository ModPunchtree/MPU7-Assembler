
def convertC(operand: str) -> list:
    if operand.startswith("R"):
        number = operand[1:]
        number = int(number, 0)
        number = bin(number)[2: ]
        number = [int(num) for num in number]
        while len(number) < 4:
            number.insert(0, 0)
        if len(number) > 4:
            raise Exception(f"FATAL - Invalid register: {operand}")
        return number
    elif operand == "SR":
        return [1, 0, 1, 1]
    elif operand == "SP":
        return [1, 1, 0, 0]
    elif operand == "RP":
        return [1, 1, 0, 1]
    elif operand == "X":
        return [1, 1, 1, 0]
    elif operand == "Y":
        return [1, 1, 1, 1]
    else:
        raise Exception(f"FATAL - Unrecognised C operand: {operand}")

def convertB(operand: str) -> list:
    if operand.startswith("R"):
        number = operand[1:]
        number = int(number, 0)
        number = bin(number)[2: ]
        number = [int(num) for num in number]
        while len(number) < 4:
            number.insert(0, 0)
        if len(number) > 4:
            raise Exception(f"FATAL - Invalid register: {operand}")
        return number
    elif operand == "IN":
        return [1, 1, 0, 0]
    elif operand == "RP":
        return [1, 1, 0, 1]
    elif operand in ("DS", "DSR"):
        return [1, 1, 1, 0]
    elif operand[0].isnumeric():
        return [1, 0, 1, 1]
    else:
        raise Exception(f"FATAL - Unrecognised B operand: {operand}")

def convertA(operand: str) -> list:
    if operand.startswith("R"):
        number = operand[1:]
        number = int(number, 0)
        number = bin(number)[2: ]
        number = [int(num) for num in number]
        while len(number) < 4:
            number.insert(0, 0)
        if len(number) > 4:
            raise Exception(f"FATAL - Invalid register: {operand}")
        return number
    elif operand == "SR":
        return [1, 1, 0, 0]
    elif operand in ("DS", "DSW"):
        return [1, 1, 0, 1]
    elif operand[0].isnumeric():
        return [1, 0, 1, 1]
    else:
        raise Exception(f"FATAL - Unrecognised A operand: {operand}")

def collisionCheck(indexes: tuple, mirrorROM: list) -> bool:
    
    for index in indexes:
        if mirrorROM[index] == 1:
            return True
    
    return False

def convertFlag(flag: str) -> list:
    if flag == "CF":
        return [0, 0, 1]
    elif flag == "!CF":
        return [0, 1, 0]
    elif flag == "ZF":
        return [0, 1, 1]
    elif flag == "!ZF":
        return [1, 0, 0]
    elif flag == "OD":
        return [1, 0, 1]
    elif flag == "NE":
        return [1, 1, 0]
    elif flag == "IN":
        return [1, 1, 1]
    else:
        raise Exception(f"FATAL - Unrecognised flag: {flag}")

def convertImmediate(immediate: str) -> list:
    number = int(immediate, 0)
    number = bin(number)[2: ]
    number = [int(num) for num in number]
    while len(number) < 8:
        number.insert(0, 0)
    if len(number) > 8:
        raise Exception(f"FATAL - Invalid immediate: {immediate}")
    return number

def assemble(code: list) -> list:
    
    # create non-flag and flag roms
    instructionROM = [[[0 for i in range(24)] for j in range(256)] for k in range(2)]
    
    # create mirror roms
    instructionROMMirror = [[[0 for i in range(24)] for j in range(256)] for k in range(2)]
    
    # create immediate roms
    immediateROM = [[[0 for i in range(8)] for j in range(256)] for k in range(2)]
    
    # create mirror immediate roms
    immediateROMMirror = [[0 for j in range(256)] for k in range(2)]
    
    # go through each line of code
    lineNumber = 0
    for line in code:
    
        # start with non-flag
        flag = 0
        tokenNumber = 0
        
        while tokenNumber < len(line):
                        
            # ; -> flag or end
            if line[tokenNumber] == ";":
                if flag == 0:
                    tokenNumber += 1
                    flag = 1
                else:
                    break

            # ( ) -> error
            elif line[tokenNumber] in ("(", ")"):
                raise Exception(f"FATAL - Bracket error on line: {line}")
            
            elif line[tokenNumber] in ("ADD", "ADC", "NOR", "ACF", "RSH"):
            
                # operation -> read operands
                if line[tokenNumber] == "ADD":
                    if collisionCheck((21, 22), instructionROMMirror[flag][lineNumber]):
                        raise Exception(f"FATAL - Duplicate main operations in line: {line}")
                    instructionROMMirror[flag][lineNumber][21] = 1
                    instructionROMMirror[flag][lineNumber][22] = 1
                    
                elif line[tokenNumber] == "ADC":
                    instructionROM[flag][lineNumber][22] = 1
                    if collisionCheck((21, 22), instructionROMMirror[flag][lineNumber]):
                        raise Exception(f"FATAL - Duplicate main operations in line: {line}")
                    instructionROMMirror[flag][lineNumber][21] = 1
                    instructionROMMirror[flag][lineNumber][22] = 1
                    
                elif line[tokenNumber] == "NOR":
                    instructionROM[flag][lineNumber][21] = 1
                    if collisionCheck((21, 22), instructionROMMirror[flag][lineNumber]):
                        raise Exception(f"FATAL - Duplicate main operations in line: {line}")
                    instructionROMMirror[flag][lineNumber][21] = 1
                    instructionROMMirror[flag][lineNumber][22] = 1
                    
                elif line[tokenNumber] == "ACF":
                    instructionROM[flag][lineNumber][21] = 1
                    if collisionCheck((21, 22), instructionROMMirror[flag][lineNumber]):
                        raise Exception(f"FATAL - Duplicate main operations in line: {line}")
                    instructionROMMirror[flag][lineNumber][21] = 1
                    instructionROMMirror[flag][lineNumber][22] = 1
                    
                elif line[tokenNumber] == "RSH":
                    instructionROM[flag][lineNumber][21] = 1
                    instructionROM[flag][lineNumber][22] = 1
                    if collisionCheck((21, 22), instructionROMMirror[flag][lineNumber]):
                        raise Exception(f"FATAL - Duplicate main operations in line: {line}")
                    instructionROMMirror[flag][lineNumber][21] = 1
                    instructionROMMirror[flag][lineNumber][22] = 1
                    
                else:
                    raise Exception(f"FATAL - Unrecognised operation: {line[tokenNumber]}")
                
                tokenNumber += 2
                operand1 = line[tokenNumber]
                operand1Binary = convertC(operand1)
                if collisionCheck((3, 4, 5, 6), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate C operand in line: {line}")
                for i in range(4):
                    instructionROM[flag][lineNumber][3 + i] = operand1Binary[i]
                    instructionROMMirror[flag][lineNumber][3 + i] = 1

                tokenNumber += 1
                operand2 = line[tokenNumber]
                if operand2.startswith("!"):
                    operand2 = operand2[1: ]
                    if collisionCheck((18, ), instructionROMMirror[flag][lineNumber]):
                        raise Exception(f"FATAL - Duplicate A side invert in line: {line}")
                    instructionROMMirror[flag][lineNumber][lineNumber][18] = 1
                else:
                    if collisionCheck((18, ), instructionROMMirror[flag][lineNumber]):
                        raise Exception(f"FATAL - Duplicate A side invert in line: {line}")
                    instructionROM[flag][lineNumber][18] = 1
                    instructionROMMirror[flag][lineNumber][18] = 1
                if operand2[0].isnumeric():
                    immediate = convertImmediate(operand2)
                    if immediateROMMirror[flag][lineNumber] == 1:
                        if immediate != immediateROM[flag][lineNumber]:
                            raise Exception(f"FATAL - Duplicate immediate values in line: {line}")
                    for i in range(8):
                        immediateROM[flag][lineNumber][i] = immediate[i]
                    immediateROMMirror[flag][lineNumber] = 1
                operand2Binary = convertA(operand2)
                if collisionCheck((13, 14, 15, 16), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate A operand in line: {line}")
                for i in range(4):
                    instructionROM[flag][lineNumber][13 + i] = operand2Binary[i]
                    instructionROMMirror[flag][lineNumber][13 + i] = 1
                
                tokenNumber += 1
                operand3 = line[tokenNumber]
                if operand3.startswith("!"):
                    operand3 = operand3[1: ]
                    if collisionCheck((17, ), instructionROMMirror[flag][lineNumber]):
                        raise Exception(f"FATAL - Duplicate B side invert in line: {line}")
                    instructionROMMirror[flag][lineNumber][17] = 1
                else:
                    if collisionCheck((17, ), instructionROMMirror[flag][lineNumber]):
                        raise Exception(f"FATAL - Duplicate B side invert in line: {line}")
                    instructionROM[flag][lineNumber][17] = 1
                    instructionROMMirror[flag][lineNumber][17] = 1
                if operand3[0].isnumeric():
                    immediate = convertImmediate(operand3)
                    if immediateROMMirror[flag][lineNumber] == 1:
                        if immediate != immediateROM[flag][lineNumber]:
                            raise Exception(f"FATAL - Duplicate immediate values in line: {line}")
                    for i in range(8):
                        immediateROM[flag][lineNumber][i] = immediate[i]
                    immediateROMMirror[flag][lineNumber] = 1
                operand3Binary = convertB(operand3)
                if collisionCheck((7, 8, 9, 10), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate B operand in line: {line}")
                for i in range(4):
                    instructionROM[flag][lineNumber][7 + i] = operand3Binary[i]
                    instructionROMMirror[flag][lineNumber][7 + i] = 1
                
                # fix R0 inverts
                if operand2 in ("R0", "DS", "DSW", "VSH", "HLT"):
                    instructionROM[flag][lineNumber][18] = 1 - instructionROM[flag][lineNumber][18]
                if operand3 in ("R0", "CLR"):
                    instructionROM[flag][lineNumber][17] = 1 - instructionROM[flag][lineNumber][17]
                
                tokenNumber += 2
                
            elif line[tokenNumber] == "FLG":
                tokenNumber += 2
                operand1 = line[tokenNumber]
                operand1Binary = convertFlag(operand1)
                if collisionCheck((0, 1, 2), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate flag operation in line: {line}")
                for i in range(3):
                    instructionROM[flag][lineNumber][i] = operand1Binary[i]
                    instructionROMMirror[flag][lineNumber][i] = 1
                
                tokenNumber += 2
                
            elif line[tokenNumber] == "VSH":
                if collisionCheck((13, 14, 15, 16), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate A operation (VSH) in line: {line}")
                binary = [1, 1, 1, 0]
                for i in range(4):
                    instructionROM[flag][lineNumber][13 + i] = binary[i]
                    instructionROMMirror[flag][lineNumber][13 + i] = 1
                
                tokenNumber += 3
                
            elif line[tokenNumber] == "SPT":
                if collisionCheck((23, ), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate SPT operation in line: {line}")
                instructionROM[flag][lineNumber][23] = 1
                instructionROMMirror[flag][lineNumber][23] = 1
                
                tokenNumber += 2
                immediate = line[tokenNumber]
                immediate = convertImmediate(immediate)
                if immediateROMMirror[flag][lineNumber] == 1:
                    if immediate != immediateROM[flag][lineNumber]:
                        raise Exception(f"FATAL - Duplicate immediate values in line: {line}")
                for i in range(8):
                    immediateROM[flag][lineNumber][i] = immediate[i]
                immediateROMMirror[flag][lineNumber] = 1
                
                tokenNumber += 2
                
            elif line[tokenNumber] == "RPT":
                if collisionCheck((11, 12), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate branch operation (RPT) in line: {line}")
                instructionROM[flag][lineNumber][11] = 1
                instructionROM[flag][lineNumber][12] = 1
                instructionROMMirror[flag][lineNumber][11] = 1
                instructionROMMirror[flag][lineNumber][12] = 1
                
                tokenNumber += 2
                immediate = line[tokenNumber]
                immediate = convertImmediate(immediate)
                if immediateROMMirror[flag][lineNumber] == 1:
                    if immediate != immediateROM[flag][lineNumber]:
                        raise Exception(f"FATAL - Duplicate immediate values in line: {line}")
                for i in range(8):
                    immediateROM[flag][lineNumber][i] = immediate[i]
                immediateROMMirror[flag][lineNumber] = 1
                
                tokenNumber += 2
                
            elif line[tokenNumber] == "HLT":
                if collisionCheck((13, 14, 15, 16), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate A operation (HLT) in line: {line}")
                binary = [1, 1, 1, 1]
                for i in range(4):
                    instructionROM[flag][lineNumber][13 + i] = binary[i]
                    instructionROMMirror[flag][lineNumber][13 + i] = 1
                
                tokenNumber += 3
                
            elif line[tokenNumber] == "JMP":
                if collisionCheck((11, 12), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate branch operation in line: {line}")
                instructionROM[flag][lineNumber][12] = 1
                instructionROMMirror[flag][lineNumber][11] = 1
                instructionROMMirror[flag][lineNumber][12] = 1
                
                tokenNumber += 2
                immediate = line[tokenNumber]
                immediate = convertImmediate(immediate)
                if immediateROMMirror[flag][lineNumber] == 1:
                    if immediate != immediateROM[flag][lineNumber]:
                        raise Exception(f"FATAL - Duplicate immediate values in line: {line}")
                for i in range(8):
                    immediateROM[flag][lineNumber][i] = immediate[i]
                immediateROMMirror[flag][lineNumber] = 1
                
                tokenNumber += 2
                
            elif line[tokenNumber] == "RET":
                if collisionCheck((11, 12), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate branch operation in line: {line}")
                instructionROM[flag][lineNumber][11] = 1
                instructionROMMirror[flag][lineNumber][11] = 1
                instructionROMMirror[flag][lineNumber][12] = 1
            
                tokenNumber += 3
                
            elif line[tokenNumber] == "STL":
                if collisionCheck((20, ), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate stall operation in line: {line}")
                instructionROM[flag][lineNumber][20] = 1
                instructionROMMirror[flag][lineNumber][20] = 1
                
                tokenNumber += 3
            
            elif line[tokenNumber] == "FFG":
                if collisionCheck((19, ), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate force flag operation in line: {line}")
                instructionROM[flag][lineNumber][19] = 1
                instructionROMMirror[flag][lineNumber][19] = 1
                
                tokenNumber += 3
            
            elif line[tokenNumber] == "CLR":
                if collisionCheck((7, 8, 9, 10), instructionROMMirror[flag][lineNumber]):
                    raise Exception(f"FATAL - Duplicate B operation (CLR) in line: {line}")
                binary = [1, 1, 1, 1]
                for i in range(4):
                    instructionROM[flag][lineNumber][7 + i] = binary[i]
                    instructionROMMirror[flag][lineNumber][7 + i] = 1
                
                tokenNumber += 3
            
            else:
                raise Exception(f"FATAL - Unrecognised operation: {line[tokenNumber]}")
            
            # check if bits have already been written
            # if its an immediate check if its the same, if not -> error
            # write bits into roms as they are read
        
        lineNumber += 1
    
    return instructionROM, immediateROM
