from constants import *
from Tkinter import *
import socket
import string
from threading import Thread
    

class Client(object):
    def __init__(self):
        self.createCommandMap()
        self.createKeyCommandMap()
        self.createKeyMoveMap()
        self.createWindow()
        self.resetIO()
        self.root.mainloop()
    
    def createCommandMap(self):
        self.commandMap = {COMMAND_MESSAGE: self.message,
                           COMMAND_CLEAR: self.setClear,
                           COMMAND_CANCEL: self.setCancel,
                           COMMAND_KEY: self.setKeyCommand,
                           COMMAND_SHIP: self.addShip,
                           COMMAND_RECON_SHIP_BOARD: self.addReconMyBoard,
                           COMMAND_RECON_BOARD: self.addReconOpponentBoard,
                           COMMAND_PEG_SHIP_BOARD: self.addPegMyBoard,
                           COMMAND_PEG_BOARD: self.addPegOpponentBoard}
        
    def createKeyCommandMap(self):
        self.keyPressMap = {
                            KEY_COMMAND_NONE: self.keyNone,
                            KEY_COMMAND_MOVE: self.keyMove,
                            KEY_COMMAND_PATTERN: self.keyPattern,
                            KEY_COMMAND_COORDINATE: self.keyCoordinate,
                            KEY_COMMAND_COORDINATE_COL: self.keyCoordinateCol,
                            KEY_COMMAND_SHIP: self.keyShip,
                            KEY_COMMAND_SHIP_COL: self.keyShipCol,
                            KEY_COMMAND_ENTER: self.keyEnter
                            }
        
    def createKeyMoveMap(self):
        self.keyMoveMap = {KEY_F1: AIRCRAFT_CARRIER_MISSILE,
                           KEY_F2: BATTLESHIP_MISSILE,
                           KEY_F3: DESTROYER_MISSILE,
                           KEY_F4: SUBMARINE_MISSILE,
                           KEY_F5: ANTI_AIRCRAFT_GUN,
                           KEY_F6: SUBMARINE_SCAN,
                           KEY_F7: RECON_1_FLY,
                           KEY_F8: RECON_1_SCAN,
                           KEY_F9: RECON_2_FLY,
                           KEY_F10: RECON_2_SCAN,}
    
    def createWindow(self):
        self.root = Tk()
        self.root.config(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.title("Battleship: Advanced Mission")
        try:
            self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='icon.gif'))
        except:
            pass
        self.root.bind('<KeyPress>', self.keyPress)
        self.createBoard()
        self.createSidePanel()
    
    def createBoard(self):
        boardWidth = (COLS+1)*(COORDINATE_SIZE+COORDINATE_OUTLINE)+COORDINATE_OUTLINE
        boardHeight = (ROWS+1)*(COORDINATE_SIZE+COORDINATE_OUTLINE)+COORDINATE_OUTLINE
        boardMinWidth = boardWidth + 2*PADX
        boardMinHeight = boardHeight + 2*PADY
        boardFrame = Frame(self.root, bg=BACKGROUND_COLOR)
        boardFrame.grid(row=0, column=0, sticky=N)
        boardFrame.columnconfigure(0, weight=1, minsize=boardMinWidth)
        boardFrame.rowconfigure(0, weight=1, minsize=boardMinHeight)
        boardFrame.rowconfigure(1, weight=1, minsize=boardMinHeight)
        self.opponentBoard = Canvas(boardFrame, width=boardWidth, height=boardHeight, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.opponentBoard.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
        self.myBoard = Canvas(boardFrame, width=boardWidth, height=boardHeight, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.myBoard.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
        self.drawBoards()

    def createSidePanel(self):
        sideFrame = Frame(self.root, bg=BACKGROUND_COLOR)
        sideFrame.grid(row=0, column=1, sticky=N+S)
        sideFrame.rowconfigure(0, weight=1)
        self.createInfo(sideFrame)
        self.createLog(sideFrame)

    def createLog(self, sideFrame):
        logFrame = Frame(sideFrame, bg=BACKGROUND_COLOR)
        logFrame.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
        logFrame.columnconfigure(0, weight=1)
        logFrame.rowconfigure(0, weight=1)
        self.log = Log(logFrame)
        self.log.grid(row=0, column=0, sticky=N+S+W+E)
        logScrollbar = Scrollbar(logFrame, orient=VERTICAL)
        logScrollbar.grid(row=0, column=1, sticky=N+S)
        self.log.config(yscrollcommand=logScrollbar.set)
        logScrollbar.config(command=self.log.yview)
        
    def createInfo(self, sideFrame):
        self.infoFrame = Frame(sideFrame, bg=BACKGROUND_COLOR)
        self.infoFrame.grid(row=1, column=0, padx=PADX, pady=PADY)
        self.infoFrame.columnconfigure(3, minsize=INFO_SPACE_MINSIZE)
        for col in [1,2,5,6]:
            self.infoFrame.columnconfigure(col, minsize=INFO_COL_MINSIZE)
        self.columnSpace = Label(self.infoFrame, bg=BACKGROUND_COLOR)
        self.columnSpace.grid(row=0, column=3)
        self.createTwoPatternInfo(0, 0, "F1", "Aircraft Carrier", AIRCRAFT_CARRIER_PATTERN_1, AIRCRAFT_CARRIER_PATTERN_2, COLOR_HIT)
        self.createOnePatternInfo(1, 0, "F2", "Battleship", BATTLESHIP_PATTERN, COLOR_HIT)
        self.createTwoPatternInfo(2, 0, "F3", "Destroyer", DESTROYER_PATTERN_1, DESTROYER_PATTERN_2, COLOR_HIT)
        self.createSubmarineInfo(3, 0, "F4", "Submarine", COLOR_HIT)
        self.createOnePatternInfo(4, 0, "F5", "Anti-Aircraft Gun", ANTI_AIRCRAFT_GUN_PATTERN, COLOR_HIT)
        self.createOnePatternInfo(0, 1, "F6", "Submarine Scan", SUBMARINE_SCAN_PATTERN, COLOR_SUBMARINE_SCAN)
        self.createReconFlyInfo(1, 1, "F7", "Recon 1 Fly")
        self.createTwoPatternInfo(2, 1, "F8", "Recon 1 Scan", RECON_ONE_SCAN_PATTERN_1, RECON_ONE_SCAN_PATTERN_2, COLOR_RECON_SCAN)
        self.createReconFlyInfo(3, 1, "F9", "Recon 2 Fly")
        self.createTwoPatternInfo(4, 1, "F10", "Recon 2 Scan", RECON_TWO_SCAN_PATTERN_1, RECON_TWO_SCAN_PATTERN_2, COLOR_RECON_SCAN)
    
    def createOnePatternInfo(self, row, col, key, title, pattern, color):
        self.createKeyTitleInfo(row, col, key, title)
        patternLabel = Label(self.infoFrame, fg=INFO_TEXT_COLOR, bg=BACKGROUND_COLOR)
        patternLabel.grid(row=3*row+1, column=4*col+1, columnspan=2)
        pattern = self.createPattern(pattern, color)
        pattern.grid(row=3*row+2, column=4*col+1, columnspan=2, pady=INFO_PATTERN_PADY)
        
    def createTwoPatternInfo(self, row, col, key, title, patternOne, patternTwo, color):
        self.createKeyTitleInfo(row, col, key, title)
        patternOneLabel = Label(self.infoFrame, text="1", fg=INFO_TEXT_COLOR, bg=BACKGROUND_COLOR)
        patternOneLabel.grid(row=3*row+1, column=4*col+1)
        patternTwoLabel = Label(self.infoFrame, text="2", fg=INFO_TEXT_COLOR, bg=BACKGROUND_COLOR)
        patternTwoLabel.grid(row=3*row+1, column=4*col+2)
        patternOne = self.createPattern(patternOne, color)
        patternOne.grid(row=3*row+2, column=4*col+1, pady=INFO_PATTERN_PADY)
        patternOne = self.createPattern(patternTwo, color)
        patternOne.grid(row=3*row+2, column=4*col+2, pady=INFO_PATTERN_PADY)
        
    def createSubmarineInfo(self, row, col, key, title, color):
        self.createKeyTitleInfo(row, col, key, title)
        patternOneLabel = Label(self.infoFrame, text="1", fg=INFO_TEXT_COLOR, bg=BACKGROUND_COLOR)
        patternOneLabel.grid(row=3*row+1, column=4*col+1)
        patternTwoLabel = Label(self.infoFrame, text="2", fg=INFO_TEXT_COLOR, bg=BACKGROUND_COLOR)
        patternTwoLabel.grid(row=3*row+1, column=4*col+2)
        patternOne = self.createVerticalArrowPattern(color)
        patternOne.grid(row=3*row+2, column=4*col+1, pady=INFO_PATTERN_PADY)
        patternOne = self.createHorizontalArrowPattern(color)
        patternOne.grid(row=3*row+2, column=4*col+2, pady=INFO_PATTERN_PADY)

    def createReconFlyInfo(self, row, col, reconKey, reconTitle):
        reconOneKeyLabel = Label(self.infoFrame, text=reconKey, bg=INFO_KEY_COLOR)
        reconOneKeyLabel.grid(row=3*row+0, column=4*col+0, padx=INFO_KEY_PADX, sticky=N)
        reconOneTitleLabel = Label(self.infoFrame, text=reconTitle, fg=INFO_TEXT_COLOR, bg=BACKGROUND_COLOR)
        reconOneTitleLabel.grid(row=3*row+0, column=4*col+1, columnspan=2, sticky=NW)
    
    def createKeyTitleInfo(self, row, col, key, title):
        keyLabel= Label(self.infoFrame, text=key, bg=INFO_KEY_COLOR, fg=INFO_KEY_TEXT_COLOR)
        keyLabel.grid(row=3*row+0, column=4*col+0, padx=INFO_KEY_PADX, sticky=N)
        titleLabel = Label(self.infoFrame, text=title, fg=INFO_TEXT_COLOR, bg=BACKGROUND_COLOR)
        titleLabel.grid(row=3*row+0, column=4*col+1, columnspan=2, sticky=NW)
    
    # combine methods
    def createPattern(self, pattern, patternColor):
        patternCanvas, _patternWidth, _patternHeight = self.createPatternCanvas(pattern, patternColor)
        return patternCanvas
    
    def createVerticalArrowPattern(self, arrowColor):
        patternCanvas, patternWidth, patternHeight = self.createPatternCanvas("---------", COLOR_HIT)
        patternCanvas.create_line(patternWidth/2, -1, patternWidth/2, patternHeight, fill=arrowColor, width=INFO_PATTERN_ARROW_WIDTH, arrow=BOTH, arrowshape=INFO_PATTERN_ARROW_SHAPE)
        return patternCanvas
    
    def createHorizontalArrowPattern(self, arrowColor):
        patternCanvas, patternWidth, patternHeight = self.createPatternCanvas("---------", COLOR_HIT)
        patternCanvas.create_line(-1, patternHeight/2, patternWidth, patternHeight/2, fill=arrowColor, width=INFO_PATTERN_ARROW_WIDTH, arrow=BOTH, arrowshape=INFO_PATTERN_ARROW_SHAPE)
        return patternCanvas
    
    def createPatternCanvas(self, pattern, patternColor):
        patternWidth = PATTERN_COLS*(INFO_PATTERN_SIZE+INFO_PATTERN_OUTLINE) - INFO_PATTERN_OUTLINE
        patternHeight = PATTERN_ROWS*(INFO_PATTERN_SIZE+INFO_PATTERN_OUTLINE) - INFO_PATTERN_OUTLINE
        patternCanvas = Canvas(self.infoFrame, width=patternWidth, height=patternHeight, bg=BACKGROUND_COLOR, highlightthickness=0)
        for patternRow in xrange(PATTERN_ROWS):
            for patternCol in xrange(PATTERN_COLS):
                left = patternCol * (INFO_PATTERN_SIZE + INFO_PATTERN_OUTLINE)
                top = patternRow * (INFO_PATTERN_SIZE + INFO_PATTERN_OUTLINE)
                right = left + INFO_PATTERN_SIZE
                bottom = top + INFO_PATTERN_SIZE
                color = patternColor if pattern[patternRow*PATTERN_COLS+patternCol] == PATTERN_MARK else COLOR_MISS
                patternCanvas.create_rectangle(left, top, right, bottom, fill=color, width=0)
        return patternCanvas, patternHeight, patternWidth
    
    def startGame(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientSocket.connect((HOST, PORT))
            clientThread = Thread(None, self.run, ())
            clientThread.start()
            self.root.mainloop()
        except:
            print "Unable to connect to %s:%d" % (HOST, PORT)
    
    def run(self):
        dataBuffer = ""
        while True:
            data = self.clientSocket.recv(RECV_SIZE)
            if not data:
                self.root.quit()
                return
            dataBuffer += data
            while END_COMMAND in dataBuffer:
                line, _end, dataBuffer = dataBuffer.partition(END_COMMAND)
                args = line.split(" ")
                command = args.pop(0)
                if command in self.commandMap:
                    self.commandMap[command](*args)
            
    def send(self, message):
        self.clientSocket.send(message)
        
    def sendReply(self):
        self.clientSocket.send(" ".join(self.currentReply))
        self.resetIO()
        
    def resetIO(self):
        self.keyCommand = KEY_COMMAND_NONE
        self.currentReply = []
        self.replyRow = 0
        self.replyCol = 0
    
    def appendReply(self, word):
        self.currentReply.append(str(word))
    
    def appendReplyRow(self):
        self.appendReply(self.replyRow)
        self.replyRow = 0
        
    def appendReplyCol(self):
        self.appendReply(self.replyCol)
        self.replyCol = 0
    
    def isValidReplyCol(self):
        return (self.replyCol > 0 and self.replyCol <= COLS)
    
    def message(self, message):
        self.log.post(message.replace("_", " "))
            
    def setClear(self):
        self.log.setClear()
    
    def setCancel(self):
        self.log.setCancel()
    
    def setKeyCommand(self, keyCommand):
        self.keyCommand = keyCommand
    
    def keyPress(self, event):
        if event.keysym == KEY_BACKSPACE or event.keysym == KEY_DELETE:
            self.log.clear()
            self.send(COMMAND_CLEAR)
            self.resetIO()
        elif event.keysym == KEY_ESCAPE:
            self.log.cancel()
            self.send(COMMAND_CANCEL)
            self.resetIO()
        elif (self.keyCommand in self.keyPressMap):
            self.keyPressMap[self.keyCommand](event)
        #handle error
            
    def keyNone(self, event):
        pass
        
    def keyMove(self, event):
        if (event.keysym in self.keyMoveMap):
            self.send(self.keyMoveMap[event.keysym])
        elif self.keyRow(event.char.upper()):
            self.send(MOVE_MISSILE)
            self.appendReplyRow()
            self.keyCommand = KEY_COMMAND_COORDINATE_COL
    
    def keyPattern(self, event):
        try:
            pattern = int(event.char)
            # change this
            if (pattern == 1 or pattern == 2):
                self.log.post(event.char)
                self.send(event.char)
        except:
            pass

    def keyRow(self, char):
        try:
            if char in string.ascii_uppercase:
                row = string.ascii_uppercase.index(char) + 1
                if (row > 0 and row <= ROWS):
                    self.log.post(char)
                    self.replyRow = row
                    return True
            return False
        except:
            return False
    
    def keyCol(self, char):
        try:
            if char in string.digits:
                col = self.replyCol*10+int(char)
                if (col > 0 and col <= COLS):
                    self.log.post(char)
                    self.replyCol = col
                    return True
            return False
        except:
            return False
                
    def keyCoordinate(self, event):
        if self.keyRow(event.char.upper()):
            self.appendReplyRow()
            self.keyCommand = KEY_COMMAND_COORDINATE_COL
    
    def keyCoordinateCol(self, event):
        char = event.char.upper()
        if (self.keyCol(char)):
            # or return?
            pass
        elif self.isValidReplyCol() and (event.keysym == KEY_ENTER or event.keysym == KEY_NUM_ENTER):
            self.appendReplyCol()
            self.sendReply()
    
    def keyShip(self, event):
        if self.keyRow(event.char.upper()):
            self.appendReplyRow()
            self.keyCommand = KEY_COMMAND_SHIP_COL
    
    def keyShipCol(self, event):
        char = event.char.upper()
        if (self.keyCol(char)):
            pass
        elif self.isValidReplyCol() and self.keyRow(char):
            self.appendReplyCol()
            self.appendReplyRow()
            self.keyCommand = KEY_COMMAND_COORDINATE_COL
                
    
    def keyEnter(self, event):
        if event.keysym == KEY_ENTER or event.keysym == KEY_NUM_ENTER:
            self.send(" ")
    
    def getCoordinateArgs(self, row, col):
        row, col = int(row), int(col)
        left = col * (COORDINATE_SIZE + COORDINATE_OUTLINE) + COORDINATE_OUTLINE
        top = row * (COORDINATE_SIZE  + COORDINATE_OUTLINE) + COORDINATE_OUTLINE
        right = left + COORDINATE_SIZE
        bottom = top + COORDINATE_SIZE
        return  left, top, right, bottom
    
    def getSquareArgs(self, row, col):
        left, top, right, bottom = self.getCoordinateArgs(row, col)
        left -= COORDINATE_OUTLINE / 2
        top -= COORDINATE_OUTLINE / 2
        right += COORDINATE_OUTLINE / 2
        bottom += COORDINATE_OUTLINE / 2
        return (left+right)/2, (top+bottom)/2, left, top, right, bottom
    
    def getPegArgs(self, row, col):
        left, top, right, bottom = self.getCoordinateArgs(row, col)
        left += PEG_PADDING
        top += PEG_PADDING
        right -= PEG_PADDING
        bottom -= PEG_PADDING
        return left, top, right, bottom
    
    def getReconArgs(self, row, col):
        left, top, right, bottom = self.getCoordinateArgs(row, col)
        left += RECON_PADDING
        top += RECON_PADDING
        right -= RECON_PADDING
        bottom -= RECON_PADDING
        return left, top, left, bottom, right, (top+bottom)/2
    
    def drawBoards(self):
        for row in xrange(ROWS+1):
            for col in xrange(COLS+1):
                x, y, left, top, right, bottom= self.getSquareArgs(row, col)
                if row == 0 and col == 0:
                    self.myBoard.create_rectangle(left, top, right, bottom, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR, width=COORDINATE_OUTLINE)
                    self.opponentBoard.create_rectangle(left, top, right, bottom, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR, width=COORDINATE_OUTLINE)
                else:
                    self.myBoard.create_rectangle(left, top, right, bottom, fill=BOARD_COLOR, outline=BOARD_OUTLINE_COLOR, width=COORDINATE_OUTLINE)
                    self.opponentBoard.create_rectangle(left, top, right, bottom, fill=BOARD_COLOR, outline=BOARD_OUTLINE_COLOR, width=COORDINATE_OUTLINE)
                    if row == 0:
                        self.myBoard.create_text(x, y, text=col, fill=BOARD_TEXT_COLOR)
                        self.opponentBoard.create_text(x, y, text=col, fill=BOARD_TEXT_COLOR)
                    if col == 0:
                        self.myBoard.create_text(x, y, text=string.ascii_uppercase[row-1], fill=BOARD_TEXT_COLOR)
                        self.opponentBoard.create_text(x, y, text=string.ascii_uppercase[row-1], fill=BOARD_TEXT_COLOR)

    def addPegMyBoard(self, row, col, color):
        left, top, right, bottom = self.getPegArgs(row, col)
        self.myBoard.create_oval(left, top, right, bottom, fill=color, width=0)
        
    def addPegOpponentBoard(self, row, col, color):
        left, top, right, bottom = self.getPegArgs(row, col)
        self.opponentBoard.create_oval(left, top, right, bottom, fill=color, width=0)
    
    def addShip(self, row, col, color):
        left, top, right, bottom = self.getCoordinateArgs(row, col)
        self.myBoard.create_rectangle(left, top, right, bottom, fill=color, width=0)
            
    def addReconMyBoard(self, row, col, color):
        x1, y1, x2, y2, x3, y3 = self.getReconArgs(row, col)
        self.myBoard.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, width=0)
        
    def addReconOpponentBoard(self, row, col, color):
        x1, y1, x2, y2, x3, y3 = self.getReconArgs(row, col)
        self.opponentBoard.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, width=0)

class Log(Text):
    def __init__(self, master, **cnf):
        Text.__init__(self, master, width=LOG_WIDTH, height=LOG_HEIGHT, bg=LOG_COLOR, fg=LOG_TEXT_COLOR, state=DISABLED, wrap=WORD, **cnf)
        self.setClear()
        self.setCancel()
        
    def setClear(self):
        self.mark_set(CLEAR, "%s -1c" % END)
        self.mark_gravity(CLEAR, LEFT)
    
    def setCancel(self):
        self.mark_set(CANCEL, "%s -1c" % END)
        self.mark_gravity(CANCEL, LEFT)
        
    def post(self, message):
        self.config(state=NORMAL)
        self.insert(END, message)
        self.config(state=DISABLED)
        self.see(END)
        
    def clear(self):
        self.config(state=NORMAL)
        self.delete(CLEAR, END)
        self.config(state=DISABLED)
        self.see(END)
        
    def cancel(self):
        self.config(state=NORMAL)
        self.delete(CANCEL, END)
        self.config(state=DISABLED)
        self.see(END)
        
Client()
