# General Explination
The program uses the methods in the Piece class to generate moves and store them in PossibleMoves which is then fed into other funcs that then make the move/check legality.
To detect checkmate and other positions it loops through the whole board and checks for certain conditions. The board is represented by a 2d array that goes y,x
# Table of Contents
[Game Class](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#gameclass)\
&nbsp;&nbsp;&nbsp;&nbsp;[Draw Board](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#drawboard)\
&nbsp;&nbsp;&nbsp;&nbsp;[Draw Piece](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#drawpiece)\
&nbsp;&nbsp;&nbsp;&nbsp;[Domove](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#domove)\
&nbsp;&nbsp;&nbsp;&nbsp;[Promotion](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#promotion)\
&nbsp;&nbsp;&nbsp;&nbsp;[Checkmate](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#checkmate)\
&nbsp;&nbsp;&nbsp;&nbsp;[Stalemate](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#stalemate)\
&nbsp;&nbsp;&nbsp;&nbsp;[Insufficient Material](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#insufficientmaterial)\
&nbsp;&nbsp;&nbsp;&nbsp;[EndOfGame](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#endofgame)\
&nbsp;&nbsp;&nbsp;&nbsp;[Resign](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#resign)\
[Piece Class](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#piececlass)\
&nbsp;&nbsp;&nbsp;&nbsp;[pawn](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#pawn)\
&nbsp;&nbsp;&nbsp;&nbsp;[rook](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#rook)\
&nbsp;&nbsp;&nbsp;&nbsp;[bishop](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#bishop)\
&nbsp;&nbsp;&nbsp;&nbsp;[knight](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#knight)\
&nbsp;&nbsp;&nbsp;&nbsp;[queen](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#queen)\
&nbsp;&nbsp;&nbsp;&nbsp;[king](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#king)\
&nbsp;&nbsp;&nbsp;&nbsp;[check](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#check)\
&nbsp;&nbsp;&nbsp;&nbsp;[castle](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#castle)\
[Misc Funcs](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#miscfuncs)\
&nbsp;&nbsp;&nbsp;&nbsp;[Setup Board](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#setupboard)\
&nbsp;&nbsp;&nbsp;&nbsp;[Load Image](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#loadimage)\
&nbsp;&nbsp;&nbsp;&nbsp;[Alternate Color](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#alternatecolor)\
&nbsp;&nbsp;&nbsp;&nbsp;[Create Object](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#createobject)\
&nbsp;&nbsp;&nbsp;&nbsp;[Increment Move 50 rule](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#incrementmove50rule)\
&nbsp;&nbsp;&nbsp;&nbsp;[Repetition](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#repetition)\
&nbsp;&nbsp;&nbsp;&nbsp;[EnemyGenerator](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#enemygenerator)\
&nbsp;&nbsp;&nbsp;&nbsp;[EnemyMoves](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#enemymoves)\
[Notes and tips](https://github.com/gamer6456pro/Chess/blob/main/Doc.md#notesandtips)

# Game&nbsp;Class
Handles drawing, making the moves, and ending the game
## Draw&nbsp;Board
```python
counter=0
        for y in range(8):
            for x in range(8):
                if counter%2==y%2:
                    pygame.draw.rect(window,LightColor,(x*100,y*100,100,100))
                else:
                    pygame.draw.rect(window,DarkColor,(x*100,y*100,100,100))
                counter+=1
```
Uses some math to draw the squares to create an alternating pattern. Does not draw pieces
## Draw&nbsp;Piece
Loops through the Board blits the pieces out
```python 
ImageCenter=self.ImageDict[y].get_rect()
                    ImageCenter.center=(100*j+50,100*i+50)
                    window.blit(self.ImageDict[y],ImageCenter)
```
## Domove
```python
 PieceDict={'p':PieceObject.pawns(captureSameColor=True),'n':PieceObject.knights(captureSameColor=True),
        'q':PieceObject.queen(captureSameColor=True),'k':PieceObject.king(captureSameColor=True,castle=True),
        'r':PieceObject.rook(captureSameColor=True),'b':PieceObject.bishop(captureSameColor=True)}
```
This dict stores all the moves that the piece can make and selects one based on what type of piece the player clicks on
After this the func highlights the square that was clicked on and highlights all the squares based on the dict. Moves are represented by strings and a (y,x) coord system
so '04' would be the black king at the start of the game.
After it does that it detects the second click where it then runs the check func in the Piece class by feeding it a copy of the board and then checking if that pos leads to check
```python
CopyOfBoard=copy.deepcopy(Board)
                            CopyOfBoard[endy][endx]=CopyOfBoard[starty][startx]
                            CopyOfBoard[starty][startx]=' '
                            for i,x in enumerate(CopyOfBoard):
                                for j,y in enumerate(x):
                                    if y=='bk':
                                        BlackKingCoords=str(i)+str(j)
                                        break
                                    elif y=='wk':
                                        WhiteKingCoords=str(i)+str(j)
                            KingCoords={'b':BlackKingCoords,'w':WhiteKingCoords}
                            for Enemy in EnemyGenerator(CopyOfBoard):
                                if PieceObject.check(Enemy,CopyOfBoard,KingCoords):
                                    return 'check'
```
If the pos is not in check, then it checks if castle or enpassant occured. If so, it moves the rook for castle and removes the enemy pawn for enpassant
After that it sets the second click of the user equal to the beginning effectively moving the piece
## Promotion
This runs after the domove func and checks if a pawn is at their respective end. If so, it runs a loop to check for user input and then sets the coords to whatever the user promoted too
## Checkmate
Runs in the main game loop works similarly to the domove check part except this loops through all possible moves
```python
pieceDict={'n':ThePiece.knights(board=CopyOfBoard),'b':ThePiece.bishop(board=CopyOfBoard),
                        'q':ThePiece.queen(board=CopyOfBoard),'p':ThePiece.pawns(board=CopyOfBoard),
                        'r':ThePiece.rook(board=CopyOfBoard),'k':ThePiece.king(board=CopyOfBoard)}
                        for z in pieceDict[y[1]]:
                            CopyOfBoard[int(z[0])][int(z[1])]=y
                            CopyOfBoard[i][j]=' '
                            for i,x in enumerate(CopyOfBoard):
                                for j,y in enumerate(x):
                                    if y=='bk':
                                        BlackKingCoords=str(i)+str(j)
                                        break
                                    elif y=='wk':
                                        WhiteKingCoords=str(i)+str(j)
                            KingCoords={'b':BlackKingCoords,'w':WhiteKingCoords}
                            for Enemy in EnemyGenerator(CopyOfBoard):
                                if ThePiece.check(Enemy,CopyOfBoard,KingCoords):
                                    isCheckMate=True
                                CopyOfBoard[int(z[0])][int(z[1])]=' '
                                CopyOfBoard[i][j]=y
```
## Stalemate
Uses EnemyMoves and then compares all the generated moves and removes them if they are in the EnemyMoves. So if all the pieces have empty lists(moves) then it is stalemate
## Insufficient&nbsp;Material
Uses a dict to count how many bishops and knights are in the position and then uses some if statements to decide if there is insufficient material. If anything besides bishops and knights are found, it returns False
## EndOfGame
A func to print text and provide a restart and quit system. Is called after any game ender ex: checkmate,stalemate
## Resign
Allows the user to resign at any point in the game
# Piece&nbsp;Class
Handles move generation including castle and enpassant and contains the check func
## pawn
Generates the moves for the pawn and calls the enpassant func to add to possible moves
## rook
Generates moves for rook
## bishop
Generates moves for bishop
## knight
Generates moves for knight
## queen
Generates moves for queen
## king
Generates moves for king and calls castle to add to possible moves
## check
Takes a enemy Object, Board, and the king coords for both sides and then runs all the enemy possible moves and checks if the king coords are in those. If so, return True
## castle
Checks all the conditions for castle. If they are met, return True
# Misc&nbsp;Funcs
Some utilities/other game enders
## Setup&nbsp;Board
Sets up the board by setting down the pieces
## Load&nbsp;Image
Loads all the images needed. Did this to pack everything together
## Alternate&nbsp;Color
Returns the opposite color based on turn. Useful for finding enemies
## Create&nbsp;Object
Creates an object for domove
## IncrementMove50Rule
Uses map with a custom func to find if a pawn has moved based on the previous pos. 
```python
try:
            if OldBoard[1]=='p' and CurrentBoard==' ':
                return True
        except IndexError:
            return False
    for x,y in zip(previousBoard,Board):
        PawnMove=list(map(Match,x,y))
        if True in PawnMove:
            CounterMove50rule=0
            return False
```
Then checks if the same number of pieces are equal in both pos. If so, it adds one to the counter
## Repetition
Stores the previous pos in a dict and then adds one each time it appears. For the castle and enpassant it adds them as strings to end of the key
```python
Pos=''
    for x in Board:
        TempPos=''.join(x)
        Pos+=TempPos
    if EnpassantInPos:
        Pos+='EnPassant'
    for x in RookMoved:
        Pos+=str(x)
    try:
        RepetitionCounter[Pos]+=1
        if 3 in RepetitionCounter.values():
            return True
    except KeyError:
        RepetitionCounter[Pos]=1
    return None
```
## EnemyGenerator
A generator that yields enemy objects. Useful for the check func and checkmate
## EnemyMoves
Uses the EnemyGenerator to then generate their moves. Used in stalemate
# Notes&nbsp;and&nbsp;tips
In line 127: Theres prob a way to save memory by clearing the dict whenever a capture occurs
In line 457: There was a bug when starting a new game with the piece methods not updating the board=Board keyword arg, so if this occurs to you try to use .clear() instead of setting the variable back to an empty list


        the queen func didn't feed the args into the hcildrne
