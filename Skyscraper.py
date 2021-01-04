from collections import defaultdict

class Game:

    def __init__(self, n, top, right, bottom, left, default_boxes):
        self.left = self.__process(left)
        self.right = self.__process(right)
        self.top = self.__process(top)
        self.bottom = self.__process(bottom)
        
        self.n = n
        self.grid = [[0 for i in range(n)] for j in range(n)]
        for key, value in default_boxes.items():
            self.grid[key[0]][key[1]] = value
        self.griddict = {}
        self.d = defaultdict(list)
        self.possibles = []
        self.rows = defaultdict(list)
        self.columns = defaultdict(list)
        self.last_count = None

    def solve(self):  
        self.__get_possibles([])

        for p in self.possibles:
            self.d[self.__count(p)].append(p)

        if self.__solve_rec():
            for i in range(self.n):
                print(*self.grid[i])
        else:
            print("Could'nt solve the complete grid. Here is the last process: ")
            for i in range(self.n):
                print(*self.grid[i])
            print("\n", self.griddict)
                
    def __solve_rec(self):
        for i in range(self.n):
            for j in range(self.n):
                self.griddict[(i, j)] = []

        self.__solve_scan()

        for i in range(self.n):
            for j in range(self.n):
                if len(self.griddict[(i, j)]) == 1:
                    self.grid[i][j] = self.griddict[(i, j)][0]

        for i in range(self.n):
            seen = defaultdict(list)
            for j in range(self.n):
                for v in self.griddict[(i, j)]:
                    seen[v].append(j)
            for key, value in seen.items():
                if len(value) == 1:
                    self.grid[i][value[0]] = key

        for j in range(self.n):
            seen = defaultdict(list)
            for i in range(self.n):
                for v in self.griddict[(i, j)]:
                    seen[v].append(i)
            for key, value in seen.items():
                if len(value) == 1:
                    self.grid[value[0]][j] = key

        c1, c2 = self.__control()
        if c1+c2 == 2:
            return True
        if c1+c2 == 0:
            return False

        return self.__solve_rec()
        
    def __control(self):
        last = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] != 0:
                    last += 1
        if self.last_count == last:
            return False, False
        elif last < self.n**2:
            self.last_count = last
            return False, True
        return True, True

    
    def __solve_scan(self):
        for i in range(self.n):
            for j in range(self.n):
                pl, pr, pt, pb = set(), set(), set(), set()
                    
                if self.left[i] != None:
                    for v in self.d[self.left[i]]:
                        if self.__fits(i, j, v, True):
                            pl.add(v[j])
                else:
                    row = self.grid[i].copy()
                    for v in range(self.n):
                        if v+1 not in row:
                            pl.add(v+1)

                if self.right[i] != None:
                    for v in self.d[self.right[i]]:
                        if self.__fits(i, j, v[::-1], True):
                            pr.add(v[::-1][j])
                else:
                    row = self.grid[i].copy()
                    for v in range(self.n):
                        if v+1 not in row:
                            pr.add(v+1)
                            
                ph = set.intersection(pl, pr)

                if self.top[j] != None:
                    for v in self.d[self.top[j]]:
                        if self.__fits(i, j, v, False):
                            pt.add(v[i])
                else:
                    column = [self.grid[m][j] for m in range(self.n)]
                    for v in range(self.n):
                        if v+1 not in column:
                            pt.add(v+1)

                if self.bottom[j] != None:
                    for v in self.d[self.bottom[j]]:
                        if self.__fits(i, j, v[::-1], False):
                            pb.add(v[::-1][i])
                else:
                    column = [self.grid[m][j] for m in range(self.n)]
                    for v in range(self.n):
                        if v+1 not in column:
                            pb.add(v+1)

                pv = set.intersection(pt, pb)

                p = set.intersection(ph, pv)

                #print(i, j, "\n", pl, pr, ph, "\n", pt, pb, pv, "\n", ph, pv, p)

                self.griddict[(i, j)] = list(p)

    def __fits(self, y, x, l, horizontal):
        if horizontal:
            for i in range(self.n):
                if self.grid[y][i] + l[i] != l[i] and self.grid[y][i] + l[i] != 2*l[i]:
                    return False
            return True
        else:
            for i in range(self.n):
                if self.grid[i][x] + l[i] != l[i] and self.grid[i][x] + l[i] != 2*l[i]:
                    return False
            return True

    def __get_possibles(self, seq):
        if len(seq) == self.n:
            self.possibles.append(tuple(seq.copy()))
            return
        for nn in range(self.n):
            if nn+1 not in seq:
                seq.append(nn+1)
                self.__get_possibles(seq)
                seq.pop()
        return

    @staticmethod
    def __count(seq):
        m = 0
        s = 0
        for v in seq:
            if m < v:
                s += 1
                m = v
        return s

    @staticmethod
    def __process(seq):
        for i, v in enumerate(seq):
            if v == 0:
                seq[i] = None
        return seq

print("Author: Kerem Kırıcı\nInstagram: keremmkirici_\n" +
      "\nEnter the wanted values in clockwise. \nIf there is no information about a " +
      "row a column then type 0.\n\n" +
      "  0 0 2 1 0  \n" +
      "  _ _ _ _ _  \n" +
      "4|_|_|_|_|_| \n" +
      "4|_|_|_|_|_| \n" +
      " |_|_|_|_|_|5\n" +
      " |_|_|_|_|_| \n" +
      " |_|_|_|_|_| \n" +
      "  2   1      \n" +
      "Here Some Input Example for a game like this: \n\n"
      "Number of Rows and Columns: 5\n" +
      "Top Side: 0 0 2 1 0\n" +
      "Right Side: 0 0 5 0 0\n" +
      "Bottom Side: 0 0 1 0 2\n" +
      "Left Side: 0 0 0 4 4\n" +
      "How many boxes filled already?\n" +
      "0\n")

number_of_columns_rows = int(input("Number of Rows and Columns: "))
top_side = list(map(int, input("Top Side: ").strip().split()))
right_side = list(map(int, input("Right Side: ").strip().split()))
bottom_side = list(map(int, input("Bottom Side: ").strip().split()))[::-1]
left_side = list(map(int, input("Left Side: ").strip().split()))[::-1]
already_filled_boxes = {}

message = "How many boxes filled already?\n"
while True:
    try:
        inp = int(input(message))
        break
    except:
        message = "How many boxes filled already? (Enter an integer)\n"
        
for i in range(inp):
    inp_row = input("Row (1 to {}): ".format(number_of_columns_rows))
    while True:
        try:
            inp_row = int(inp_row)
            if 0 < inp_row <= number_of_columns_rows:
                break
            print("Invalid input")
            inp_row = input("Row (1 to {}): ".format(number_of_columns_rows))
        except:
            print("Invalid input")
            inp_row = input("Row (1 to {}): ".format(number_of_columns_rows))
            
    inp_column = input("Column (1 to {}): ".format(number_of_columns_rows))
    while True:
        try:
            inp_column = int(inp_column)
            if 0 < inp_column <= number_of_columns_rows:
                break
            print("Invalid input")
            inp_column = input("Column (1 to {}): ".format(number_of_columns_rows))
        except:
            print("Invalid input")
            inp_column = input("Column (1 to {}): ".format(number_of_columns_rows))
    
    inp_value = input("Value (0 for empty, 0 to {}): ".format(number_of_columns_rows))
    while True:
        try:
            inp_value = int(inp_value)
            if 0 <= inp_value <= number_of_columns_rows:
                break
            print("Invalid input")
            inp_value = input("Value (0 for empty, 0 to {}): ".format(number_of_columns_rows))
        except:
            print("Invalid input")
            inp_value = input("Value (0 for empty, 0 to {}): ".format(number_of_columns_rows))
    
    already_filled_boxes[(inp_row-1, inp_column-1)] = inp_value

Problem = Game(number_of_columns_rows, top_side, right_side,
               bottom_side, left_side, already_filled_boxes)

print("\nOutput: \n")

Problem.solve()

input("Waiting for any key press to kill the program..")

