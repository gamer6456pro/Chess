The board is represented by a 2d array that goes y,x
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

## EndOfGame
## Resign
# Piece&nbsp;Class
## pawn
## rook
## bishop
## knight
## queen
## king
## check
## castle
# Misc&nbsp;Funcs
## Setup&nbsp;Board
## Load&nbsp;Image
## Alternate&nbsp;Color
## Create&nbsp;Object
## IncrementMove50Rule
## Repetition
## EnemyGenerator
## EnemyMoves
# Notes&nbsp;and&nbsp;tips
Notes:        #also could optimize this by clearing the dict when a piece is captured but too lazy so have to sacrifice cpu by adding this
        #but it saves memory
