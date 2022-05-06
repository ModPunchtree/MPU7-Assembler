
def getType(op: str = 1) -> str:
    if op == "0":
        return "REG", "R0"
    if op == "255":
        return "REG", "!R0"
    if op.startswith("R") or (op == "SP"):
        return "REG", op
    if op[0].isnumeric() or op.startswith((".", "M", "%", "'", "~")):
        return "IMM", op
    if op == "PC":
        return "PC", op
    raise Exception(f"FATAL - Unrecognised operand type: {op}")

def translate(opCode: str, op1: str = "" , op2: str = "", op3: str = "") -> str:
    
    if op1:
        op1Type, op1 = getType(op1)
    if op2:
        op2Type, op2 = getType(op2)
    if op3:
        op3Type, op3 = getType(op3)
    
    if op1.startswith("M"):
        op1[0] = "#"
    if op2.startswith("M"):
        op2[0] = "#"
    if op3.startswith("M"):
        op3[0] = "#"
    
    answer = 69
    
    if opCode == "ADD":
        if (op2Type == "IMM") and (op3Type == "IMM"):
            answer = """IMM(<A>, <B>);;
ADD(<A>, <C>);;"""
        else:
            answer = """ADD(<A>, <B>, <C>);;"""
        
    elif opCode == "RSH":
        answer = """RSH(<A>, <B>);;"""
        
    elif opCode == "LOD":
        if op1Type == "REG":
            if op2Type == "IMM":
                answer = """SPT(<B>); FFG();
STL(~-1) FLG(ZF); LOD(<A>);"""
            else:
                answer = """ADD(SP, <B>, R0) STL(~+1);;
STL(~+0) FLG(!CF); LOD(<A>);"""
        else:
            if op2Type == "IMM":
                answer = """SPT(<A>); FFG();
STL(~-1) FLG(!CF); LOD(R9);
ADD(RP, R9, R0) STL(~+0) FLG(!CF); STL(RET);"""
            else:
                answer = """MOV(SP, <A>) STL(~+1); LOD(R9) FFG();
STL(~-1) FLG(!CF); ADD(RP, R0, R9);
STL(RET);;"""
        
    elif opCode == "STR":
        if op2Type == "REG":
            if op1Type == "IMM":
                answer = """STR(<B>) SPT(<A>);;"""
            else:
                answer = """MOV(SP, <A>) STL(~+0) FLG(!CF); STR(<B>);"""
        else:
            if op1Type == "IMM":
                answer = """IMM(SP, <A>);;
STR(<B>);;"""
            else:
                answer = """MOV(SP, <A>) STL(~+0) FLG(!CF); STR(<B>);"""
        
    elif opCode == "BGE":
        
        if op1Type == "IMM" and op2Type == "REG" and op3Type == "REG":
            answer = """SUB(R0, <B>, <C>) FLG(CF) STL(~+1);;
; STL(<A>);"""
        elif op1Type == "IMM" and op2Type == "REG" and op3Type == "IMM":
            answer = """RPT(~+2);;
SUB(R0, <B>, <C>) FLG(CF) STL(RET);;
; STL(<A>);"""
        elif op1Type == "IMM" and op2Type == "IMM" and op3Type == "REG":
            answer = """RPT(~+2);;
SUB(R0, <B>, <C>) FLG(CF) STL(RET);;
; STL(<A>);"""
        elif op1Type == "REG" and op2Type == "REG" and op3Type == "REG":
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); SUB(R0, <B>, <C>) FLG(CF) STL(~+1);
; STL(RET);"""
        elif op1Type == "REG" and op2Type == "REG" and op3Type == "IMM":
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <C>);
SUB(R0, <B>, R9) FLG(CF) STL(~+1);;
; STL(RET);"""
        elif op1Type == "REG" and op2Type == "IMM" and op3Type == "REG":
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <B>);
SUB(R0, R9, <C>) FLG(CF) STL(~+1);;
; STL(RET);"""
        
    elif opCode == "NOR":
        answer = """NOR(<A>, <B>, <C>);;"""
        
    elif opCode == "SUB":
        if (op2Type == "IMM") and (op3Type == "IMM"):
            answer = """IMM(<A>, <B>);;
SUB(<A>, <C>);;"""
        else:
            answer = """SUB(<A>, <B>, <C>);;"""
        
    elif opCode == "JMP":
        if op1Type == "IMM":
            answer = """STL(<A>);;"""
        else:
            answer = """;;
ADD(RP, R0, <A>) STL(~+0); STL(RET);"""
        
    elif opCode == "MOV":
        if op2Type == "REG":
            answer = """MOV(<A>, <B>);;"""
        else:
            answer = """IMM(<A>, <B>);;"""
            
    elif opCode == "NOP":
        answer = """;;"""
        
    elif opCode == "IMM":
        answer = """IMM(<A>, <B>);;"""
        
    elif opCode == "LSH":
        answer = """LSH(<A>, <B>);;"""
        
    elif opCode == "INC":
        answer = """INC(<A>, <B>);;"""
        
    elif opCode == "DEC":
        answer = """DEC(<A>, <B>);;"""
        
    elif opCode == "NEG":
        answer = """NEG(<A>, <B>);;"""
        
    elif opCode == "AND":
        answer = """AND(<A>, <B>, <C>);;"""
        
    elif opCode == "OR":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """NOR(<A>, <B>, <C>) STL(~+0) FLG(!CF); NOT(<A>);"""
        else:
            answer = """NOR(<A>, <B>, <C>);;
NOT(<A>);;"""
        
    elif opCode == "NOT":
        answer = """NOT(<A>, <B>);;"""
        
    elif opCode == "XNOR":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """AND(<A>, <B>, <C>); NOR(<A>, R9) FFG();
NOR(R9, <B>, <C>) STL(~-1) FLG(!CF); NOT(<A>);"""
        else:
            answer = """AND(<A>, <B>, <C>);;
NOR(R9, <B>, <C>);;
NOR(<A>, R9) STL(~+0) FLG(!CF); NOT(<A>);"""
        
    elif opCode == "XOR":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """AND(<A>, <B>, <C>);;
NOR(R9, <B>, <C>) STL(~+0) FLG(!CF); NOR(<A>, R9);"""
        else:
            answer = """AND(<A>, <B>, <C>);;
NOR(R9, <B>, <C>);;
NOR(<A>, R9);;"""
        
    elif opCode == "NAND":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """AND(<A>, <B>, <C>) STL(~+0) FLG(!CF); NOT(<A>);"""
        else:
            answer = """AND(<A>, <B>, <C>);;
NOT(<A>);;"""
        
    elif opCode == "BRL":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <B>, <C>) FLG(!CF) STL(~+1);;
; STL(<A>);"""
        elif op1Type == "IMM":
            answer = """RPT(~+2);;
SUB(R0, <B>, <C>) FLG(!CF) STL(RET);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); SUB(R0, <B>, <C>) FLG(!CF) STL(~+1);
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <C>);
SUB(R0, <B>, R9) FLG(!CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <B>);
SUB(R0, R9, <C>) FLG(!CF) STL(~+1);;
; STL(RET);"""
        
    elif opCode == "BRG":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <C>, <B>) FLG(!CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """RPT(~+2);;
SUB(R0, <C>, <B>) FLG(!CF) STL(RET);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """RPT(~+2);;
SUB(R0, <C>, <B>) FLG(!CF) STL(RET);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); SUB(R0, <C>, <B>) FLG(!CF) STL(~+1);
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <C>);
SUB(R0, R9, <B>) FLG(!CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <B>);
SUB(R0, <C>, R9) FLG(!CF) STL(~+1);;
; STL(RET);"""
        
    elif opCode == "BRE":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <B>, <C>) FLG(ZF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """RPT(~+2);;
SUB(R0, <C>, <B>) FLG(ZF) STL(RET);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """RPT(~+2);;
SUB(R0, <C>, <B>) FLG(ZF) STL(RET);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); SUB(R0, <C>, <B>) FLG(ZF) STL(~+1);
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <C>);
SUB(R0, R9, <B>) FLG(ZF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <B>);
SUB(R0, <C>, R9) FLG(ZF) STL(~+1);;
; STL(RET);"""
    
    elif opCode == "BNE":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <B>, <C>) FLG(!ZF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """RPT(~+2);;
SUB(R0, <C>, <B>) FLG(!ZF) STL(RET);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """RPT(~+2);;
SUB(R0, <C>, <B>) FLG(!ZF) STL(RET);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); SUB(R0, <C>, <B>) FLG(!ZF) STL(~+1);
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <C>);
SUB(R0, R9, <B>) FLG(!ZF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <B>);
SUB(R0, <C>, R9) FLG(!ZF) STL(~+1);;
; STL(RET);"""
    
    elif opCode == "BOD":
        if op1Type == "REG":
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); ADD(R0, <B>) FLG(OD) STL(~+1);
; STL(RET);"""
        else:
            answer = """ADD(R0, <B>) FLG(OD) STL(~+1);;
; STL(<A>);"""
    
    elif opCode == "BEV":
        if op1Type == "REG":
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); ADD(R0, <B>) FLG(OD) STL(~+1);
STL(RET);;"""
        else:
            answer = """ADD(R0, <B>) FLG(OD) STL(~+1);;
STL(<A>);;"""
        
    elif opCode == "BLE":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <C>, <B>) FLG(CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """RPT(~+2);;
SUB(R0, <C>, <B>) FLG(CF) STL(RET);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """RPT(~+2);;
SUB(R0, <C>, <B>) FLG(CF) STL(RET);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); SUB(R0, <C>, <B>) FLG(CF) STL(~+1);
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <C>);
SUB(R0, R9, <B>) FLG(CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <B>);
SUB(R0, <C>, R9) FLG(CF) STL(~+1);;
; STL(RET);"""
        
    elif opCode == "BRZ":
        if op1Type == "IMM":
            answer = """ADD(R0, <B>) FLG(ZF) STL(~+1);;
; STL(<A>);"""
        else:
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); ADD(R0, <B>) FLG(ZF) STL(~+1);
; STL(RET);"""
        
    elif opCode == "BNZ":
        if op1Type == "IMM":
            answer = """ADD(R0, <B>) FLG(!ZF) STL(~+1);;
; STL(<A>);"""
        else:
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); ADD(R0, <B>) FLG(!ZF) STL(~+1);
; STL(RET);"""
        
    elif opCode == "BRN":
        if op1Type == "IMM":
            answer = """ADD(R0, <B>) FLG(NE) STL(~+1);;
; STL(<A>);"""
        else:
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); ADD(R0, <B>) FLG(NE) STL(~+1);
; STL(RET);"""
        
    elif opCode == "BRP":
        if op1Type == "IMM":
            answer = """ADD(R0, <B>) FLG(NE) STL(~+1);;
STL(<A>);;"""
        else:
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); ADD(R0, <B>) FLG(NE) STL(~+1);
STL(RET);;"""
        
    elif opCode == "PSH":
        answer = """DEC(R10) STL(~+0) FLG(!ZF); MOV(SP, R10);
STR(<A>);;"""
        
    elif opCode == "POP":
        answer = """INC(R10); STL(~+1) FLG(!CF);
MOV(SP, R10) STL(~-1) FLG(!CF); LOD(<A>);"""
        
    elif opCode == "CAL":
        if op1Type == "IMM":
            answer = """DEC(R10) STL(~+1); STR(~+2) FFG();
ADD(SP, R10, R0) STL(~-1) FLG(!CF); STL(<A>);"""
        else:
            answer = """DEC(R10); ADD(SP, R10, R0) FFG();
ADD(RP, R0, <A>) STL(~-1) FLG(!CF); STR(~+1) STL(RET);"""
        
    elif opCode == "RET":
        answer = """;;
MOV(SP, R10) STL(~+0) FLG(!CF); INC(R10) STL(~+1);
LOD(R9) STL(~+0) FLG(!CF); MOV(RP, R9);
STL(RET);;"""
        
    elif opCode == "HLT":
        answer = """HLT();;"""
        
    elif opCode == "CPY":
        if (op1Type == "IMM") and (op2Type == "IMM"):
            answer = """SPT(<B>); FFG();
STL(~-1) FLG(!CF); LOD(SR) SPT(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG"):
            answer = """MOV(SP, <B>) STL(~+0) FLG(!CF); STL(~+1);
LOD(SR) SPT(<A>);;"""
        elif (op1Type == "REG") and (op2Type == "IMM"):
            answer = """SPT(<B>); FFG();
MOV(SP, <A>) STL(~-1) FLG(!CF); LOD(SR);"""
        elif (op1Type == "REG") and (op2Type == "REG"):
            answer = """MOV(SP, <B>) STL(~+0) FLG(!CF); MOV(SP, <A>) STL(~+1);
LOD(SR);;"""
        
    elif opCode == "BRC":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(R0, <B>, <C>) STL(~+1) FLG(CF);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """RPT(~+2);;
ADD(R0, <B>, <C>) STL(RET) FLG(CF);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """RPT(~+2);;
ADD(R0, <B>, <C>) STL(RET) FLG(CF);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, <A>, R0) STL(~+0) FLG(!CF); ADD(R0, <B>, <C>) FLG(CF) STL(~+1);
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <C>);
ADD(R0, <B>, R9) FLG(CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <B>);
ADD(R0, R9, <C>) FLG(CF) STL(~+1);;
; STL(RET);"""
        
    elif opCode == "BNC":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(R0, <B>, <C>) STL(~+1) FLG(!CF);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """RPT(~+2);;
ADD(R0, <B>, <C>) STL(RET) FLG(!CF);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """RPT(~+2);;
ADD(R0, <B>, <C>) STL(RET) FLG(!CF);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, <A>, R0) STL(~+0) FLG(!CF); ADD(R0, <B>, <C>) FLG(!CF) STL(~+1);
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <C>);
ADD(R0, <B>, R9) FLG(!CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>) STL(~+0) FLG(!CF); IMM(R9, <B>);
ADD(R0, R9, <C>) FLG(!CF) STL(~+1);;
; STL(RET);"""
        
    elif opCode == "MLT":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SPT(128) STR(<B>); STL(~+1) FLG(!CF);
SPT(129) STR(<C>); STL(~+1) FLG(!CF);
STL(~-2) FLG(!CF); LOD(R1);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """SPT(128) STR(<B>); STL(~+1) FLG(!CF);
SPT(129); FFG();
STR(<C>); FFG();
STL(~-3) FLG(!CF); LOD(R1);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """SPT(128); STL(~+1) FLG(!CF);
STR(<B>); FFG();
SPT(129) STR(<C>); FFG();
STL(~-3) FLG(!CF); LOD(R1);"""
        
    elif opCode == "DIV":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SPT(132) STR(R0); STL(~+1) FLG(!CF);
SPT(131) STR(<B>); STL(~+1) FLG(!CF);
SPT(130) STR(<C>); STL(~+1) FLG(!CF);
STL(~-3) FLG(!CF); LOD(<A>);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """SPT(132) STR(R0);;
SPT(131) STR(<B>); STL(~+1) FLG(!CF);
SPT(130); STL(~+1) FLG(!CF);
STR(<C>); STL(~+1) FLG(!CF);
STL(~-3) FLG(!CF); LOD(<A>);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """SPT(132) STR(R0);;
SPT(131); STL(~+1) FLG(!CF);
STR(<B>); STL(~+1) FLG(!CF);
SPT(130) STR(<C>); STL(~+1) FLG(!CF);
STL(~-3) FLG(!CF); LOD(<A>);"""
        
    elif opCode == "MOD":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SPT(132) STR(R0); STL(~+1) FLG(!CF);
SPT(130) STR(<C>); STL(~+1) FLG(!CF);
SPT(131) STR(<B>); STL(~+1) FLG(!CF);
STL(~-3) FLG(!CF); LOD(<A>);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """SPT(132) STR(R0);;
SPT(130); STL(~+1) FLG(!CF);
STR(<C>); STL(~+1) FLG(!CF);
SPT(131) STR(<B>); STL(~+1) FLG(!CF);
STL(~-3) FLG(!CF); LOD(<A>);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """SPT(132) STR(R0);;
SPT(130) STR(<C>); STL(~+1) FLG(!CF);
SPT(131); STL(~+1) FLG(!CF);
STR(<B>); STL(~+1) FLG(!CF);
STL(~-3) FLG(!CF); LOD(<A>);"""
        
    elif opCode == "BSR":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(<A>, <B>) FLG(!CF) STL(~+0); MOV(R9, <C>) FLG(ZF) STL(~+1);
DEC(R9) FLG(ZF) STL(~+1); STL(~+2);
RSH(<A>) STL(~-1); RSH(<A>);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(<A>, <B>) RPT(~+2);;
IMM(R9, <C>) FLG(ZF) STL(RET);;
DEC(R9) FLG(ZF) STL(~+1); STL(~+2);
RSH(<A>) STL(RET); RSH(<A>);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(<A>, <B>);;
MOV(R9, <C>) FLG(ZF) STL(~+1);;
DEC(R9) FLG(ZF) STL(~+1); STL(~+2);
RSH(<A>) STL(~-1); RSH(<A>);"""
        
    elif opCode == "BSL":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(<A>, <B>) FLG(!CF) STL(~+0); MOV(R9, <C>) FLG(ZF) STL(~+1);
DEC(R9) FLG(ZF) STL(~+1); STL(~+2);
LSH(<A>) STL(~-1); LSH(<A>);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(<A>, <B>) RPT(~+2);;
IMM(R9, <C>) FLG(ZF) STL(RET);;
DEC(R9) FLG(ZF) STL(~+1); STL(~+2);
LSH(<A>) STL(RET); LSH(<A>);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            if op1 == op3:
                raise Exception(f"FATAL - No translation exists for BSL when <A> == <C>, in instruction: {opCode} {op1} {op2} {op3}")
            answer = """IMM(<A>, <B>);;
MOV(R9, <C>) FLG(ZF) STL(~+1);;
DEC(R9) FLG(ZF) STL(~+1); STL(~+2);
LSH(<A>) STL(~-1); LSH(<A>);"""
        
    elif opCode == "SRS":
        answer = """RSH(<A>, <B>) RPT(~+2);;
SUB(R0, <A>, 64) FLG(CF) STL(RET);;
; ADD(<A>, 128);"""
        
    elif opCode == "BSS":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(R8, <B>) STL(~+0) FLG(!CF); MOV(R9, <C>);
MOV(R0, R9) FLG(ZF) STL(~+1);;
MOV(R0, R8) FLG(NE) STL(~+1); MOV(<A>, R8) STL(~+3);
RSH(R8); RSH(R8) FFG() RPT(~+1);
DEC(R9) FLG(ZF) STL(~-2); ADD(R8, 128) STL(RET);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(R8, <B>) STL(~+0) FLG(!CF); IMM(R9, <C>);
MOV(R0, R9) FLG(ZF) STL(~+1);;
MOV(R0, R8) FLG(NE) STL(~+1); MOV(<A>, R8) STL(~+3);
RSH(R8); RSH(R8) FFG() RPT(~+1);
DEC(R9) FLG(ZF) STL(~-2); ADD(R8, 128) STL(RET);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """MOV(R9, <C>) STL(~+0) FLG(!CF); IMM(R8, <B>);
MOV(R0, R9) FLG(ZF) STL(~+1);;
MOV(R0, R8) FLG(NE) STL(~+1); MOV(<A>, R8) STL(~+3);
RSH(R8); RSH(R8) FFG() RPT(~+1);
DEC(R9) FLG(ZF) STL(~-2); ADD(R8, 128) STL(RET);"""
        
    elif opCode == "SETE":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <B>, <C>) FLG(ZF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """IMM(R9, <C>);;
SUB(R0, <B>, R9) FLG(ZF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R9, <B>);;
SUB(R0, R9, <C>) FLG(ZF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        
    elif opCode == "SETNE":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <B>, <C>) FLG(!ZF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """IMM(R9, <C>);;
SUB(R0, <B>, R9) FLG(!ZF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R9, <B>);;
SUB(R0, R9, <C>) FLG(!ZF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        
    elif opCode == "SETG":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <C>, <B>) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """IMM(R9, <C>);;
SUB(R0, R9, <B>) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R9, <B>);;
SUB(R0, <C>, R9) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        
    elif opCode == "SETL":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <B>, <C>) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """IMM(R9, <C>);;
SUB(R0, <B>, R9) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R9, <B>);;
SUB(R0, R9, <C>) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        
    elif opCode == "SETGE":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <B>, <C>) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """IMM(R9, <C>);;
SUB(R0, <B>, R9) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R9, <B>);;
SUB(R0, R9, <C>) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        
    elif opCode == "SETLE":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SUB(R0, <C>, <B>) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """IMM(R9, <C>);;
SUB(R0, R9, <B>) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R9, <B>);;
SUB(R0, <C>, R9) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        
    elif opCode == "SETC":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(R0, <B>, <C>) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """IMM(R9, <C>);;
ADD(R0, <B>, R9) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R9, <B>);;
ADD(R0, R9, <C>) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        
    elif opCode == "SETNC":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(R0, <B>, <C>) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """IMM(R9, <C>);;
ADD(R0, <B>, R9) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R9, <B>);;
ADD(R0, R9, <C>) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        
    elif opCode == "LLOD":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(R9, <B>, <C>) STL(~+1); STL(~+1);
ADD(SP, R9, R0) STL(~-1) FLG(!CF); LOD(<A>);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(R9, <B>, <C>);;
; STL(~+1);
ADD(SP, R9, R0) STL(~-1) FLG(!CF); LOD(<A>);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(R9, <B>, <C>);;
; STL(~+1);
ADD(SP, R9, R0) STL(~-1) FLG(!CF); LOD(<A>);"""
        elif (op2Type == "IMM") and (op3Type == "IMM"):
            answer = """IMM(R8, <B>); ADD(SP, R8, R9) STL(~+1) FLG(!CF);
ADD(R9, R8, <C>); STL(~+1) FLG(!CF);
STL(~-2); LOD(<A>);"""
            
    elif opCode == "LSTR":
        if (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(R9, <A>, <B>); ADD(SP, R9, R0) FFG();
STL(~-1) FLG(!CF); STR(<C>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(R9, <A>, <B>); ADD(SP, R9, R0) FFG();
STL(~-1) FLG(!CF); STR(<C>);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(R9, <A>, <B>); ADD(SP, R9, R0) FFG();
STL(~-1) FLG(!CF); STR(<C>);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "IMM"):
            answer = """IMM(R9, <B>);;
ADD(R9, <A>, R9); ADD(SP, R9, R0) FFG();
STL(~-1) FLG(!CF); STR(<C>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(R9, <A>, <B>); ADD(SP, R9, R0) FFG();
STL(~-1) FLG(!CF); STR(<C>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(R9, <A>, <B>); ADD(SP, R9, R0) FFG();
STL(~-1) FLG(!CF); STR(<C>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(R9, <A>, <B>); ADD(SP, R9, R0) FFG();
STL(~-1) FLG(!CF); STR(<C>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "IMM"):
            answer = """IMM(R9, <B>);;
ADD(R9, <A>, R9); ADD(SP, R9, R0) FFG();
STL(~-1) FLG(!CF); STR(<C>);"""
        
    elif opCode == "SDIV":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """SPT(132) STR(R0);;
AND(R9, <B>, 128);;
ADD(SR, <B>, R9) SPT(131);;
AND(R8, <C>, 128); STL(~+1) FLG(!CF);
ADD(SR, <C>, R8) SPT(130); STL(~+1) FLG(!CF);
STL(~-2) FLG(!CF); ADD(R0, R8, R9) FLG(NE) STL(~+1);
LOD(<A>); ADD(<A>, !SR, R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """SPT(132) STR(R0);;
IMM(R8, 128);;
AND(R9, <B>, R8);;
ADD(SR, <B>, R9) SPT(131);;
AND(R8, <C>, R8);;
SPT(130); STL(~+1) FLG(!CF);
ADD(SR, <C>, R8); STL(~+1) FLG(!CF);
STL(~-2) FLG(!CF); ADD(R0, R8, R9) FLG(NE) STL(~+1);
LOD(<A>); ADD(<A>, !SR, R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """SPT(132) STR(R0);;
IMM(R8, 128);;
AND(R9, <B>, R8);;
SPT(131);;
ADD(SR, <B>, R9);;
AND(R8, <C>, R8); STL(~+1) FLG(!CF);
ADD(SR, <C>, R8) SPT(130); STL(~+1) FLG(!CF);
STL(~-2) FLG(!CF); ADD(R0, R8, R9) FLG(NE) STL(~+1);
LOD(<A>); ADD(<A>, !SR, R0);"""
        
    elif opCode == "SBRL":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(!CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(!CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(!CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>);;
MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(!CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>);;
MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(!CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>);;
IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(!CF) STL(~+1);;
; STL(RET);"""
        
    elif opCode == "SBRG":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(!CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(!CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(!CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>);;
MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(!CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>);;
MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(!CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>);;
IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(!CF) STL(~+1);;
; STL(RET);"""
            
    elif opCode == "SBLE":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>);;
MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>);;
IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(CF) STL(~+1);;
; STL(RET);"""
            
    elif opCode == "SBGE":
        if (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "IMM") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(CF) STL(~+1);;
; STL(<A>);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>);;
MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "REG") and (op3Type == "IMM"):
            answer = """ADD(RP, R0, <A>);;
MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(CF) STL(~+1);;
; STL(RET);"""
        elif (op1Type == "REG") and (op2Type == "IMM") and (op3Type == "REG"):
            answer = """ADD(RP, R0, <A>);;
IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(CF) STL(~+1);;
; STL(RET);"""
            
    elif opCode == "SSETL":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        
    elif opCode == "SSETG":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(!CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
            
    elif opCode == "SSETLE":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R9, R8) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
            
    elif opCode == "SSETGE":
        if (op2Type == "REG") and (op3Type == "REG"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "REG") and (op3Type == "IMM"):
            answer = """MOV(R8, <B>) FLG(NE) STL(~+1);;
; ADD(R8, 128);
IMM(R9, <C>);;
MOV(R0, R9) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
        elif (op2Type == "IMM") and (op3Type == "REG"):
            answer = """IMM(R8, <B>);;
MOV(R0, R8) FLG(NE) STL(~+1);;
; ADD(R8, 128);
MOV(R9, <C>) FLG(NE) STL(~+1);;
; ADD(R9, 128);
SUB(R0, R8, R9) FLG(CF) STL(~+1);;
RST(<A>); MOV(<A>, !R0);"""
            
    elif opCode == "IN":
        if op2 == "%TEXT":
            answer = """SPT(146);;
FLG(IN) STL(~+0); ADD(R0, R0, IN) SPT(143);
FLG(!CF) STL(~+0); FFG(); 
STL(~+1); ADD(X, SR, !R0) STL(~+0);
STL(~+0) FLG(!CF); STL(~+1);
STL(~+0) FLG(!CF); STL(~+1);
ADD(<A>, VSH, DSR);;"""
        elif op2 == "%NUMB":
            answer = """SPT(146);;
FLG(IN) STL(~+0); ADD(R0, R0, IN) SPT(143);
STL(~+0) FLG(!CF); IMM(R8, 100) FFG();
STL(~+1); ADD(X, SR, 253) FFG();
STL(~+1); ADD(X, SR, 254) FFG();
STL(~+1); ADD(X, SR, !R0) FFG();
STL(~+1); STL(~-3);
STR(R8) SPT(129); LSH(<A>, R8) FFG();
ADD(SR, R0, DSR) SPT(128); LSH(<A>) FFG();
ADD(R8, R0, DSR); ADD(R8, <A>) FFG();
ADD(R9, VSH, DSR) STL(~-3) FLG(!CF); LSH(R8) STL(~+1) FLG(!CF);
ADD(<A>, SR, R9); ADD(R9, R8) STL(~+0);"""
        
    elif opCode == "OUT":
        if (op1 == "%NUMB") and (op2Type == "REG"):
            answer = """STR(<B>) SPT(133);;
SETX(R0) VSH() STL(~+0) FLG(!CF); RPT(~+4);
SPT(135) RET();;
SPT(134) RET();;
SPT(133);;
ADD(R0, SR, DSW);;"""
        elif (op1 == "%NUMB") and (op2Type == "IMM"):
            answer = """SPT(133);;
STR(<B>);;
SETX(R0) VSH() STL(~+0) FLG(!CF); RPT(~+4);
SPT(135) RET();;
SPT(134) RET();;
SPT(133);;
ADD(R0, SR, DSW);;"""
        elif op1 == "%TEXT":
            if op2 == "'\\n'":
                answer = """STL(~+0) FLG(!CF); SETX(R0) VSH();"""
            elif op2 in ("'w'", "'m'", "'W'", "'M'", "'N'", "'~'"):
                answer = """PRT(<B>0);;
PRT(<B>1);;"""
            else:
                answer = """PRT(<B>);;"""
        elif op1 == "%MACROX":
            answer = """SETX(<B>);;"""
        elif op1 == "%MACROY":
            answer = """SETY(<B>);;"""
        elif op1 == "%CCHAR0":
            if op2Type == "REG":
                answer = """STR(<B>) SPT(150);;"""
            else:
                answer = """SPT(150);;
STR(<B>);;"""
        elif op1 == "%CCHAR1":
            if op2Type == "REG":
                answer = """STR(<B>) SPT(151);;"""
            else:
                answer = """SPT(151);;
STR(<B>);;"""
        elif op1 == "%CCHAR2":
            if op2Type == "REG":
                answer = """STR(<B>) SPT(152);;"""
            else:
                answer = """SPT(152);;
STR(<B>);;"""
        elif op1 == "%CCHAR3":
            if op2Type == "REG":
                answer = """STR(<B>) SPT(153);;"""
            else:
                answer = """SPT(153);;
STR(<B>);;"""
        elif op1 == "%CCHAR":
            answer = """STR(R0) SPT(156);;"""
        else:
            raise Exception(f"FATAL - Unrecognised port in instruction: {opCode} {op1} {op2}")

    elif opCode == "DW":
        answer = """ADD(SP, R9, R0) STL(~+0) FLG(!CF); STR(<A>);
INC(R9) STL(~+1);;"""

    elif opCode.startswith("."):
        answer = opCode

    else:
        raise Exception(f"FATAL - Unrecognised instruction: {opCode}")
    
    if answer == 69:
        raise Exception(f"FATAL - Failed to find translation for: {opCode} {op1} {op2} {op3}")
    
    if op1:
        if op1 == "SP":
            op1 = "R10"
            answer = ";;\n" + answer
        answer = answer.replace("<A>", op1)
    if op2:
        if op2 == "SP":
            op2 = "R10"
            answer = ";;\n" + answer
        answer = answer.replace("<B>", op2)
    if op3:
        if op3 == "SP":
            op3 = "R10"
            answer = ";;\n" + answer
        answer = answer.replace("<C>", op3)
    
    return answer













