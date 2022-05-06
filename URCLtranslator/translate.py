
from copy import deepcopy
from URCLtranslator.translations import translate

def translateToMPU7(URCL: list) -> str:
    MPU7 = "RST(R9) STL(~+0) FLG(!CF); IMM(R10, 128);\n"

    DWcount = 0
    lineNumber = 0
    while lineNumber < len(URCL):
        line = URCL[lineNumber]
        if line[0] == "DW":
            temp = []
            lineNumber2 = lineNumber - 1
            if lineNumber2 > -1:
                while URCL[lineNumber2][0].startswith("."):
                    temp.append(URCL[lineNumber2])
                    URCL.pop(lineNumber2)
                    lineNumber -= 1
                    lineNumber2 -= 1
                    if lineNumber2 < 0:
                        break
                temp = temp[: : -1]
                for label in temp:
                    for i, j in enumerate(URCL):
                        for k, l in enumerate(j):
                            if l == label:
                                URCL[i][k] = str(DWcount) # replace DW label references with RAM location of DW value
            MPU7 += f"// {line[0]} {line[1]}\n" + translate(line[0], line[1]) + "\n"
            URCL.pop(lineNumber)
            DWcount += 1

        else:
            lineNumber += 1
            
    if MPU7 == "RST(R9) STL(~+0) FLG(!CF); IMM(R10, 128);\n":
        MPU7 = "IMM(R10, 128);;\n"
    elif MPU7.endswith("INC(R9) STL(~+1);;\n"):
        MPU7 = MPU7[: -(len("INC(R9) STL(~+1);;\n"))]

    for line in URCL:
        if len(line) == 1:
            if line[0].startswith("."):
                MPU7 += translate(line[0]) + "\n"
            else:
                MPU7 += f"// {line[0]}\n" + translate(line[0]) + "\n"
        elif len(line) == 2:
            MPU7 += f"// {line[0]} {line[1]}\n" + translate(line[0], line[1]) + "\n"
        elif len(line) == 3:
            MPU7 += f"// {line[0]} {line[1]} {line[2]}\n" + translate(line[0], line[1], line[2]) + "\n"
        elif len(line) == 4:
            MPU7 += f"// {line[0]} {line[1]} {line[2]} {line[3]}\n" + translate(line[0], line[1], line[2], line[3]) + "\n"

    MPU7 = MPU7[: -1]
    
    # translate M prepended values
    for number in range(128):
        MPU7.replace(f"M{number}", f"{number + DWcount}")
    
    instructionTotal = MPU7.count(";") >> 1
    if instructionTotal > 256:
        raise Exception(f"FATAL - Translated code is too long for MPU 7 ROM - Code is {instructionTotal} lines long, the maximum is 256.")
    
    return MPU7





