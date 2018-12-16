# Hamilton Evans
# 12/16/18
# Sodoku Solver !!
from copy import deepcopy

def printTable (table):
    """
    Taking 2d array and printing as sodoku board.
    """
    for i in range(0,9):
        if (i!=0 and i%3==0): 
            print('- - - - - - - - - - - ')
        for j in range (0,9):
            if (j!=0 and j%8==0): 
                print(table[i][j])
            else:
                if (j!=0 and j%3==0): 
                    print ('|',end=' ')
                print(table[i][j], end=' ')

def fillTable ():
    """
    Filling table out.
    """
    table = [[0] * (9) for i in range(9)] # init table
    valid = ['', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    table[0][0] = 'X' # X to track current location
    print(50 * '\n')
    printTable(table)
    i = 0
    j = 0
    
    while (i<9):
        while (j<9):
            num = ''
            num = input('Next number: ')
            
            if (num == 'd'): # delete last number
                table[i][j] = 0
                if (j == 0 and i!= 0):
                    table[i-1][8] = 'X'
                    j=8
                    i-=1
                else:
                    if (j != 0):
                        table[i][j-1] = 'X'
                        j-=1
                    else:
                        table[0][0] = 'X'
            else:    
                while (num not in valid): # if non-valid guess
                    print(50 * '\n')
                    print('"' + str(num) + '"' + ' is not a valid number.')
                    print('Please input a number between 1 and 9.')
                    print()
                    printTable(table)
                    num = input('Next number: ')
                
                if (num != ''):
                    table[i][j] = int(num)
                else:
                    table[i][j] = 0
                
                if (j == 8):
                    if (i!=8):
                        table[i+1][0] = 'X'
                        i += 1
                        j = 0
                    else: 
                        print(50 * '\n')
                        printTable(table)
                        return table
                else:
                    table[i][j+1] = 'X'
                    j += 1
            print(50 * '\n')
            printTable(table)

def horizontals (table):
    """
    Returning horizontal rows.
    """
    allHoriz = []
    for i in range (0,9):
        temp = []
        for j in range (0,9):
            temp.append(table[i][j])
        allHoriz.append(temp)
    return allHoriz

def verticals (table):
    """
    Returning vertical rows.
    """
    allVertz = []
    for i in range (0,9):
        temp = []
        for j in range (0,9):
            temp.append(table[j][i])
        allVertz.append(temp)
    return allVertz

def boxes (table):
    """
    Returning boxes as array.
    """
    allBoxes = []
    allHoriz = horizontals (table)
    
    allBoxes.append(runBoxesLoop(0,3,0,3,allHoriz))
    allBoxes.append(runBoxesLoop(0,3,3,6,allHoriz))
    allBoxes.append(runBoxesLoop(0,3,6,9,allHoriz))
    allBoxes.append(runBoxesLoop(3,6,0,3,allHoriz))
    allBoxes.append(runBoxesLoop(3,6,3,6,allHoriz))
    allBoxes.append(runBoxesLoop(3,6,6,9,allHoriz))
    allBoxes.append(runBoxesLoop(6,9,0,3,allHoriz))
    allBoxes.append(runBoxesLoop(6,9,3,6,allHoriz))
    allBoxes.append(runBoxesLoop(6,9,6,9,allHoriz))
    
    return (allBoxes)

def runBoxesLoop (x, y, m, n, allHoriz):
    """
    Helper function for boxes.
    """
    temp = []
    for i in range(x,y):
        for j in range(m,n):
            temp.append(allHoriz[i][j])
    return temp

def allCombos (table): 
    """
    Combining arrays from horiz, vert, boxes into one.
    """
    combos = []
    horiz = horizontals(table)
    vertz = verticals(table)
    boxz = boxes (table)
    
    for array in horiz:
        combos.append(array)
    for array in vertz:
        combos.append(array)
    for array in boxz:
        combos.append(array)
    
    return combos

def checkIfValid (table): 
    """
    Checking if table is valid.
    """
    combos = allCombos(table)
    valid = False
    
    for array in combos: 
        temp = []
        for number in array: 
            if ((number in temp) and (number != 0)):
                return valid # table is not valid 
            temp.append(number)
            
    valid = True
    return valid

def possibleVals (table):
    """
    Returning possible values for location without numbers.
    """
    allVals = [1, 2, 3, 4, 5, 6, 7, 8, 9]    
    possibleArrTable = deepcopy(table)
    
    horiz = horizontals(table)
    vertz = verticals(table)
    boxz = boxes (table)
    
    for i in range(0,9): 
        for j in range(0,9):
            possibleVals = []
            if (table[i][j] == 0):
                currentHoriz = horiz[i]
                currentVert = vertz[j]
    
                if (i<3):
                    currentBox = boxz[(j//3)]
                elif(i>=3 and i<6):
                    currentBox = boxz[(j//3) + 3]
                else:
                    currentBox = boxz[(j//3) + 6]
              
                for number in allVals:
                    if ((number not in currentHoriz) and (number not in currentVert) and (number not in currentBox)):
                        possibleVals.append(number)
                
                possibleArrTable[i][j] = possibleVals        
    
    return possibleArrTable


def fillOutHoriz (table):
    """
    Checks horizontal array and fills out any value it can.
    """
    possible = possibleVals(table)
    horiz = horizontals(possible)
    for i in range(0,9):
        temp = []
        for j in range(0,9):
            if (type(horiz[i][j])!=int):
                for k in range(len(horiz[i][j])): 
                    temp.append(horiz[i][j][k])
                    
        for j in range(0,9):
            if (type(horiz[i][j])!=int):
                for k in range(len(horiz[i][j])):
                    count = 0
                    for number in temp:
                        if (horiz[i][j][k] == number):
                            count+=1
                    if (count == 1 or len(horiz[i][j]) == 1):
                        table[i][j] = (horiz[i][j][k])
                        return 
    
def fillOutVertz (table):
    """
    Checks vertical array and fills out any value it can.
    """
    possible = possibleVals(table)
    vertz = verticals(possible)
    for i in range(0,9):
        temp = []
        for j in range(0,9):
            if (type(vertz[i][j])!=int):
                for k in range(len(vertz[i][j])): 
                    temp.append(vertz[i][j][k])
                    
        for j in range(0,9):
            if (type(vertz[i][j])!=int):
                for k in range(len(vertz[i][j])):
                    count = 0
                    for number in temp:
                        if (vertz[i][j][k] == number):
                            count+=1
                    if (count == 1 or len(vertz[i][j]) == 1):
                        table[j][i] = (vertz[i][j][k])
                        return 

def fillOutBoxz (table):
    """
    Checks boxes array and fills out any value it can.
    """
    possible = possibleVals(table)
    boxz = boxes(possible)
    for i in range(0,9):
        temp = []
        for j in range(0,9):
            if (type(boxz[i][j])!=int):
                for k in range(len(boxz[i][j])): 
                    temp.append(boxz[i][j][k])
                    
        for j in range(0,9):
            if (type(boxz[i][j])!=int):
                for k in range(len(boxz[i][j])):
                    count = 0
                    for number in temp:
                        if (boxz[i][j][k] == number):
                            count+=1
                    if (count == 1 or len(boxz[i][j]) == 1):
                        if (i <3):
                            if(j<3): 
                                x = 0
                            elif(j<6): 
                                x = 1
                            elif(j<9):
                                x = 2
                        elif (i <6):
                            if(j<3): 
                                x = 3
                            elif(j<6): 
                                x = 4
                            elif(j<9):
                                x = 5
                        elif (i <9):
                            if(j<3): 
                                x = 6
                            elif(j<6): 
                                x = 7
                            elif(j<9):
                                x = 8
                        
                        y = (j%3)+(3*(i%3))
                       
                        table[x][y] = (boxz[i][j][k])
                        return 
                    
def isComplete (table): 
    """
    Checks if table is full.
    """
    complete = True
    for i in range (0,9):
        for j in range (0,9):
            if (table[i][j] == 0):
                complete = False
    return complete

def fillInitial (table):
    """
    Runs through table and fills out what it can.
    """
    complete = 0
    while (complete <= 81):
        complete += 1
        fillOutBoxz (table)
        fillOutVertz (table)
        fillOutHoriz (table)
    return table

def whichNext (table, i, j):
    """
    Gives location of next 0 (unkown value).
    """
    for i in range(i,9):
        for j in range(j,9):
            if (table[i][j] == 0):
                return i,j
    for i in range(0,9):
        for j in range(0,9):
            if (table[i][j] == 0):
                return i,j
            
    return -1, -1
    
def fillOutAll (table, i=0, j=0):
    """
    Fills out numbers that fillInitial couldn't using brute force.
    """
    i,j = whichNext(table, i, j)
    if (i == -1):
        return True
    
    poss = possibleVals (table)

    for k in (poss[i][j]):
        table[i][j] = k
        if (checkIfValid(table)):
            table[i][j] = k
            if fillOutAll(table, i, j):
                return True
            table[i][j] = 0
    return False

def solveSodoku ():
    """
    Puts it all together and solves table (assuming it is solvable).
    """
    table = fillTable()
    
    fillInitial (table)
    if not isComplete(table):
        fillOutAll(table)
    print(50 * '\n')
    if (isComplete(table) == False):
        printTable(table)
        print()
        print('This sodoku puzzle is not solvable.')
    else:
        printTable(table)
    
solveSodoku()