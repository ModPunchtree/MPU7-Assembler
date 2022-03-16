
from rom_encoder.generateCommand import generateCommand
from rom_encoder.stringEncoder import stringEncode
from rom_encoder.videoEncoder import videoEncode

string = """
N0N1ever gonna
give you up,
N0N1ever gonna let
you dow0w1n,
N0N1ever gonna run
around and
desert you,
N0N1ever gonna
m0m1ake you cry,
N0N1ever gonna say
goodbye,
N0N1ever gonna
tell a lie and
hurt you :)
"""

string = string[1: ]

# WARNING - Each line must be at least 4 chars long for VSH to work

#print(stringEncode(string))

MacroPixels = 64
Error = 11789
f = open(f"{MacroPixels}_ERROR_{Error}_Bad_Apple.txt", "r")
UniqueMacroPixels, MacroPixelIndexes = f.readlines()
f.close()

bestUniqueMacroPixels = eval(UniqueMacroPixels)
bestMacroPixelIndexes = eval(MacroPixelIndexes)

result = videoEncode(bestMacroPixelIndexes)

answer = ""

for page in range(32):
    temp = str(page)
    if len(temp) < 2:
        temp = " " + temp
    answer += "Page " + temp + ":\n"
    for group in range(64):
        temp = str(group)
        if len(temp) < 2:
            temp = " " + temp
        answer += "    " + temp + ":    "
        line = ""
        for i in result[page][group]:
            if len(str(i)) < 2:
                line += " " + str(i) + "  "
            else:
                line += str(i) + "  "
        answer += line[: -2] + "\n"
    answer += "\n\n"

print(answer)

answer = generateCommand(result, 16)

f = open("command.txt", "w+")
f.write(answer)
f.close()

result = []

for index in range(64):
    signal = []
    for macroY in range(8):
        nible = []
        for macroX in range(4):
            nible.append(bestUniqueMacroPixels[index][macroX][macroY])
        number = nible[0] * 8 + nible[1] * 4 + nible[2] * 2 + nible[3]
        signal.append(number)
    result.append(signal)

answer = ""

for charNum in range(len(result)):
    temp = str(charNum)
    if len(temp) < 2:
        temp = " " + temp
    if charNum % 16 == 0:
        temp = "\n" + temp
    answer += temp + ":    "
    line = ""
    for i in result[charNum]:
        if len(str(i)) < 2:
            line += " " + str(i) + "  "
        else:
            line += str(i) + "  "
    answer += line[: -2] + "\n"

#print(answer)
