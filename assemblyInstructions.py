class instruction():
    def __init__(self, name = "NULL", number = 0):
        self.number = number
        self.name = name
    def to_binary(self):
        self.binary = "NULL"
    def get_binary(self):
        return self.binary
    def set_tag(self, tag):
        self.tag = tag
    def calculate_offset(self, offsets):
        try:
            self.offset = (offsets[self.tag] - self.number) - 2 #subtract 2 because always two ahead
        except Exception:
            pass
    def set_instruction_number(self, number):
        self.number = number
    def __str__(self) -> str:
        return f"{self.number} {self.name} \n {self.binary} "


class MOV(instruction):
    movw_hardcode = "00110000" #bits 5-12
    movt_hardcode = "00110100"
    def __init__(self, name, *args):
        super().__init__(name)
        self.condition_code = "1110"
        self.register = args[1]
        self.operand = args[2]
        if self.name == "MOVW":
            self.hardcode = self.movw_hardcode
        else:
            self.hardcode = self.movt_hardcode
    def to_binary(self):
        self.register = bin(int(self.register[1:]))[2:].zfill(4)
        self.operand = bin(int(self.operand, 16))[2:].zfill(16)
        #seperate operand into imm4 (first 4 digits) and imm12 (last 12 digits))
        self.imm4 = self.operand[:4]
        self.imm12 = self.operand[4:] 
        self.binary = self.condition_code + self.hardcode + self.imm4 + self.register + self.imm12
    def get_binary(self):
        return self.binary


class STR(instruction):
    def __init__(self, *args):
        super().__init__("STR")
        self.condition_code = "1110"
        self.hardcode = "01"
        self.I = "0"
        self.P = "0"
        self.U = "0"
        self.B = "0"
        self.W = "0"
        self.L = "0"
        self.Rn = args[2] #these are flipped as per the spec
        self.Rd = args[1] #flipped
        # if offset exists then self.offset = args[3] else self.offset = "000000000000"
        self.offset = args[3] if len(args) == 4 else "000000000000"
    def to_binary(self):
        self.Rn = bin(int(self.Rn[1:]))[2:].zfill(4)
        self.Rd = bin(int(self.Rd[1:]))[2:].zfill(4)
        self.offset = bin(int(self.offset, 16))[2:].zfill(12)
        self.binary = self.condition_code + self.hardcode + self.I + self.P + self.U + self.B + self.W + self.L + self.Rn + self.Rd + self.offset

#basically the same as STR except L = 1
class LDR(instruction):
    def __init__(self, *args):
        super().__init__("LDR")
        self.condition_code = "1110"
        self.hardcode = "01"
        self.I = "0"
        self.P = "0"
        self.U = "0"
        self.B = "0"
        self.W = "0"
        self.L = "1"
        self.Rn = args[2] #these are flipped as per the spec
        self.Rd = args[1] #flipped
        # if offset exists then self.offset = args[3] else self.offset = "000000000000"
        self.offset = args[3] if len(args) == 4 else "000000000000"
    def to_binary(self):
        self.Rn = bin(int(self.Rn[1:]))[2:].zfill(4)
        self.Rd = bin(int(self.Rd[1:]))[2:].zfill(4)
        self.offset = bin(int(self.offset, 16))[2:].zfill(12)
        self.binary = self.condition_code + self.hardcode + self.I + self.P + self.U + self.B + self.W + self.L + self.Rn + self.Rd + self.offset

class ADD(instruction):
    def __init__(self, *args):
        super().__init__("ADD")
        self.condition_code = "1110"
        self.hardcode = "00"
        self.op_code = "0100"
        self.I = "1"
        self.S = "0"
        self.Rn = args[2]
        self.Rd = args[1]
        self.operand2 = args[3]

    def to_binary(self):
        self.Rn = bin(int(self.Rn[1:]))[2:].zfill(4)
        self.Rd = bin(int(self.Rd[1:]))[2:].zfill(4)
        self.operand2 = bin(int(self.operand2, 16))[2:].zfill(12)
        self.binary = self.condition_code + self.hardcode + self.I + self.op_code + self.S + self.Rn + self.Rd + self.operand2
class SUBS(instruction):
    def __init__(self, *args):
        super().__init__("SUBS")
        self.condition_code = "1110"
        self.hardcode = "00"
        self.op_code = "0010"
        self.I = "1"
        self.S = "1"#HARD CODED FOR NOW
        self.Rn = args[2]
        self.Rd = args[1]
        self.operand2 = args[3]
    def to_binary(self):
        self.Rn = bin(int(self.Rn[1:]))[2:].zfill(4)
        self.Rd = bin(int(self.Rd[1:]))[2:].zfill(4)
        self.operand2 = bin(int(self.operand2, 16))[2:].zfill(12)
        self.binary = self.condition_code + self.hardcode + self.I + self.op_code + self.S + self.Rn + self.Rd + self.operand2
class ORR(instruction):
    def __init__(self, *args):
        super().__init__("ORR")
        self.condition_code = "1110"
        self.hardcode = "00"
        self.op_code = "1100"
        self.I = "1"
        self.S = "0"
        self.Rn = args[1]
        self.Rd = args[2]
        self.operand2 = args[3]
    def to_binary(self):
        self.Rn = bin(int(self.Rn[1:]))[2:].zfill(4)
        self.Rd = bin(int(self.Rd[1:]))[2:].zfill(4)
        self.operand2 = bin(int(self.operand2, 16))[2:].zfill(12)
        self.binary = self.condition_code + self.hardcode + self.I + self.op_code + self.S + self.Rn + self.Rd + self.operand2
        
class B(instruction):
    def __init__(self, *args, condition_code = "1110", l = "0", name = "B"):
        super().__init__(name)
        self.condition_code = condition_code #default is always
        self.hardcode = "101"
        self.L = l
        if ":" in args[-1]:
            self.offset = "0"
            self.tag = args[1][1:]
        else:
            self.offset = args[1]

    def to_binary(self):
        #bin(((1 << 32) - 1) & -5) covers both positive and negative offsets
        self.offset = bin(((1 << 24) - 1) & int(self.offset))[2:].zfill(24)
        self.binary = self.condition_code + self.hardcode + self.L + self.offset

class BX(instruction):
    def __init__(self, *args, condition_code = "1110"):
        super().__init__(args[0])
        self.condition_code = condition_code
        self.hardcode = "000100101111111111110001"
        self.register = args[1]

    def to_binary(self):
        self.register = bin(int(self.register[1:]))[2:].zfill(4)
        self.binary = self.condition_code + self.hardcode + self.register
    
    