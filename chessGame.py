from Knight import knight
from Pawn import pawn
from Piece import piece
from Bishop import bishop
from Queen import queen
from Rook import rook
from King import king

from speechRecognitionTest import chessMic
from arduinoInterfacing import arduinoCom

import json
#plays a virtual chess game between two players https://en.wikibooks.org/wiki/Chess/Sample_chess_game
class chessGame:

	lastMoveWhite=[None,None]#for en passant, stores location of last move only if last move was pawn moving two squares
	lastMoveBlack=[None,None]#^
	kingWhite=[0,4]#stores location of king, used for check
	kingBlack=[7,4]
	checkWhite=[False]#stores whether or not this color is in check
	checkBlack=[False]

	def createRow(self, boolean, num):
		arr=[]
		if num==1:	
		#num= means create row of high value pieces
			if boolean==True:
				#if boolean=true, color is white, create a row of white pieces
				arr=[rook("white"),knight("white"),bishop("white"),queen("white"),king("white"),bishop("white"),knight("white"),rook("white")]
			else:
				arr=[rook("black"),knight("black"),bishop("black"),queen("black"),king("black"),bishop("black"),knight("black"),rook("black")]
		else:
		#create a row of pawns
			if boolean==True:
				arr=[pawn("white"),pawn("white"),pawn("white"),pawn("white"),pawn("white"),pawn("white"),pawn("white"),pawn("white")]
			else:
				arr=[pawn("black"),pawn("black"),pawn("black"),pawn("black"),pawn("black"),pawn("black"),pawn("black"),pawn("black")]
		return arr

	def getRow(self, s):
		#get the array index of the row number
		referenceNumbers=['1','2','3','4','5','6','7','8']
		i=0
		for num in referenceNumbers:
			if num==s:
				return i
			else:
				i=i+1

	def numToLetter(self, num):
		#return the letter equivalent of number
		referenceAlphabet=["a","b","c","d","e","f","g","h"]
		return referenceAlphabet[int(num)]

	def getColumn(self, s):
		#get the array index of the column number
		i=0
		referenceAlphabet=["A","B","C","D","E","F","G","H"]
		for letter in referenceAlphabet:
			if letter==s or letter.lower()==s:
				return i
			else:
				i=i+1

	def switch(self, type, color):
		#creates object of specified type
		if type=="knight":
			return knight(color)
		if type=="queen":
			return queen(color)
		if type=="king":
			return king(color)
		if type=="pawn":
			return pawn(color)
		if type=="rook":
			return rook(color)
		if type=="bishop":
			return bishop(color)

	def formatMove(self, row, column, rowCheck, columnCheck):
		#properly formats move for addition to move list, piece moves from one index to next index
		return "["+str(row)+"]["+str(column)+"]=>["+str(rowCheck)+"]["+str(columnCheck)+"]"#[rowNumber][column]=>[newRowNumber][newColumn]

	def canKingsideCastle(self, board, clr):
		#checks to see if kingside castling is possible given the board state
		if clr=="white" and self.checkWhite[0]==True:#can't castle out of check
			return False
		if clr=="black" and self.checkBlack[0]==True:
			return False
		if clr=="white":
			if type(board[0][4]).__name__!="int" and type(board[0][7]).__name__!="int":
				if board[0][0].moved==False and board[0][4].moved==False and type(board[0][1]).__name__=="int" and type(board[0][2]).__name__=="int":
					#if the king and rook have not moved and there is nothing blocking the spaces in between
					return True
		elif clr=="black":
			if type(board[7][4]).__name__!="int" and type(board[7][7]).__name__!="int":
				if board[7][7].moved==False and board[7][4].moved==False and type(board[7][6]).__name__=="int" and type(board[7][5]).__name__=="int":
					#if the king and rook have not moved and there is nothing blocking the spaces in between
					return True
		return False

	def canQueensideCastle(self, board, clr):
		#checks to see if queenside castling is possible given the board state
		if clr=="white" and self.checkWhite[0]==True:#can't castle out of check
			return False
		if clr=="black" and self.checkBlack[0]==True:
			return False
		if clr=="white":
			if type(board[0][0]).__name__!="int" and type(board[0][4]).__name__!="int":
				if board[0][0].moved==False and board[0][4].moved==False and type(board[0][6]).__name__=="int" and type(board[0][5]).__name__=="int" and type(board[0][4]).__name__=="int":
					#if the king and rook have not moved and there is nothing blocking the spaces in between
					return True
		elif clr=="black":
			if type(board[7][0]).__name__!="int" and type(board[7][4]).__name__!="int":
				if board[7][0].moved==False and board[7][4].moved==False and type(board[7][1]).__name__=="int" and type(board[7][2]).__name__=="int" and type(board[7][3]).__name__=="int":
					#if the king and rook have not moved and there is nothing blocking the spaces in between
					return True
		return False

	def encodeBoard(self, board):
		#takes board and creates a string encoding of it
		rows=[None,None,None,None,None,None,None,None]
		i=0
		for row in board:
			rowStr=""
			for space in row:
				if space!=-1:
					color=space.color
					pieceType=type(space).__name__
					rowStr=rowStr+color+'/'+pieceType+'*'
				else:
					rowStr=rowStr+str(space)+'*'
			rows[i]=rowStr
			i=i+1
		return json.dumps(rows)

	def decodeBoard(self, boardStr):
		#takes json encoded array and creates two dimensional array boardstate
		rows=json.loads(boardStr)
		board=self.createBoard()
		i=0
		while i<len(board):
			cols=rows[i].split('*')
			j=0
			while j<len(board):
				name=cols[j]
				if name=="-1":
					board[i][j]=-1
				else:
					board[i][j]=self.switch(name.split('/')[1], name.split('/')[0])
				j=j+1
			i=i+1
		return board



	def castle(self, board, clr, castleType):
		#executes castling on board
		if castleType=="q":
			if clr=="black":
				rook=board[7][0]
				king=board[7][4]
				board[7][0]=-1
				board[7][4]=-1
				board[7][3]=rook
				board[7][2]=king
			elif clr=="white":
				rook=board[0][0]
				king=board[0][4]
				board[0][0]=-1
				board[0][4]=-1
				board[0][3]=rook
				board[0][2]=king
		elif castleType=="k":
			if clr=="black":
				rook=board[7][7]
				king=board[7][4]
				board[7][7]=-1
				board[7][4]=-1
				board[7][5]=rook
				board[7][6]=king
			elif clr=="white":
				rook=board[0][7]
				king=board[0][4]
				board[0][7]=-1
				board[0][4]=-1
				board[0][5]=rook
				board[0][6]=king

	def getLegalMoves(self, board, clr):
		#get list of all legal moves
		#******REMEMBER TO ACCOUNT FOR CHECK*******
		moveList=list()#list of legal moves
		rowNumber=0#keeps track of row number of piece we are examining
		for row in board:
			column=0#column number of piece we are examining, must reset after every finished iteration
			for space in row:
				#----IMPLEMENTATION FOR PAWN ATTACKING PATTERNS---------
				if type(space).__name__=="pawn" and space.color==clr:
					#check attacking patterns for pawns including en passant, while not discounting the possibility for other moves
					attackRow=0
					attackColumn=0
					if clr=="white":
						attackRow=rowNumber+1
						attackColumn=column+1
					else:
						attackRow= rowNumber-1
						attackColumn=column-1
					if attackRow>-1 and attackColumn>-1 and attackRow<8 and attackColumn<8:#check to make sure we do not go past highest index
						if type(board[attackRow][attackColumn]).__name__!='int' and board[attackRow][attackColumn].color!=clr:
							moveList.append([self.formatMove(rowNumber, column, attackRow, attackColumn),type(board[rowNumber][column]).__name__])
						if clr=="white":
							if attackRow-1<8 and attackRow-1>-1:
								if type(board[attackRow][attackColumn]).__name__=='int' and [attackRow-1,attackColumn]==self.lastMoveBlack:
									#if the space we are attacking is a blank space and en passant is a possibility
									moveList.append([self.formatMove(rowNumber, column, attackRow, attackColumn),type(board[rowNumber][column]).__name__])
						else:
							if attackRow+1<8 and attackRow+1>-1:
								if type(board[attackRow][attackColumn]).__name__=='int' and [attackRow+1,attackColumn]==self.lastMoveWhite:
									#if the space we are attacking is a blank space and en passant is a possibility
									moveList.append([self.formatMove(rowNumber, column, attackRow, attackColumn),type(board[rowNumber][column]).__name__])
					if clr=="white":
						attackColumn=column-1
					else:
						attackColumn=column+1
					if attackRow>-1 and attackColumn>-1 and attackRow<8 and attackColumn<8:
						if type(board[attackRow][attackColumn]).__name__!='int' and board[attackRow][attackColumn].color!=clr:
							moveList.append([self.formatMove(rowNumber, column, attackRow, attackColumn),type(board[rowNumber][column]).__name__])	
						if clr=="white":
							if attackRow-1<8 and attackRow-1>-1:
								if type(board[attackRow][attackColumn]).__name__=='int' and [attackRow-1,attackColumn]==self.lastMoveBlack:
									#if the space we are attacking is a blank space and en passant is a possibility
									moveList.append([self.formatMove(rowNumber, column, attackRow, attackColumn),type(board[rowNumber][column]).__name__])
						else:
							if attackRow+1<8 and attackRow+1>-1:
								if type(board[attackRow][attackColumn]).__name__=='int' and [attackRow+1,attackColumn]==self.lastMoveWhite:
									#if the space we are attacking is a blank space and en passant is a possibility
									moveList.append([self.formatMove(rowNumber, column, attackRow, attackColumn),type(board[rowNumber][column]).__name__])
				#-----END IMPLEMENTATION--------

				if type(space).__name__=="int" or space.color!=clr:#if blank space or opposite color, no move can be executed
					column=column+1
					continue
				else:#if not a blank space, possibility for moves
					movement=space.movement#get array of possible moves
					i=0
					for move in movement:#check each possible movement pattern for this piece
						rowCheck=0#just creating the variable
						columnCheck=0#^^
						if clr=="white":#if color is white, then you add the movement to the current row/column, because white moves from low to high on the board
						#ie 0-8, a-h as opposed to 8-0, h-a
							rowCheck=rowNumber+move[0]#row index of space to check for legal move
							columnCheck=column+move[1]#column index of space to check for legal move
						else:
							#color is black, so you subtract the movement because pieces move from the opposite end of the board forwards
							#ie 8-0, h-a
							rowCheck=rowNumber-move[0]#row index of space to check for legal move
							columnCheck=column-move[1]#column index of space to check for legal move
						j=0
						while (rowCheck<8) and (columnCheck<8) and (rowCheck>-1) and (columnCheck>-1):#make sure we have not left the board
							spaceCheck=board[rowCheck][columnCheck]#actual object we are checking
							#int that keeps track of number of times we have searched in this direction
							if type(spaceCheck).__name__=='int':#if type is int, we can automatically move there legally
								moveList.append([self.formatMove(rowNumber, column, rowCheck, columnCheck),type(board[rowNumber][column]).__name__])
							elif spaceCheck.color==clr or type(board[rowNumber][column]).__name__=="pawn":
								#if our piece is the same color, end dis loop bc we can go no further in this direction
								#this also applies to pawns bc if a pawn has any piece blocking it's straight path, then it cannot go further
								break
							else:
								#only other case is that the piece is of the other color and we are not a pawn, in which case we take it 
								moveList.append([self.formatMove(rowNumber, column, rowCheck, columnCheck),type(board[rowNumber][column]).__name__])
							if (board[rowNumber][column].multiple==True and type(spaceCheck).__name__=="int") or (type(board[rowNumber][column]).__name__=="pawn" and board[rowNumber][column].moved==False and j<2) :
								#make sure we can continue going in the same direction in one turn. IE queen, rook, bishop, but not knight, pawn, and king
								#if the pawn has not moved, we can possibly go further in this direction bc pawns can move two spaces ahead on their first move
								if clr=="white":#logic found above
									rowCheck=rowCheck+move[0]#row index of space to check for legal move
									columnCheck=columnCheck+move[1]#column index of space to check for legal move
								else:
									rowCheck=rowCheck-move[0]#row index of space to check for legal move
									columnCheck=columnCheck-move[1]#column index of space to check for legal move
							else:#piece cannot move multiple times in the same direction
								break
							j=j+1
						i=i+1
					column=column+1#we have found all we can in this row-column combination, move to the next one
			rowNumber=rowNumber+1#we have exhausted all row-column combinations in this row, move to the next row and thereby reset column to 0 (done at the top of the loop)	
		#----------check all spaces for two pieces of the same color and type attacking space, add modifier to each-----------
		IndexFirstMove=0#stores index in movelist of first move
		for singleMove in moveList:
			IndexSecondMove=0
			Index=[singleMove[0][9],singleMove[0][12]]#recieve the ending space of specified move
			while IndexSecondMove<len(moveList):#check these indices against all others to see if there is a match
				eachMove=moveList[IndexSecondMove]
				if eachMove==singleMove:#if they are the exact same move, go forward one
					IndexSecondMove=IndexSecondMove+1
					continue
				if eachMove[0][9]==Index[0] and eachMove[0][12]==Index[1] and eachMove[1]==singleMove[1]:#if the ending indices and types of the attacking pieces are the
				#same for both moves, then we have to add a special identifier
					startIndexFirstMove=[singleMove[0][1],singleMove[0][4]]#recieve starting index of first move
					startIndexSecondMove=[eachMove[0][1],eachMove[0][4]]#recieve starting index of second move
					if startIndexFirstMove[1]!=startIndexSecondMove[1]:
						#if the column number for the two is not the same, then add the letter denoting the column to each of the pieces
						moveList[IndexFirstMove][1]=moveList[IndexFirstMove][1]+self.numToLetter(startIndexFirstMove[1])#piece will be in format ex: "knightg" 
						moveList[IndexSecondMove][1]=moveList[IndexSecondMove][1]+self.numToLetter(startIndexSecondMove[1])
					else:#the two have the same column index, denote with number of row
						moveList[IndexFirstMove][1]=moveList[IndexFirstMove][1]+startIndexFirstMove[0]
						moveList[IndexSecondMove][1]=moveList[IndexSecondMove][1]+startIndexSecondMove[0]
				IndexSecondMove=IndexSecondMove+1
			IndexFirstMove=IndexFirstMove+1
		#-------------End Implementation---------------
		#-----------Check to see if castling is possible, add possible castling moves to movelist------------------
		#format: [castle, kingside/queenside]
		if self.canKingsideCastle(board, clr)==True:
			moveList.append(["castle","kingside"])
		if self.canQueensideCastle(board, clr)==True:
			moveList.append(["castle","queenside"])
		#----END IMPLEMENTATION----
		return moveList

	def getPieceType(self, piece):
		#takes individual letter marking a type of piece and returns the full name of the piece
		if piece=='B':
			return 'bishop'
		elif piece=='K':
			return 'king'
		elif piece=='Q':
			return 'queen'
		elif piece=='R':
			return 'rook'
		else:
			return 'knight'

	def switchOrder(self, move):
		#takes a row,column move and converts it to the properly lettered column,row equivalent
		row=int(move[1])+1#because array indexes start at 0, and chessboard index starts at 1, add 1 to row
		column=self.numToLetter(move[4])#recieves letter of column
		return "["+column+"]["+str(row)+"]"


	def parseInput(self, board, s, clr):
		#takes input and makes change to boardstate, move is user input, clr is color of mover
		#legalMoves=getLegalMoves(clr)
		startCoordinates=[-1,-1]
		endCoordinates=[-1,-1]
		move=s#stores move
		if len(s)==0:
			return False#size 0 input, get outta here
		success=False
		pieceType=''#stores type of piece we are moving
		length=len(move)#length of move string
		spec=''#specification for piece, if two pieces can go for the same space
		specType=""#stores type of specifier, letter or number
		dest=''#stores destination of move
		moveList=self.getLegalMoves(board, clr)
		if move[length-1]=='+' or move[length-1]=='#':
			#remove the check or checkmate operator from move, not a necessary part for parsing
			move=move[:-1]
			length=length-1#since we are removing the last character, the length of the string is cut down by 1
		if move[length-1]=='0':
			#castling
			if len(move)==5:
				#queenside
				for move in moveList:
					if move[0]=="castle" and move[1]=="queenside":
						castle(clr, "q")#executes actual castling on board
						return "0-0-0"
			else:
				#kingside
				for move in moveList:
					if move[0]=="castle" and move[1]=="kingside":
						castle(clr, "k")#executes actual castling on board
						return "0-0"
		elif ord(move[length-1])-ord('a')<0:#if the ascii value for this character subtracted from a, the lowest ascii valued letter, is less than 0, then this index is a number
			dest='['+move[length-2]+']['+move[length-1]+']'#stores destination of move
			if move[0].isupper()==False:#Capital letters mark pieces, while lowercase letters mark indices. If no piece type is given, it is automatically assumed to be a pawn.
				pieceType='pawn'
			else:# pieceType is equal to the first character bc if not a pawn, then the first character will mark the type of the piece that is moving
				pieceType=self.getPieceType(move[0])
			if 3<length and move[1]!='x':
				#if the length of the string is greater than three characters and the second character is not a X indicating the taking of a piece
				spec=move[1]#the move specifier is the second character, for example NA, or N2, depending on if indication is row or number
				pieceType=pieceType+spec#include the specifier at the end of the character
		for singleMove in moveList:
		#check to see if the ending destination of a legal move is the same as the specified move destination
			legalPieceType=singleMove[1]
			unformattedDestination=singleMove[0][8:]
			legalDestination=self.switchOrder(unformattedDestination)
			#print(legalDestination+" vs "+dest)
			if legalDestination==dest and legalPieceType==pieceType:#our move is legal
				endPoint=[int(unformattedDestination[1]),int(unformattedDestination[4])]
				startPoint=[int(singleMove[0][1]),int(singleMove[0][4])]
				startCooardinates=startPoint
				endCooardinates=endPoint
				thePiece=board[startPoint[0]][startPoint[1]]#our start piece
				wasMoved=thePiece.moved#stored for check later on, if the move was illegal and the piece hasn't been moved this needs to stay that way
				thePiece.moved=True
				temp=board[endPoint[0]][endPoint[1]]#store value of final spot bc if we are still in check, move is not legal, do not execute
				board[endPoint[0]][endPoint[1]]=thePiece#move the piece to the new location
				board[startPoint[0]][startPoint[1]]=-1#the place the piece used to be is now a blank space
				KW=self.kingWhite#stores original value of king's location just in case it needs to revert
				KB=self.kingBlack
				#-----IMPLENTATION FOR MOVING KING-----
				if type(thePiece).__name__=="king":
					if clr=="white":
						self.kingWhite[0]=endPoint[0]
						self.kingWhite[1]=endPoint[1]
					else:
						self.kingBlack[0]=endPoint[0]
						self.kingBlack[1]=endPoint[1]
				#-----END IMPLEMENTATION-------
				#-------------IMPLEMENTATION FOR CHECK------------
				if clr=="white" and self.checkWhite[0]==True:
					#if the color of the person currently moving is white and they are in check
					newList=self.getLegalMoves(board, "black")#get the list of moves for black after this move has been executed
					for move in newList:
						#check to see if king index appears anywhere
						unformattedSpecDest=move[0][8:]
						specDest=[int(unformattedSpecDest[1]),int(unformattedSpecDest[4])]
						if specDest==self.kingWhite:
							#the person moving is stil in check after the move has been executed, move is illegal, move everything back to its original place
							thePiece.moved=wasMoved
							board[startPoint[0]][startPoint[1]]=thePiece
							board[endPoint[0]][endPoint[1]]=temp
							if type(thePiece).__name__=="king":
								if clr=="white":
									self.kingWhite[0]=KW[0]
									self.kingWhite[1]=KW[1]
								else:
									self.kingBlack[0]=KB[0]
									self.kingBlack[1]=KB[1]
							return False#this move is not legal due to check
						self.checkWhite[0]=False
				elif clr=="black" and self.checkBlack[0]==True:
					#if the color of the person currently moving is white and they are in check
					newList=self.getLegalMoves(board, "white")#get the list of moves for black after this move has been executed
					for move in newList:
						#check to see if king index appears anywhere
						unformattedSpecDest=move[0][8:]
						specDest=[int(unformattedSpecDest[1]),int(unformattedSpecDest[4])]
						if specDest==self.kingBlack:
							#the person moving is stil in check after the move has been executed, move is illegal, move everything back to its original place
							thePiece.moved=wasMoved
							board[startPoint[0]][startPoint[1]]=thePiece
							board[endPoint[0]][endPoint[1]]=temp
							return False#this move is not legal due to check
					self.checkBlack[0]=False
				#-----END IMPLEMENTATION------
				if clr=="white" and self.lastMoveBlack!=[None,None]:
					if endPoint==[self.lastMoveBlack[0]+1,self.lastMoveBlack[1]] and pieceType=="pawn":
						#if endpoint row-1 is the location of the last black move, and the piece type is pawn, it is en passant
						board[self.lastMoveBlack[0]][self.lastMoveBlack[1]]=-1#set the previous square =0
				elif self.lastMoveWhite!=[None,None]:
					if endPoint==[self.lastMoveWhite[0]-1,self.lastMoveWhite[1]] and pieceType=="pawn":
						#if endpoint row-1 is the location of the last black move, and the piece type is pawn, it is en passant
						board[self.lastMoveWhite[0]][self.lastMoveWhite[1]]=-1#set the previous square =0
				success=True
				#---------IMPLEMENTATION FOR EN PASSANT-------
				if clr=="black":
					if pieceType=="pawn" and (startPoint[0]-endPoint[0])==2:#if the pawn moved two squares last turn as its first move
						self.lastMoveBlack[0]=endPoint[0]#stores row,column index of moved pawn
						self.lastMoveBlack[1]=endPoint[1]
					else:
						self.lastMoveBlack[0]=None
						self.lastMoveBlack[1]=None
				else:
					if pieceType=="pawn" and (endPoint[0]-startPoint[0])==2:#if the pawn moved two squares last turn as its first move
						self.lastMoveWhite[0]=endPoint[0]#stores row,column index of moved pawn
						self.lastMoveWhite[1]=endPoint[1]
					else:
						self.lastMoveWhite[0]=None
						self.lastMoveWhite[1]=None
				#-----END IMPLEMENTATION--------
				#-----IMPLENTATION TO CHECK FOR CHECK AT THE END OF TURN------
				specMoveList=self.getLegalMoves(board, clr)
				for move2 in specMoveList:
					if move2[0]!="castle":
						unformattedDestination2=move2[0][8:]
						endPoint2=[int(unformattedDestination2[1]),int(unformattedDestination2[4])]
						if clr=="white" and endPoint2==self.kingBlack:#if any of the moves next turn attack the king, then that king's color is in check
							self.checkBlack[0]=True
						if clr=="black" and endPoint2==self.kingWhite:#if any of the moves next turn attack the king, then that king's color is in check
							self.checkWhite[0]=True
				#-----END IMPLEMENTATION-----
				break
		if success==True:
			return ['('+str(startCoordinates[0])+','+str(startCoordinates[1])+')=>('+str(endCoordinates[0])+','+str(endCoordinates[1])+')',self.encodeBoard(board)]
		else:
			return False

	def createBoard(self):
		#initialize board, return board
		board=[self.createRow(True, 1),self.createRow(True, 2),[-1]*8,[-1]*8,[-1]*8,[-1]*8,self.createRow(False,2),self.createRow(False,1)]
		return board

	def play(self):
		#executes moves
		chessMic1=chessMic()#creates chessMic 
		board=self.createBoard()
		inpt=chessMic1.readAudio()
		i=1
		clr=""
		while inpt!='quit':
			if(type(inpt)!="str" and inpt[0]==False):
				print("The move you said doesn't make any sense.")
				print("Move: "+inpt[1])
				inpt=chessMic1.readAudio()
				continue
			print("statement: "+inpt)
			if i%2==1:
				clr="white"
			else:
				clr="black"
			success=self.parseInput(board, inpt, clr)
			if success==False:
				print("Illegal Move")
			else:
				arduino=arduinoCom()
				arduino.sendWord(json.dumps(success))
				board=self.decodeBoard(success[1])
				self.printBoard(board)
				if self.checkBlack[0]==True:
					print("Black is in check!")
				elif self.checkWhite[0]==True:
					print("White is in check!")
				i=i+1
			inpt=chessMic1.readAudio()

	def printBoard(self, board):
		#prints visual representation of board, accepts 2d array representing board
		print("move executed")
		print('')
		print('     a        b        c        d        e        f        g        h')
		j=1
		for row in board:
			r=str(j)#row represents
			for space in row:
				prevlen=len(r)
				if type(space).__name__!="int":
					r=r+'|'+type(space).__name__+":"+space.color[0]
				else:
					r=r+'|'
				while len(r)-prevlen<9:
					r=r+' '
			print(r+'|')
			print('  ------------------------------------------------------------------------')
			j=j+1


























