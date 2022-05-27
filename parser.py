import string

class Parser:
    """Parser class will read and manipulare *.asm files to generate a binary output"""
    symbol_table = {
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576}

    def __init__(self, input):
        self.input = input
        self.count = 16
        self.strip_whitespace()
        self.fill_symbol_table()
        self.encode()


    def encode(self):
        with open("output.asm", 'r') as outf:
            with open("binary.asm", 'w') as binf:
                for line in outf:
                    # Check for A Instruction
                    if line[0] == "@":
                        if str.isdigit(line[1:-1]):
                            binf.write('0{0:015b}'.format(int(line[1:]))+ '\n')
                        else:
                            binf.write('0{0:015b}'.format(self.symbol_table.get(line[1:-1])) + '\n')
                    elif line[0] == '(':
                            #binf.write("0{0:015b}".format(self.symbol_table.get(line[1:-2])) + '\n')
                            pass
                    else:
                        #Create new C instruction
                        C_inst = '0000000000000000'
                        offset = 0
                        
                        #Set the Jump bits
                        if 'JGT' in line:
                            C_inst = C_inst[:13] + '001'
                        elif 'JEQ' in line:
                            C_inst = C_inst[:13] + '010'
                        elif 'JGE' in line:
                            C_inst = C_inst[:13] + '011'
                        elif 'JLT' in line:
                            C_inst = C_inst[:13] + '100'
                        elif 'JNE' in line:
                            C_inst = C_inst[:13] + '101'
                        elif 'JLE' in line:
                            C_inst = C_inst[:13] + '110'
                        elif 'JMP' in line:
                            C_inst = C_inst[:13] + '111'
                        else:
                            C_inst = C_inst[:13] + '000'

                        #Set the destination bits
                        split_line = line.split("=")
                        jump_split = line.split(";")
                        if len(split_line) > 1:
                            offset = 1
                            if split_line[0] == "M":
                                C_inst = C_inst[:10] + "001" + C_inst[13:]
                            elif split_line[0] == "D":
                                C_inst =  C_inst[:10] + "010" + C_inst[13:]
                            elif split_line[0] == "DM":
                                C_inst = C_inst[:10] + "011" + C_inst[13:]
                            elif split_line[0] == "A":
                                C_inst = C_inst[:10] + "100" + C_inst[13:]
                            elif split_line[0] == "AM":
                                C_inst = C_inst[:10] + "101" + C_inst[13:]
                            elif split_line[0] == "AD":
                                C_inst = C_inst[:10] + "110" + C_inst[13:]
                            elif split_line[0] == "ADM":
                                C_inst = C_inst[:10] + "111" + C_inst[13:]
                            else:
                                C_inst = "000"
                        
                        #Set the comp bits if there is a destination
                        if len(split_line) > 1:
                            if split_line[0+offset][:-1] == "0":
                                C_inst = "1110101010" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "1":
                                C_inst = "1110111111" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "-1":
                                C_inst = "1110111010" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D":
                                C_inst = "1110001100" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "A":
                                C_inst = "1110110000" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "!D":
                                C_inst = "1110001101" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "!A":
                                C_inst = "1110110001" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "-D":
                                C_inst = "1110001111" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "-A":
                                C_inst = "1110110011" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D+1":
                                C_inst = "1110111111" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "A+1":
                                C_inst = "1110110111" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D-1":
                                C_inst = "1110001110" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "A-1":
                                C_inst = "1110110010" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D+A":
                                C_inst = "1110000010" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D-A":
                                C_inst = "1110010011" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "A-D":
                                C_inst = "1110000111" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D&A":
                                C_inst = "1110000000" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D|A":
                                C_inst = "1110010101" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "M":
                                C_inst = "1111110000" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "!M":
                                C_inst = "1111110001" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "-M":
                                C_inst = "1111110011" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "M+1":
                                C_inst = "1111110111" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "M-1":
                                C_inst = "1111110010" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D+M":
                                C_inst = "1111000010" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D-M":
                                C_inst = "11111010011" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "M-D":
                                C_inst = "1111000111" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D&M":
                                C_inst = "1111000000" + C_inst[10:]
                            elif split_line[0+offset][:-1] == "D|M":
                                C_inst = "1111010101" + C_inst[10:]
                        else:
                            if jump_split[0+offset] == "0":
                                C_inst = "1110101010" + C_inst[10:]
                            elif split_line[0+offset] == "1":
                                C_inst = "1110111111" + C_inst[10:]
                            elif split_line[0+offset] == "-1":
                                C_inst = "1110111010" + C_inst[10:]
                            elif jump_split[0+offset] == "D":
                                C_inst = "1110001100" + C_inst[10:]
                            elif split_line[0+offset] == "A":
                                C_inst = "1110110000" + C_inst[10:]
                            elif split_line[0+offset] == "!D":
                                C_inst = "1110001101" + C_inst[10:]
                            elif split_line[0+offset] == "!A":
                                C_inst = "1110110001" + C_inst[10:]
                            elif split_line[0+offset] == "-D":
                                C_inst = "1110001111" + C_inst[10:]
                            elif split_line[0+offset] == "-A":
                                C_inst = "1110110011" + C_inst[10:]
                            elif split_line[0+offset] == "D+1":
                                C_inst = "1110111111" + C_inst[10:]
                            elif split_line[0+offset] == "A+1":
                                C_inst = "1110110111" + C_inst[10:]
                            elif split_line[0+offset] == "D-1":
                                C_inst = "1110001110" + C_inst[10:]
                            elif split_line[0+offset] == "A-1":
                                C_inst = "1110110010" + C_inst[10:]
                            elif split_line[0+offset] == "D+A":
                                C_inst = "1110000010" + C_inst[10:]
                            elif split_line[0+offset] == "D-A":
                                C_inst = "1110010011" + C_inst[10:]
                            elif split_line[0+offset] == "A-D":
                                C_inst = "1110000111" + C_inst[10:]
                            elif split_line[0+offset] == "D&A":
                                C_inst = "1110000000" + C_inst[10:]
                            elif split_line[0+offset] == "D|A":
                                C_inst = "1110010101" + C_inst[10:]
                            elif split_line[0+offset] == "M":
                                C_inst = "1111110000" + C_inst[10:]
                            elif split_line[0+offset] == "!M":
                                C_inst = "1111110001" + C_inst[10:]
                            elif split_line[0+offset] == "-M":
                                C_inst = "1111110011" + C_inst[10:]
                            elif split_line[0+offset] == "M+1":
                                C_inst = "1111110111" + C_inst[10:]
                            elif split_line[0+offset] == "M-1":
                                C_inst = "1111110010" + C_inst[10:]
                            elif split_line[0+offset] == "D+M":
                                C_inst = "1111000010" + C_inst[10:]
                            elif split_line[0+offset] == "D-M":
                                C_inst = "11111010011" + C_inst[10:]
                            elif split_line[0+offset] == "M-D":
                                C_inst = "1111000111" + C_inst[10:]
                            elif split_line[0+offset] == "D&M":
                                C_inst = "1111000000" + C_inst[10:]
                            elif split_line[0+offset] == "D|M":
                                C_inst = "1111010101" + C_inst[10:]

                        binf.write(C_inst + '\n')


    def fill_symbol_table(self):
        line_count = 0
        with open("output.asm", 'r') as f:
            for line in f:
                if line[0] == '@' and not str.isdigit(line[1:-1]):
                    if not line[1:-1] in self.symbol_table:
                        self.symbol_table[line[1:-1]] = self.count
                elif line[0] == '(':
                    if not line[1:-2] in self.symbol_table:
                        self.symbol_table[line[1:-2]] = line_count
                self.count += 1
                line_count += 1

        print(self.symbol_table)




    def strip_whitespace(self):
        """Remove all whitespace from the file"""

        # Open the output file as a writeable file
        with open("output.asm", 'w') as outf:
            #Open the asm file as readonly
            with open(self.input, 'r')as inf:
                for line in inf:
                    # Strip all whitespace from the line
                    stripped_line = line.translate(str.maketrans('', '', string.whitespace))

                    # Remove Line if empty or is a comment
                    if stripped_line == '\n' or stripped_line[0:2] == '//' or stripped_line == '':
                        continue

                    #split the line by // to fins comments after the instruction
                    stripped_list = stripped_line.split("//")

                    #write the instructions only to output
                    outf.write(stripped_list[0] + '\n')










