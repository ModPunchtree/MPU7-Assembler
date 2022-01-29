
from unittest import result
from Pseudo_Assembly_Converter.pseudo_assembly_converter import convertPseudoAssembly
from assembler.assembler import assemble
from tokeniser.tokeniser import tokenise

name = "test"

f = open(f"MPU7_Code\{name}.mpu7", "r")
code = f.read()
f.close()

code = tokenise(code)

code = convertPseudoAssembly(code)

instructionROM, immediateROM = assemble(code)

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
    if sum(instructionROM[1][lineNumber]) > 0:
        flagROM += f"{instructionROM[1][lineNumber][: 12]}{instructionROM[1][lineNumber][12: ]} *\n"
    else:
        flagROM += f"{instructionROM[1][lineNumber][: 12]}{instructionROM[1][lineNumber][12: ]}\n"
    if sum(instructionROM[0][lineNumber]) > 0:
        nonFlagROM += f"{instructionROM[0][lineNumber][: 12]}{instructionROM[0][lineNumber][12: ]} *\n"
    else:
        nonFlagROM += f"{instructionROM[0][lineNumber][: 12]}{instructionROM[0][lineNumber][12: ]}\n"
    if sum(immediateROM[0][lineNumber]) > 0:
        nonFlagImmediate += f"{immediateROM[0][lineNumber]} *\n"
    else:
        nonFlagImmediate += f"{immediateROM[0][lineNumber]}\n"
    if sum(immediateROM[1][lineNumber]) > 0:
        flagImmediate += f"{immediateROM[1][lineNumber]} *\n"
    else:
        flagImmediate += f"{immediateROM[1][lineNumber]}\n"

answer = f"Non-flag Instruction ROM:\n{nonFlagROM}\nFlag Instruction ROM:\n{flagROM}\nNon-flag Immediate ROM\n{nonFlagImmediate}\nFlag Immediate ROM\n{flagImmediate}"

print(answer)
