import numpy 
import random
import matplotlib.pyplot as plt

class GameOfLife:

    def __init__(self, N, T):
        self.N=N
        self.old_grid=numpy.zeros(N*N,dtype='i').reshape(N,N)
        self.new_grid=numpy.zeros(N*N,dtype='i').reshape(N,N)
        self.T=T

        for i in range(0,self.N):
            for j in range(0,self.N):
                if(random.randint(0,100) < 15):
                    self.old_grid[i][j]=1
                else:
                    self.old_grid[i][j]=0

    def live_neighbours(self,i,j):
        s=0
        for x in [i-1,i,i+1]:
            for y in [j-1,j,j+1]:
                if(x==i and y ==j):
                    continue
                if(x != self.N and y !=self.N):
                    s += self.old_grid[x][y]
                elif(x == self.N and y != self.N):
                    s += self.old_grid[0][y]
                elif(x != self.N and y == self.N):
                    s += self.old_grid[x][0]
                else:
                    s += self.old_grid[0][0]

        return s

    def play(self):

        plt.imshow(self.old_grid)
        plt.savefig("generation0.png")

        t=1
        write_frequency = 1
        while t <= self.T:
            print "At time level %d" % t

            for i in range(self.N):
                for j in range(self.N):
                    live = self.live_neighbours(i,j)
                    if(self.old_grid[i][j] == 1 and live < 2):
                        self.new_grid[i][j] = 0
                    elif(self.old_grid[i][j] == 1 and (live == 2 or live == 3)):
                        self.new_grid[i][j] == 1
                    elif(self.old_grid[i][j] == 1 and live >3):
                        self.new_grid[i][j] = 0
                    elif(self.old_grid[i][j] == 0 and live == 3):
                        self.new_grid[i][j] = 1

            if(t % write_frequency == 0):
                plt.imshow(self.new_grid)
                plt.savefig("generation%d.png" % t)

            self.old_grid = self.new_grid.copy()

            t += 1 

if(__name__ == "__main__"):
    
    game = GameOfLife (N=100, T=10)
    game.play()
