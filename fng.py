"""
FOX AND GEESE 

INFANTE - GATDULA 

ARTIFICIAL INTELLIGENCE - CASE STUDY 

simple fox and geese game
Objective of the geese: Trap the fox
Objective of the fox: eat the geese until the geese cannot trap the fox or reach the parallel end.

RULES: 
- YELLOW Pieces are geese
- RED Pieces is/are the fox/es
- Fox/es can eat the geese 
- Fox/es can "double" eat

"""

import pygame, sys, random
from pygame.locals import *

pygame.font.init()

##COLORS##
#             R    G    B 
WHITE    = (255, 255, 255)
RED     = (  0,   0, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)
GOLD     = (255, 215,   0)
HIGH     = (160, 190, 255)
YELLOW   = (255, 255,   0)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"
NORTH 	  = "north"
SOUTH 	  = "south"
EAST	  = "east"
WEST      = "west"



class Game:
	#Main game

	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()
		
		self.turn = RED
		self.selected_piece = None # a board location. 
		self.hop = False
		self.selected_legal_moves = []

	def setup(self):
		#Show board
		self.graphics.setup_window()

	def event_loop(self):
		#move pieces
		self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos()) # mouse position
		if self.selected_piece != None:
			self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)

		for event in pygame.event.get():

			if event.type == QUIT:
				self.terminate_game()

			if event.type == MOUSEBUTTONDOWN:
				if self.hop == False:
					if self.board.location(self.mouse_pos).occupant != None and self.board.location(self.mouse_pos).occupant.color == self.turn:
						self.selected_piece = self.mouse_pos

					elif self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece):

						self.board.move_piece(self.selected_piece, self.mouse_pos)
					
						if self.mouse_pos not in self.board.adjacent(self.selected_piece):
							self.board.remove_piece((self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2))
						
							self.hop = True
							self.selected_piece = self.mouse_pos

						else:
							self.end_turn()

				if self.hop == True:					
					if self.selected_piece != None and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
						self.board.move_piece(self.selected_piece, self.mouse_pos)
						self.board.remove_piece((self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) / 2, self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) / 2))

					if self.board.legal_moves(self.mouse_pos, self.hop) == []:
							self.end_turn()

					else:
						self.selected_piece = self.mouse_pos


	def update(self):
		#Update display
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

	def terminate_game(self):
		#if winner = true : end game
		pygame.quit()
		sys.exit

	def main(self):
		#"MAIN" 
		self.setup()

		while True: # main game loop
			self.event_loop()
			self.update()

	def end_turn(self):
		#switch turns. Switches the current player. 
		#end_turn() also checks for and game and resets 
		
		if self.turn == RED:
			self.turn = YELLOW
		else:
			self.turn = RED

		self.selected_piece = None
		self.selected_legal_moves = []
		self.hop = False

		if self.check_for_endgame():
			if self.turn == RED:
				self.graphics.draw_message("GEESE WINS!")
			else:
				self.graphics.draw_message("FOX WINS!")

	def check_for_endgame(self):
		#Check if the player runout of moves
		# to see if a player has run out of moves or pieces. If so, then return True. Else return False.
	
		for x in xrange(8):
			for y in xrange(8):
				if self.board.location((x,y)).color == BLACK and self.board.location((x,y)).occupant != None and self.board.location((x,y)).occupant.color == self.turn:
					if self.board.legal_moves((x,y)) != []:
						return False

		return True

class Graphics:
	def __init__(self):
		self.caption = "Fox And Geese"

		self.fps = 60
		self.clock = pygame.time.Clock()

		self.window_size = 600
		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.background = pygame.image.load('board.png')

		self.square_size = self.window_size / 8
		self.piece_size = self.square_size / 2

		self.message = False

	def setup_window(self):
		#Just caption and window
		pygame.init()
		pygame.display.set_caption(self.caption)

	def update_display(self, board, legal_moves, selected_piece):
		#Update display
		self.screen.blit(self.background, (0,0))
		
		self.highlight_squares(legal_moves, selected_piece)
		self.draw_board_pieces(board)

		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		pygame.display.update()
		self.clock.tick(self.fps)

	def draw_board_squares(self, board):
		#draw squares
		for x in xrange(8):
			for y in xrange(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )
	
	def draw_board_pieces(self, board):
		#draw pieces
		for x in xrange(8):
			for y in xrange(8):
				if board.matrix[x][y].occupant != None:
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, self.pixel_coords((x,y)), self.piece_size) 

					if board.location((x,y)).occupant.fox == True:
						pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x,y)), int (self.piece_size / 1.7), self.piece_size / 4)


	def pixel_coords(self, board_coords):
		#Takes in a tuple of board coordinates (x,y) and returns the pixel coordinates of the center of the square at that location.
		
		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

	def board_coords(self, (pixel_x, pixel_y)):
		#Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
		
		return (pixel_x / self.square_size, pixel_y / self.square_size)	

	def highlight_squares(self, squares, origin):
		"""
		Squares is a list of board coordinates. 
		highlight_squares highlights them.
		"""
		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))	

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

	def draw_message(self, message):
		"""
		Draws message to the screen. 
		"""
		self.message = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size / 2, self.window_size / 2)

class Board:
	def __init__(self):
		self.matrix = self.new_board()

	def new_board(self):
		#Create a new board

		# initialize squares and place them in matrix

		matrix = [[None] * 8 for i in xrange(8)]

		for x in xrange(8):
			for y in xrange(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0): 
					matrix[y][x] = Square(BLACK)

		# initialize the pieces and put them in the appropriate squares

		for x in xrange(8):
			for y in xrange(2):
				if matrix[x][y].color == BLACK:
					matrix[x][y].occupant = Piece(YELLOW,)
			# for y in xrange(7, 8):
			# 	if matrix[x][y].color == BLACK:
			# 		posx= random.randint(4,7)
			# 		posy= random.randint(4,7)
			# 		matrix[posx][posy].occupant = Piece(RED, True)
		for x in xrange(8):
			for y in xrange(7,8):
				if matrix[x][y].color == BLACK:
					posx = random.randrange(0,8,2)
					posy = random.randrange(4,8,2)
					print posx ,posy
					matrix[posx][posy].occupant = Piece(RED, True)
		return matrix

	def board_string(self, board):
		"""
		Takes a board and returns a matrix of the board space colors. Used for testing new_board()
		"""

		board_string = [[None] * 8] * 8 

		for x in xrange(8):
			for y in xrange(8):
				if board[x][y].color == WHITE:
					board_string[x][y] = "WHITE"
				else:
					board_string[x][y] = "BLACK"


		return board_string
	
	def rel(self, dir, (x,y)):
		"""
		Returns the coordinates one square in a different direction to (x,y).

		===DOCTESTS===

		>>> board = Board()

		>>> board.rel(NORTHWEST, (1,2))
		(0,1)

		>>> board.rel(SOUTHEAST, (3,4))
		(4,5)

		>>> board.rel(NORTHEAST, (3,6))
		(4,5)

		>>> board.rel(SOUTHWEST, (2,5))
		(1,6)
		"""
		if dir == NORTHWEST:
			return (x - 1, y - 1)
		elif dir == NORTHEAST:
			return (x + 1, y - 1)
		elif dir == SOUTHWEST:
			return (x - 1, y + 1)
		elif dir == SOUTHEAST:
			return (x + 1, y + 1)
		elif dir == NORTH:
			return (x  , y + 1)
		elif dir == SOUTH:
			return (x  , y - 1)
		elif dir == EASY:
			return (x + 1, y)
		elif dir == WEST:
			return (x - 1, y)

		else:
			return 0


	def adjacent(self, (x,y)):
		"""
		Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
		"""

		return [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)),self.rel(SOUTHWEST, (x,y)),self.rel(SOUTHEAST, (x,y))]
		#self.rel(NORTH,(x,y)), self.rel(SOUTH,(x,y)), self.rel(EAST(x,y)), self.rel(WEST,(x,y))

	def location(self, (x,y)):
		"""
		Takes a set of coordinates as arguments and returns self.matrix[x][y]
		This can be faster than writing something like self.matrix[coords[0]][coords[1]]
		"""

		return self.matrix[x][y]

	def blind_legal_moves(self, (x,y)):
		"""
		Returns a list of blind legal move locations from a set of coordinates (x,y) on the board. 
		If that location is empty, then blind_legal_moves() return an empty list.
		"""

		if self.matrix[x][y].occupant != None:
			
			if self.matrix[x][y].occupant.fox == False and self.matrix[x][y].occupant.color == RED:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y))]
				
			elif self.matrix[x][y].occupant.fox == False and self.matrix[x][y].occupant.color == YELLOW:
				blind_legal_moves = [self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

			else:
				blind_legal_moves = [self.rel(NORTHWEST, (x,y)), self.rel(NORTHEAST, (x,y)), self.rel(SOUTHWEST, (x,y)), self.rel(SOUTHEAST, (x,y))]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	def legal_moves(self, (x,y), hop = False):
		"""
		Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
		If that location is empty, then legal_moves() returns an empty list.
		"""

		blind_legal_moves = self.blind_legal_moves((x,y)) 
		legal_moves = []

		if hop == False:
			for move in blind_legal_moves:
				if hop == False:
					if self.on_board(move):
						if self.location(move).occupant == None:
							legal_moves.append(move)

						elif self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
							legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		else: # hop == True
			for move in blind_legal_moves:
				if self.on_board(move) and self.location(move).occupant != None:
					if self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
						legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		return legal_moves

	def remove_piece(self, (x,y)):
		"""
		Removes a piece from the board at position (x,y). 
		"""
		self.matrix[x][y].occupant = None

	def move_piece(self, (start_x, start_y), (end_x, end_y)):
		"""
		Move a piece from (start_x, start_y) to (end_x, end_y).
		"""

		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.remove_piece((start_x, start_y))

		#self.king((end_x, end_y))

	def is_end_square(self, coords):
		"""
		Is passed a coordinate tuple (x,y), and returns true or 
		false depending on if that square on the board is an end square.

		===DOCTESTS===

		>>> board = Board()

		>>> board.is_end_square((2,7))
		True

		>>> board.is_end_square((5,0))
		True

		>>>board.is_end_square((0,5))
		False
		"""

		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False

	def on_board(self, (x,y)):
		"""
		Checks to see if the given square (x,y) lies on the board.
		If it does, then on_board() return True. Otherwise it returns false.

		===DOCTESTS===
		>>> board = Board()

		>>> board.on_board((5,0)):
		True

		>>> board.on_board(-2, 0):
		False

		>>> board.on_board(3, 9):
		False
		"""

		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


	# def king(self, (x,y)):
	# 	#set fox moves to all directions
	# 	if self.location((x,y)).occupant != None:
	# 		if (self.location((x,y)).occupant.color == RED and y == 0) or (self.location((x,y)).occupant.color == YELLOW and y == 7):
	# 			self.location((x,y)).occupant.king = True 

class Piece:
	def __init__(self, color, fox = False):
		self.color = color
		self.fox = fox

class Square:
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Square object

def main():
	game = Game()
	game.main()

if __name__ == "__main__":
	main()
