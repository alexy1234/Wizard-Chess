'''Basic Chess Piece Class
	name: identifier of specific piece
	movement: array storing the minimum movement
	multiple: possibility for moving multiple patterns at once'''
class piece:
	movement=[]#FORMAT ROW,COLUMN
	multiple=False
	moved=False
	color=""
	def __init__(self, clr, movement1, multiple1):
		self.color=clr
		self.movement=movement1
		self.multiple=multiple1

