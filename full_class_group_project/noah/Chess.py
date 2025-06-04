import random #For Random AI Player

#Player Class
class Player():
    def __init__(self, color):
        self.color = color
        self.pieces = [] #List of all of a player's pieces
        self.abr = 'w' if color == 'White' else 'b' #To more easily give designations to pieces
        self.givePieces()
        
    def givePieces(self): #Gives the player's pieces
        self.pieces.append(king(self.abr, 1))
        self.pieces.append(queen(self.abr, 1))
        for p in range(8):
            self.pieces.append(pawn(self.abr, p+1))
        for p in range(2):
            self.pieces.append(bishop(self.abr, p+1))
            self.pieces.append(knight(self.abr, p+1))
            self.pieces.append(rook(self.abr, p+1))
    
    def make_move(self, game): #Bug Check
        print("ERROR! At class Player()") #Checking for errors

#Human Player Class, inherits from Player
class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        self.givePieces()
        
    def make_move(self,game):
        while True:
            possibleMoves = []
            piece = str(input(f"\nEnter which {self.color} piece you want to move: ")) #First chooses a piece
            gamePiece = None
            for p in self.pieces:
                if p.desig == piece:
                    gamePiece = p
                    possibleMoves = gamePiece.movement(game) #Gets all the possible moves the piece chosen piece can make
                    break
            
            if gamePiece in self.pieces and gamePiece.eliminated == False and len(possibleMoves) > 0: #Then chooses a move
                print("\n\nListing Possible Moves...\n\n"+"\033[4m## : (x, y) \033[0m")
                for moves in range(len(possibleMoves)):
                    if moves < 9:
                        print("0"+str(moves+1)+" : (" + str(possibleMoves[moves][1]+1) + ', ' + str(possibleMoves[moves][0]+1) + ")")
                    else:
                        print(str(moves+1)+" : (" + str(possibleMoves[moves][1]+1) + ', ' + str(possibleMoves[moves][0]+1) + ")")
                z = 0
                while z<1 or z>len(possibleMoves):
                    z = int(input("\nChoose which move: ")) #Chooses a move based on numbered input
                game.make_move(possibleMoves[z-1],gamePiece)
                break
            else:
                print("Choose again.")
        return True

#Random AI Player that chooses a random piece and then chooses a random available move for that piece. Inherits from Player.
class AIPlayerRandom(Player):
    def __init__(self, color):
        super().__init__(color)
        self.givePieces()
    def make_move(self,game):
        while True:
            possiblePieces = []
            possibleMoves = []
            z = 0
            gamePiece = None
            for p in self.pieces: #Loop to get all the available pieces
                if p.eliminated == False: 
                    possiblePieces.append(p)
            if len(possiblePieces) == 0:
                return False #Added to check why there were sometimes 0 possible moves to make.
            gamePiece = possiblePieces[random.randint(1,len(possiblePieces))-1] #Chooses piece
            possibleMoves = gamePiece.movement(game)
            if gamePiece in self.pieces and gamePiece.eliminated == False and len(possibleMoves) > 0: #Chooses move
                z = random.randint(0,len(possibleMoves))-1 #Chooses random move
                game.make_move(possibleMoves[z],gamePiece)
                break
        
#Class for the game
class Chess():
    def __init__(self, player1, player2):
        self.board = [['   ' for i in range(8)] for i in range(8)]
        self.pieces = {player1.color:player1.pieces, player2.color:player2.pieces} #All the Pieces, organized by color/player
        self.p1color = player1.color 
        self.p2color = player2.color 
        self.players = [player1, player2]
        self.Cor = {} #Dictionary for Coordinates

    def boarding(self):
        window = pygame.display.set_mode((400, 400))
        background = pygame.Surface(window.get_size())
        ts, w, h, c1, c2 = 50, *background.get_size(), (100, 100, 100), (50, 50, 50)
        tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
        [pygame.draw.rect(background, color, rect) for rect, color in tiles]
        window.blit(background, (0, 0))
        for a in [self.p1color,self.p2color]:
            for pieces in self.pieces[a]:
                [y, x] = pieces.checkPos(self)
                font1 = pygame.font.SysFont('freesanbold.ttf', 40)
                text1 = font1.render(pieces.type, True, ((255,255,255) if pieces.color=="w" else (0,0,0)))
                textRect1 = text1.get_rect()
                textRect1.center = ((x*50)+25, (y*50)+25)
                window.blit(text1, textRect1)
        pygame.display.flip()
        clock.tick(60)
        
    def winscreen(self, winner): 
        screen = pygame.display.set_mode((300,300))
        font1 = pygame.font.SysFont('freesanbold.ttf', 40)
        text1 = font1.render("White Wins!" if winner=='w' else "Black Wins!", True, ((255,255,255) if winner=="w" else (0,0,0)))
        screen.fill((0,0,0) if winner=="w" else (255,255,255))
        textRect1 = text1.get_rect()
        textRect1.center = (150, 150)
        screen.blit(text1, textRect1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                pygame.display.flip()
                clock.tick(60)
    
    def play(self):
        self.setBoard()
        self.boarding()
        while True:
            for player in self.players:
                self.showBoard(SHOW_BOARD)
                x = player.make_move(game)
                self.checkEnPassants(player) #After a player takes a turn, makes all the opposite color's enPassant_able equal False
                self.checkElims() #Checks if any pieces have been eliminated after every move/turn 
                if x == False: #Leftover from bug testing, x is only equal to false if there are no moves for. Kept because of the sheer amount of possible boards.
                    print("Draw")
                    self.showBoard(SHOW_BOARD)
                    break
                winner = self.checkWin() #Gets the winner from checkWin Method.
                if winner != 'None':
                    if SHOW_WINNER == True: 
                        if winner == 'b':
                            print("Black Wins!")
                        else:
                            print("White Wins!")
                        self.showBoard(True)
                        self.winscreen(winner)
                    return winner
                    
    def checkElims(self): #Checks which pieces are on the board. If it's not on the board, it's marked as eliminated
        for colors in [self.p1color,self.p2color]:   
            for pieces in self.pieces[colors]:
                for y in range(8):
                    if pieces.desig not in self.board[y]:
                        pieces.eliminated = True
                    else:
                        pieces.eliminated = False #Ends innermost loop after the piece is found
                        break
        return

    def checkWin(self):
        for colors in [self.p1color,self.p2color]:
            king = self.pieces[colors][0] #King is always the first piece appended to the list.
            if king.eliminated == True:
                return king.opcolor #Returns Winner
        return 'None'

    def checkEnPassants(self, player): #Resets opposite color's enPassant_able to False
        opcolor = 'White' if player.abr == 'b' else 'Black'
        for pieces in self.pieces[opcolor]:
            if pieces.type == 'P':
                pieces.enPassant_able = False
    
    def showBoard(self, SHOWBOARD): #Went through several different formats for the board. This ended up being the one that looked the best.
        if SHOWBOARD == True: #If you want to see the board or not
            print('\n   ', '  1  ', '  2  ', '  3  ', '  4  ', '  5  ', '  6  ', '  7  ','  8  \n')
            for y in range(8):
                print (y+1, '', '|',self.board[y][0], '|',self.board[y][1], '|',self.board[y][2], '|',self.board[y][3], '|',self.board[y][4], '|',self.board[y][5], '|',self.board[y][6], '|',self.board[y][7],'|',)
                print('   ',' ---  ', '---  ', '---  ', '---  ', '---  ', '---  ', '---  ', '---  ')
            self.boarding()
            
    def allPieceCoords(self): #Method added to bug test
        for a in [self.p1color,self.p2color]:
            for pieces in self.pieces[a]:
                print(pieces.desig, self.Cor[pieces])
            print("-")
            
    def setCoords(self): #Sets coords for all the pieces
        self.Cor = {} #Coord dictionary
        for a in [self.p1color,self.p2color]: #Loop that assigns a piece's coords to all pieces
            for pieces in self.pieces[a]:
                self.Cor[pieces] = pieces.checkPos(game)

    def setBoard(self): #Basically puts all the pieces on the board as well as assigns the coordinates for pieces.
        self.board = [['   ' for i in range(8)] for i in range(8)] #Added to wipe the board clean before putting the pieces on the board. Prevents pieces from spilling over from past games
        for x in range(8):
            self.board[1][x] = 'wP'+str(x+1)
            self.board[6][x] = 'bP'+str(x+1)
        for c in ['w','b']:
            if c == 'w':
                y=0
            else:
                y=7
            x = 0
            for p in ['R','N','B']:
                self.board[y][x] = c+p+str(1)
                self.board[y][-(1+x)] = c+p+str(2) # -(1+x) is an equation to get the reflected x coordinate
                x = x+1
            for p in range(2):
                self.board[y][x] =  c+'K'+str(1)
                self.board[y][-(1+x)] = c+'Q'+str(1)
                
        self.setCoords() #Assigns Coordinates
        self.checkElims() #Ensures everything is on the board and registers as such

    def make_move(self, coords, piece): #Method to actually makes a move on the board
        currPieceCoords = piece.checkPos(game)
        self.board[coords[0]][coords[1]] = piece.desig #First moves the piece to the spot
        self.board[currPieceCoords[0]][currPieceCoords[1]] = '   ' #Then erases itself from the spot it moved from.
        if len(coords) == 3:
            if coords[2] == "En Passant": #Added for En Passant
                self.board[coords[0]- (1 if piece.color == 'w' else -1)][coords[1]] = '   '
            colour = "White" if piece.color == 'w' else "Black"
            if coords[2] == "Castle1": #Castle for R1s
                 for pieces in self.pieces[colour]:
                    if pieces.type == "R" and pieces.num == 1:
                        self.board[coords[0]][0] = '   '
                        self.board[coords[0]][coords[1]+1] = pieces.desig
                        pieces.hasMoved = True
                        break
            if coords[2] == "Castle2": #Castle for R2s
                for pieces in self.pieces[colour]:
                    if pieces.type == "R" and pieces.num == 2:
                        self.board[coords[0]][7] = '   '
                        self.board[coords[0]][coords[1]-1] = pieces.desig
                        pieces.hasMoved = True   
                        break
        if piece.type == 'P': #Checks for pawn promotions
            player = None
            for x in self.players:
                if x.abr == piece.color:
                    player = x 
            piece.promotion(self, player) #Calls the pawn's promotion method


#Class for all the pieces on the board
class Piece():
    def __init__(self, color="w", num=0, eliminated=False, type = "type"):
        self.color = color
        self.eliminated = eliminated #Keeps track of if the piece is on the board/eliminated
        self.type = type 
        if color == 'b':
            self.opcolor = 'w' #opcolor means opponent's color
        else:
            self.opcolor= 'b'
        self.num = num #Differentiates it from pieces of same color and type
        self.desig = type + str(num) #Desig is short for designation. 
        self.hasMoved = False #Checks if a piece has moved yet. Is used for things like Castles and Pawn double move
        
    def checkPos(self,game): #Gets a piece's current coordinates.
        self.cor = [0,0]
        self.cor[0] = 100
        self.cor[1] = 100
        if self.eliminated == False:
            for y in range(8):
                if self.desig in game.board[y]:
                    self.cor[0] = y #Coordinate Y
                    for x in range(8):
                        if self.desig == game.board[y][x]:
                            self.cor[1] = x #Coordinated X
        return self.cor #Coordinates are not in [x, y], they're in [y, x] due to how the board is a nested list
    
    def movement(self):
        print("ERROR!") #Bug Testing
        
#Pawn Class, inherits from Piece
class pawn(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "P" #Overides self.type = "type"
        self.desig = self.color + self.type + str(self.num) #Overrides self.desig.
        self.enPassant_able = False
        
    def movement(self, game): #Probably the most different/unique movement Method from the rest of the other pieces, probably because it was the first one, and En Passant. Also, Override.
        validMoves = [] #Only piece that uses validMoves as a list name
        y = 0 #These variables are mostly so I don't get confused which coordinate I am changing since coords are usually (x, y) and not (y, x)
        x = 1
        c = 0 #The 'c' stands for 'color' since it changes values based on the color
        if self.color == 'w':
            c = -1
        else:
            c = 1
        cor = self.checkPos(game)
        yT = cor[y]-c #The possible Y coordinate it can move to. 
        xT = [cor[x]-1, cor[x]+1] #The possible X coordinates it can move to
        takes = [[yT,xT[0]], [yT,xT[1]]]
        if yT < 8 and y > -1:
            if game.board[yT][cor[x]] == '   ':
                validMoves.append([yT,cor[x]])
        if self.hasMoved != True and (yT-c < 8 and yT-c > -1): #Double space move on first move for pawns
            if game.board[yT-c][x] == '   ':
                validMoves.append([yT-c, cor[x]])
            self.hasMoved = True
            self.enPassant_able = True #Makes them able to be En Passant-ed
        for move in takes:
            if (move[x] > -1 and move[x] < 8):
                if self.opcolor in game.board[cor[y]][move[x]]:
                    for players in game.players:
                        if players.abr == self.opcolor:
                            for pieces in game.pieces[players.color]:
                                if pieces.type == "P":
                                    if pieces.enPassant_able == True:
                                        opcor = pieces.checkPos(game)
                                        validMoves.append([opcor[y]-c, opcor[x], "En Passant"]) #En Passant
                if (move[y] > -1 and move[y] < 8):
                    if self.opcolor in game.board[move[y]][move[x]]:
                        validMoves.append(move)
        return validMoves #returns all valid moves.
    
    def promotion(self, game, player): #Method for a pawn's promotions 
        possiblePieces = ['Q', 'B', 'R', 'N'] #Possible pieces the pawn can promote into
        cor = self.checkPos(game)
        num = 1
        if cor[0] == 0 or cor[0] == 7:
            while isinstance(player, HumanPlayer) == True:
                num = 1
                newPiece = str(input("Would you like to promote to a Queen(Q), Bishop(B), Rook(R), or Knight(N)?\nType the letter in the parentheses in the same case: ")) #Letters are the abbreviations/types assigned
                for pieces in player.pieces:
                    if pieces.type == newPiece: #Gets all the existing piece of the same type to properly number the new/replacement/promoted piece.
                        num = num + 1
                game.board[cor[0]][cor[1]] = self.color + newPiece + str(num)
                if newPiece in possiblePieces: #Appends piece to the list of pieces of the current player
                    if newPiece == 'Q':
                        player.pieces.append(queen(self.color, num))
                    if newPiece == 'B':
                        player.pieces.append(bishop(self.color, num))
                    if newPiece == 'R':
                        player.pieces.append(rook(self.color, num))
                    if newPiece == 'N':
                        player.pieces.append(knight(self.color, num))
                    break
                else:
                    print("Choose again.")
            if isinstance(player, AIPlayerRandom) == True: #Doesn't seem to work for the Random AI Player for some reason.
                newPiece = possiblePieces[random.randint(0,3)]
                for pieces in player.pieces:
                    if pieces.type == newPiece:
                        num = num + 1
                game.board[cor[0]][cor[1]] = self.color + newPiece + str(num)
                if newPiece == 'Q':
                    player.pieces.append(queen(self.color, num))
                if newPiece == 'B':
                    player.pieces.append(bishop(self.color, num))
                if newPiece == 'R':
                    player.pieces.append(rook(self.color, num))
                if newPiece == 'N':
                    player.pieces.append(knight(self.color, num))
            game.pieces[player.color] = player.pieces #Adds the new/promoted piece to the pieces dictionary
            game.setCoords() #Assigns coordinates
            game.checkElims() #Eliminates the pawn that was promoted

#King Class, inherits from Piece
class king(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "K"
        self.desig = self.color + self.type + str(self.num)
        
    def movement(self,game):
        availableMoves = []
        rooks = [] #Holds Rooks for Castling
        cor = self.checkPos(game)
        y = cor[0]
        x = cor[1]
        s=1 #The size of the radius for the King's movement
    
        for players in game.players:
            if players.abr == self.color:
                for pieces in players.pieces:
                    if pieces.type == 'R':
                        rooks.append(pieces)
        for num in range(2):
            if rooks[num].eliminated == False and self.hasMoved == False and rooks[num].hasMoved == False: #Castles
                if x-2 > 8: #Castle for R1s
                    if rooks[num].num == 1 and game.board[y][x-1] == '   ' and game.board[y][x-2] == '   ':
                        availableMoves.append([y, x-2, "Castle1"])
                if x+3 < 8: #Castle for R2s
                    if rooks[num].num == 2 and game.board[y][x+1] == '   ' and game.board[y][x+2] == '   ' and game.board[y][x+3] == '   ':
                        availableMoves.append([y, x+2, "Castle2"])
                self.hasMoved == False
        #Buch of 'if' statements to append all the possible moves. Mostly Copy and Pasted from the queen section, then removed the loops in favor of s=1
        if y+s < 8 and x+s < 8: 
            if self.color not in game.board[y+s][x+s]:
                availableMoves.append([y+s,x+s])
        if y-s > -1 and x-s > -1:
            if self.color not in game.board[y-s][x-s]:
                availableMoves.append([y-s,x-s])
        if x+s < 8 and y-s > -1:
            if self.color not in game.board[y-s][x+s]:
                availableMoves.append([y-s,x+s])
        if x-s > -1 and y+s < 8:
            if self.color not in game.board[y+s][x-s]:
                availableMoves.append([y+s,x-s])
        if y+s < 8:
            if self.color not in game.board[y+s][x]:
                availableMoves.append([y+s,x])
        if y-s > -1:
            if self.color not in game.board[y-s][x]:
                availableMoves.append([y-s,x])
        if x+s < 8:
            if self.color not in game.board[y][x+s]:
                availableMoves.append([y,x+s])       
        if x-s > -1:
            if self.color not in game.board[y][x-s]:
                availableMoves.append([y,x-s])
        return availableMoves #returns all available moves

#Queen Class, inherits from Piece
class queen(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "Q"
        self.desig = self.color + self.type + str(self.num)
    def movement(self,game):
        availableMoves = []
        cor = self.checkPos(game)
        y = cor[0]
        x = cor[1]
        #Bunch of for loops with 'if' statements to get all available moves. 4 of the 'for loops' are copy and pasted from bishop, and 4 copy and pasted from rook.
        for s in range(1,7): #Bishop
            if y+s < 8 and x+s < 8:
                if self.color in game.board[y+s][x+s]:
                    break
                if self.opcolor in game.board[y+s][x+s]:
                    availableMoves.append([y+s,x+s])
                    break
                if game.board[y+s][x+s] == '   ':
                    availableMoves.append([y+s,x+s])
        for s in range(1,7): #Bishop
            if y-s > -1 and x-s > -1:
                if self.color in game.board[y-s][x-s]:
                    break
                if self.opcolor in game.board[y-s][x-s]:
                    availableMoves.append([y-s,x-s])
                    break
                if game.board[y-s][x-s] == '   ':
                    availableMoves.append([y-s,x-s])
        for s in range(1,7): #Bishop
            if x+s < 8 and y-s > -1:
                if self.color in game.board[y-s][x+s]:
                    break
                if self.opcolor in game.board[y-s][x+s]:
                    availableMoves.append([y-s,x+s])
                    break
                if game.board[y-s][x+s] == '   ':
                    availableMoves.append([y-s,x+s])
        for s in range(1,7): #Bishop
            if x-s > -1 and y+s < 8:
                if self.color in game.board[y+s][x-s]:
                    break
                if self.opcolor in game.board[y+s][x-s]:
                    availableMoves.append([y+s,x-s])
                    break
                if game.board[y+s][x-s] == '   ':
                    availableMoves.append([y+s,x-s])
        for s in range(1,7): #Rook
            if y+s < 8:
                if self.color in game.board[y+s][x]:
                    break
                if self.opcolor in game.board[y+s][x]:
                    availableMoves.append([y+s,x])
                    break
                if game.board[y+s][x] == '   ':
                    availableMoves.append([y+s,x])
        for s in range(1,7): #Rook
            if y-s > -1:
                if self.color in game.board[y-s][x]:
                    break
                if self.opcolor in game.board[y-s][x]:
                    availableMoves.append([y-s,x])
                    break
                if game.board[y-s][x] == '   ':
                    availableMoves.append([y-s,x])
        for s in range(1,7): #Rookk
            if x+s < 8:
                if self.color in game.board[y][x+s]:
                    break
                if self.opcolor in game.board[y][x+s]:
                    availableMoves.append([y,x+s])
                    break
                if game.board[y][x+s] == '   ':
                    availableMoves.append([y,x+s])
        for s in range(1,7):#Rook
            if x-s > -1:
                if self.color in game.board[y][x-s]:
                    break
                if self.opcolor in game.board[y][x-s]:
                    availableMoves.append([y,x-s])
                    break
                if game.board[y][x-s] == '   ':
                    
                    availableMoves.append([y,x-s])
        return availableMoves #Returns all available moves

#Bishop Class, inherits from Piece
class bishop(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "B"
        self.desig = self.color + self.type + str(self.num)
    def movement(self,game):
        availableMoves = []
        cor = self.checkPos(game)
        y = cor[0]
        x = cor[1]
        #4 'for' loops checking ±y and ±x for available diagonal moves.
        for s in range(1,7):
            if y+s < 8 and x+s < 8: #Down and Right relative to the shown board
                if self.color in game.board[y+s][x+s]:
                    break
                if self.opcolor in game.board[y+s][x+s]:
                    availableMoves.append([y+s,x+s])
                    break
                if game.board[y+s][x+s] == '   ':
                    availableMoves.append([y+s,x+s])
        for s in range(1,7): 
            if y-s > -1 and x-s > -1: #Up and Left
                if self.color in game.board[y-s][x-s]:
                    break
                if self.opcolor in game.board[y-s][x-s]:
                    availableMoves.append([y-s,x-s])
                    break
                if game.board[y-s][x-s] == '   ':
                    availableMoves.append([y-s,x-s])
        for s in range(1,7):
            if x+s < 8 and y-s > -1: #Right and Up
                if self.color in game.board[y-s][x+s]:
                    break
                if self.opcolor in game.board[y-s][x+s]:
                    availableMoves.append([y-s,x+s])
                    break
                if game.board[y-s][x+s] == '   ':
                    availableMoves.append([y-s,x+s])
        for s in range(1,7):
            if x-s > -1 and y+s < 8: #Left and Down
                if self.color in game.board[y+s][x-s]:
                    break
                if self.opcolor in game.board[y+s][x-s]:
                    availableMoves.append([y+s,x-s])
                    break
                if game.board[y+s][x-s] == '   ':
                    availableMoves.append([y+s,x-s])
        return availableMoves #returns available moves

#Rook Class, inherits from Piece
class rook(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "R"
        self.desig = self.color + self.type + str(self.num)
    def movement(self,game):
        availableMoves = []
        cor = self.checkPos(game)
        y = cor[0]
        x = cor[1]
        #4 'for' loops checking ±x or ±y for the horizontal and vertical available moves
        for s in range(1,7):
            if y+s < 8: #Down compared to shown board
                if self.color in game.board[y+s][x]:
                    break
                if self.opcolor in game.board[y+s][x]:
                    availableMoves.append([y+s,x])
                    break
                if game.board[y+s][x] == '   ':
                    availableMoves.append([y+s,x])
        for s in range(1,7):
            if y-s > -1: #Up
                if self.color in game.board[y-s][x]:
                    break
                if self.opcolor in game.board[y-s][x]:
                    availableMoves.append([y-s,x])
                    break
                if game.board[y-s][x] == '   ':
                    availableMoves.append([y-s,x])
        for s in range(1,7):
            if x+s < 8: #Right
                if self.color in game.board[y][x+s]:
                    break
                if self.opcolor in game.board[y][x+s]:
                    availableMoves.append([y,x+s])
                    break
                if game.board[y][x+s] == '   ':
                    availableMoves.append([y,x+s])
        for s in range(1,7):
            if x-s > -1: #Left
                if self.color in game.board[y][x-s]:
                    break
                if self.opcolor in game.board[y][x-s]:
                    availableMoves.append([y,x-s])
                    break
                if game.board[y][x-s] == '   ':
                    availableMoves.append([y,x-s])
        return availableMoves #Returns available moves

#Knight Class, inherits from Piece
class knight(Piece):
    def __init__(self, color="White", num=0, eliminated=False, type="type"):
        super().__init__(color, num, eliminated, type)
        self.type = "N"
        self.desig = self.color + self.type + str(self.num)
        
    def movement(self,game): #Probably the easiest movement to make due to the ability to 'jump' over pieces
        availableMoves = []
        coords = self.checkPos(game)
        y = coords[0]
        x = coords[1]
        for p in [1,2]: #Loop that makes p and i 
            if p == 2:
                i = 1
            if p == 1:
                i = 2
            if (y + p < 8) and (x + i < 8): #Down 1/2 and Right 2/1
                if self.color not in game.board[y+p][x+i]:
                    availableMoves.append([y+p,x+i])
            if (y - p > -1) and (x - i > -1): #Up 1/2 and Left 2/1
                if self.color not in game.board[y-p][x-i]:
                    availableMoves.append([y-p,x-i])
            if (y + p < 8) and (x - i > -1): #Down 1/2 and Left 2/1
                if self.color not in game.board[y+p][x-i]:
                    availableMoves.append([y+p,x-i])
            if (y - p > -1) and (x + i < 8): #UP 1/2 and Right 2/1
                if self.color not in game.board[y-p][x+i]:
                    availableMoves.append([y-p,x+i])     
        return availableMoves    #Returns available moves
        
if __name__ == "__main__": #Main Function
    
    SHOW_BOARD = True #Toggle for if you want the board shown
    SHOW_WINNER = True #Toggle for if you want the winner shown. 
    
    #playerW = HumanPlayer("White")
    playerW = AIPlayerRandom("White")
    
    playerB = HumanPlayer("Black")
    #playerB = AIPlayerRandom("Black")
    
    game = Chess(playerW,playerB)

    bk = 0 #Black Wins
    wt = 0 #White Wins
    
    x = int(input("\nHow many games do you want to play? "))
    for x in range(x):
        w = game.play()
        if w == "w":
            wt += 1
        if w == "b":
            bk += 1
            
    print("Black:", bk, "| White:", wt)
    #game.allPieceCoords()
    game.showBoard(True)
