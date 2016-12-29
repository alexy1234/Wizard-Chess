from Piece import piece
class queen(piece):
	def __init__(self, clr):
	#constructor that allows for name distinction
		piece.__init__(self, clr, [[1,0],[0,1],[1,1],[-1,0],[0,-1],[-1,-1],[-1,1],[1,-1]], True)