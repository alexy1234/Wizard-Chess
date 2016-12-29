import speech_recognition as sr

# obtain audio from the microphone
class chessMic:
	#uses mic to read audio, then interprets it into valid chess moves
	def readAudio(self):
		#creates microphone and  		
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("Press the space bar to talk")
			st=input()
			if(st==' '):
				audio = r.listen(source)

				# recognize speech using Sphinx
				try:
					inpt=self.chessNotation(r.recognize_sphinx(audio))
					return inpt
				except sr.UnknownValueError:
					print("Sphinx could not understand audio")
				except sr.RequestError as e:
					print("Sphinx error; {0}".format(e))
			elif(st=="quit"):
				return st
	def chessNotation(self, s):
		#takes string and converts to algebraic chess notation
		#three cases: took (capture), castle(castle, look for king, queen, k or q), I have (things)
		#This function provides a switch to test for the various possible move types (castling, pawns, all other moves)
		inpt=self.trimString(s)#removes unnecessary words and replaces possible mis-recognition with the proper word
		if self.castleCheck(inpt)!=False:
			return self.castleCheck(inpt)
		
		if self.pawnCheck(inpt)!=False:
			return self.pawnCheck(inpt)#returns algebraic pawn move

		if self.generalCheck(inpt)!=False:#does input denote any other normal move
			return self.generalCheck(inpt)

		#if none of the previous functions returned something other than false, string is invalid. return False.
		return [False, s]

	def generalCheck(self, arr):
		#checks to see if move follows form (piece, row, column) ex: Na5
		#phrase follows form coded piece name, number, word starting with column letter. ex: Ninety one avocados=Na1
		#returns false if does not, returns correct algebraic word if not
		if arr.__len__()!=3:#length must equal 3
			return False
		finalStr=''#stores final algebraic move
		pieceArr=['ninety/N','twenty/B', 'fifty/R', 'seventy/Q', 'sixty/K']#stores translated words for each piece name, and algebraic notation for that piece
		piece=arr[0]#stores coded piece name. ex: ninety for Knight
		for codedPiece in pieceArr:
			name=codedPiece.split('/')[0]
			algName=codedPiece.split('/')[1]
			if name==piece:
				#if we have found a correct translation for our piece name, add algebraic name to final string
				finalStr=algName
		if finalStr=='':#if no correct translation was found
			return False
		columnArr=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']#valid letters for column
		for column in columnArr:
			ltr=arr[2][0]
			if ltr==column:
				finalStr=finalStr+ltr
		if finalStr.__len__()==1:#if nothing was added to string, no valid column was found
			return False
		rowArr=['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']#stores string representation of row numbers
		i=0
		while i<8:
			rowNumber=arr[1]#stores number, second word
			if rowNumber==rowArr[i]:
				row=i+1#i lags one behind actual representative number
				finalStr=finalStr+str(row)
			i=i+1
		if finalStr.__len__()!=3:
			#if the final length is not three letters, then something went wrong. return false
			return False
		#if we have gotten to this point, we should have a valid algebraic move.
		return finalStr

	def castleCheck(self, arr):
		#recieves array, checks for queenside and kingside castling
		king=False#check for king or queen
		queen=False
		castle=False
		for word in arr:
			if word=="king":
				king=True
			elif word=="queen":
				queen=True
			elif word=="castle":
				castle=True
		if king==True and castle==True:
			return "0-0"
		elif queen==True and castle==True:
			return "0-0-0"
		else:
			return False

	def letterCheck(self, s):
		#takes letter and checks to see if it represents a valid chess piece
		arr=['k','q','r','n','s','i']
		for ltr in arr:
			if ltr==s:
				return True
		return False

	def trimString(self, s):
		#removes starting words and replaces common misrecognitions with the correct word. ie the raid=three
		replaceList=['won/one', 'an/one', 'of the kind of/avocado', 'to/two', 'sex/six', 'for/four', 'set/seven', 'the rear/three', 'said in/seven', 'council/castle']#commonly misrecognized words/correct word
		for word in replaceList:
			replaced=word.split('/')[0]
			replacer=word.split('/')[1]
			s=s.replace(replaced, replacer)
		s=s.replace('and ', '')
		s=s.replace('yes ', '')
		s=s.replace('the ', '')
		s=s.replace('there ', '')
		s=s.replace('what ', '')
		s=s.replace('but ')
		print(s)
		return s.split()

	def pawnCheck(self, arr):
		#checks to see if statement represents pawn movement. If so, returns algebraic chess move, if no return false
		#correct format: ex. one avocado (number, word starting with column)
		if arr.__len__()!=2:
			return False
		numberArr=['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
		i=0
		row=-1
		while(i-1<8):
			if numberArr[i-1]==arr[0]:
				row=i
				break
			i=i+1
		if row==-1:
			return False
		col=arr[1][0]#first letter of second word indicates column
		return col+str(i)#column, row algebraic move returned

	