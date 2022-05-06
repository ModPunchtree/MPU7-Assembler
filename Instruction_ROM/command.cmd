cd C:\Users\gsada\OneDrive\Repositories\MPU7-Assembler\Instruction_ROM
SnbtCmd.exe path "C:\Users\gsada\OneDrive\Repositories\MPU7-Assembler\Instruction_ROM\test_IMMROM.snbt" to-nbt > "test_IMMROM.schematic"
gzip "test_IMMROM.schematic"
rename "C:\Users\gsada\OneDrive\Repositories\MPU7-Assembler\Instruction_ROM\test_IMMROM.schematic.gz" "test_IMMROM.schematic"