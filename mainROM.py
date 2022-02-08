
from rom_encoder.stringEncoder import stringEncode

string = """The quick brown
fox jumped over
the lazy dog
"""

# WARNING - Each line must be at least 4 chars long for VSH to work

print(stringEncode(string))


