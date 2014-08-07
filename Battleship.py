from constants import *
import socket
import string
from threading import Thread

class Game(object):
    
    def __init__(self):
        self.createMoveMap()
        self.createHitMap()
        self.createColorMap()
        self.createSocket()
        while True:
            self.startNewGame()

    def createMoveMap(self):
        self.moveMap = {MOVE_MISSILE: self.missile,
                        AIRCRAFT_CARRIER_MISSILE: self.aircraftCarrierMissile,
                        BATTLESHIP_MISSILE: self.battleshipMissile,
                        DESTROYER_MISSILE: self.destroyerMissile,
                        SUBMARINE_MISSILE: self.submarineMissile,
                        ANTI_AIRCRAFT_GUN: self.antiAircraftGun,
                        SUBMARINE_SCAN: self.submarineScan,
                        RECON_1_FLY: self.reconOneFly,
                        RECON_1_SCAN: self.reconOneScan,
                        RECON_2_FLY: self.reconTwoFly,
                        RECON_2_SCAN: self.reconTwoScan}
        
    def createHitMap(self):
        self.shipMap = {STATUS_AIRCRAFT_CARRIER: self.aircraftCarrierHit,
                        STATUS_BATTLESHIP: self.battleshipHit,
                        STATUS_DESTROYER: self.destroyerHit,
                        STATUS_SUBMARINE: self.submarineHit,
                        STATUS_PATROL_BOAT: self.patrolBoatHit,
                        STATUS_RECON_ONE: self.reconOneHit,
                        STATUS_RECON_TWO: self.reconTwoHit}
    
    def createColorMap(self):
        self.colorMap = {STATUS_EMPTY: BOARD_COLOR,
                         STATUS_SUBMARINE_SCAN: COLOR_SUBMARINE_SCAN,
                         STATUS_RECON_SCAN: COLOR_RECON_SCAN,
                         STATUS_MISS: COLOR_MISS,
                         STATUS_HIT: COLOR_HIT,
                         STATUS_AIRCRAFT_CARRIER: COLOR_AIRCRAFT_CARRIER,
                         STATUS_BATTLESHIP: COLOR_BATTLESHIP,
                         STATUS_DESTROYER: COLOR_DESTROYER,
                         STATUS_SUBMARINE: COLOR_SUBMARINE,
                         STATUS_PATROL_BOAT: COLOR_PATROL_BOAT,
                         STATUS_RECON_ONE: COLOR_RECON_ONE,
                         STATUS_RECON_TWO: COLOR_RECON_TWO}
    
    def intMap(self, values):
        return tuple([int(value) for value in values])
    
    def coordinateString(self, row, col):
        return string.ascii_uppercase[row-1] + str(col)
    
    def broadcastMessage(self, message, newLine=True):
        self.currentPlayer.sendMessage(message, newLine)
        self.otherPlayer.sendMessage(message, newLine)
        
    def broadcastSetCancel(self):
        self.currentPlayer.setCancel()
        self.otherPlayer.setCancel()
        
    def createSocket(self):
        print "Starting server"
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((HOST, PORT))
        self.serverSocket.listen(2)

    def startNewGame(self):
        try:
            playerOneSocket, playerOneAddress = self.serverSocket.accept()
            print "%s:%d connected" % playerOneAddress
            self.currentPlayer = Player("Player 1", playerOneSocket)
            self.currentPlayer.sendMessage("You are Player 1.", False)
            playerTwoSocket, playerTwoAddress = self.serverSocket.accept()
            print "%s:%d connected" % playerTwoAddress
            self.otherPlayer = Player("Player 2", playerTwoSocket)
            self.otherPlayer.sendMessage("You are Player 2.", False)
            self.broadcastMessage("\nRemote_terminal_activated.")
            self.broadcastMessage("Satellite_link_established.")
            self.getFleet2()
            self.changePlayer()
            self.getFleet2()
            self.changePlayer()
            self.doTurn()
        except:
            self.broadcastMessage("\nError: Game ended.")
        self.endGame()
      
    def doTurn(self):
        self.broadcastMessage("\nAwaiting orders from %s: " % self.currentPlayer.name)
        self.broadcastSetCancel()
        while True:
            try:
                move = self.currentPlayer.sendRecv(COMMAND_KEY, KEY_COMMAND_MOVE)
                if move not in self.moveMap:
                    continue
                if not self.moveMap[move]():
                    self.currentPlayer.sendMessage("\nAwaiting orders from %s: " % self.currentPlayer.name)
                    continue
                if self.isGameOver() or True:
                    self.broadcastMessage("\nGame over.\n%s wins!" % self.currentPlayer.name)
                    return
                break
            except (Clear, Cancel):
                continue
            except Closed as e:
                raise e
        self.changePlayer()
        self.doTurn()
        
    def changePlayer(self):
        self.currentPlayer, self.otherPlayer = self.otherPlayer, self.currentPlayer
    
    def isGameOver(self):
        return (self.otherPlayer.aircraftCarrier.isSunk() and
                self.otherPlayer.battleship.isSunk() and
                self.otherPlayer.destroyer.isSunk() and
                self.otherPlayer.submarine.isSunk() and
                self.otherPlayer.patrolBoat.isSunk())
        
    def endGame(self):
        self.broadcastMessage("\nPress Enter to exit.")
        currentPlayerExit = Thread(None, self.currentPlayer.exit, ())
        otherPlayerExit = Thread(None, self.otherPlayer.exit, ())
        currentPlayerExit.start()
        otherPlayerExit.start()
        currentPlayerExit.join()
        otherPlayerExit.join()
        
    def getFleet(self):
        self.otherPlayer.sendMessage("\nGetting fleet configuration from %s..." % self.currentPlayer.name)
        self.getShip("\nAircraft Carrier reporting", AIRCRAFT_CARRIER_SIZE, STATUS_AIRCRAFT_CARRIER, COLOR_AIRCRAFT_CARRIER)
        self.getShip("\nBattleship reporting", BATTLESHIP_SIZE, STATUS_BATTLESHIP, COLOR_BATTLESHIP)
        self.getShip("\nDestroyer reporting", DESTROYER_SIZE, STATUS_DESTROYER, COLOR_DESTROYER)
        self.getShip("\nSubmarine reporting", SUBMARINE_SIZE, STATUS_SUBMARINE, COLOR_SUBMARINE)
        self.getShip("\nPatrol Boat reporting", PATROL_BOAT_SIZE, STATUS_PATROL_BOAT, COLOR_PATROL_BOAT)
        self.getRecon("\nRecon 1 reporting", self.currentPlayer.reconOne, STATUS_RECON_ONE, COLOR_RECON_ONE)
        self.getRecon("\n\nRecon 2 reporting", self.currentPlayer.reconTwo, STATUS_RECON_TWO, COLOR_RECON_TWO)
        
    def getFleet2(self):
        self.currentPlayer.setShip([(1,1),(1,2), (1,3), (1,4), (1,5)], STATUS_AIRCRAFT_CARRIER, COLOR_AIRCRAFT_CARRIER)
        self.currentPlayer.setShip([(3,1),(3,2), (3,3), (3,4)], STATUS_BATTLESHIP, COLOR_BATTLESHIP)
        self.currentPlayer.setShip([(5,1),(5,2), (5,3)], STATUS_DESTROYER, COLOR_DESTROYER)
        self.currentPlayer.setShip([(8,14),(9,14), (10,14)], STATUS_SUBMARINE, COLOR_SUBMARINE)
        self.currentPlayer.setShip([(7,1),(7,2)], STATUS_PATROL_BOAT, COLOR_PATROL_BOAT)
        self.currentPlayer.setRecon(self.currentPlayer.reconOne, (1,1), STATUS_RECON_ONE, COLOR_RECON_ONE)
        self.currentPlayer.setRecon(self.currentPlayer.reconTwo, (1,2), STATUS_RECON_TWO, COLOR_RECON_TWO)
      
    def getShip(self, message, size, status, color):
        self.currentPlayer.sendMessage(message)
        self.currentPlayer.setCancel()
        self.currentPlayer.setShip(self.getShipCoordinates(size), status, color)
        
    def getRecon(self, message, recon, status, color):
        self.currentPlayer.sendMessage(message)
        self.currentPlayer.setCancel()
        self.currentPlayer.setRecon(recon, self.getReconCoordinates(), status, color)
    
    def getShipCoordinates(self, size):
        self.currentPlayer.sendMessage("Enter coordinates: ")
        self.currentPlayer.setCancel()
        while True:
            try:
                startRow, startCol, endRow, endCol = self.intMap(self.currentPlayer.sendRecv(COMMAND_KEY, KEY_COMMAND_SHIP))
                coordinates = self.validateShipCoordinates(size, startRow, startCol, endRow, endCol)
                if coordinates is None:
                    self.currentPlayer.sendMessage("Incorrect coordinates")
                    self.currentPlayer.sendMessage("Enter coordinates: ")
                    continue
                return coordinates
            except (Clear, Cancel):
                continue
            except Closed as e:
                raise e
            except:
                self.currentPlayer.sendMessage("Incorrect coordinates")
                self.currentPlayer.sendMessage("Enter coordinates: ")
                self.currentPlayer.setCancel()
                continue
                                                                      
    def validateShipCoordinates(self, size, startRow, startCol, endRow, endCol):
        if not self.isValidCoordinate(startRow, startCol) or not self.isValidCoordinate(endRow, endCol):
            return None
        if startRow == endRow and endCol-startCol == size-1:
            coordinates = [(startRow, col) for col in xrange(startCol, endCol+1)]
        elif startRow == endRow and startCol-endCol == size-1:
            coordinates = [(startRow, col) for col in xrange(endCol, startCol+1)]
        elif startCol == endCol and endRow-startRow == size-1:
            coordinates = [(row, startCol) for row in xrange(startRow, endRow+1)]
        elif startCol == endCol and startRow-endRow == size-1:
            coordinates = [(row, startCol) for row in xrange(endRow, startRow+1)]
        else:
            return None
        for row, col in coordinates:
            if self.currentPlayer.getShipStatus(row, col) != STATUS_EMPTY:
                return None
        return coordinates
    
    def getReconCoordinates(self):
        self.currentPlayer.sendMessage("Enter coordinates: ")
        self.currentPlayer.setCancel()
        while True:
            try:  
                row, col = self.intMap(self.currentPlayer.sendRecv(COMMAND_KEY, KEY_COMMAND_COORDINATE))
                if not self.isValidReconCoordinate(row, col):
                    self.currentPlayer.sendMessage("Incorrect coordinates")
                    self.currentPlayer.sendMessage("Enter coordinates: ")
                    self.currentPlayer.setCancel()
                    continue
                return row, col
            except (Clear, Cancel):
                continue
            except Closed as e:
                raise e
            except:
                self.currentPlayer.sendMessage("Incorrect coordinates")
                self.currentPlayer.sendMessage("Enter coordinates: ")
                self.currentPlayer.setCancel()
                continue                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        
    def isValidReconCoordinate(self, row, col):
        return self.isValidCoordinate(row, col) and self.currentPlayer.getShipStatus(row, col) == STATUS_AIRCRAFT_CARRIER
    
    def getCoordinates(self, validateCoordinates, *args):
        self.currentPlayer.sendMessage("Enter coordinates: ")
        self.currentPlayer.setClear()
        while True:
            try:
                row, col = self.intMap(self.currentPlayer.sendRecv(COMMAND_KEY, KEY_COMMAND_COORDINATE))
                coordinates = validateCoordinates(row, col, *args)
                if coordinates is None:
                    self.currentPlayer.sendMessage("Incorrect coordinates")
                    self.currentPlayer.sendMessage("Enter coordinates: ")
                    self.currentPlayer.setClear()
                    continue
                return row, col, coordinates
            except Clear as e:
                continue
            except (Cancel, Closed) as e:
                raise e
            except:
                self.currentPlayer.sendMessage("Incorrect coordinates")
                self.currentPlayer.sendMessage("Enter coordinates: ")
                self.currentPlayer.setClear()
                continue
    
    def isValidCoordinate(self, row, col):
        return row > 0 and row <= ROWS and col > 0 and col <= COLS
    
    def isValidInnerCoordinate(self, row, col):
        return row > 1 and row < ROWS and col > 1 and col < COLS
    
    def getPatternCoordinates(self, row, col, pattern):
        coordinates = []
        startRow, startCol = row-1, col-1
        for patternRow in xrange(PATTERN_ROWS):
            for patternCol in xrange(PATTERN_COLS):
                if pattern[patternRow*PATTERN_COLS+patternCol] == PATTERN_MARK:
                    coordinates.append((startRow+patternRow, startCol+patternCol))
        return coordinates
    
    def getFiringPattern(self):
        self.currentPlayer.sendMessage("Enter firing pattern: ")
        self.currentPlayer.setClear()
        while True:
            try:
                pattern = int(self.currentPlayer.sendRecv(COMMAND_KEY, KEY_COMMAND_PATTERN))
                if not self.isValidPattern(pattern):
                    self.currentPlayer.sendMessage("Incorrect firing pattern")
                    self.currentPlayer.sendMessage("Enter firing pattern: ")
                    self.currentPlayer.setClear()
                    continue
                return pattern
            except Clear as e:
                continue
            except (Cancel, Closed) as e:
                raise e
            except:
                self.currentPlayer.sendMessage("Incorrect firing pattern")
                self.currentPlayer.sendMessage("Enter firing pattern: ")
                self.currentPlayer.setClear()
                continue
        
    def getScanPattern(self):
        self.currentPlayer.sendMessage("Enter surveillance pattern: ")
        self.currentPlayer.setClear()
        while True:
            try:
                pattern = int(self.currentPlayer.sendRecv(COMMAND_KEY, KEY_COMMAND_PATTERN))
                if not self.isValidPattern(pattern):
                    self.currentPlayer.sendMessage("Incorrect surveillance pattern")
                    self.currentPlayer.sendMessage("Enter surveillance pattern: ")
                    self.currentPlayer.setClear()
                    continue
                return pattern
            except Clear as e:
                continue
            except (Cancel, Closed) as e:
                raise e
            except:
                self.currentPlayer.sendMessage("Incorrect surveillance pattern")
                self.currentPlayer.sendMessage("Enter surveillance pattern: ")
                self.currentPlayer.setClear()
                continue
        
    def isValidPattern(self, pattern):
        return pattern if pattern == 1 or pattern ==2 else None
        
    def missile(self):
        row, col = self.intMap(self.currentPlayer.recv())
        self.sendMissileInfo("Missile", row, col)
        self.doMissile(row, col)
        return True
        
    def aircraftCarrierMissile(self):
        if self.currentPlayer.aircraftCarrier.isSunk():
            self.currentPlayer.sendMessage("Aircraft Carrier sunk")
            return False
        if self.currentPlayer.aircraftCarrier.missilesRemaining <= 0:
            self.currentPlayer.sendMessage("Aircraft Carrier missile unavailable")
            return False
        self.currentPlayer.sendMessage("Aircraft Carrier reporting, launch code accepted. Exocet missile armed.")
        pattern = self.getFiringPattern()
        row, col, coordinates = self.getCoordinates(self.validateAircraftCarrierMissileCoordiantes, pattern)
        self.sendMissileInfo("Aircraft Carrier missile", row, col, pattern)
        self.doMissiles(coordinates)
        self.currentPlayer.aircraftCarrier.missilesRemaining -= 1
        return True
        
    def validateAircraftCarrierMissileCoordiantes(self, row, col, pattern):
        if not self.isValidInnerCoordinate(row, col):
            return None
        if pattern == 1:
            coordinates = self.getPatternCoordinates(row, col, AIRCRAFT_CARRIER_PATTERN_1)
        elif pattern == 2:
            coordinates = [(row-1,col), (row,col-1), (row,col), (row,col+1), (row+1,col)]
        else:
            return None
        return coordinates
    
    def battleshipMissile(self):
        if self.currentPlayer.battleship.isSunk():
            self.currentPlayer.sendMessage("Battleship sunk")
            return False
        if self.currentPlayer.battleship.missilesRemaining <= 0:
            self.currentPlayer.sendMessage("Battleship missile unavailable")
            return False
        self.currentPlayer.sendMessage("Battleship reporting, active radar guidance systems operative. Tomahawk missile armed.")
        row, col, coordinates = self.getCoordinates(self.validateBattleshipMissileCoordiantes)
        self.sendMissileInfo("Battleship missile", row, col)
        self.doMissiles(coordinates)
        self.currentPlayer.battleship.missilesRemaining -= 1
        return True
        
    def validateBattleshipMissileCoordiantes(self, row, col):
        if not self.isValidInnerCoordinate(row, col):
            return None
        coordinates = [(row-1,col-1), (row-1,col), (row-1,col+1),
                       (row,col-1), (row,col), (row,col+1),
                       (row+1,col-1), (row+1,col), (row+1,col+1)]
        return coordinates
    
    def destroyerMissile(self):
        if self.currentPlayer.destroyer.isSunk():
            self.currentPlayer.sendMessage("Destroyer sunk")
            return False
        if self.currentPlayer.destroyer.missilesRemaining <= 0:
            self.currentPlayer.sendMessage("Destroyer missile unavailable")
            return False
        self.currentPlayer.sendMessage("Destroyer reporting, target window achieved. Apache missile armed.")
        pattern = self.getFiringPattern()
        row, col, coordinates = self.getCoordinates(self.validateDestroyerMissileCoordiantes, pattern)
        self.sendMissileInfo("Destroyer missile", row, col)
        self.doMissiles(coordinates)
        self.currentPlayer.destroyer.missilesRemaining -= 1
        return True
        
        
    def validateDestroyerMissileCoordiantes(self, row, col, pattern):
        if pattern == 1:
            coordinates = [(row,col-1), (row,col), (row,col+1)]
        elif pattern == 2:
            coordinates = [(row-1,col), (row,col), (row+1,col)]
        else:
            return None
        for row, col in coordinates:
            if not self.isValidCoordinate(row, col):
                return None
        return coordinates
    
    def submarineMissile(self):
        if self.currentPlayer.submarine.isSunk():
            self.currentPlayer.sendMessage("Submarine sunk")
            return False
        if self.currentPlayer.submarine.missilesRemaining <= 0:
            self.currentPlayer.sendMessage("Submarine torpedo unavailable")
            return False
        self.currentPlayer.sendMessage("Submarine reporting, periscope depth and stable. Torpedo armed.")
        pattern = self.getFiringPattern()
        row, col, (dRow, dCol) = self.getCoordinates(self.validateSubmarineMissileCoordiantes, pattern)
        self.sendMissileInfo("Submarine torpedo", row, col, pattern)
        self.doSubmarineMissile(row, col, dRow, dCol)
        self.currentPlayer.submarine.missilesRemaining -= 1
        return True
        
    def validateSubmarineMissileCoordiantes(self, row, col, pattern):
        if pattern == 1:
            if row == 1:
                return 1, 0
            elif row == ROWS:
                return -1, 0
        elif pattern == 2:
            if col == 1:
                return 0, 1
            elif col == COLS:
                return 0, -1
        return None
    
    def antiAircraftGun(self):
        self.currentPlayer.sendMessage("Badit sighted.  Closing in a 5,000 feet.")
        row, col, _coordinates = self.getCoordinates(self.validateAntiAircraftGunCoordinates)
        self.sendAntiAircraftGunInfo("Anti-aircraft gun", row, col)
        self.doAntiAircraftGun(row, col)
        return True
        
    def validateAntiAircraftGunCoordinates(self, row, col):
        return (row, col) if self.isValidInnerCoordinate(row, col) else None
    
    def submarineScan(self):
        if self.currentPlayer.submarine.isSunk():
            self.currentPlayer.sendMessage("Submarine sunk")
            return False
        self.currentPlayer.sendMessage("Submarine reporting, periscope depth and stable. Sonar online.")
        _row, _col, coordinates = self.getCoordinates(self.validateSubmarineScanCoordiantes)
        detected = self.doSubmarineScan(coordinates)
        self.sendSubmarineScanInfo("Submarine scan", detected)
        return True
        
    def validateSubmarineScanCoordiantes(self, row, col):
        if not self.isValidInnerCoordinate(row, col):
            return None
        coordinates = [(row-1,col-1), (row-1,col), (row-1,col+1),
                       (row,col-1), (row,col), (row,col+1),
                       (row+1,col-1), (row+1,col), (row+1,col+1)]
        return coordinates
    
    def reconOneFly(self):
        if self.currentPlayer.reconOne.hit:
            self.currentPlayer.sendMessage("Recon 1 destroyed")
            return False
        self.currentPlayer.sendMessage("Recon 1 reporting.")
        self.reconFly(self.currentPlayer.reconOne, COLOR_RECON_ONE, "Recon 1 fly")
        return True
        
    def reconTwoFly(self):
        if self.currentPlayer.reconTwo.hit:
            self.currentPlayer.sendMessage("Recon 2 destroyed")
            return False
        self.currentPlayer.sendMessage("Recon 2 reporting.")
        self.reconFly(self.currentPlayer.reconTwo, COLOR_RECON_TWO, "Recon 2 fly")
        return True
        
    def reconFly(self, recon, color, message):
        row, col, _coordinates = self.getCoordinates(self.validateReconFlyCoordinates, recon)
        self.sendReconFlyInfo(message)
        self.doReconFly(recon, row, col, color)
                
    def validateReconFlyCoordinates(self, row, col, recon):
        return (row, col) if self.isValidInnerCoordinate(row, col) and (row, col) != recon.coordinates else None
    
    def reconOneScan(self):
        if self.currentPlayer.reconOne.hit:
            self.currentPlayer.sendMessage("Recon 1 destroyed")
            return False
        if self.currentPlayer.reconOne.onShip:
            self.currentPlayer.sendMessage("Recon 1 not deployed")
            return False
        self.currentPlayer.sendMessage("Recon 1 reporting, altitude reached. Early warning systems online.")
        row, col = self.currentPlayer.reconOne.coordinates
        self.reconScan(row, col, "Recon 1 scan.")
        return True
    
    def reconTwoScan(self):
        if self.currentPlayer.reconTwo.hit:
            self.currentPlayer.sendMessage("Recon 2 destroyed")
            return False
        if self.currentPlayer.reconTwo.onShip:
            self.currentPlayer.sendMessage("Recon 2 not deployed")
            return False
        self.currentPlayer.sendMessage("Recon 2 reporting, altitude reached. Early warning systems online.")
        row, col = self.currentPlayer.reconTwo.coordinates
        self.reconScan(row, col, "Recon 2 scan.")
        return True
    
    def reconScan(self, row, col, message):
        pattern = self.getScanPattern()
        coordinates  = self.validateReconScanCoordinates(row, col, pattern)
        detectedCoordinates = self.doReconScan(coordinates)
        self.sendReconScanInfo(message, pattern, detectedCoordinates)
        
    def validateReconScanCoordinates(self, row, col, pattern):
        if not self.isValidInnerCoordinate(row, col):
            return None
        if pattern == 1:
            coordinates = [(row-1,col-1), (row-1,col+1), (row+1,col-1), (row+1,col+1)]
        elif pattern == 2:
            coordinates = [(row-1,col), (row,col-1), (row,col+1), (row+1,col)]
        else:
            return None
        return coordinates
    
    def doMissile(self, row, col):
        shipStatus = self.otherPlayer.getShipStatus(row, col)
        if shipStatus in self.shipMap:
            self.broadcastMessage("Hit at " + self.coordinateString(row, col))
            self.currentPlayer.addPegBoard(row, col, STATUS_HIT, COLOR_HIT)
            self.otherPlayer.addPegShipBoard(row, col, STATUS_HIT, COLOR_HIT)
            self.shipMap[shipStatus]()
            return True
        elif shipStatus in [STATUS_EMPTY]:
            self.currentPlayer.addPegBoard(row, col, STATUS_MISS, COLOR_MISS)
        return False

    def doMissiles(self, coordinates):
        for row, col in coordinates:
            self.doMissile(row, col)
            
    def doSubmarineMissile(self, row, col, dRow, dCol):
        while self.isValidCoordinate(row, col):
            if self.doMissile(row, col):
                break
            row += dRow
            col += dCol
    
    def doAntiAircraftGun(self, row, col):
        if not self.otherPlayer.reconOne.onShip and (row, col) == self.otherPlayer.reconOne.coordinates:
            self.reconOneShot()
        elif not self.otherPlayer.reconTwo.onShip and (row, col) == self.otherPlayer.reconTwo.coordinates:
            self.reconTwoShot()
        else:
            return
        oldStatus = self.currentPlayer.getBoardStatus(row, col)
        oldColor = self.colorMap[oldStatus]
        self.currentPlayer.addPegBoard(row, col, oldStatus, oldColor)
        
    def doSubmarineScan(self, coordinates):
        detected = False
        for row, col in coordinates:
            if self.otherPlayer.getShipStatus(row, col) in self.shipMap:
                detected = True
                break
        status = STATUS_SUBMARINE_SCAN if detected else STATUS_MISS
        color = COLOR_SUBMARINE_SCAN if detected else COLOR_MISS
        for row, col in coordinates:
            if self.currentPlayer.getBoardStatus(row, col) in [STATUS_EMPTY]:
                self.currentPlayer.addPegBoard(row, col, status, color)
        return detected
    
    def doReconFly(self, recon, row, col, color):
        oldRow, oldCol = recon.coordinates
        if recon.onShip:
            recon.onShip = False
            self.currentPlayer.send(COMMAND_SHIP, oldRow, oldCol, COLOR_AIRCRAFT_CARRIER)
        else:
            oldStatus = self.currentPlayer.getBoardStatus(oldRow, oldCol)
            oldColor = self.colorMap[oldStatus]
            self.currentPlayer.addPegBoard(oldRow, oldCol, oldStatus, oldColor)
        self.currentPlayer.send(COMMAND_RECON_BOARD, row, col, color)
        recon.coordinates = (row, col)
        
    def doReconScan(self, coordinates):
        detectedCoordinates = []
        for row, col in coordinates:
            if self.otherPlayer.getShipStatus(row, col) in self.shipMap:
                detectedCoordinates.append((row, col))
                self.currentPlayer.addPegBoard(row, col, STATUS_RECON_SCAN, COLOR_RECON_SCAN)
            elif self.currentPlayer.getBoardStatus(row, col) in [STATUS_EMPTY, STATUS_SUBMARINE_SCAN]:
                self.currentPlayer.addPegBoard(row, col, STATUS_MISS, COLOR_MISS)
        return detectedCoordinates
           
    def aircraftCarrierHit(self):
        self.otherPlayer.aircraftCarrier.hits += 1
        if (self.otherPlayer.aircraftCarrier.isSunk()):
            self.broadcastMessage("Aircraft Carrier sunk!")
        
    def battleshipHit(self):
        self.otherPlayer.battleship.hits += 1
        if (self.otherPlayer.battleship.isSunk()):
            self.broadcastMessage("Battleship sunk!")
            
    def destroyerHit(self):
        self.otherPlayer.destroyer.hits += 1
        if (self.otherPlayer.destroyer.isSunk()):
            self.broadcastMessage("Destroyer sunk!")
        
    def submarineHit(self):
        self.otherPlayer.submarine.hits += 1
        if (self.otherPlayer.submarine.isSunk()):
            self.broadcastMessage("Submarine sunk!")
          
    def patrolBoatHit(self):
        self.otherPlayer.patrolBoat.hits += 1
        if (self.otherPlayer.patrolBoat.isSunk()):
            self.broadcastMessage("Patrol Boat sunk!")
        
    def reconOneHit(self):
        self.aircraftCarrierHit()
        if self.currentPlayer.reconOne.onShip:
            self.reconOneShot()
        
    def reconTwoHit(self):
        self.aircraftCarrierHit()
        if self.currentPlayer.reconTwo.onShip:
            self.reconTwoShot()
            
    def reconOneShot(self):
        self.otherPlayer.reconOne.hit = True
        self.broadcastMessage("Recon 1 destroyed!")
        
    def reconTwoShot(self):
        self.otherPlayer.reconTwo.hit = True
        self.broadcastMessage("Recon 2 destroyed!")
        
    def sendMissileInfo(self, message, row, col, pattern=None):
        self.otherPlayer.sendMessage(message)
        if pattern is not None:
            self.otherPlayer.sendMessage("Firing pattern: " + str(pattern))
        self.otherPlayer.sendMessage("Coordinates: %s" % self.coordinateString(row, col))
        
    def sendAntiAircraftGunInfo(self, message, row, col):
        self.otherPlayer.sendMessage(message)
        self.otherPlayer.sendMessage("Coordinates: %s" % self.coordinateString(row, col))
        
    def sendSubmarineScanInfo(self, message, detected):
        self.otherPlayer.sendMessage(message)
        if detected:
            self.broadcastMessage("Sonar system detects enemy craft")
        else:
            self.broadcastMessage("Sonar system confirms clear waters")
        
    def sendReconScanInfo(self, message, pattern, detectedCoordinates):
        self.otherPlayer.sendMessage(message)
        self.broadcastMessage("Surveillance pattern: " + str(pattern))
        if not detectedCoordinates:
            self.broadcastMessage("No enemies sighted")
        else:
            self.broadcastMessage("Enemies sighted at: ")
            for row, col in detectedCoordinates:
                self.broadcastMessage(self.coordinateString(row, col))
            
    def sendReconFlyInfo(self, message):
        self.otherPlayer.sendMessage(message)
    
class Player(object):
    def __init__(self, name, playerSocket):
        self.name = name
        self.playerSocket = playerSocket
        self.shipBoard = [([STATUS_EMPTY] * COLS) for _row in xrange(ROWS)]
        self.board = [([STATUS_EMPTY] * COLS) for _row in xrange(ROWS)]
        self.aircraftCarrier = Ship(AIRCRAFT_CARRIER_SIZE, AIRCRAFT_CARRIER_MISSILES)
        self.battleship = Ship(BATTLESHIP_SIZE, BATTLESHIP_MISSILES)
        self.destroyer = Ship(DESTROYER_SIZE, DESTROYER_MISSILES)
        self.submarine = Ship(SUBMARINE_SIZE, SUBMARINE_MISSILES)
        self.patrolBoat = Ship(PATROL_BOAT_SIZE, PATROL_BOAT_MISSILES)
        self.reconOne = Recon()
        self.reconTwo = Recon()
        
    def strMap(self, values):
        return [str(value) for value in values]
    
    def exit(self):
        self.sendRecv(COMMAND_KEY, KEY_COMMAND_ENTER)
        self.playerSocket.close()

    def send(self, command, *args):
        args = self.strMap(args)
        args.insert(0, command)
        try:
            self.playerSocket.send(" ".join(args) + END_COMMAND)
        except:
            pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        
    def recv(self):
        reply = tuple(self.playerSocket.recv(RECV_SIZE).split())
        if len(reply) == 1:
            if reply[0] == COMMAND_CLEAR:
                raise Clear
            elif reply[0] == COMMAND_CANCEL:
                raise Cancel
            return reply[0]
        return reply

    def sendRecv(self, command, args):
        self.send(command, args)
        return self.recv()
       
    def sendMessage(self, message, newLine=True):
        self.send(COMMAND_MESSAGE, "%s%s" % ("\n" if newLine else "", message.replace(" ", "_")))
        
    def setClear(self):
        self.send(COMMAND_CLEAR)
        
    def setCancel(self):
        self.setClear()
        self.send(COMMAND_CANCEL)
                    
    def setShip(self, coordinates, status, color):
        for row, col in coordinates:
            self.setShipStatus(row, col, status)
            self.send(COMMAND_SHIP, row, col, color)
    
    def setRecon(self, recon, coordinates, status, color):
        recon.coordinates = coordinates
        row, col = coordinates
        self.setShipStatus(row, col, status)
        self.send(COMMAND_RECON_SHIP_BOARD, row, col, color)
    
    def getShipStatus(self, row, col):
        return self.shipBoard[row-1][col-1]
    
    def setShipStatus(self, row, col, status):
        self.shipBoard[row-1][col-1] = status
    
    def getBoardStatus(self, row, col):
        return self.board[row-1][col-1]
    
    def setBoardStatus(self, row, col, status):
        self.board[row-1][col-1] = status
        
    def addPegShipBoard(self, row, col, status, color):
        self.setShipStatus(row, col, status)
        self.send(COMMAND_PEG_SHIP_BOARD, row, col, color)
        
    def addPegBoard(self, row, col, status, color):
        self.setBoardStatus(row, col, status)
        self.send(COMMAND_PEG_BOARD, row, col, color)
        if not self.reconOne.onShip and (row, col) == self.reconOne.coordinates:
            self.send(COMMAND_RECON_BOARD, row, col, COLOR_RECON_ONE)
        elif not self.reconTwo.onShip and (row, col) == self.reconTwo.coordinates:
            self.send(COMMAND_RECON_BOARD, row, col, COLOR_RECON_TWO)
                    
class Ship(object):
    
    def __init__(self, size, missiles):
        self.coordinates = []
        self.size = size
        self.hits = 0
        self.missilesRemaining = missiles
            
    def isSunk(self):
        return self.hits == self.size
    
class Recon(object):
    
    def __init__(self):
        self.coordinates = None
        self.onShip = True
        self.hit = False
    
class Clear(Exception):
    pass    
    
class Cancel(Exception):
    pass

Game()