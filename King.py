from Piece import piece
class king(piece):
	#hasMoved exists for castling purposes, castling can only occur if the king and rooks haven't been moved
	def __init__(self, clr):
	#constructor that allows for name distinction
		piece.__init__(self, clr, [[1,0],[0,1],[1,1],[-1,0],[0,-1],[-1,-1],[-1,1],[1,-1]], False)