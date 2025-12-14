# 22 bit Assembler for mips (Assembly instruction -> Binary machine code -> Hexadecimal input suited for logisim's memory)

def checkOpcode(inst):              #done(22bits)
    convertOpcode = " "
    if inst in ["ADD", "SUB", "XOR", "SRL", "NOP"]:
        convertOpcode = "00000"
  
    elif inst == "BNE":
        convertOpcode = "00001"
    elif inst == "SLTi":
        convertOpcode = "00010"  
    elif inst == "J":
        convertOpcode = "00011" 
    elif inst == "SW":
        convertOpcode = "00100"
    elif inst == "ORi":
        convertOpcode = "00101"        
    elif inst == "LW":
        convertOpcode = "00110"
    else:
        convertOpcode = "Invalid instrcution"
    return convertOpcode

# checkOpcode("LW")

def checkRegister(reg):
    convertReg = ""
    if reg == "R0":
        convertReg = "0000"
    elif reg == "R1":
        convertReg = "0001"
    elif reg == "R2":
        convertReg = "0010"
    elif reg == "R3":
        convertReg = "0011"
    elif reg == "R4":
        convertReg = "0100"
    elif reg == "R5":
        convertReg = "0101"
    elif reg == "R6":
        convertReg = "0110"
    elif reg == "R7":
        convertReg = "0111"
    elif reg == "R8":
        convertReg = "1000"
    elif reg == "R9":
        convertReg = "1001"
    elif reg == "R10":
        convertReg = "1010"
    elif reg == "R11":
        convertReg = "1011"
    elif reg == "R12":
        convertReg = "1100"
    elif reg == "R13":
        convertReg = "1101"
    elif reg == "R14":
        convertReg = "1110"
    elif reg == "R15":
        convertReg = "1111"
    else:
        convertReg ="Invalid Register"
    return convertReg

# checkRegister("R11")

def checkFunction(inst):     #done(22 bits)
    convertFunction = ""
    if inst == "ADD":
        convertFunction = "00"
    elif inst == "SUB":
        convertFunction = "01"   
    elif inst == "XOR":
        convertFunction = "10"
    elif inst == "SRL":
        convertFunction = "11"   
    else:
        convertFunction = "Invalid instrcution"
    return convertFunction

# checkFunction("XOR")

def checkShamt(inst_name, num):  # num is decimal  #done(22 bits)
  if(inst_name in ["ADD", "SUB", "XOR"]):
    return "000"

  if inst_name in ["SRL"]:
    if num < 0 or num > 7:
      return "Invalid Shamt input"

    result = ""
    if num == 0:
      result = "000"
    else:
      while num > 0:
        remainder = num % 2
        result = str(remainder) + result
        num = num // 2

    # Pad to 5 bits
    while len(result) < 3:
        result = "0" + result
    return result

# checkShamt("SUB", 21)
# checkShamt("SRA", 45)

def checkImmediate(num):  # num is decimal  #done(22 bits)

    if num < -256 or num > 255  or num > 512: # Check if num fits in 16-bit signed range, and also check if in range for unsigned number
        return "Invalid immediate: Out of 9-bit range"

    # Convert negative numbers using 2's complement
    if num < 0:
        num = (1 << 9) + num

    result = ""

    # Convert to binary
    if num == 0:
        result = "0"
    else:
        while num > 0:
            remainder = num % 2
            result = str(remainder) + result
            num = num // 2

    # Pad to 16 bits
    while len(result) < 9:
        result = "0" + result

    return result

# checkImmediate(-1)

def checkJumpAddress(address):  #done(22 bits)
  if address < 0 or address > 131071:
    return "Invalid jump address"

  result = ""

  if address == 0:
    result = "0"
  else:
    while address > 0:
      remainder = address % 2
      result = str(remainder) + result
      address = address // 2

  # Pad to 26 bits
  while len(result) < 17:
      result = "0" + result

  return result

# checkJumpAddress(12)

def convertBinToHex(bin):
    hex =""
    if bin == "0000":
        hex = "0"
    elif bin == "0001":
        hex = "1"
    elif bin == "0010":
        hex = "2"
    elif bin == "0011":
        hex = "3"
    elif bin == "0100":
        hex = "4"
    elif bin == "0101":
        hex = "5"
    elif bin == "0110":
        hex = "6"
    elif bin == "0111":
        hex = "7"
    elif bin == "1000":
        hex = "8"
    elif bin == "1001":
        hex = "9"
    elif bin == "1010":
        hex = "A"
    elif bin == "1011":
        hex = "B"
    elif bin == "1100":
        hex = "C"
    elif bin == "1101":
        hex = "D"
    elif bin == "1110":
        hex = "E"
    elif bin == "1111":
        hex = "F"
    return hex

def main():
  with open('mips_test.txt', 'r') as readf, open('mips_hex_ROM_outputFile.txt', 'w') as writef:
    writef.write("v2.0 raw\n")

    for i in readf:
      splitted = i.split()

      if(splitted[0] in ["ADD", "SUB", "XOR"]):
        conv_opcode = checkOpcode(splitted[0])
        conv_rd = checkRegister(splitted[1])
        conv_rs = checkRegister(splitted[2])
        conv_rt = checkRegister(splitted[3])

        conv_shamt = "000"      # conv_shamt = checkShamt(splitted[0], splitted[3])
        conv_function = checkFunction(splitted[0])

        binary_ins = conv_opcode + conv_rs + conv_rt + conv_rd + conv_shamt + conv_function
        print(binary_ins)

      elif(splitted[0] in ["SRL"]):
        conv_opcode = checkOpcode(splitted[0])
        conv_rd = checkRegister(splitted[1])
        conv_rs = checkRegister(splitted[2])
        conv_rt = checkRegister("R0")

        conv_shamt = checkShamt(splitted[0], int(splitted[3]))
        conv_function = checkFunction(splitted[0])

        binary_ins = conv_opcode + conv_rs + conv_rt + conv_rd + conv_shamt + conv_function
        print(binary_ins)

      elif splitted[0] in ["SLTi","SW", "ORi", "LW"]:    # instruction pattern: addi $rt, $rs, immediate
        conv_opcode = checkOpcode(splitted[0])
        conv_rt = checkRegister(splitted[1])
        conv_rs = checkRegister(splitted[2])
        conv_im = checkImmediate(int(splitted[3]))

        binary_ins = conv_opcode + conv_rs + conv_rt + conv_im
        print(binary_ins)

      elif splitted[0] in ["BNE"]:          # instruction pattern: beq $rs, $rt, label
        conv_opcode = checkOpcode(splitted[0])
        conv_rs = checkRegister(splitted[1])
        conv_rt = checkRegister(splitted[2])
        conv_label = checkImmediate(int(splitted[3]))

        binary_ins = conv_opcode + conv_rs + conv_rt + conv_label
        print(binary_ins)

      elif splitted[0] == "J":
        conv_opcode = checkOpcode(splitted[0])
        conv_address = checkJumpAddress(int(splitted[1]))
        binary_ins = conv_opcode + conv_address
        print(binary_ins)

      elif splitted[0] == "NOP":
        conv_opcode = checkOpcode(splitted[0])
        binary_ins = conv_opcode + "00000000000000000"
        print(binary_ins)

      while len(binary_ins) % 4 != 0:
       binary_ins = "0" + binary_ins

      hex_ins = ""
      for i in range(0, len(binary_ins), 4):
        group = binary_ins[i:i+4]
        hex_digit = convertBinToHex(group)
        hex_ins += hex_digit
      writef.write(hex_ins+ "\n")

if __name__ == "__main__":
    main()

print("Reading contents of mips_hex_ROM_outputFile.txt file:")
with open('mips_hex_ROM_outputFile.txt', 'r') as f:
  content = f.read()
  print(content)
