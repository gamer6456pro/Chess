First large project. Hopefully helps other beginners includes a doc explaining. 
# Table of Contents
[Game Class](#Game_Class)\
&nbsp;&nbsp;&nbsp;&nbsp;[Draw Board](#Draw_Board)\
&nbsp;&nbsp;&nbsp;&nbsp;[Draw Piece](#Draw_Piece)\
&nbsp;&nbsp;&nbsp;&nbsp;[Domove](#Domove)\
&nbsp;&nbsp;&nbsp;&nbsp;[Promotion](#Promotion)\
&nbsp;&nbsp;&nbsp;&nbsp;[Checkmate](#Checkmate)\
&nbsp;&nbsp;&nbsp;&nbsp;[Stalemate](#Stalemate)\
&nbsp;&nbsp;&nbsp;&nbsp;[Insufficient Material](#Insufficient_Material)\
&nbsp;&nbsp;&nbsp;&nbsp;[EndOfGame](#EndOfGame)\
&nbsp;&nbsp;&nbsp;&nbsp;[Resign](#Resign)\
[Piece Class](#Piece_Class)\
&nbsp;&nbsp;&nbsp;&nbsp;[pawn](#pawn)\
&nbsp;&nbsp;&nbsp;&nbsp;[rook](#rook)\
&nbsp;&nbsp;&nbsp;&nbsp;[bishop](#bishop)\
&nbsp;&nbsp;&nbsp;&nbsp;[knight](#night)\
&nbsp;&nbsp;&nbsp;&nbsp;[queen](#queen)\
&nbsp;&nbsp;&nbsp;&nbsp;[king](#king)\
&nbsp;&nbsp;&nbsp;&nbsp;[check](#check)\
&nbsp;&nbsp;&nbsp;&nbsp;[castle](#castle)\
[Misc Funcs](#Misc_Funcs)\
&nbsp;&nbsp;&nbsp;&nbsp;[Setup Board](#Setup_Board)\
&nbsp;&nbsp;&nbsp;&nbsp;[Load Image](#Load_Image)\
&nbsp;&nbsp;&nbsp;&nbsp;[Alternate Color](#Alternate_Color)\
&nbsp;&nbsp;&nbsp;&nbsp;[Create Object](#Create_Object)\
&nbsp;&nbsp;&nbsp;&nbsp;[Increment Move 50 rule](#IncrementMove50Rule)\
&nbsp;&nbsp;&nbsp;&nbsp;[Repetition](#Repetition)\
&nbsp;&nbsp;&nbsp;&nbsp;[EnemyGenerator](#EnemyGenerator)\
&nbsp;&nbsp;&nbsp;&nbsp;[EnemyMoves](#EnemyMoves)\
[Notes and tips](#Notes_and_tips)


# header
Notes:        #also could optimize this by clearing the dict when a piece is captured but too lazy so have to sacrifice cpu by adding this
        #but it saves memory
