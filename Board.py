import numpy as np
import math

class Board:
    data = np.full((4, 4), -1)

    def add_tile(self, player, coord):
        if self.data[coord[0]][coord[1]] == -1:
            self.data[coord[0]][coord[1]] = player
            return True
        else:
            return False

    def remove_tile(self, coord):
        self.data[coord[0]][coord[1]] = -1

    def get_coord(self, coord):
        return self.data[coord[0]][coord[1]]

    def valid_swap(self, start_coord, new_coord):
        r0, c0 = start_coord
        r1, c1 = new_coord
        if 0 <= r1 <= 3 and 0 <= c1 <= 3 and math.fabs(r1 - r0)\
            + math.fabs(c1 - c0) == 1 and self.data[r1][c1] == -1:
            return True
        else:
            return False
    
    def full(self):
        for i in range(4):
            for j in range(4):
                if self.data[i][j] == -1:
                    return False
        return True

    def game_over(self):
        winner = -1

        # column, row, and diagonal win values
        # r, c = np.full(4, -1)
        # d = np.full(2, -1)
        c = [self.data[0][0],self.data[0][1],self.data[0][2],self.data[0][3]]
        r = [self.data[0][0],self.data[1][0],self.data[2][0],self.data[3][0]]
        d = [self.data[0][0], self.data[0][3]]

        for i in range(4):
            for j in range(4):
                if not c[j] == -1:
                    if not self.data[i][j] == c[j]:
                        c[j] = -1
                    elif i == 3:
                        if winner == (not c[j]):
                            # game is a draw
                            return 2
                        else:
                            # only c[j] has won so far
                            winner = c[j]
                    
                if not r[i] == -1:
                    if not self.data[i][j] == r[i]:
                        r[i] = -1
                    elif j == 3:
                        if winner == (not r[i]):
                            # game is a draw
                            return 2
                        else:
                            # only r[i] has won so far
                            winner = r[i]
                
                if i == j and not (d[0] == -1):
                    if not self.data[i][j] == d[0]:
                        d[0] = -1
                    elif j == 3:
                        if winner == (not d[0]):
                            # game is a draw
                            return 2
                        else:
                            # only d[0] has won so far
                            winner = d[0]
                
                if 3 - i == j and not (d[1] == -1):
                    if not self.data[i][j] == d[1]:
                        d[1] = -1
                    elif i == 3:
                        if winner == (not d[1]):
                            # game is a draw
                            return 2
                        else:
                            # only d[1] has won so far
                            winner = d[1]
        
        return winner
    

    def rotate(self):
        new_data = np.full((4, 4), -1)
        new_data[0][0] = self.data[0][1]
        new_data[0][1] = self.data[0][2]
        new_data[0][2] = self.data[0][3]
        new_data[0][3] = self.data[1][3]
        new_data[1][0] = self.data[0][0]
        new_data[1][1] = self.data[1][2]
        new_data[1][2] = self.data[2][2]
        new_data[1][3] = self.data[2][3]
        new_data[2][0] = self.data[1][0]
        new_data[2][1] = self.data[1][1]
        new_data[2][2] = self.data[2][1]
        new_data[2][3] = self.data[3][3]
        new_data[3][0] = self.data[2][0]
        new_data[3][1] = self.data[3][0]
        new_data[3][2] = self.data[3][1]
        new_data[3][3] = self.data[3][2]
        self.data = new_data