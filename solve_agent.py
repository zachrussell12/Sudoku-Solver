import copy

class Solve_Agent():

    def __init__(self):
        pass


    def check_puzzle_solved(self, puzzle_grid):

        #check rows
        for i in range(len(puzzle_grid)):
            tmpArray = []
            for j in range(len(puzzle_grid)):
                tmpArray.append(puzzle_grid[i][j])

        if len(tmpArray) > len(set(tmpArray)):
            #print("Duplicate found in row!")
            return False

        #check cols
        for i in range(len(puzzle_grid)):
            tmpArray = []
            for j in range(len(puzzle_grid)):
                tmpArray.append(puzzle_grid[j][i])

        if len(tmpArray) > len(set(tmpArray)):
            #print("Duplicate found in column!")
            return False
            
        for i in range(len(puzzle_grid)):
            for j in range(len(puzzle_grid)):
                if puzzle_grid[j][i] == ".":
                    #print("Still moves to be made.")
                    return False

        print("Puzzle solved!")
        return True
    
    def check_valid_move(self, puzzle_grid, move, row, col):

        #print("Checking move: ", move)

        rowArray = []
        for j in range(len(puzzle_grid)):
            rowArray.append(puzzle_grid[row][j])

        #print("Row array: ", rowArray)
        if move in rowArray:
            #print("Move already done in row: ", move)
            return False
            
        colArray = []
        for j in range(len(puzzle_grid)):
            colArray.append(puzzle_grid[j][col])

        #print("Column array: ", colArray)
        if move in colArray:
            #print("Move already done in column: ", move)
            return False
        
        quadrant_row = (row // 3) * 3
        quadrant_col = (col // 3) * 3

        for i in range(quadrant_row, quadrant_row+3):
            for j in range(quadrant_col, quadrant_col+3):
                if puzzle_grid[i][j] == move:
                    return False
    
        return True
        

    def solve_puzzle(self, puzzle_grid, sudokuContainer, root):

        initial_state = puzzle_grid.copy()
        expanded_nodes_stack = []
        visited_states = []
        j = 0

        while self.check_puzzle_solved(puzzle_grid) == False:

            current_state = []
            move_row = None
            move_col = None

            if j == 0:
                current_state = copy.deepcopy(initial_state)
            else:

                current_state = expanded_nodes_stack.pop()

            visited_states.append(current_state)

            #print("Current State: ", current_state)


            for i in range(len(current_state)):
                for k in range(len(current_state)):
                    if current_state[i][k] != puzzle_grid[i][k]:
                        sudokuContainer.winfo_children()[(i*9) + k].configure(text=current_state[i][k], foreground="#67c3f5")
                    root.update()

            #print(current_state)

            for i in range(len(current_state)):
                for k in range(len(current_state)):
                    if current_state[i][k] == ".":
                        move_row = i
                        move_col = k
                        break

                if move_row is not None and move_col is not None:
                    break
            
            #print("Move row: ", move_row)
            #print("Move col: ", move_col)

            if move_row is not None and move_col is not None:

                for k in range(len(current_state)):

                    temp = copy.deepcopy(current_state)

                    if self.check_valid_move(temp, k+1, move_row, move_col):
                        #print("Found valid move: ", k+1)
                        temp[move_row][move_col] = k+1
                        expanded_nodes_stack.append(temp)

            j += 1

            #print("Expanded Node Stack: ", expanded_nodes_stack)

            puzzle_grid = copy.deepcopy(current_state)

            #print(current_state)

        return True


