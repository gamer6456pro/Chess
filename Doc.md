The board is represented by a 2d array that goes y,x
# Table of Contents
[Game Class](#Game&nbsp;Class)\
&nbsp;&nbsp;&nbsp;&nbsp;[Draw Board](#Draw&nbsp;Board)\
&nbsp;&nbsp;&nbsp;&nbsp;[Draw Piece](#Draw&nbsp;Piece)\
&nbsp;&nbsp;&nbsp;&nbsp;[Domove](#Domove)\
&nbsp;&nbsp;&nbsp;&nbsp;[Promotion](#Promotion)\
&nbsp;&nbsp;&nbsp;&nbsp;[Checkmate](#Checkmate)\
&nbsp;&nbsp;&nbsp;&nbsp;[Stalemate](#Stalemate)\
&nbsp;&nbsp;&nbsp;&nbsp;[Insufficient Material](#Insufficient&nbsp;Material)\
&nbsp;&nbsp;&nbsp;&nbsp;[EndOfGame](#EndOfGame)\
&nbsp;&nbsp;&nbsp;&nbsp;[Resign](#Resign)\
[Piece Class](#Piece&nbsp;Class)\
&nbsp;&nbsp;&nbsp;&nbsp;[pawn](#pawn)\
&nbsp;&nbsp;&nbsp;&nbsp;[rook](#rook)\
&nbsp;&nbsp;&nbsp;&nbsp;[bishop](#bishop)\
&nbsp;&nbsp;&nbsp;&nbsp;[knight](#knight)\
&nbsp;&nbsp;&nbsp;&nbsp;[queen](#queen)\
&nbsp;&nbsp;&nbsp;&nbsp;[king](#king)\
&nbsp;&nbsp;&nbsp;&nbsp;[check](#check)\
&nbsp;&nbsp;&nbsp;&nbsp;[castle](#castle)\
[Misc Funcs](#Misc&nbsp;Funcs)\
&nbsp;&nbsp;&nbsp;&nbsp;[Setup Board](#Setu&nbsp;Board)\
&nbsp;&nbsp;&nbsp;&nbsp;[Load Image](#Load&nbsp;Image)\
&nbsp;&nbsp;&nbsp;&nbsp;[Alternate Color](#Alternate&nbsp;Color)\
&nbsp;&nbsp;&nbsp;&nbsp;[Create Object](#Create&nbsp;Object)\
&nbsp;&nbsp;&nbsp;&nbsp;[Increment Move 50 rule](#IncrementMove50Rule)\
&nbsp;&nbsp;&nbsp;&nbsp;[Repetition](#Repetition)\
&nbsp;&nbsp;&nbsp;&nbsp;[EnemyGenerator](#EnemyGenerator)\
&nbsp;&nbsp;&nbsp;&nbsp;[EnemyMoves](#EnemyMoves)\
[Notes and tips](#Notes&nbsp;and&nbsp;tips)

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
## Promotion
## Checkmate
## Stalemate
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
