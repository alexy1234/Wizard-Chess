from Piece import piece
class knight(piece):
	def __init__(self, clr):
	#constructor that allows for name distinction
		piece.__init__(self, clr, [[2,1],[1,2],[-1,-2],[-1,2],[1,-2],[-2,1],[2,-1],[-2,-1]], False)



