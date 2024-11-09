import matplotlib.pyplot as plt

class Sudoku:

    def __init__(self, grid):
        self.grid = grid

    def draw(self, title='', show_rc_nums=False, show_valid_vals=False):
        # Draw lines
        fig, self.ax = plt.subplots(figsize=(8,8))
        for i in range(0,10,3):
            self.ax.plot([i,i],[0,9],linewidth=2,color='k')
            self.ax.plot([0,9],[i,i],linewidth=2,color='k')
        for i in range(1,9):
            self.ax.plot([i,i],[0,9],linewidth=1,color='k')
            self.ax.plot([0,9],[i,i],linewidth=1,color='k')

        # Print row and column numbers if desired
        if show_rc_nums:
            for i in range(9):
                self.ax.text((-.5),(i+.5), str(i), size=12,color = 'r',
                    ha="center", va="center")
                self.ax.text((i+.5),(-.5), str(i), size=12,color = 'r',
                    ha="center", va="center")

        # Print known values
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.ax.text((j+.5),(i+.5), str(self.grid[i][j]), size=18,
                        ha="center", va="center")

        # Print valid values using small green numbers, if desired
        if show_valid_vals and hasattr(self,'V'):
            for i in range(9):
                for j in range(9):
                    if self.grid[i][j] == 0:
                        for n in self.V.get((i,j), []):
                            n1 = n-1
                            self.ax.text((j+.5+(n1%3-1)*.25),(i+.5+(n1//3-1)*.25), str(n), size=10,
                                         color = 'g', ha="center", va="center")

        self.ax.axis('off')
        self.ax.set_title(title, y=-.05,size = 18)
        self.ax.set_aspect(1.0)
        self.ax.invert_yaxis()
        plt.show()

    def find_neighbors(self):
        self.N = {} # (r,c):{coords (x,y) that are neighbours with rc}
        
        for i in range(9):
            for j in range(9):
                self.N[(i,j)] = set()
                # row
                for k in range(9):
                    if k!=j:
                        self.N[(i,j)].add((i,k))

                # column
                for z in range(9):
                    if z!=i:
                        self.N[(i,j)].add((z,j))
                
                # block
                # identify the starting corner coordinates
                corner_i, corner_j = self.start_corner(i,j)

                for row in range(corner_i, corner_i+3):
                    for column in range(corner_j, corner_j+3):
                        if (row, column) != (i,j):
                            self.N[(i,j)].add((row,column))


    # Method that returns the coordinates of the top corner of the corresponding block to a pair of coodinates
    def start_corner(self,i:int,j:int):
        tr = (i//3)*3
        tc = (j//3)*3
        return tr,tc

    def init_valid(self):
        self.V = {} # (r, c):{valid numbers 1-9}

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    self.V[(i,j)] = {1,2,3,4,5,6,7,8,9}

                    for neighbors in self.N[(i,j)]:
                        row = neighbors[0]
                        column = neighbors[1]

                        if self.grid[row][column] in self.V[(i,j)]:
                            self.V[(i,j)].remove(self.grid[row][column])
                else:
                    self.V[(i,j)] = {}
            
    def solve(self):
        self.find_neighbors()
        self.init_valid()

        known = self.find_knowns()
        while len(known) > 0:
            (val, row, column) = known.pop() # this is a tuple (val,i,j)
            self.grid[row][column] = val 

            # we can use the same method to get all possible values again
            self.init_valid()
        
        return self.endstate()

    # method to fill the known set
    def find_knowns(self):
        # fill known with possible values
        known = set() # (val, row, column)
        for key in self.V.keys(): # { (row,colum):{1,2,4,5} }
            if len(self.V[key]) == 1:
                known_temp = (self.V[key].pop(), key[0], key[1])
                known.add(known_temp)
        return known
    
    # method to determine the end state of a puzzle 
    # 1 if solved
    # -1 if there is at least 1 cell with missing val and no possible vals
    # 0 if 1 empty cell with possible vals
    def endstate(self):
        for i in range(9):
            for j in range(9):
                # if we find an empty cell, and the associated possible values set is empty
                if self.grid[i][j] == 0:
                    if len(self.V[(i,j)]) == 0:
                        return -1

        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    if len(self.V[(i,j)]) > 0:
                        return 0
        
        return 1
                
    def solve_backtrack(self):
        self.find_neighbors()
        self.init_valid()

        empty_cell = self.find_empty_cell()
        if empty_cell is None:
            return 1
        
        row = empty_cell[0]
        column = empty_cell[1]
        
        for value in self.V[(row,column)]:
            self.grid[row][column] = value
            
            solution = self.solve_backtrack()
            if (solution == 1):
                return solution
            
            self.grid[row][column] = 0
        return -1
                
    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None
