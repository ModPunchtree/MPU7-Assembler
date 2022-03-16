
from rom_encoder.fourByteConverter import fourByteConvert

def videoEncode(macroPixelIndexes: list) -> tuple:
    
    source = []
    
    # macroPixelIndexes[frameNumber][macroX][macroY]
    
    for frameNumber in range(416):
        for macroY in range(2, -1, -1):
            for macroX in range(0, 8, 4):
                group = []
                for index in range(4):
                    macroPixel = macroPixelIndexes[frameNumber][macroX + index][macroY]
                    macroPixel = bin(macroPixel)[2: ]
                    while len(macroPixel) < 6:
                        macroPixel = "0" + macroPixel
                    macroPixel = macroPixel[: : -1]
                    group.append(macroPixel)
                last = group[3]
                group[0] = group[0] + last[0: 2]
                group[1] = group[1] + last[2: 4]
                group[2] = group[2] + last[4: 6]
                group.pop(3)
                for byte in group:
                    source.append([int(bit) for bit in byte])
    
    source += [[0 for j in range(8)] for i in range(72)]
    
    answer = []
    
    for pageNumber in range(30):
        page = []
        for frame0 in range(7):
            for byteNumber in range(0, 18 * 2, 4):
                group2 = []
                for i in range(4):
                    group2.append(source[byteNumber + frame0 * (18 * 2) + i + pageNumber * (18 * 14)])
                page.append(fourByteConvert(group2))
        page.append((0, 0, 0, 0, 0, 0, 0, 0))
        answer.append(page)

    for i in range(2):
        page = [tuple([0 for j in range(8)]) for k in range(64)]
        answer.append(page)

    return tuple(answer)

