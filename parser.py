import string

class Parser:
    """Parser class will read and manipulare *.asm files to generate a binary output"""

    def __init__(self, input):
        self.input = input
        symbol_table = {}


    def encode(self):
        with open("output.asm", 'r') as outf:
            with open("binary.asm", 'w') as binf:
                for line in outf:
                    # Check for A Instruction
                    if line[0] == "@":
                        if str.isdigit(line[1:-1]):
                            binf.write('{0:015b}'.format(int(line[1:]))+ '\n')
                        else:
                            #retrieve from the Symbol Table
                        
    
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

        self.encode()








