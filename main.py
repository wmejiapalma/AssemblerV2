import assemblyInstructions as ins
import binaryToImg as converter
file = open("input.txt", "r")
lines = file.readlines()

#calculating offset (where going - where at) - 2
'''
def convert_instruction_to_bytes(instruction, instruction_number):
    img_converter = converter.img_converter()
    instruction = get_instruction_data(instruction, instruction_number)
    binary = instruction.get_binary()
    return img_converter.convert_to_bytes(binary)
'''

def convert_line_to_bytes(line):
    if line == "" or line == "\n":
        return
    instructions = split_instructions(line)
    #print(instructions)
    #intructions are now in a array [MOVT, R4, 0x3F20]
    return convert_instruction_to_bytes(instructions)

def convert_line_to_object(line, instruction_number):
    instructions = split_instructions(line)
    #print(instructions)
    #intructions are now in a array [MOVT, R4, 0x3F20]
    return get_instruction_data(instructions, instruction_number)

#splits instructions on the spaces and removes commas

def get_instruction_data(line, instruction_number):
    instruction = None
    if line[0] == "MOVW":
        instruction = ins.MOV("MOVW", *line)
    elif line[0] == "MOVT":
        instruction = ins.MOV("MOVT", *line)
    elif line[0] == "STR":
        instruction = ins.STR(*line)
    elif line[0] == "LDR":
        instruction = ins.LDR(*line)
    elif line[0] == "ADD":
        instruction = ins.ADD(*line)
    elif line[0] == "ORR":
        instruction = ins.ORR(*line)
    elif line[0] == "SUBS":
        instruction = ins.SUBS(*line)
    elif line[0] == "B":
        instruction = ins.B(*line)
    elif line[0] == "BPL":
        instruction = ins.B(*line, condition_code= "0101", name="BPL")
    elif line[0] == "BL":
        instruction = ins.B(*line, l = "1", name = "BL")
    elif line[0] == "BX":
        instruction = ins.BX(*line);

    if instruction == None:
        return None
    instruction.set_instruction_number(instruction_number)
    return instruction

def split_instructions(line):
    instructions = line.split(" ")
    for i in range(len(instructions)):
        instructions[i] = instructions[i].replace(",", "")
        instructions[i] = instructions[i].replace("(","")
        instructions[i] = instructions[i].replace(")","")
        instructions[i] = instructions[i].strip()
    return instructions
'''
with open("kernel7.img", "wb") as file:
    instructions =[]
    for line in lines:
        #line example: MOVT R4, 0x3F20
        b = convert_line_to_bytes(line)
        if b != None:
            file.write(b)
'''

def main():
    #instructions in object form
    instructions = []
    offsets = {}
    
    for idx, line in enumerate(lines):
        if line == "" or line == "\n":
            continue

        #finding out if the line contains a # tag
        ins = split_instructions(line)
        try:
            tag = ins[-1]
            if tag[0] == "#":
                offsets[tag[1:]] = idx
        except Exception:
            pass

        #converting instruction to object and adding it to list
        instructions.append(convert_line_to_object(line, idx))
    for instruction in instructions:
        instruction.calculate_offset(offsets)
        instruction.to_binary()
    write_to_img(instructions)
        
def write_to_img(instructions):
    img_converter = converter.img_converter()
    with open("kernel7.img", "wb") as file:
        for instruction in instructions:
            binary = instruction.get_binary()
            file.write(img_converter.convert_to_bytes(binary))
'''
offsets = {"DELAY": 6} (tag: instruction number of tag with #)

a
a
a :DELAY [instruction number: 3] (a.tag= {"DELAY": 3} (tag: current instruction number) )
a
a
thing #delay offsets['delay'] = 6
a
a
...
z


for instruction in instructions:
    if instruction.tag == None:
        continue
    
    instruction.calcuate_offset(offsets)
    calculate_offset(self, offsets){
        self.offset = offsets[self.tag] - self.number
    }

'''

if __name__ == "__main__":
    main()