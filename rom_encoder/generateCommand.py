
def itemNumber(signalStrength: int) -> int:
    if signalStrength == 0:
        return 0
    if signalStrength == 1:
        return 1
    if signalStrength == 2:
        return 2
    if signalStrength == 3:
        return 4
    if signalStrength == 4:
        return 6
    if signalStrength == 5:
        return 8
    if signalStrength == 6:
        return 10
    if signalStrength == 7:
        return 12
    if signalStrength == 8:
        return 14
    if signalStrength == 9:
        return 16
    if signalStrength == 10:
        return 18
    if signalStrength == 11:
        return 20
    if signalStrength == 12:
        return 22
    if signalStrength == 13:
        return 24
    if signalStrength == 14:
        return 26
    if signalStrength == 15:
        return 27
    raise Exception(f"FATAL - Invalid signal strength: {signalStrength}")

def generateBarrel(x: int, y: int, z: int, signalStrength):
    
    barrel = f"clone {1641 + signalStrength} 80 483 {1641 + signalStrength} 80 483 {x} {y} {z}"
    
    return barrel

def generateCommand(source: tuple, dumb: int) -> str:
    
    command = "summon falling_block ~ ~.5 ~ {Time:1,BlockState:{" + """Name:redstone_block},Passengers:[{id:armor_stand,Health:0,Passengers:[{id:falling_block,Time:1,BlockState:{""" + """Name:activator_rail},Passengers:["""

    for page in range(dumb, dumb + 1):
        for group in range(32, 64):
            for barrel in range(8):
                x = 1673 + (2 * page) + 200
                # add 200 for debugging
                
                if group < 8:
                    y = 85 - (group % 2) + (2 * barrel)
                elif group < 16:
                    y = 103 - (group % 2) + (2 * barrel)
                elif group < 24:
                    y = 121 - (group % 2) + (2 * barrel)
                elif group < 32:
                    y = 139 - (group % 2) + (2 * barrel)
                elif group < 40:
                    y = 85 - (group % 2) + (2 * barrel)
                elif group < 48:
                    y = 103 - (group % 2) + (2 * barrel)
                elif group < 56:
                    y = 121 - (group % 2) + (2 * barrel)
                elif group < 64:
                    y = 139 - (group % 2) + (2 * barrel)
                
                if group < 32:
                    z = 445 - (2 * (group % 8))
                else:
                    z = 453 + (2 * (group % 8))
    
                text = generateBarrel(x, y, z, source[page][group][barrel])
                
                text = "{id:command_block_minecart,Command:'" + text + "'},"
                # {id:command_block_minecart,Command:''},
                
                command += text
                
    command += """{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:"fill ~ ~ ~ ~ ~-3 ~ air"}'},{id:command_block_minecart,Command:'kill @e[type=command_block_minecart,distance=..1]'}]}]}]}"""

    return command
