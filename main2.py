
from URCLtranslator.URCLtokeniser import getURCL
from URCLtranslator.translate import translateToMPU7

URCL = getURCL()

MPU7 = translateToMPU7(URCL)

print("\n".join([" ".join(line) for line in URCL]))
print("\n\n")
print(MPU7)









