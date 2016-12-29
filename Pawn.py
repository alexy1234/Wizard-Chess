from Piece import piece
class pawn(piece):
	# pawns have special attacking patterns 
	attackPattern=[1,1]
	attackMultiple=False
	def __init__(self, clr):
	#constructor that allows for name distinction
		piece.__init__(self, clr, [[1,0]], False)