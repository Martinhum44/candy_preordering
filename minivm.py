from time import sleep
from sys import argv

class Program:
  PUSH = 0x00
  PUSH_TO_REGISTER = 0x01
  LOAD_FROM_REGISTER = 0x02
  ADD = 0x03
  SUB = 0x04
  MUL = 0x05
  DIV = 0x06
  PRINT_REGISTER = 0x07
  EQUALS = 0x08
  JUMP_IF = 0x09
  LESS_THAN = 0x0A
  GREATER_THAN = 0x0B
  SWAP_1 = 0x0C
  LOAD_CALLDATA = 0x0D
  DUPLICATE = 0x0E
  POP = 0x0F
  EXIT = 0xFF
  PRINT_STACK = 0xA0
  JUMP = 0xA1
  FLIP_BIT = 0xA2
  USE = 0xA3
  SWAP_2 = 0xA4
  VERBOSE = 0xA5

  INSTRUCTIONS = {
    "PUSH": lambda v: bytes([Program.PUSH, int(v)]),

    "SET": lambda r, v: bytes([Program.PUSH, int(v), Program.PUSH, int(r), Program.PUSH_TO_REGISTER]),

    "SET_STACK": lambda r: bytes([Program.PUSH, int(r), Program.PUSH_TO_REGISTER]),

    "LOAD": lambda r: bytes([Program.PUSH, int(r), Program.LOAD_FROM_REGISTER]),

    "PRINT": lambda r: bytes([Program.PUSH, int(r), Program.PRINT_REGISTER]),

    "ADD": lambda: bytes([Program.ADD]),

    "SUB": lambda: bytes([Program.SUB]),

    "MUL": lambda: bytes([Program.MUL]),

    "DIV": lambda: bytes([Program.DIV]),

    "DUP": lambda: bytes([Program.DUPLICATE]),

    "POP": lambda: bytes([Program.POP]),

    "CALLDATA": lambda: bytes([Program.LOAD_CALLDATA]),

    "PRINT_STACK": lambda: bytes([Program.PRINT_STACK]),

    "EQUALS_TWO_ITEMS_STACK": lambda: bytes([Program.EQUALS]),

    "EQUALS_ONE_ITEM_STACK": lambda i: bytes([Program.PUSH, int(i), Program.EQUALS]),

    "EQUALS_CALLDATA": lambda v: bytes([Program.PUSH, int(v), Program.LOAD_CALLDATA, Program.EQUALS]),

    "EQUALS_CALLDATA_STACK": lambda: bytes([Program.LOAD_CALLDATA, Program.EQUALS]),

    "COMPARE_BYTE_VALUE_TWO_ITEMS_STACK": lambda: bytes([Program.GREATER_THAN]),

    "COMPARE_BYTE_VALUE_ONE_ITEM_STACK": lambda i: bytes([Program.PUSH, int(i), Program.GREATER_THAN]),

    "COMPARE_WITH_CALLDATA": lambda i: bytes([Program.PUSH, int(i), Program.LOAD_CALLDATA, Program.GREATER_THAN]),

    "COMPARE_WITH_CALLDATA_STACK": lambda: bytes([Program.LOAD_CALLDATA, Program.GREATER_THAN]),

    "JUMP_IF": lambda d: bytes([Program.PUSH, int(d), Program.SWAP_1, Program.JUMP_IF]),

    "JUMP_IF_NOT": lambda d: bytes([Program.FLIP_BIT, Program.PUSH, int(d), Program.SWAP_1, Program.JUMP_IF]),

    "REGISTER_PLUS": lambda r, v: bytes([Program.PUSH, int(r), Program.LOAD_FROM_REGISTER, Program.PUSH, int(v), Program.ADD]),

    "PLUS_EQUALS": lambda r, a: bytes([Program.PUSH, int(r), Program.LOAD_FROM_REGISTER, Program.PUSH, int(a), Program.ADD, Program.PUSH, int(r), Program.PUSH_TO_REGISTER]),

    "MINUS_EQUALS": lambda r, a: bytes([Program.PUSH, int(r), Program.LOAD_FROM_REGISTER, Program.PUSH, int(a), Program.SUB, Program.PUSH, int(r), Program.PUSH_TO_REGISTER]),

    "TIMES_EQUALS": lambda r, a: bytes([Program.PUSH, int(r), Program.LOAD_FROM_REGISTER, Program.PUSH, int(a), Program.MUL, Program.PUSH, int(r), Program.PUSH_TO_REGISTER]),

    "DIVIDE_EQUALS": lambda r, a: bytes([Program.PUSH, int(r), Program.LOAD_FROM_REGISTER, Program.PUSH, int(a), Program.DIV, Program.PUSH, int(r), Program.PUSH_TO_REGISTER]),

    "PLUS_EQUALS_STACK": lambda r: bytes([Program.PUSH, int(r), Program.LOAD_FROM_REGISTER, Program.ADD, Program.PUSH, Program.PUSH, int(r), Program.PUSH_TO_REGISTER]),

    "PRINT_VALUE": lambda v: bytes([Program.PUSH, int(v), Program.PUSH, 31, Program.PUSH_TO_REGISTER, Program.PUSH, 31, Program.PRINT_REGISTER]),

    "SWAP": lambda: bytes([Program.SWAP_1]),

    "SWAP_2": lambda: bytes([Program.SWAP_2]),

    "VERBOSE": lambda: bytes([Program.VERBOSE])
  }
  
  @staticmethod
  def load_file(file_path):
    if not file_path.endswith(".bin"):
      raise ValueError("File must be .bin")
      
    with open(file_path, "rb") as f:
       return Program(f.read())
      
  def __init__(self, _bytes, inital_stack=[]):
    self.bytes = _bytes
    self.imports = dict()
    self.instructions = Program.INSTRUCTIONS
    self.initial_stack = inital_stack

  @staticmethod
  def load_code_file(path):
    if not path.endswith(".fose"):
      raise ValueError("File extension must be .fose")
    
    with open(path, "r") as f:
      return Program.compile_code(f.read())

  @staticmethod
  def compile_code(code):
    try:
      _bytes = b""
    
      code = code.replace("START", "0")

      for line in code.splitlines():
        values = line.strip().split(" ")
        if values[0] == "DECLARE":
          code = code.replace(values[1], values[2])

      for line in code.splitlines():
        values = line.strip().split(" ")
        #print(values)
        instruction = values[0]

        if line.startswith("#"):
          continue

        if instruction == "DECLARE":
          continue

        if instruction == "USE":
          byte_values = bytes([0xa3, int(values[1]), len(values[2])]) + str.encode(values[2])
          _bytes += byte_values
          continue

        if instruction in Program.INSTRUCTIONS:
          byte_values = Program.INSTRUCTIONS[instruction](*values[1:])
          _bytes += byte_values
        else:
          if instruction != "":
            raise ValueError(f"Unknown instruction {instruction}")
      return Program(_bytes)
    except ValueError as e:
      print(e)
      raise e
       
  def run(self, _calldata):
    registers = [0] * 32
    pc = 0
    stack = self.initial_stack
    verbose = False

    while pc < len(self.bytes):
      if verbose:
        sleep(1)
        print(stack)
      try:
        match self.bytes[pc]:
         case 0x00: # push
           stack.insert(0, self.bytes[pc+1])
           pc += 2
         case 0x01: # push to register
           register = stack.pop(0)
           value = stack.pop(0)
           registers[register] = value
           pc += 1
           #print(registers)
         case 0x02: # load from register
           register = stack.pop(0)
           value = registers[register]
           stack.insert(0, value)
           pc += 1
         case 0x03: # add
           value1 = stack.pop(0)
           value2 = stack.pop(0)
           pc += 1
           stack.insert(0, ((value2) + (value1)) % 256)
         case 0x04: # sub
           value1 = stack.pop(0)
           value2 = stack.pop(0)
           stack.insert(0, ((value2) - (value1)) % 256)
           pc += 1 
         case 0x05: # mul
           value1 = stack.pop(0)
           value2 = stack.pop(0)
           stack.insert(0, ((value2) * (value1)) % 256)
           pc += 1
         case 0x06: # div
           value1 = stack.pop(0)
           value2 = stack.pop(0)
           stack.insert(0, (value2) // (value1))
           pc += 1
         case 0x07: # print register
           register = stack.pop(0)
           print(registers[register])
           pc += 1
         case 0x08: # equals
           value1 = stack.pop(0)
           value2 = stack.pop(0)
           stack.insert(0, 0x01 if value1 == value2 else 0x00)
           pc += 1
         case 0x09: # jump if
           condition = stack.pop(0)
           to = stack.pop(0)
           if condition != 0x00:
             pc = to
           else:
             pc += 1
         case 0x0A: # less than
           value1 = stack.pop(0)
           value2 = stack.pop(0)
           stack.insert(0, 0x01 if value1 < value2 else 0x00)
           pc += 1
         case 0x0B: # greater than
           value1 = stack.pop(0)
           value2 = stack.pop(0)
           stack.insert(0, 0x01 if value1 > value2 else 0x00)
           pc += 1
         case 0x0C: # swap 1
           stack[0], stack[1] = stack[1], stack[0]
           pc += 1
         case 0x0D: # load calldata
           if type(_calldata) is bytes:
            stack.insert(0, int(_calldata[0]))
           else:
             stack.insert(0, int(_calldata))
           pc += 1
         case 0x0E: # duplicate
           stack.insert(0, stack[0])
           pc += 1
         case 0x0F: # pop
           stack.pop(0)
           pc += 1
         case 0xA0: # print stack
           print(stack)
           pc += 1
         case 0xA1: # jump 
           to = stack.pop(0)
           pc = to
         case 0xA2: # filp bit
           v = stack.pop(0)
           stack.append(0x00 if v > 0 else 0x01)
           pc += 1
         case 0xA3: # use module
           length_of_module_name = self.bytes[pc+2]
           module = bytes.decode(self.bytes[pc+3:pc+3+length_of_module_name])
           calldata = self.bytes[pc+1]
           with open(module, "r") as f:
             code = Program.compile_code(f.read())
           stack = code.run(calldata)
           pc += 3 + length_of_module_name
         case 0xA4:
            stack[1], stack[2] = stack[2], stack[1]
            pc += 1
         case 0xA5:
            verbose = True
            pc += 1
         case 0xFF: # exit
           break
         case _:
           raise ValueError(f"Unknown opcode {self.bytes[pc]}")
      except ValueError as e:
        print(e)
        return
      """except IndexError as e:
        print("Stack underflow")
        return"""
    return stack
      
  def __bytes__(self):
    return self.bytes
  
  def __len__(self):
    return len(self.bytes)
   
  def write_to_binary_file(self, path):
    if not path.endswith(".bin"):
      raise ValueError("File extension must be .bin")
    
    with open(path, "wb") as f:
      f.write(bytes(self))

def load_fose(*args):
  if len(args) != 2:
    raise ValueError(f'Expected 2 arguments "path" and "calldata" got {len(args)}')
  path, calldata = args
  Program.load_code_file(path).run(calldata)

def load_bin(*args):
  if len(args) != 2:
    raise ValueError(f'Expected 2 arguments "path" and "calldata". Got {len(args)}')
  path, calldata = args
  Program.load_file(path).run(calldata)

def print_bytes_from_fose(*args):
  if len(args) != 1:
    raise ValueError(f'Expected 1 arguments "path". Got {len(args)}')
  path = args[0]
  print(bytes(Program.load_code_file(path)))

def print_bytes_from_bin(*args):
  if len(args) != 1:
    raise ValueError(f'Expected 1 arguments "path". Got {len(args)}')
  path = args[0]
  print(bytes(Program.load_file(path)))

def len_of_bin(*args):
  if len(args) != 1:
    raise ValueError(f'Expected 1 argument "path". Got {len(args)}')
  path = args[0]
  print(len(Program.load_file(path)))

def len_of_fose(*args):
  if len(args) != 1:
    raise ValueError(f'Expected 1 argument "path". Got {len(args)}')
  path = args[0]
  print(len(Program.load_code_file(path)))

def fose_to_bin(*args):
  if len(args) != 2:
    raise ValueError(f'Expected 2 arguments "src_path" and "dest_path". Got {len(args)}')
  src_path, dest_path = args
  Program.load_code_file(src_path).write_to_binary_file(dest_path)
  
functions = {
  "run_fose_program": load_fose,
  "run_binary_program": load_bin,
  "print_bytes_from_fose": print_bytes_from_fose,
  "print_bytes_from_bin": print_bytes_from_bin,
  "print_len_of_fose": len_of_fose,
  "print_len_of_bin": len_of_bin,
  "compile_fose_to_bin": fose_to_bin
}

_, func, *rest = argv

if func not in functions:
  print(f"function {func} does not exist.")
  exit()

try:
  functions[func](*rest)

except ValueError as e:
  print(e)