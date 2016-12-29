from Piece import piece
class rook(piece):
	#hasMoved exists for castling purposes, castling can only occur if the king and rooks haven't been moved
	hasMoved=False
	def __init__(self, clr):
	#constructor that allows for name distinction
		piece.__init__(self, clr, [[0,1],[1,0],[-1,0],[0,-1]], True)