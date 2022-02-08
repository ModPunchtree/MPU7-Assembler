
from rom_encoder.fourByteConverter import fourByteConvert

def stringEncode(string: str) -> tuple:
    
    source = []
    index = 0
    while index < len(string):
        loop = 0
        char = string[index: index + loop + 1]
        if char == "\n":
            source[-2][7] = 1
        else:
            while True:
                try:
                    number = convertChar(char)
                    index += len(char) - 1
                    break
                except Exception:
                    loop += 1
                    if index + loop > len(string):
                        raise Exception(f"Fatal - Invalid char: {string[index]}")
                    char = string[index: index + loop]
            number = int(number)
            number = bin(number)[2:]
            while len(number) < 8:
                number = "0" + number
            number = number[: : -1]
            byte = []
            for num in number:
                byte.append(int(num))
            source.append(byte)
        index += 1
    
    count = len(source) // 4
    number = len(source) % 4
    if number > 0:
        count += 1
    number = 4 - number
    while (number < 4) and (number > 0):
        source.append([0 for i in range(8)])
        number -= 1
    
    answer = [fourByteConvert(source[i * 4: i * 4 + 4]) for i in range(count)]
    
    while len(answer) < 64:
        answer.append(tuple([0 for i in range(8)]))
    
    return tuple(answer)

def convertChar(char: str) -> str:
    if char == "0":
        return "0"
    if char == "1":
        return "1"
    if char == "2":
        return "2"
    if char == "3":
        return "3"
    if char == "4":
        return "4"
    if char == "5":
        return "5"
    if char == "6":
        return "6"
    if char == "7":
        return "7"
    if char == "8":
        return "8"
    if char == "9":
        return "9"
    if char == "A":
        return "10"
    if char == "B":
        return "11"
    if char == "C":
        return "12"
    if char == "D":
        return "13"
    if char == "E":
        return "14"
    if char == "F":
        return "15"
    if char == "G":
        return "16"
    if char == "H":
        return "17"
    if char == "I":
        return "18"
    if char == "J":
        return "19"
    if char == "K":
        return "20"
    if char == "L":
        return "21"
    if char == "M0":
        return "22"
    if char == "M1":
        return "23"
    if char == "N0":
        return "24"
    if char == "N1":
        return "25"
    if char == "O":
        return "26"
    if char == "P":
        return "27"
    if char == "Q":
        return "28"
    if char == "R":
        return "29"
    if char == "S":
        return "30"
    if char == "T":
        return "31"
    if char == "U":
        return "32"
    if char == "V":
        return "33"
    if char == "W0":
        return "34"
    if char == "W1":
        return "35"
    if char == "X":
        return "36"
    if char == "Y":
        return "37"
    if char == "Z":
        return "38"
    if char == "a":
        return "39"
    if char == "b":
        return "40"
    if char == "c":
        return "41"
    if char == "d":
        return "42"
    if char == "e":
        return "43"
    if char == "f":
        return "44"
    if char == "g":
        return "45"
    if char == "h":
        return "46"
    if char == "i":
        return "47"
    if char == "j":
        return "48"
    if char == "k":
        return "49"
    if char == "l":
        return "50"
    if char == "m0":
        return "51"
    if char == "m1":
        return "52"
    if char == "n":
        return "53"
    if char == "o":
        return "54"
    if char == "p":
        return "55"
    if char == "q":
        return "56"
    if char == "r":
        return "57"
    if char == "s":
        return "58"
    if char == "t":
        return "59"
    if char == "u":
        return "60"
    if char == "v":
        return "61"
    if char == "w0":
        return "62"
    if char == "w1":
        return "63"
    if char == "x":
        return "64"
    if char == "y":
        return "65"
    if char == "z":
        return "66"
    if char == "+":
        return "67"
    if char == "-":
        return "68"
    if char == "*":
        return "69"
    if char == "/":
        return "70"
    if char == "=":
        return "71"
    if char == "!":
        return "72"
    if char == "?":
        return "73"
    if char == ":":
        return "74"
    if char == ";":
        return "75"
    if char == "'":
        return "76"
    if char == "_":
        return "77"
    if char == '"':
        return "78"
    if char == "%":
        return "79"
    if char == "^":
        return "80"
    if char == "(":
        return "81"
    if char == ")":
        return "82"
    if char == "[":
        return "83"
    if char == "]":
        return "84"
    if char == "{":
        return "85"
    if char == "}":
        return "86"
    if char == "\\":
        return "87"
    if char == "|":
        return "88"
    if char == "||":
        return "89"
    if char == "<":
        return "90"
    if char == ">":
        return "91"
    if char == "<=":
        return "92"
    if char == ">=":
        return "93"
    if char == ".":
        return "94"
    if char == ",":
        return "95"
    if char == "¬":
        return "96"
    if char == "divison":
        return "97"
    if char == "integral":
        return "98"
    if char in ("sum", "Sigma"):
        return "99"
    if char == "rad":
        return "100"
    if char == "pi":
        return "101"
    if char == "mu":
        return "102"
    if char == "degree":
        return "103"
    if char == "theta":
        return "104"
    if char == "Delta":
        return "105"
    if char == "delta":
        return "106"
    if char in ("Xi", "==", "==="):
        return "107"
    if char == "€":
        return "108"
    if char == "~0":
        return "109"
    if char == "~1":
        return "110"
    if char == "multiply":
        return "111"
    if char in ("dot", "bullet"):
        return "112"
    if char == "lambda":
        return "113"
    if char == "$":
        return "114"
    if char == "£":
        return "115"
    if char == "p0":
        return "116"
    if char == "p1":
        return "117"
    if char == "p2":
        return "118"
    if char == "p3":
        return "119"
    if char == "p4":
        return "120"
    if char == "p5":
        return "121"
    if char == "p6":
        return "122"
    if char == "p7":
        return "123"
    if char == "P0":
        return "124"
    if char == "P1":
        return "125"
    if char == "P2":
        return "126"
    if char == " ":
        return "127"
    raise Exception(f"FATAL - Unrecognised char: {char}")

