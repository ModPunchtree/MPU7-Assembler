# MPU7-Assembler

MPU7 Assembler and URCL converter written in Python.

To assemble MPU7 code:

Place .mpu7 file containing MPU7 assembly in the MPU7_Code folder

Run main.py and enter in the name of the file without the .mpu7 extention

It will generate 2 new .schematic files in the Instruction_ROM folder (the file directory will need changing in the assemblyToSchem.py file to wherever the repo is on your computer)

Paste in the generated schematics on top of the instruction ROM and Immediate ROM (ask in the URCL discord if you can't figure out where these are located)

Reset and then run the CPU (make sure clock is off before reseting!!)

To convert URCL to MPU7 assembly:

Place the .urcl file containing URCL code in the URCL and B code folder

Run main2.py and enter in the name if the file without the .urcl file extention

It will print out the translated code into the console - copy paste this into a .mpu7 file if you want to assemble it

Warning - Millage may vary with this, and if something goes wrong with this it will be mostly up to you to debug.
I won't be maintaining this code as I am mostly finished with the MPU7

Feel free to ask me questions in the URCL discord if you need to: https://discord.gg/Nv8jzWg5j8
