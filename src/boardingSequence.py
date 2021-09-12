'''
Name: Boarding Sequence Simulation Project
By: Damian Poclitar
Date: 27/04/2021
Python Version: 3.9.2 64-bit

Description: Small GUI that uses different algorithms to simulate passengers boarding various plane layours with different methods
'''


#Importing libraries
import time
from tkinter import *


#Creating the GUI
root = Tk()
root.title("Boarding Sequence Simulation")
root.iconbitmap('planeIcon.ico')
root.geometry("1200x800")
root.resizable(width=False, height=False)


#Initializing variables
rows = 0
columns = 0
layout = []
hCurrentRow = 0
hCurrentCol = 0
totalSeats = 0
hTotalCount = 0 
hLeftToMove = 0
hMiddleTotal = 0
hMiddleLeft = 0
speed = 0

path = '_'
seat = 'L'
human = 'O'

timeTaken = 0
middle = 0

ignoreList = []

BTF = False
WILMA = False
FTB = False
SP = False
SM = False
priority = False


#Adding humans method, finds the middle of the 2d layout and adds the human in column 0 if there is a spot open, 
#Returns total humans and total humans in the middle
def addHuman(hMiddleTotal, hTotalCount):

            if (layout[middle][0] == path):
                layout[middle][0] = human
                hMiddleTotal = hMiddleTotal + 1
                hTotalCount = hTotalCount + 1
                humanCanvas = simulationCanvas.create_oval(xCanvas, yCanvas+(50*middle), xCanvas+50, yCanvas+50+(50*middle), fill="yellow", outline="black", width="3")
                root.update()
                time.sleep(speed)
                print("Human added")

                for i in range(rows):
                    print(layout[i])

            else:
                print("No spot, did not add human")

            return hMiddleTotal, hTotalCount

#Create Layout method, creates a 2d layout based on the selected shape using nested loop, it adds path and seating
#Exceptions added for priority layout in order to skip some "blocks" in the layout
#Returns total seats in the layout
def createLayout(totalSeats):

    for i in range(rows):
        sub = []

        for f in range(columns):
            if priority == True:
                if (i == middle):
                    sub.append(path)
                    seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*f), yCanvas+(50*i), xCanvas+50+(50*f), yCanvas+50+(50*i), fill="white", outline="black", width="1")

                else:
                    if (f < 3 and (i == 0 or i == rows-1)):
                        sub.append(path)
                        seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*f), yCanvas+(50*i), xCanvas+50+(50*f), yCanvas+50+(50*i), fill="white", outline="black", width="1")

                    else:
                        sub.append(seat)
                        totalSeats = totalSeats + 1
                        seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*f), yCanvas+(50*i), xCanvas+50+(50*f), yCanvas+50+(50*i), fill="#606de0", outline="black", width="3")

            else:
                if (i == middle):
                    sub.append(path)
                    seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*f), yCanvas+(50*i), xCanvas+50+(50*f), yCanvas+50+(50*i), fill="white", outline="black", width="1")

                else:
                    sub.append(seat)
                    totalSeats = totalSeats + 1
                    seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*f), yCanvas+(50*i), xCanvas+50+(50*f), yCanvas+50+(50*i), fill="#606de0", outline="black", width="3")
            
        layout.append(sub)
    return totalSeats

#Method to get the human's X and Y position in the layout based on how many there are in the middle of the layout
#Returns X and Y position (row and column)
def getHumanPos(hCurrentRow, hCurrentCol, hMiddleLeft):

    hit = hMiddleLeft

    for i in range(columns):
        if (layout[middle][i] == human and (hit == hit-1 or hit == 1)):
            hCurrentRow = middle
            hCurrentCol = i

            return hCurrentRow, hCurrentCol

        elif (layout[middle][i] == human and hit != 1):
            hit = hit - 1 

            continue

        else:

            continue

#Algorithm for Back to Front boarding method
#Takes X and Y position of the current human once it reaches the target seat and updates to a new one
#Moves up and down until it reaches the middle and then it moves 1 spot to the left
#Returns new target X and Y position
def changeTargetBTF(tRow, tColumn):

    #Bellow
    if (tRow > middle):
        tRow = tRow - 1

        if (tRow == middle):
            tRow = 0

    #Above
    elif (tRow < middle):
        tRow = tRow + 1

        if (tRow == middle):
            tColumn = tColumn - 1
            tRow = rows - 1

    return tRow, tColumn


#Algorithm for WILMA boarding method
#Takes X and Y position of the current human once it reaches the target seat and updates to a new one
#Moves left until it reaches the border of the layout, after that it moves back at the back of the plane with updated row either lower or higher
#Returns new target X and Y position
def changeTargetWILMA(tRow, tColumn):

    #Bellow
    if (tRow > middle):
        tColumn = tColumn - 1

        if (tColumn < 0 or layout[tRow][tColumn] != seat):
            tColumn = columns - 1
            tRow = 0

            while (layout[tRow][tColumn] == human):
                tRow = tRow + 1

    #Above
    elif (tRow < middle):
        tColumn = tColumn - 1

        if (tColumn < 0 or layout[tRow][tColumn] != seat):
            tColumn = columns - 1
            tRow = rows - 1

            while (layout[tRow][tColumn] == human):
                tRow = tRow - 1

    return tRow, tColumn


#Algorthm for Front to back boarding method
#Takes X and Y position of the current human once it raches the target seat and updates to a new one
#Same as the Back to front algorithm but instead of going left once it reaches middle it goes right instead
#Exception added if priority layout is used, priority passengers use FTB first before the chosen boarding method
#Returns new target X and Y position
def changeTargetFTB(tRow, tColumn):

    global priority

    if (priority == True):
        #Bellow
        if (tRow > middle):
            tRow = tRow - 1

            if (tRow == middle):
                tRow = 1
        #Above
        elif (tRow < middle):
            tRow = tRow + 1

            if (tRow == middle and tColumn == 2):
                priority = False

            elif (tRow == middle):
                tRow = rows - 2
                tColumn = tColumn + 1

        return tRow, tColumn

    #Bellow
    elif (tRow > middle):
        if (tRow -1 == middle):
            tRow = 0
            return tRow, tColumn

        tRow = tRow - 1
    
    #Above
    elif (tRow < middle):
        if (tRow + 1 == middle):
            tColumn = tColumn + 1
            tRow = rows - 1
            return tRow, tColumn

        tRow = tRow + 1

    return tRow, tColumn

#Algorithm for Steffen Perfect boarding method
#Takes X and Y position of the current human once it reaches the target seat and updates to a new one
#Moves every other column to the left once target seat is reached, once it reaches the border it changes the side of the seats
#If the seat is occupied once it tries to changes side then it will loop left to check if empty, if that too is occupied it will move down or up and right
#It will repeat until it finds an empty seat
#Returns new target X and Y position
def changeTargetSP(tRow, tColumn):

    #Bellow
    if (tRow > middle):
        tColumn = tColumn - 2

        if (tColumn < 0 or layout[tRow][tColumn] != seat):
            tColumn = columns - 1
            tRow = 0

            if (layout[tRow][tColumn] == human):
                tColumn = tColumn - 1

                if (layout[tRow][tColumn] == human):
                    for i in range(1, middle+1):
                        for f in range(1, 3):
                            if (layout[tRow + i][columns - f] != human):
                                tColumn = columns - f
                                tRow = tRow + i
                                return tRow, tColumn

                            else:
                                continue


    #Above              
    elif (tRow < middle):
        tColumn = tColumn - 2

        if (tColumn < 0 or layout[tRow][tColumn] != seat):
            tColumn = columns - 1
            tRow = rows - 1

            if (layout[tRow][tColumn] == human):
                tColumn = tColumn - 1

                if (layout[tRow][tColumn] == human):
                    for i in range(1, middle+1):
                        for f in range(1, 3):
                            if (layout[rows - i][columns - f] != human):
                                tColumn = columns - f
                                tRow = rows - i
                                return tRow, tColumn

                            else:
                                continue

    return tRow, tColumn


#Algorthm for Steffen Modified boarding method
#Takes X and Y position of the current human once it raches the target seat and updates to a new one
#It will move every other seat to the left until it reaches border, once that is done it goes back to the plane and moves either down or up depending on the side
#Once it reaches the middle it will change side
#Returns new target X and Y position
def changeTargetSM(tRow, tColumn):


    #Bellow
    if (tRow > middle):
        tColumn = tColumn - 2

        if (tColumn < 0 or layout[tRow][tColumn] != seat):
            tRow = tRow - 1
            tColumn = columns - 1

            if (layout[tRow][tColumn] == human):
                tColumn = tColumn - 1

            if (tRow == middle):
                tColumn = columns - 1
                tRow = 0

                if (layout[tRow][tColumn] == human):
                    tColumn = tColumn - 1

        return tRow, tColumn

    #Above
    elif (tRow < middle):
        tColumn = tColumn - 2

        if (tColumn < 0 or layout[tRow][tColumn] != seat):
            tRow = tRow + 1
            tColumn = columns - 1

            if (layout[tRow][tColumn] == human):
                tColumn = tColumn - 1

            if (tRow == middle):
                tColumn = columns - 1
                tRow = rows - 1

                if (layout[tRow][tColumn] == human):
                    tColumn = tColumn - 1

        return tRow, tColumn



#Method that takes the current human position and moves them towards the target position
#Returns new target position
def humanMove(hCurrentRow, hCurrentCol, tRow, tColumn, hMiddleLeft):

    global timeTaken

    #Update the tick count on the GUI
    timeLabel.configure(text="Tick: " + str(timeTaken))

    #Does not move the human if they are already in target position
    if (int(str(hCurrentCol) + str(hCurrentRow)) in ignoreList):
        print("Human already in target position, skipping")
        return tRow, tColumn

    if (hCurrentCol == tColumn and hCurrentRow == tRow):
        print("Human in target position, skipping")
        return tRow, tColumn


    #Moves the human up and down the layout if they are in the target column
    elif (hCurrentCol == tColumn and hCurrentRow != tRow):

        #While loop to move the human up and down
        while (hCurrentRow != tRow):
        
            #Does not move if human blocking path
            if (tRow > hCurrentRow and layout[hCurrentRow+1][hCurrentCol] == human) or (tRow < hCurrentRow and layout[hCurrentRow-1][hCurrentCol] == human):
                print("Human in pathway, not moving")
                break

            #Moving down
            if tRow > hCurrentRow:

                #Changes the tile down to human
                layout[hCurrentRow+1][hCurrentCol] = human

                #Changes the current tile to path tile if in middle
                #Add ticks to the human movement
                if hCurrentRow == middle:
                    timeTaken = timeTaken + 2

                    if (layout[hCurrentRow][hCurrentCol-1] != path or hCurrentCol-1 < 0):
                        timeTaken = timeTaken + (totalSeats - len(ignoreList) - hMiddleLeft)

                    layout[hCurrentRow][hCurrentCol] = path
                    seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*hCurrentCol), yCanvas+(50*hCurrentRow), xCanvas+50+(50*hCurrentCol), yCanvas+50+(50*hCurrentRow), fill="white", outline="black", width="1")

                #Changes the current tile to seat tile
                #Add ticks to the human movement
                else:
                    timeTaken = timeTaken + 1
                    layout[hCurrentRow][hCurrentCol] = seat
                    seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*hCurrentCol), yCanvas+(50*hCurrentRow), xCanvas+50+(50*hCurrentCol), yCanvas+50+(50*hCurrentRow), fill="#606de0", outline="black", width="3")


                #Add human tile in the GUI and update the GUI
                humanCanvas = simulationCanvas.create_oval(xCanvas+(50*hCurrentCol), yCanvas+(50*(hCurrentRow+1)), xCanvas+50+(50*hCurrentCol), yCanvas+50+(50*(hCurrentRow+1)), fill="yellow", outline="black", width="3")
                root.update()
                time.sleep(speed)
                hCurrentRow = hCurrentRow+1
                

            #Moving up, the same as the moving down if statement
            elif tRow < hCurrentRow:

                layout[hCurrentRow-1][hCurrentCol] = human

                if hCurrentRow == middle:
                    if (layout[hCurrentRow][hCurrentCol-1] == human or hCurrentCol-1 < 0):
                        timeTaken = timeTaken + (totalSeats -  len(ignoreList) - hMiddleLeft)


                    layout[hCurrentRow][hCurrentCol] = path
                    seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*hCurrentCol), yCanvas+(50*hCurrentRow), xCanvas+50+(50*hCurrentCol), yCanvas+50+(50*hCurrentRow), fill="white", outline="black", width="1")

                else:
                    timeTaken = timeTaken + 1
                    layout[hCurrentRow][hCurrentCol] = seat
                    seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*hCurrentCol), yCanvas+(50*hCurrentRow), xCanvas+50+(50*hCurrentCol), yCanvas+50+(50*hCurrentRow), fill="#606de0", outline="black", width="3")

                humanCanvas = simulationCanvas.create_oval(xCanvas+(50*hCurrentCol), yCanvas+(50*(hCurrentRow-1)), xCanvas+50+(50*hCurrentCol), yCanvas+50+(50*(hCurrentRow-1)), fill="yellow", outline="black", width="3")
                root.update()
                time.sleep(speed)
                hCurrentRow = hCurrentRow-1

            #Print layout in console
            for f in range(rows):
                print(layout[f])
        
            print("")



        #Front to back movement called if chosen in the drop down menu in the GUI or if priority layout is chosen
        #Adds position in a list
        #Calls the FTB algorith with the current target X and Y position to get an updated one
        if ((FTB == True and hCurrentCol == tColumn and hCurrentRow == tRow) or priority == True):
            if int(str(tColumn) + str(tRow)) not in ignoreList:
                ignoreList.append(int(str(tColumn) + str(tRow)))
            tRow, tColumn = changeTargetFTB(tRow, tColumn)
            timeTaken = timeTaken + 2
            print("Target changed to " + str(tRow) + " " + str(tColumn))
            seatsLabel.configure(text="Seats: " + str(len(ignoreList)) + "/" + str(totalSeats))
            hMiddleLeft = hMiddleLeft - 1

        #Back to Front movement called if chosen in the drop down menu in the GUI
        #Adds position in a list
        #Calls the BTF algorith with the current target X and Y position to get an updated one
        elif (BTF == True and hCurrentCol == tColumn and hCurrentRow == tRow):
            if int(str(tColumn) + str(tRow)) not in ignoreList:
                ignoreList.append(int(str(tColumn) + str(tRow)))
            tRow, tColumn = changeTargetBTF(tRow, tColumn)
            timeTaken = timeTaken + 2
            print("Target changed to " + str(tRow) + " " + str(tColumn))
            seatsLabel.configure(text="Seats: " + str(len(ignoreList)) + "/" + str(totalSeats))
            hMiddleLeft = hMiddleLeft - 1

        #WILMA movement called if chosen in the drop down menu in the GUI
        #Adds position in a list
        #Calls the WILMA algorith with the current target X and Y position to get an updated one
        elif(WILMA == True and hCurrentCol == tColumn):
            if int(str(hCurrentCol) + str(hCurrentRow)) not in ignoreList:
                ignoreList.append(int(str(hCurrentCol) + str(hCurrentRow)))
            tRow, tColumn = changeTargetWILMA(tRow, tColumn)
            print("Target changed to " + str(tRow) + " " + str(tColumn))
            seatsLabel.configure(text="Seats: " + str(len(ignoreList)) + "/" + str(totalSeats))
            hMiddleLeft = hMiddleLeft - 1

        #Steffen Perfect movement called if chosen in the drop down menu in the GUI
        #Adds position in a list
        #Calls the Steffen Perfect algorith with the current target X and Y position to get an updated one
        elif (SP == True and hCurrentCol == tColumn):
            if int(str(hCurrentCol) + str(hCurrentRow)) not in ignoreList:
                ignoreList.append(int(str(hCurrentCol) + str(hCurrentRow)))
            tRow, tColumn = changeTargetSP(tRow, tColumn)
            print("Target changed to " + str(tRow) + " " + str(tColumn))
            seatsLabel.configure(text="Seats: " + str(len(ignoreList)) + "/" + str(totalSeats))
            hMiddleLeft = hMiddleLeft - 1

        #Steffen Modified movement called if chosen in the drop down menu in the GUI
        #Adds position in a list
        #Calls the Steffen Modified algorith with the current target X and Y position to get an updated one
        elif (SM == True and hCurrentCol == tColumn):
            if int(str(hCurrentCol) + str(hCurrentRow)) not in ignoreList:
                ignoreList.append(int(str(hCurrentCol) + str(hCurrentRow)))
            tRow,tColumn = changeTargetSM(tRow, tColumn)
            timeTaken = timeTaken + 2
            print("Target changed to " + str(tRow) + " " + str(tColumn))
            seatsLabel.configure(text="Seats: " + str(len(ignoreList)) + "/" + str(totalSeats))
            hMiddleLeft = hMiddleLeft - 1

        for f in range(rows):
            print(layout[f])
        print("")

    #Moving the human to the right if the current column is not the target column and the path is free
    elif (hCurrentCol+1 < columns and layout[hCurrentRow][hCurrentCol+1] == path and hCurrentCol != tColumn):
    
        #Update tiles in the layout array
        layout[hCurrentRow][hCurrentCol + 1] = human
        layout[hCurrentRow][hCurrentCol] = path
        hCurrentCol = hCurrentCol+1


        #Update movement in the GUI Canvas
        seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*(hCurrentCol-1)), yCanvas+(50*hCurrentRow), xCanvas+50+(50*(hCurrentCol-1)), yCanvas+50+(50*hCurrentRow), fill="white", outline="black", width="1")
        humanCanvas = simulationCanvas.create_oval(xCanvas+(50*hCurrentCol), yCanvas+(50*hCurrentRow), xCanvas+50+(50*hCurrentCol), yCanvas+50+(50*hCurrentRow), fill="yellow", outline="black", width="3")
        timeTaken = timeTaken + 1
        
        if (speed != 0):
            root.update()
            time.sleep(speed)

        for f in range(rows):
            print(layout[f])
        print("")


    #Moving the human to the left, almost the same as the move to the right if statement
    elif (layout[hCurrentRow][hCurrentCol-1] == path and hCurrentCol != tColumn):

        layout[hCurrentRow][hCurrentCol - 1] = human
        layout[hCurrentRow][hCurrentCol] = path
        hCurrentCol = hCurrentCol-1

        #print(str(hCurrentRow) + "!!!!!" + str(hCurrentCol))
        seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*(hCurrentCol+1)), yCanvas+(50*hCurrentRow), xCanvas+50+(50*(hCurrentCol+1)), yCanvas+50+(50*hCurrentRow), fill="white", outline="black", width="1")
        humanCanvas = simulationCanvas.create_oval(xCanvas+(50*hCurrentCol), yCanvas+(50*hCurrentRow), xCanvas+50+(50*hCurrentCol), yCanvas+50+(50*hCurrentRow), fill="yellow", outline="black", width="3")
        timeTaken = timeTaken + 1
        
        if (speed != 0):
            root.update()
            time.sleep(speed)
        

        for f in range(rows):
            print(layout[f])
        print("")

    else:
        print("Something went wrong")
        return tRow, tColumn, hMiddleLeft


    return tRow, tColumn, hMiddleLeft


#Main method that is called once the "Start" button is pressed in the GUI
#Initiates everything, calls all the functions in order
def startButtonClick():
    global BTF
    global WILMA
    global FTB
    global SP
    global SM
    global totalSeats
    global hMiddleTotal
    global hTotalCount
    global hMiddleLeft
    global hCurrentRow
    global hCurrentCol
    global rows
    global columns
    global middle
    global speed
    global priority

    tRow = 0
    tColumn = 0

    startButton["state"] = "disabled"
    ddLayoutDrop["state"] = "disabled"
    ddMethodDrop["state"] = "disabled"
    ddSpeedDrop["state"] = "disabled"
    
    layoutStr = clicked.get()
    methodStr = clicked2.get()
    speedStr = clicked3.get()


    #Dropdown options for the boarding method
    if (methodStr == "Back-to-Front"):
        BTF = True

    elif (methodStr == "WILMA"):
        WILMA = True

    elif (methodStr == "Front-to-Back"):
        FTB = True

    elif (methodStr == "Steffen Perfect"):
        SP = True

    elif (methodStr == "Steffen Modified"):
        SM = True

    #Dropdown options for the layout method
    if (layoutStr == "Default (7x10)"):
        rows = 7
        columns = 10

    elif (layoutStr == "Embraer E-170 (5x18)"):
        rows = 5    
        columns = 18

    elif (layoutStr == "Gulfstream G550 (3x8)"):
        rows = 3
        columns = 8
        
    elif (layoutStr == "Default with Priority"):
        rows = 7
        columns = 13
        priority = True
        
    elif (layoutStr == "High Capacity (9x20)"):
        rows = 9
        columns = 20

    #Dropdown options for the simulation speed
    if (speedStr == "Fast"):
        speed = 0
    
    elif (speedStr == "Medium"):
        speed = 0.05

    elif (speedStr == "Slow"):
        speed = 0.5


    #Calculate the middle and update the seat and tick label
    middle = int(rows/2)
    seatsLabel.configure(text="Seats: 0/" + str((rows*columns)-columns))
    timeLabel.configure(text="Tick: " + str(timeTaken))


    #Creates the layout by calling the layout function
    totalSeats = createLayout(totalSeats)

    #Prints 2d layout in console for debugging
    for i in range(rows):
        print (layout[i])
    print("")


    #Adds human to the layout by calling the function
    hMiddleTotal, hTotalCount = addHuman(hMiddleTotal, hTotalCount)
    hMiddleLeft = hMiddleTotal

    #Gets the human X and Y position by calling the function
    hCurrentRow, hCurrentCol = getHumanPos(hCurrentRow, hCurrentCol, hMiddleTotal)

    #If front to back method is chosen then set the first target seat bottom left
    if (FTB == True):
        tRow = rows - 1
        tColumn = 0


    #If function for the priority layout
    if (priority == True):
        tRow = rows - 2
        tColumn = 0

        #While the priority seats aren't filled loop the following
        while(priority == True):

            #Loop until there is nobody in the middle
            while (hMiddleLeft != 0):

                #Set the target seat red
                seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*tColumn), yCanvas+(50*tRow), xCanvas+50+(50*tColumn), yCanvas+50+(50*tRow), fill="red", outline="black", width="3")

                #Get the current human position
                hCurrentRow, hCurrentCol = getHumanPos(hCurrentRow, hCurrentCol, hMiddleLeft)

                #Use the coordinates of the current human position and move them towards the target position
                tRow, tColumn, hMiddleTotal = humanMove(hCurrentRow, hCurrentCol, tRow, tColumn, hMiddleTotal)

                hMiddleLeft = hMiddleLeft - 1


            #If the people inside the plane isn't equal to the number of seats add people in the plane
            if (hTotalCount < totalSeats and len(ignoreList) != (rows*columns)-columns):
                hMiddleTotal, hTotalCount = addHuman(hMiddleTotal, hTotalCount)
                hMiddleLeft = hMiddleTotal
            else:
                hMiddleLeft = hMiddleTotal
        
        #Updates the target to bottom left if the front to back is selected in the priority layout
        if (FTB == True):
            tRow = rows - 1
            tColumn = 3

    #Set the target to bottom right if any layout other than FTB is selected
    if (BTF == True or WILMA == True or SP == True or SM == True):
        tRow = rows - 1
        tColumn = columns - 1

        
            
    #For loop, repeat from 0 to X times Y of the layout
    for i in range(0, rows*columns):

        #While the priority seats aren't filled loop the following
        while (hMiddleLeft != 0):

            #Set the target seat red
            seatCanvas = simulationCanvas.create_rectangle(xCanvas+(50*tColumn), yCanvas+(50*tRow), xCanvas+50+(50*tColumn), yCanvas+50+(50*tRow), fill="red", outline="black", width="3")

            #Console info printer for debugging
            print("Getting human position")
            print("People in the middle: " + str(hMiddleTotal))

            #Get the current human position
            hCurrentRow, hCurrentCol = getHumanPos(hCurrentRow, hCurrentCol, hMiddleLeft)

            #Use the coordinates of the current human position and move them towards the target position
            print("Moving human from pos: " + str(hCurrentRow) + " " +  str(hCurrentCol) + " to " + str(tRow) + " " + str(tColumn))

            tRow, tColumn, hMiddleTotal = humanMove(hCurrentRow, hCurrentCol, tRow, tColumn, hMiddleTotal)
            hMiddleLeft = hMiddleLeft - 1
            

        #If the people inside the plane isn't equal to the number of seats add people in the plane
        #If all the seats are occupied, break out of the loop
        if (hTotalCount < totalSeats and len(ignoreList) != (rows*columns)-columns):
            hMiddleTotal, hTotalCount = addHuman(hMiddleTotal, hTotalCount)
            hMiddleLeft = hMiddleTotal
            
        elif (FTB == True and len(ignoreList) == (rows*columns)-columns):
            print("The seats are all occupied")
            break

        elif ((BTF == True or WILMA == True or SP == True or SM == True) and len(ignoreList) == totalSeats):
            print("The seats are all occupied")
            break

        else:
            hMiddleLeft = hMiddleTotal

        
    #Printing console info for easier debugging
    print(" ")
    for f in range(rows):
        print(layout[f])
    print("Total people in the plane: " + str(hTotalCount))
    print("Total seats in the plane: " + str(totalSeats))




#Tkinter GUI parameters being created and set
clicked = StringVar()
clicked2 = StringVar()
clicked3 = StringVar()
clicked.set("Default (7x10)")
clicked2.set("Back-to-Front")
clicked3.set("Medium")

widthCanvas = 1100
heightCanvas = 600

xCanvas = 50
yCanvas = 50


statusFrame = LabelFrame(root, text="Options", padx=50, pady=1)
simulationFrame = LabelFrame(root, text="Simulation", width=1150, height=700)
simulationCanvas = Canvas(simulationFrame, width=widthCanvas, height=heightCanvas, bg="white")
ddLayoutLabel = Label(statusFrame, text="Choose your layout")
ddMethodLabel = Label(statusFrame, text="Choose your boarding method")
ddSpeedLabel = Label(statusFrame, text="Choose your simulation speed")
timeLabel = Label(statusFrame, text="Tick: 0")
seatsLabel = Label(statusFrame, text="Seats: 0/0")
startButton = Button(statusFrame, text="Start", command=startButtonClick)
ddLayoutDrop = OptionMenu(statusFrame, clicked, "Default (7x10)", "Embraer E-170 (5x18)", "Gulfstream G550 (3x8)", "Default with Priority", "High Capacity (9x20)" )
ddMethodDrop = OptionMenu(statusFrame, clicked2, "Back-to-Front", "Front-to-Back", "WILMA", "Steffen Perfect", "Steffen Modified")
ddSpeedDrop = OptionMenu(statusFrame, clicked3, "Fast", "Medium", "Slow")



statusFrame.grid(pady=1, padx=10, column=0, row=0)
ddLayoutLabel.grid(pady=1, padx=10, column=0, row=0)
ddLayoutDrop.grid(pady=1, padx=10, column=0, row=1)
ddMethodLabel.grid(pady=1, padx=10, column=1, row=0)
ddMethodDrop.grid(pady=1, padx=10, column=1, row=1)
ddSpeedLabel.grid(pady=1, padx=10, column=2, row=0)
ddSpeedDrop.grid(pady=1, padx=10, column=2, row=1)
timeLabel.grid(pady=10, padx=10, column=3, row=1)
seatsLabel.grid(pady=10, padx=10, column=4, row=1)
startButton.grid(pady=10, padx=10, column=5, row=1)
simulationFrame.grid(pady=1, padx=10, column=0, row=1)
simulationCanvas.grid()


root.mainloop()
            
