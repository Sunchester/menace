'''Implementation of Quadratic Probing Hash Table'''
import re
import string
from board import *
from ast import literal_eval


class BoardHashTable:
    ''' Quadratic Hash Class '''
    def __init__(self, seedfilename=None):
        ''' Initialization of Hash Table '''
        self.tablesize = 251
        self.count = 0
        self.arr = []
        
        for i in range(self.tablesize):
            self.arr.append(None)
        if seedfilename != None:
            self.load_file(seedfilename)

    def get_conflict_resolved_index(self,key):
        ''' Gets a free index in the table based on 
        the key with the proper conflict resolution strategy'''
        indx = self.myhash(key,self.get_tablesize())
        orig = indx
        inc = 0
        while self.arr[indx] is not None and self.arr[indx][0] != key:
            inc += 1
            indx = orig + inc**2
            indx %= self.get_tablesize()
        return indx


    def put(self, board, movelist=None):
        '''inserts the keyitem pair into the table, rehashes if table too large'''
        if self.get_load_fact() > 0.4:
            copy = self.arr
            oldct = self.count
            self.tablesize = self.tablesize*2 + 1
            self.count = 0
            self.arr = []
            for i in range(self.tablesize):
                self.arr.append(None)
            for tup in copy:
                if tup is not None:
                    self.put(Board(tup[0]),tup[1])
            if abs(oldct - self.count) >= 1:
                print("old=%d, new=%d" % (oldct,self.count))
                raise AssertionError("lost elements in rehash")

        # print("ok")
        indx = self.get_conflict_resolved_index(board.get_key())

        if self.arr[indx] == None:
            if movelist is None:
                movelist = board.make_movelist()
            self.arr[indx] = (board.get_key(),movelist)
            self.count += 1
        else:
            raise AssertionError("double put")

    
    def contains(self,board):
        '''returns true if the key is indeed in the list'''
        indx = self.get_conflict_resolved_index(board.get_key())

        # print(self.arr[indx])
        if self.arr[indx] is None:
            return False

        if self.arr[indx][0] == board.get_key():
            return True

    def get_movelist(self, board):
        ''' Uses given key to find and return the item, key pair'''

        indx = self.get_conflict_resolved_index(board.get_key())

        if self.arr[indx] == None:
            raise LookupError()

        if self.arr[indx][0] == board.get_key():
            return self.arr[indx][1]


    def get_tablesize(self):
        '''returns Size of Hash Table'''
        return self.tablesize

    def get_load_fact(self):
        '''returns the load factor of the hash table'''
        return float(self.count) / float(self.tablesize)

    def myhash(self, key, table_size):
        '''hashes based on horners rule'''
        num = 0
        for i in range(min(len(key),9)):
            num = 31*num + self.strangeord(key[i])
        return num % table_size

    def strangeord(self, char):
        if char == '-':
            return 0
        elif char == 'o':
            return 1
        elif char == 'x':
            return 2
        else:
            return ord(char)

    def print_all_boards(self):
        for i in range(self.tablesize):
            if self.arr[i] is not None:
                Board(self.arr[i][0]).print_board()
                print(self.arr[i][1])

    def menace_save(self,filename):
        f = open(filename, 'w')
        for i in range(self.tablesize):
            if self.arr[i] is not None:
                line = self.arr[i][0] + "|" + str(self.arr[i][1]) + '\n'
                f.write(line)
        f.close()

    def load_file(self,filename):
        f = open(filename,'r')
        while True:
            line = f.readline()
            if not line:
                break
            pretup = line.split('|')
            self.put(Board(pretup[0]),literal_eval(pretup[1]))


