
from rom_encoder.stringEncoder import stringEncode

string = """The quick brow0w1n
fox jum0m1ped over
the lazy dog
"""

# WARNING - Each line must be at least 4 chars long for VSH to work

print(stringEncode(string))


