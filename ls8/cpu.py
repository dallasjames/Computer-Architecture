"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

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
            self.pc += 2
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
            ir = self.ram[self.pc]

            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]

            if ir == 0b00000001:
                running = self.hlt()
                self.pc += 1

            elif ir == 0b10000010:
                self.ldi(operand_a, operand_b)
                self.pc += 3

            elif ir == 0b01000111:
                self.prn(operand_a)
                self.pc += 2

            elif ir == 0b10100010:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 1

            elif ir == 0b01000101:
                reg_address = self.ram_read(self.pc + 1)
                value = self.reg[reg_address]
                self.reg[7] -= 1
                self.ram[self.reg[7]] = value
                self.pc += 2

            elif ir == 0b01000110:
                reg_address = self.ram_read(self.pc + 1)
                value = self.ram[self.reg[7]]
                self.reg[reg_address] = value
                self.reg[7] += 1
                self.pc += 2
