import sys

symbolMap = {
    "R0": "0", "R1":"1", "R2": "2", "R3": "3", "R4":"4", "R5": "5","R6": "6", "R7":"7",
    "R8": "8","R9": "9", "R10":"10", "R11": "11","R12":"12", "R13": "13","R14": "14",
    "R15":"15", "R16": "16", "SCREEN": "16384", "KBD": "24576", "SP": "0", "LCL": "1",
    "ARG": "2", "THIS": "3", "THAT": 4
}

jumpMap = {
    "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

compMap = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}

nextVarIndex = 17

def main():
    if  len(sys.argv) == 1:
        print("You must supply a file to compile in the arguments")
        return
    try:
        assemblyFile = open(sys.argv[1], "r")
        assemblyFileLines = assemblyFile.readlines()
        binaryName = sys.argv[1].split(".")[0] + ".hack"
        binaryFile = open(binaryName, "w+")

        removeCommentsAndWhitespace(assemblyFileLines)
        addLabelsToMap(assemblyFileLines, symbolMap)
        removeLabels(assemblyFileLines)      

        for line in assemblyFileLines:
            processLine(line, binaryFile)

        
    finally:
        assemblyFile.close()
        binaryFile.close()
        return

def writeBinaryToFile(binary, binaryFile):
    binaryFile.write(binary + "\n")

def processComp(comp):    
    return compMap[comp]

def processJump(jump):
    return jumpMap[jump]

def processDest(destination):
    d1 = "0"
    d2 = "0"
    d3 = "0"

    if "A" in destination:
        d1 = "1"
    if "D" in destination:
        d2 = "1"
    if "M" in destination:
        d3 = "1"

    return d1 + d2 + d3

def processCCommand(command, binaryFile):
    prefix = "111"
    
    equalsIndex = command.find("=")
    if equalsIndex != -1:
        destBits =  processDest(command[0:equalsIndex])
        command = command[equalsIndex+1:]
    else:
        destBits = "000"
    
    jumpIndex = command.find(";")
    if jumpIndex != -1:
        jumpBits =  processJump(command[jumpIndex+1:])
        command = command[:jumpIndex]
    else:
        jumpBits = "000"

    compBits = processComp(command)


    binary = prefix + compBits + destBits + jumpBits
    writeBinaryToFile(binary, binaryFile)
    
    return

def processACommand(command, binaryFile):
    binary = ""
    if command.isnumeric():
        binary = "0" + str(format(int(command), "015b"))
    else:
        if command in symbolMap:
            value = symbolMap[command]
            binary = "0" + str(format(int(value), "015b"))
        else:
            value = nextVarIndex
            symbolMap[command] = str(nextVarIndex)
            binary = "0" + str(format(nextVarIndex, "015b"))        
            nextVarIndex += 1   

    writeBinaryToFile(binary, binaryFile)
    return

def processLine(line, binaryFile):
    if line[0] == "@":
        processACommand(line[1:], binaryFile)
    else:
        processCCommand(line, binaryFile)
    return


def removeLabels(assemblyFileLines):
    for i in range(len(assemblyFileLines)-1,-1,-1):
        if assemblyFileLines[i].find("(") != -1:
            assemblyFileLines.pop(i)
    return

def addLabelsToMap(assemblyFileLines, symbolMap):
        n = 0
        for line in assemblyFileLines:
            labelStartIndex = line.find("(")
            if labelStartIndex == -1:
                n +=1
                continue
            foundEndIndex = line.find(")")
            label = line[labelStartIndex+1:foundEndIndex]
            if label not in symbolMap.keys():
                symbolMap[label] = n
        return


def removeCommentsAndWhitespace(assemblyFileLines):
    for i in range(len(assemblyFileLines)-1,-1,-1):
        commentStartIndex = assemblyFileLines[i].find("/")
        if commentStartIndex != -1:
            assemblyFileLines[i] = assemblyFileLines[i][0:commentStartIndex]

        assemblyFileLines[i] = assemblyFileLines[i].strip()
        if len(assemblyFileLines[i]) == 0:
            assemblyFileLines.pop(i)
    return

if __name__ == "__main__":
    main()

