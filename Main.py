from typing import Counter
import pygame
import sys
import math
import copy
from pygame import cursors
from pygame.event import post
from pygame.locals import *
pygame.init()
pygame.font.init

font=pygame.font.Font('C:/Users/Austin/Programming/Pygame/Fonts/RetniSans-Medium.ttf',35)
PROMOTIONTXT=font.render('Press Q to promote to queen, N for knight etc...',False,(0,172,255))
INSUFFICIENTMATERIALTXT=font.render('Insufficient material: draw',False,(0,172,255))
CHECKMATETXT=font.render('Checkmate!',False,(0,172,255))
STALEMATETXT=font.render('Stalemate: draw',False,(0,172,255))
ENDTXT=font.render('Press r to restart or press q to quit',False,(0,172,255))
MOVE50RULETXT=font.render('50 move rule: draw',False,(0,172,255))
REPETITIONTXT=font.render('Repetition: draw',False,(0,172,255))
CHECKTXT=font.render('You are moving or are in check!',False,(0,172,255))
RESIGNTXT=font.render('Press r at any time in the game to resign!',False,(0,172,255))
RESIGNCONFIRMTXT=font.render('Press r to confirm, else press escape', False,(0,172,255))
WHITETURNTXT=font.render('It is white\'s turn',False,(0,172,255))
BLACKTURNTXT=font.render('It is Black\'s turn',False,(0,172,255))
TurnDict={'w':WHITETURNTXT,'b':BLACKTURNTXT}
CounterMove50rule=0
RepetitionCounter={}
DidMove=False
Turn='w'
Board=[]
RookMoved=[False,False,False,False] #lb,rb,lw,rw,
EnpassantInPos=False #used to detect enpassant for repetition


#Set up the Board goes (y,x)
for x in range(8):
    HorizontalBoard=[]
    Board.append(HorizontalBoard)
    for y in range(8):
        HorizontalBoard.append(' ')

def setUpBoard():
    global Board
    WhitePieceSetUp=['wr','wn','wb','wq','wk','wb','wn','wr']
    BlackPieceSetUp=['br','bn','bb','bq','bk','bb','bn','br']
    for x in range(0,8):
        Board[7][x]=WhitePieceSetUp[x]
        Board[0][x]=BlackPieceSetUp[x]
    for x in range(0,8):
        Board[6][x]='wp'
        Board[1][x]='bp'

def loadImage():
    bb=pygame.image.load('bb.png')
    bk=pygame.image.load('bk.png')
    bp=pygame.image.load('bp.png')
    bq=pygame.image.load('bq.png')
    br=pygame.image.load('br.png')
    bn=pygame.image.load('bn.png')
    wb=pygame.image.load('wb.png')
    wk=pygame.image.load('wk.png')
    wp=pygame.image.load('wp.png')
    wq=pygame.image.load('wq.png')
    wr=pygame.image.load('wr.png')
    wn=pygame.image.load('wn.png')
    ImageDict={'bb':bb,'bk':bk,'bp':bp,'bq':bq,'br':br,'bn':bn,'wb':wb,'wk':wk,'wp':wp,'wq':wq,'wr':wr,'wn':wn}
    return ImageDict
ImageDict=loadImage()

PossibleMoveColor=pygame.Color(0,255,180)
window=pygame.display.set_mode((800,800))
DarkColor=pygame.Color(125,144,179)
LightColor=pygame.Color(255,228,207)
HighlightColor=pygame.Color(0,255,0)
pygame.display.set_caption('Chess')

def AlternateColor():
    if Turn=='w':
        return 'b'
    elif Turn=='b':
        return 'w'

def CreateObject():
    x,y=pygame.mouse.get_pos()
    x=math.floor(x/100)
    y=math.floor(y/100)
    if y==8:
        y=7
    elif x==8:
        x=7
    PieceObject=Piece(Turn,(y,x))
    return PieceObject

def IncrementMove50Rule():
    global CounterMove50rule
    global previousBoard
    global Board
    PieceCounter=0
    CurrentPieceCounter=0
    if CounterMove50rule==50:
            return True
    def Match(OldBoard,CurrentBoard):
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
    for x in previousBoard:
        for y in x:
            if len(y)==2:
                PieceCounter+=1
    for x in Board:
        for y in x:
            if len(y)==2:
                CurrentPieceCounter+=1
    if PieceCounter!=CurrentPieceCounter:
        CounterMove50rule=0
        return False
    else:
        CounterMove50rule+=1

def repetition():
    global RepetitionCounter
    global previousBoard
    global Board
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

def EnemyGenerator(board):
        for i,x in enumerate(board):
            for j,y in enumerate(x):
                if y[0]==AlternateColor():
                    Type=y[1]
                    Object=Piece(AlternateColor(),(i,j))
                    Object.setType(Type)
                    yield Object
                else:
                    continue

def EnemyMoves():
    EnemyMoves=[]
    for EnemyObject in EnemyGenerator(Board):
        PieceDict={'p':EnemyObject.pawns(captureSameColor=True),'n':EnemyObject.knights(captureSameColor=True),
        'q':EnemyObject.queen(captureSameColor=True),'k':EnemyObject.king(captureSameColor=True),
        'r':EnemyObject.rook(captureSameColor=True),'b':EnemyObject.bishop(captureSameColor=True)}
        EnemyMoves.append(PieceDict[Board[EnemyObject.coords[0]][EnemyObject.coords[1]][1]])
    return EnemyMoves


#Class for handling drawing, moving, special moves, and turns
class Game():
    def __init__(self,ImageDict):
        self.ImageDict=ImageDict

    def DrawBoard(self):
        counter=0
        for y in range(8):
            for x in range(8):
                if counter%2==y%2:
                    pygame.draw.rect(window,LightColor,(x*100,y*100,100,100))
                else:
                    pygame.draw.rect(window,DarkColor,(x*100,y*100,100,100))
                counter+=1

    def DrawPiece(self):
        global window
        for i,x in enumerate(Board):
            for j,y in enumerate(x):
                try:
                    ImageCenter=self.ImageDict[y].get_rect()
                    ImageCenter.center=(100*j+50,100*i+50)
                    window.blit(self.ImageDict[y],ImageCenter)
                except:
                    pass

    def doMove(self,PieceObject):
        global previousBoard
        global Board
        global DidMove
        global CHECKTXT
        PieceDict={'p':PieceObject.pawns(captureSameColor=True),'n':PieceObject.knights(captureSameColor=True),
        'q':PieceObject.queen(captureSameColor=True),'k':PieceObject.king(captureSameColor=True,castle=True),
        'r':PieceObject.rook(captureSameColor=True),'b':PieceObject.bishop(captureSameColor=True)}
        self.DrawBoard()
        self.DrawPiece()
        while True:
            pygame.event.pump()
            try:
                startx,starty=pygame.mouse.get_pos()
                startx=math.floor(startx/100)
                starty=math.floor(starty/100)
                if Board[starty][startx][0]!=Turn:
                    return 'wrongturn'
                pygame.draw.rect(window,HighlightColor,(startx*100,starty*100,100,100))
                ValidMoves=PieceDict[Board[starty][startx][1]]
                ValidMoves[:]=[x for x in ValidMoves if ValidMoves[-1]=='EnPassant' or ValidMoves[-1]=='castle' or Board[int(x[0])][int(x[1])][0]!=Turn]
                try:
                    length=len(ValidMoves) if ValidMoves[-1]!='EnPassant' and ValidMoves[-1]!='castle' else len(ValidMoves)-1
                    for x,y in ValidMoves[:length]:
                        x,y=int(x),int(y)
                        pygame.draw.rect(window,PossibleMoveColor,(y*100,x*100,100,100))
                except Exception as e:
                    print(e)
                self.DrawPiece()
                pygame.display.update()
            except Exception as e:
                print(e)
                continue
            break

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.event.pump()
            keys=pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        endx,endy=pygame.mouse.get_pos()
                        endx=math.floor(endx/100)
                        endy=math.floor(endy/100)
                        Move=str(endy)+str(endx)
                        if Move in ValidMoves:
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
                            previousBoard=copy.deepcopy(Board)
                            MoveIndex=ValidMoves.index(Move)
                            #castle
                            try:
                                if ValidMoves[MoveIndex+1]=='castle':
                                    if Move=='72':
                                        Board[7][0]=' '
                                        Board[7][3]='wr'
                                    elif Move=='76':
                                        Board[7][7]=' '
                                        Board[7][5]='wr'
                                    if Move=='02':
                                        Board[0][0]=' '
                                        Board[0][3]='br'
                                    elif Move=='06':
                                        Board[0][7]=' '
                                        Board[0][5]='br'
                            except Exception as e:
                                # print(e)
                                pass
                            #enpassant
                            ColorDict={'b':-1,'w':1}
                            try:
                                if ValidMoves[MoveIndex+1]=='EnPassant':
                                    Board[int(Move[0])+ColorDict[Turn]][int(Move[1])]=' '
                            except Exception as e:
                                print(e)
                            Board[endy][endx]=Board[starty][startx]
                            Board[starty][startx]=' '
                            self.DrawBoard()
                            self.DrawPiece()
                            pygame.display.update()
                            DidMove=True
                            return

    def promotion(self):
        global Turn
        global Board
        for x in [0,7]:
            if x==0:
                PromotionColor='w'
            else:
                PromotionColor='b'
            for y in range(8):
                try:
                    if Board[x][y][1]=='p' and PromotionColor==Board[x][y][0]:
                        window.blit(PROMOTIONTXT,(40,35))
                        pygame.display.update()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                            keys=pygame.key.get_pressed()
                            if keys[pygame.K_q]:
                                Board[x][y]=Turn+'q'
                                return
                            elif keys[pygame.K_r]:
                                Board[x][y]=Turn+'r'
                                return
                            elif keys[pygame.K_b]:
                                Board[x][y]=Turn+'b'
                                return
                            elif keys[pygame.K_n]:
                                Board[x][y]=Turn+'n'
                                return
                except IndexError:
                    pass

    def stalemate(self):
        global Board
        global EnemyPossibleMoves
        isStalemate=True
        for i,x in enumerate(Board):
            for j,y in enumerate(x):
                if y[0]==Turn:
                    ThePiece=Piece(Turn,(i,j))
                    PieceDict={'p':ThePiece.pawns(),'n':ThePiece.knights(),'q':ThePiece.queen(),'k':ThePiece.king(),'r':ThePiece.rook(),
                    'b':ThePiece.bishop()}
                    if y[1]=='k':
                        KingMoves=PieceDict['k']
                        KingMoves=[x for x in KingMoves if x not in EnemyPossibleMoves[0]]
                    try:
                        if not KingMoves:
                            continue
                    except:
                        pass
                    if y[1]!='k' and not PieceDict[y[1]]:
                        continue
                    isStalemate=False
        return isStalemate

    def checkmate(self):
        global Board
        IsCheck=False
        isCheckMate=False
        CopyOfBoard=copy.deepcopy(Board)
        BoardCheck=Piece(Turn,(0,0)) #an object just to check if current pos is in check
        for i,x in enumerate(CopyOfBoard):
            for j,y in enumerate(x):
                if y=='bk':
                    BlackKingCoords=str(i)+str(j)
                    break
                elif y=='wk':
                    WhiteKingCoords=str(i)+str(j)
        KingCoords={'b':BlackKingCoords,'w':WhiteKingCoords}
        for enemy in EnemyGenerator(Board):
            if BoardCheck.check(enemy,Board,KingCoords):
                IsCheck=True
        if IsCheck:
            for i,x in enumerate(Board):
                for j,y in enumerate(x):
                    if y[0]==Turn:
                        ThePiece=Piece(Turn,(i,j))
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
            return isCheckMate

    def inSufficientMaterial(self):
        BlackSufficientDict={'bb':0,'bn':0}
        WhiteSufficientDict={'wb':0,'wn':0}
        for x in Board:
            for y in x:
                try:
                    if y[1]!='b' or y[1]!='n':
                        return False
                except:
                    pass
                if y in BlackSufficientDict:
                    BlackSufficientDict[y]+=1
                elif y in WhiteSufficientDict:
                    WhiteSufficientDict[y]+=1
        if (
            1 in BlackSufficientDict.values()
        and 0 in WhiteSufficientDict.values() and len(set(WhiteSufficientDict.values()))==1
        ):

            return True
        elif (
            1 in WhiteSufficientDict.values()
        and 0 in BlackSufficientDict.values() and len(set(BlackSufficientDict.values()))==1
        ):

            return True
        #problem is here
        elif WhiteSufficientDict['wn']==2 and 1 not in BlackSufficientDict.values():
            return True
        elif BlackSufficientDict['bn']==2 and 1 not in WhiteSufficientDict.values():
            return True
        else:
            return False

    def EndOfGame(self,TXT):
        global DidMove
        global ENDTXT
        global Turn
        global Board
        global RepetitionCounter
        global CounterMove50rule
        global RookMoved
        global EnpassantInPos
        TXTCENTER=TXT.get_rect(center=(400,20))
        ENDTXTCENTER=ENDTXT.get_rect(center=(400,50))
        window.blit(ENDTXT,(ENDTXTCENTER))
        window.blit(TXT,(TXTCENTER))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    keys=pygame.key.get_pressed()
                    if keys[pygame.K_r]:
                        CounterMove50rule=0
                        EnpassantInPos=False
                        RepetitionCounter={}
                        Board.clear()
                        RookMoved=[False,False,False,False]
                        for _ in range(8):
                            HorizontalBoard=[]
                            Board.append(HorizontalBoard)
                            for _ in range(8):
                                HorizontalBoard.append(' ')
                        setUpBoard()
                        DidMove=False
                        Turn='w'
                        pygame.display.update()
                        self.DrawBoard()
                        self.DrawPiece()
                        window.blit(RESIGNTXT,(90,20))
                        return
                    elif keys[pygame.K_q]:
                        pygame.quit()
                        exit()

    def resign(self):
        global Turn
        global font
        self.DrawBoard()
        self.DrawPiece()
        window.blit(RESIGNCONFIRMTXT,(90,20))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.DrawBoard()
                        self.DrawPiece()
                        pygame.display.update()
                        return True
                    elif event.key==pygame.K_ESCAPE:
                        self.DrawBoard()
                        self.DrawPiece()
                        pygame.display.update()
                        return False


#Class that handles piece movements, check, and generating special moves
class Piece():
    def __init__(self, color, coords):
        self.color=color
        self.coords=coords

    def pawns(self,board=Board,captureSameColor=False):
        PossibleMoves=[]
        if self.color=='w':
            if self.coords[0]-1>-1 and board[self.coords[0]-1][self.coords[1]]==' ':
                Move=str(self.coords[0]-1)+str(self.coords[1])
                if self.coords[0]==6 and self.coords[0]-2>-2 and board[self.coords[0]-2][self.coords[1]]==' ':
                    PossibleMoves.append(Move)
                    Move=str(self.coords[0]-2)+str(self.coords[1])
                    PossibleMoves.append(Move)
                else:
                    PossibleMoves.append(Move)

                if self.coords[0]==3:
                    Move=self.EnPassant()
                    if isinstance(Move,str):
                        PossibleMoves.append(Move)
                        PossibleMoves.append('EnPassant')

            #capture diagonally
            for i in[1,-1]:
                x=self.coords[1]
                x+=i
                try:
                    if -1<x<8 and self.coords[0]-1>-1 and board[self.coords[0]-1][x]!=' ':
                        Move=str(self.coords[0]-1)+str(x)
                        PossibleMoves.append(Move)
                except:
                    pass
            return PossibleMoves
        elif self.color=='b':
            if self.coords[0]+1<8 and board[self.coords[0]+1][self.coords[1]]==' ':
                Move=str(self.coords[0]+1)+str(self.coords[1])
                if self.coords[0]==1 and self.coords[0]+2<8 and board[self.coords[0]+2][self.coords[1]]==' ':
                    PossibleMoves.append(Move)
                    Move=str(self.coords[0]+2)+str(self.coords[1])
                    PossibleMoves.append(Move)
                else:
                    PossibleMoves.append(Move)

                if self.coords[0]==4:
                    Move=self.EnPassant()
                    if isinstance(Move,str):
                        PossibleMoves.append(Move)
                        PossibleMoves.append('EnPassant')

            #capture diagonally
            for i in[1,-1]:
                x=self.coords[1]
                x+=i
                try:
                    if -1<x<8 and self.coords[0]+1<8 and board[self.coords[0]+1][x]!=' ':
                        Move=str(self.coords[0]+1)+str(x)
                        PossibleMoves.append(Move)
                except:
                    pass
            return PossibleMoves

    def rook(self,board=Board,captureSameColor=False):
        PossibleMoves=[]
        for x in range(1+self.coords[1],8):
            Move=str(self.coords[0])+str(x)
            PossibleMoves.append(Move)
            if board[self.coords[0]][x]!=' ':
                break
        for x in reversed(range(self.coords[1])):
            Move=str(self.coords[0])+str(x)
            PossibleMoves.append(Move)
            if board[self.coords[0]][x]!=' ':
                break
        #y
        for y in range(1+self.coords[0],8):
            Move=str(y)+str(self.coords[1])
            PossibleMoves.append(Move)
            if board[y][self.coords[1]]!=' ':
                break
        for y in reversed(range(self.coords[0])):
            Move=str(y)+str(self.coords[1])
            PossibleMoves.append(Move)
            if board[y][self.coords[1]]!=' ':
                break
        if captureSameColor:
            PossibleMoves[:]=[x for x in PossibleMoves if board[int(x[0])][int(x[1])][0]!=self.color]
        return PossibleMoves

    def knights(self,board=Board,captureSameColor=False):
        PossibleMoves=[]
        for y in [self.coords[1]-1,self.coords[1]+1]:
            for x in [self.coords[0]+2,self.coords[0]-2]:
                if x>7 or y>7 or y<0 or x<0:
                    continue
                Move=str(x)+str(y)
                PossibleMoves.append(Move)
        for x in [self.coords[1]+2,self.coords[1]-2]:
            for y in [self.coords[0]-1,self.coords[0]+1]:
                if x>7 or y>7 or y<0 or x<0:
                    continue
                Move=str(y)+str(x)
                PossibleMoves.append(Move)
        if captureSameColor:
            PossibleMoves[:]=[x for x in PossibleMoves if board[int(x[0])][int(x[1])][0]!=self.color]
        return PossibleMoves

    def bishop(self,board=Board,captureSameColor=False):
        PossibleMoves=[]
        xcoord=''
        for x in [1,-1]:
            xcoord=self.coords[1]
            for y in range(self.coords[0]+1,8):
                xcoord+=x
                if xcoord<0 or xcoord>7:
                    continue
                Move=str(y)+str(xcoord)
                PossibleMoves.append(Move)
                if board[y][xcoord]!=' ':
                    break
        for x in [1,-1]:
            xcoord=self.coords[1]
            for y in range(self.coords[0]-1,-1,-1):
                xcoord+=x
                if xcoord<0 or xcoord>7:
                    continue
                Move=str(y)+str(xcoord)
                PossibleMoves.append(Move)
                if board[y][xcoord]!=' ':
                    break
        if captureSameColor:
            PossibleMoves[:]=[x for x in PossibleMoves if board[int(x[0])][int(x[1])][0]!=self.color]
        return PossibleMoves

    def queen(self,board=Board,captureSameColor=False):
        # PossibleMoves=self.rook()+self.bishop()
        # #couldn't find the bug with this line but ended up being the queen not feeding the args to the rook and bishop ^
        PossibleMoves=[]
        xcoord=''
        for x in [1,-1]:
            xcoord=self.coords[1]
            for y in range(self.coords[0]+1,8):
                xcoord+=x
                if xcoord<0 or xcoord>7:
                    continue
                Move=str(y)+str(xcoord)
                PossibleMoves.append(Move)
                if board[y][xcoord]!=' ':
                    break
        for x in [1,-1]:
            xcoord=self.coords[1]
            for y in range(self.coords[0]-1,-1,-1):
                xcoord+=x
                if xcoord<0 or xcoord>7:
                    continue
                Move=str(y)+str(xcoord)
                PossibleMoves.append(Move)
                if board[y][xcoord]!=' ':
                    break
        for x in range(1+self.coords[1],8):
            Move=str(self.coords[0])+str(x)
            PossibleMoves.append(Move)
            if board[self.coords[0]][x]!=' ':
                break
        for x in reversed(range(self.coords[1])):
            Move=str(self.coords[0])+str(x)
            PossibleMoves.append(Move)
            if board[self.coords[0]][x]!=' ':
                break
        #y
        for y in range(1+self.coords[0],8):
            Move=str(y)+str(self.coords[1])
            PossibleMoves.append(Move)
            if board[y][self.coords[1]]!=' ':
                break
        for y in reversed(range(self.coords[0])):
            Move=str(y)+str(self.coords[1])
            PossibleMoves.append(Move)
            if board[y][self.coords[1]]!=' ':
                break
        if captureSameColor:
            PossibleMoves[:]=[x for x in PossibleMoves if board[int(x[0])][int(x[1])][0]!=self.color]
        return PossibleMoves

    def knights(self,board=Board,captureSameColor=False):
        PossibleMoves=[]
        for y in [self.coords[1]-1,self.coords[1]+1]:
            for x in [self.coords[0]+2,self.coords[0]-2]:
                if x>7 or y>7 or y<0 or x<0:
                    continue
                Move=str(x)+str(y)
                PossibleMoves.append(Move)
        for x in [self.coords[1]+2,self.coords[1]-2]:
            for y in [self.coords[0]-1,self.coords[0]+1]:
                if x>7 or y>7 or y<0 or x<0:
                    continue
                Move=str(y)+str(x)
                PossibleMoves.append(Move)
        if captureSameColor:
            PossibleMoves[:]=[x for x in PossibleMoves if board[int(x[0])][int(x[1])][0]!=self.color]
        return PossibleMoves

    def king(self,board=Board,captureSameColor=False,castle=False):
        PossibleMoves=[]
        #diagonals
        for x in [1,-1]:
            for y in [1,-1]:
                xcoord=self.coords[1]+x
                ycoord=self.coords[0]+y
                if xcoord>7 or ycoord>7 or xcoord<0 or ycoord<0:
                    continue
                Move=str(ycoord)+str(xcoord)
                PossibleMoves.append(Move)
        #laterals
        for x in [1,-1]:
            xcoord=self.coords[1]+x
            if xcoord>7 or xcoord<0:
                continue
            Move=str(self.coords[0])+str(xcoord)
            PossibleMoves.append(Move)
        for y in [1,-1]:
            ycoord=self.coords[0]+y
            if ycoord>7 or ycoord<0:
                continue
            Move=str(ycoord)+str(self.coords[1])
            PossibleMoves.append(Move)
        if captureSameColor:
            PossibleMoves[:]=[x for x in PossibleMoves if board[int(x[0])][int(x[1])][0]!=self.color]
        #castle
        if castle:
            CastlePossible=self.castle()
            if isinstance(CastlePossible,list) and True in CastlePossible:
                indexes=[i for i,x in enumerate(CastlePossible) if x==True]
                for x in indexes:
                    if x==0:
                        Move=str(self.coords[0])+str(self.coords[1]-2)
                        PossibleMoves.append(Move)
                        PossibleMoves.append('castle')
                    if x==1:
                        Move=str(self.coords[0])+str(self.coords[1]+2)
                        PossibleMoves.append(Move)
                        PossibleMoves.append('castle')
        return PossibleMoves

    #dead func iirc
    def setType(self,type):
        self.type=type

    def check(self,enemy,Newboard,kingcoords):
        pieceDict={'n':enemy.knights(board=Newboard),'b':enemy.bishop(board=Newboard),
        'q':enemy.queen(board=Newboard),'p':enemy.pawns(board=Newboard),
        'r':enemy.rook(board=Newboard),'k':enemy.king(board=Newboard)}
        try:
            EnemyCoordy=enemy.coords[0]
            EnemyCoordx=enemy.coords[1]
            if kingcoords[Turn] in pieceDict[Newboard[EnemyCoordy][EnemyCoordx][1]]:
                return True
        except Exception as e:
            print(e)
        return False

    def castle(self):
        global RookMoved
        CastleIsLegal=[True,True,True,True] #lb,rb,lw,rw
        counter=0
        KingCoords={'w':'74','b':'04'}

        #checking if king or rookmoved and if current state is in check
        if all(RookMoved):
            return False
        for enemy in EnemyGenerator(Board):
            if self.check(enemy,Board,KingCoords):
                return False
        if Board[0][4]!='bk':
            RookMoved[:2]=[True,True]
        elif Board[7][4]!='wk':
            RookMoved[2:]=[True,True]
        for y,x in ['00','07','70','77']:
            y=int(y)
            x=int(x)
            if Board[y][x]!='br' and y==0:
                RookMoved[counter]=True
            elif Board[y][x]!='wr' and y==7:
                RookMoved[counter]=True
            counter+=1
        if all(RookMoved):
            return False

        CastleIsLegal=[not x for x in RookMoved]
        #check if the squares are empty too between rook and king
        for i,y in enumerate([0,7]): #long
            for x in [1,2,3]:
                if Board[y][x]!=' ':
                    if i==1:
                        CastleIsLegal[2]=False
                    else:
                        CastleIsLegal[0]=False
        for i,y in enumerate([0,7]): #short
            for x in [5,6]:
                if Board[y][x]!=' ':
                    if i==1:
                        CastleIsLegal[3]=False
                    else:
                        CastleIsLegal[1]=False

        #check if castling into check
        for i,x in enumerate(CastleIsLegal):
            if not x:
                continue
            if Turn=='w' and i<2:
                continue
            elif Turn=='b' and i>1:
                continue
            if i%2==0:
                ycoord='0' if i==0 else '7'
                for x in [2,3]:
                    KingCoords[Turn]=ycoord+str(x)
                    for enemy in EnemyGenerator(Board):
                        if self.check(enemy,Board,KingCoords):
                            CastleIsLegal[i]=False
            else:
                ycoord='0' if i==1 else '7'
                for x in [5,6]:
                    KingCoords[Turn]=ycoord+str(x)
                    for enemy in EnemyGenerator(Board):
                        if self.check(enemy,Board,KingCoords):
                            CastleIsLegal[i]=False
        if Turn=='b':
            return CastleIsLegal[:2]
        elif Turn=='w':
            return CastleIsLegal[2:]

    def EnPassant(self):
        global Turn
        global EnpassantInPos
        ColorDict={'b':1,'w':-1}
        for x in [-1,1]:
            if (-1<self.coords[0]+(2*ColorDict[Turn])<8 and -1<self.coords[1]+x<8 and previousBoard[self.coords[0]+(2*ColorDict[Turn])][self.coords[1]+x]==AlternateColor()+'p' and
            Board[self.coords[0]][self.coords[1]+x]==AlternateColor()+'p'):
                EnpassantInPos=True
                return str(self.coords[0]+ColorDict[Turn])+str(self.coords[1]+x)

setUpBoard()
game=Game(ImageDict)
clock=pygame.time.Clock()
game.DrawBoard()
game.DrawPiece()
window.blit(RESIGNTXT,(90,20))
while True:
    EnemyPossibleMoves=EnemyMoves()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if game.resign():
                    TurnColorDict={'w':'white','b':'black'}
                    RESIGNLOSSTXT=font.render(TurnColorDict[Turn]+' has resigned!',False,(0,172,255))
                    game.EndOfGame(RESIGNLOSSTXT)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                WRONGTURN=game.doMove(CreateObject())
                game.promotion()
                game.DrawBoard()
                game.DrawPiece()
                if WRONGTURN=='wrongturn':
                    rect=TurnDict[Turn].get_rect(center=(400,20))
                    window.blit(TurnDict[Turn],rect)
                elif WRONGTURN=='check':
                    rect=CHECKTXT.get_rect(center=(400,20))
                    window.blit(CHECKTXT,rect)
                pygame.display.update()
                if game.stalemate():
                    game.EndOfGame(STALEMATETXT)
                elif game.inSufficientMaterial():
                    game.EndOfGame(INSUFFICIENTMATERIALTXT)

    if game.checkmate():
        game.EndOfGame(CHECKMATETXT)

    if DidMove:

        if Turn=='w':
            Turn='b'
            DidMove=False
        elif Turn=='b':
            Turn='w'
            DidMove=False
        if repetition():
            game.EndOfGame(REPETITIONTXT)
        try:
            if IncrementMove50Rule():
                game.EndOfGame(MOVE50RULETXT)
        except Exception as e:
            print(e)
        EnpassantInPos=False
    clock.tick(30)
