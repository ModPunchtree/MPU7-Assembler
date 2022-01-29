
from unittest import result
from Pseudo_Assembly_Converter.pseudo_assembly_converter import convertPseudoAssembly
from assembler.assembler import assemble
from tokeniser.tokeniser import tokenise

name = input("File name: ")

f = open(f"MPU7_Code\{name}.mpu7", "r")
code = f.read()
f.close()

code = tokenise(code)

code = convertPseudoAssembly(code)

instructionROM, immediateROM = assemble(code)

# column checksums
nonFlagROMColumns = []
flagROMColumns = []
for column in range(24):
    nonFlagROMColumns.append([instructionROM[0][lineNumber][column] for lineNumber in range(256)])
    flagROMColumns.append([instructionROM[1][lineNumber][column] for lineNumber in range(256)])
    
nonFlagColumnChecksums = [str(sum(nonFlagROMColumns[column])) for column in range(24)]
flagColumnChecksums = [str(sum(flagROMColumns[column])) for column in range(24)]

nonFlagROM = ""
flagROM = ""
nonFlagImmediate = ""
flagImmediate = ""
for lineNumber in range(256):
    if lineNumber < 10:
        flagROM += " "
        nonFlagROM += " "
        nonFlagImmediate += " "
        flagImmediate += " "
    if lineNumber < 100:
        flagROM += " "
        nonFlagROM += " "
        nonFlagImmediate += " "
        flagImmediate += " "
    flagROM += str(lineNumber) + ": "
    nonFlagROM += str(lineNumber) + ": "
    nonFlagImmediate += str(lineNumber) + ": "
    flagImmediate += str(lineNumber) + ": "
    temp = sum(instructionROM[1][lineNumber])
    if temp > 0:
        flagROM += f"{instructionROM[1][lineNumber][: 12]}{instructionROM[1][lineNumber][12: ]} {temp}*\n"
    else:
        flagROM += f"{instructionROM[1][lineNumber][: 12]}{instructionROM[1][lineNumber][12: ]}\n"
    temp = sum(instructionROM[0][lineNumber])
    if temp > 0:
        nonFlagROM += f"{instructionROM[0][lineNumber][: 12]}{instructionROM[0][lineNumber][12: ]} {temp}*\n"
    else:
        nonFlagROM += f"{instructionROM[0][lineNumber][: 12]}{instructionROM[0][lineNumber][12: ]}\n"
    temp = sum(immediateROM[0][lineNumber])
    if temp > 0:
        nonFlagImmediate += f"{immediateROM[0][lineNumber]} {temp}*\n"
    else:
        nonFlagImmediate += f"{immediateROM[0][lineNumber]}\n"
    temp = sum(immediateROM[1][lineNumber])
    if temp > 0:
        flagImmediate += f"{immediateROM[1][lineNumber]} {temp}*\n"
    else:
        flagImmediate += f"{immediateROM[1][lineNumber]}\n"
        
nonflagColumn = "     " + " ".join(nonFlagColumnChecksums[: 12]) + " | " + " ".join(nonFlagColumnChecksums[12: ])
flagColumn = "     " + " ".join(flagColumnChecksums[: 12]) + " | " + " ".join(flagColumnChecksums[12: ])

answer = f"Non-flag Instruction ROM:\n{nonFlagROM}{nonflagColumn}\n\nFlag Instruction ROM:\n{flagROM}{flagColumn}\n\nNon-flag Immediate ROM\n{nonFlagImmediate}\nFlag Immediate ROM\n{flagImmediate}"

print(answer)
