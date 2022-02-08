
def fourByteConvert(bytes: tuple) -> tuple:
    
    answer = [0 for i in range(8)]
    
    for i in range(8):
        number = 15 - (bytes[0][i] + bytes[1][i] * 2 + bytes[2][i] * 4 + bytes[3][i] * 8)
        answer[i] = number
    
    return tuple(answer)

