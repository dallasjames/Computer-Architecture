import sys
import time


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.l = 0
        self.g = 0
        self.e = 0

    def hlt(self):
        return False

    def ldi(self, op1, op2):
        self.reg[op1] = op2

    def prn(self, op1):
        print(self.reg[op1])

    def load(self):
        """Load a program into memory."""

        address = 0
        program = []
        with open(sys.argv[1]) as f:
            for line in f:
                line_split = line.split('#')
                command = line_split[0].strip()
                if command == "":
                    continue
                command_num = int(command, 2)
                program.append(command_num)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.e = 1
                self.l = 0
                self.g = 0
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.e = 0
                self.l = 1
                self.g = 0
            else:
                self.e = 0
                self.l = 0
                self.g = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            sp = 7
            ir = self.ram[self.pc]

            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            if ir == 0b00000001:  # HALT
                running = self.hlt()
                self.pc += 1
            elif ir == 0b10000010:  # LDI
                self.ldi(operand_a, operand_b)
                self.pc += 3
            elif ir == 0b01000111:  # PRN
                self.prn(operand_a)
                self.pc += 2
            elif ir == 0b10100010:  # MUL
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == 0b10100000:  # ADD
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif ir == 0b01000101:  # PUSH
                reg_address = self.ram_read(self.pc + 1)
                value = self.reg[reg_address]
                self.reg[sp] -= 1
                self.ram[self.reg[sp]] = value
                self.pc += 2
            elif ir == 0b01000110:  # POP
                reg_address = self.ram_read(self.pc + 1)
                value = self.ram[self.reg[sp]]
                self.reg[reg_address] = value
                self.reg[sp] += 1
                self.pc += 2
            elif ir == 0b01010000:  # CALL
                self.reg[sp] -= 1
                self.ram[self.reg[sp]] = self.pc + 2
                reg_num = self.ram[self.pc + 1]
                self.pc = self.reg[reg_num]
            elif ir == 0b00010001:  # RET
                self.pc = self.ram[self.reg[sp]]
                self.reg[sp] += 1
                self.pc += 1
            elif ir == 0b10100111:  # CMP
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            elif ir == 0b01010101:  # JEQ
                if self.e == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif ir == 0b01010110:  # JNE
                if self.e == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif ir == 0b01010100:
                self.pc = self.reg[operand_a]
