
from os import system

def fetchEmptyInstructionROM() -> tuple:
    
    f = open("Instruction_ROM\MPU7ROM.snbt", "r")
    result = f.read()
    f.close()
    
    index = result.index("BlockData:") + len("BlockData:")
    start = result[: index]
    result = result[index: ]
    index = result.index("]") + 1
    end = result[index: ]
    result = result[: index]
    result = result.replace("b", "")
    result = result.replace("B;", "")
    result = eval(result)
    
    return start, result, end

def fetchEmptyImmediateROM() -> tuple:

    f = open("Instruction_ROM\MPU7IMMROM.snbt", "r")
    result = f.read()
    f.close()
    
    index = result.index("BlockData:") + len("BlockData:")
    start = result[: index]
    result = result[index: ]
    index = result.index("]") + 1
    end = result[index: ]
    result = result[: index]
    result = result.replace("b", "")
    result = result.replace("B;", "")
    result = eval(result)
    
    return start, result, end

def generateInstructionROM(instructionROM: list, immediateROM: list, name: str) -> None:
    
    start, outputBlocks, end = fetchEmptyInstructionROM()

    lengthX = 68
    lengthY = 38
    lengthZ = 54
    
    for flag in range(2):
        for instruction in range(256):
            for bit in range(24):
                value = instructionROM[flag][instruction][bit]
                
                if value == 1:
                    # x coord
                    blockX = lengthX - ((instruction & 63) + ((instruction & 63) >> 4)) - 2
                    
                    # y coord
                    blockY = (instruction >> 6) * 5
                    if bit in (0, 22):
                        blockY += 1
                    elif bit == 23:
                        blockY += 2
                    if flag == 0:
                        blockY += 20
                    
                    # z coord
                    if bit == 0:
                        blockZ = 0
                    elif bit == 22:
                        blockZ = lengthZ - 2
                    elif bit == 23:
                        blockZ = lengthZ - 1
                    elif bit < 12:
                        blockZ = (bit << 1) - 1
                    else:
                        blockZ = 33 + ((bit - 12) << 1)
                        
                    blockIndex = blockX + (blockZ * lengthX) + (blockY * lengthX * lengthZ)
                    
                    if bit == 0:
                        outputBlocks[blockIndex] = 3 # south observer
                    elif bit >= 22:
                        outputBlocks[blockIndex] = 5 # north observer
                    else:
                        outputBlocks[blockIndex] = 4 # upwards observer
    
    outputBlocks = str(outputBlocks).replace(" ", "")
    outputBlocks = outputBlocks[: -1] + "b]"
    outputBlocks = "[B;" + outputBlocks[1: ]
    outputBlocks = outputBlocks.replace(",", "b,")
    
    result = start + outputBlocks + end
    
    f = open(f"Instruction_ROM\{name}.snbt", "w")
    f.write(result)
    f.close()
    
    command = f"cd C:\\Users\\gsada\\OneDrive\\Repositories\\MPU7-Assembler\\Instruction_ROM\nSnbtCmd.exe path \"C:\\Users\\gsada\\OneDrive\\Repositories\\MPU7-Assembler\\Instruction_ROM\\{name}.snbt\" to-nbt > \"{name}.schematic\"\ngzip \"{name}.schematic\"\nrename \"C:\\Users\\gsada\\OneDrive\\Repositories\\MPU7-Assembler\\Instruction_ROM\\{name}.schematic.gz\" \"{name}.schematic\""
    f = open("Instruction_ROM\command.cmd", "w")
    f.write(command)
    f.close()
    
    system("C:\\Users\\gsada\\OneDrive\\Repositories\\MPU7-Assembler\\Instruction_ROM\\command.cmd")

    ################################################################################
    
    # Immediate ROM
    
    ################################################################################

    start, outputBlocks, end = fetchEmptyImmediateROM()

    lengthX = 67
    lengthY = 33
    lengthZ = 41

    for flag in range(2):
        for instruction in range(256):
            for bit in range(8):
                value = immediateROM[flag][instruction][bit]
                
                # x coord
                blockX = (63 - ((instruction & 31) << 1))
                if (instruction + 1) & 7:
                    blockX -= (1 - ((7 - bit) & 1))
                
                # y coord
                if instruction & 1:
                    if (instruction + 1) & 7:
                        blockY = ((((7 - bit) + 1) - (((7 - bit) + 1) & 1)) << 1) + (1 - ((7 - bit) & 1))
                    else:
                        blockY = 2 + ((7 - bit) << 1)
                else:
                    blockY = 2 + (((7 - bit) - ((7 - bit) & 1)) << 1) + ((7 - bit) & 1)
                if flag == 0:
                    blockY += 16
                
                # z coord
                blockZ = (36, 34, 26, 24, 16, 14, 6, 4)[instruction >> 5]
                
                blockIndex = blockX + (blockZ * lengthX) + (blockY * lengthX * lengthZ)
                
                
                if ((instruction + 1) & 7 == 0) and (bit & 1):
                    if value == 1:
                        outputBlocks[blockIndex] = 4 # torch east
                    else:
                        outputBlocks[blockIndex] = 0 # glowstone
                elif (instruction >> 5) & 1:
                    if value == 1:
                        outputBlocks[blockIndex] = 5 # torch south
                    else:
                        outputBlocks[blockIndex] = 0 # glowstone
                else:
                    if value == 1:
                        outputBlocks[blockIndex] = 1 # torch north
                    else:
                        outputBlocks[blockIndex] = 0 # glowstone
                    
    outputBlocks = str(outputBlocks).replace(" ", "")
    outputBlocks = outputBlocks[: -1] + "b]"
    outputBlocks = "[B;" + outputBlocks[1: ]
    outputBlocks = outputBlocks.replace(",", "b,")
    
    result = start + outputBlocks + end
    
    f = open(f"Instruction_ROM\{name}_IMMROM.snbt", "w")
    f.write(result)
    f.close()
    
    command = f"cd C:\\Users\\gsada\\OneDrive\\Repositories\\MPU7-Assembler\\Instruction_ROM\nSnbtCmd.exe path \"C:\\Users\\gsada\\OneDrive\\Repositories\\MPU7-Assembler\\Instruction_ROM\\{name}_IMMROM.snbt\" to-nbt > \"{name}_IMMROM.schematic\"\ngzip \"{name}_IMMROM.schematic\"\nrename \"C:\\Users\\gsada\\OneDrive\\Repositories\\MPU7-Assembler\\Instruction_ROM\\{name}_IMMROM.schematic.gz\" \"{name}_IMMROM.schematic\""
    f = open("Instruction_ROM\command.cmd", "w")
    f.write(command)
    f.close()
    
    system("C:\\Users\\gsada\\OneDrive\\Repositories\\MPU7-Assembler\\Instruction_ROM\\command.cmd")






