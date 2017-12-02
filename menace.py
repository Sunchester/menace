from board import *
from quat_ht import *
from random import randint

class Menace():
	def __init__(self, xoro):
		self.new_game(xoro)
		self.ht = BoardHashTable()


	def new_game(self, xoro):
		self.move_history = []
		self.marker = xoro

	def make_move(self,board):
		tup = board.find_soft_equal_tuple(self.ht)
		if tup[0] is None:
			self.ht.put(board)
			safe = board
			backid = 0
		else:
			safe = tup[0]
			backid = tup[1]
		mm = self.safe_move(safe)
		return mm.transform(backid)

	def safe_move(self,board):
		mvlist = self.ht.get_movelist(board)
		msum = 0
		for n in mvlist:
			msum += n
		ogrand = randint(0,msum-1)
		rnd = ogrand

		# print(rnd)
		# print(mvlist)
		sv = -1
		for i in range(9):
			rnd -= mvlist[i]
			if rnd < 0:
				sv = i
				break
		if sv == -1:
			raise AssertionError("MENACE tried -1 index")
			print("msum=%d ogrand=%d" %(msum,ogrand))
		self.move_history.append((board,sv))
		cpy = board.transform(0)
		if cpy.arr[sv] != '-':
			for x in range(10):
				print()
			print("what the fuck Menace msum=%d ogrand=%d sv=%d" %(msum,ogrand,sv))
			board.print_board()
			for x in range(10):
				print()
		cpy.arr[sv] = self.marker
		return cpy

	def learn(self,delta):
		for i in range(len(self.move_history)):
			mvboard = self.move_history[i][0]
			# print("FOR THIS BOARD:")
			# mvboard.print_board()
			# print(self.ht.get_movelist(mvboard))
			self.ht.get_movelist(mvboard)[self.move_history[i][1]] += delta
			self.ht.get_movelist(mvboard)[self.move_history[i][1]] = max(self.ht.get_movelist(mvboard)[self.move_history[i][1]],0)
			# print(self.ht.get_movelist(mvboard))

	




