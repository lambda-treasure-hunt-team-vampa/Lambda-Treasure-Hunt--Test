"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.SP = 7
        self.fl = 0
        self.branchtable = {}
        self.branchtable[0b10000010] = self.handle_LDI
        self.branchtable[0b01000111] = self.handle_PRN
        self.branchtable[0b10100010] = self.handle_MUL
        self.branchtable[0b01000101] = self.handle_PUSH
        self.branchtable[0b01000110] = self.handle_POP
        self.branchtable[0b10100111] = self.handle_CMP
        self.branchtable[0b01010100] = self.handle_JMP
        self.branchtable[0b01010101] = self.handle_JEQ
        self.branchtable[0b01010110] = self.handle_JNE
        self.branchtable[0b01001000] = self.handle_PRA
        self.branchtable[0b10101000] = self.handle_AND
        self.branchtable[0b10101011] = self.handle_XOR

    def load(self, ls8_file):
        """Load a program into memory."""

        address = 0

        try:
            with open(ls8_file) as opened_file:
                for line in opened_file:

                    num = line.split('#', 1)[0]

                    self.ram[address] = int(num, 2)

                    address += 1

        except FileNotFoundError:
            print(f"{ls8_file} was not found.")
            sys.exit(2)

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            return self.reg[reg_a]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_LDI(self, a, b):
        self.reg[a] = b

        self.pc += 3

    def handle_PRN(self, a, b):
        print(self.reg[a])

        self.pc += 2

    def handle_MUL(self, a, b):
        self.alu('MUL', a, b)

        self.pc += 3

    def handle_PUSH(self, a, b):
        self.reg[self.SP] -= 1

        value = self.reg[a]

        self.ram[self.reg[self.SP]] = value

        self.pc += 2

    def handle_POP(self, a, b):
        value = self.ram[self.reg[self.SP]]

        self.reg[a] = value

        self.reg[self.SP] += 1
        self.pc += 2

    def handle_CMP(self, a, b):
        self.alu('CMP', a, b)

        self.pc += 3

    def handle_JMP(self, a, b):
        self.pc = self.reg[a]

    def handle_JEQ(self, a, b):
        if self.fl == 1:

            self.pc = self.reg[a]
        else:

            self.pc += 2

    def handle_JNE(self, a, b):
        if self.fl == 0:

            self.pc = self.reg[a]
        else:

            self.pc += 2

    def handle_PRA(self, a, b):
        print(chr(self.reg[a]))

        self.pc += 2

    def handle_AND(self, a, b):
        bitwise_and = ''
        binary_string_a = f'{self.reg[a]:08b}'
        binary_string_b = f'{self.reg[b]:08b}'
        for i in range(8):
            if (binary_string_a[i] == '0') and (binary_string_b[i] == '0'):
                bitwise_and += '0'
            elif (binary_string_a[i] == '0') and (binary_string_b[i] == '1'):
                bitwise_and += '0'
            elif (binary_string_a[i] == '1') and (binary_string_b[i] == '0'):
                bitwise_and += '0'
            elif (binary_string_a[i] == '1') and (binary_string_b[i] == '1'):
                bitwise_and += '1'
        self.reg[a] = int(bitwise_and, 2)
        
        self.pc += 3

    def handle_XOR(self, a, b):
        bitwise_xor = ''
        binary_string_a = f'{self.reg[a]:08b}'
        binary_string_b = f'{self.reg[b]:08b}'
        for i in range(8):
            if (binary_string_a[i] == '0') and (binary_string_b[i] == '0'):
                bitwise_xor += '0'
            elif (binary_string_a[i] == '0') and (binary_string_b[i] == '1'):
                bitwise_xor += '1'
            elif (binary_string_a[i] == '1') and (binary_string_b[i] == '0'):
                bitwise_xor += '1'
            elif (binary_string_a[i] == '1') and (binary_string_b[i] == '1'):
                bitwise_xor += '0'
        self.reg[a] = int(bitwise_xor, 2)
        
        self.pc += 3

    def run(self):
        """Run the CPU."""

        HTL = 0b00000001

        while True:

            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HTL:
                break

            else:
                try:
                    self.branchtable[ir](operand_a, operand_b)
                except:
                    print(f"Instruction unknown {ir}")
                    sys.exit(1)