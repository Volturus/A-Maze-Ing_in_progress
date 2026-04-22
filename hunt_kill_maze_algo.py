import random
from typing import Optional


class Maze:
    def __init__(self, width: int, height: int, start: tuple[int, int], seed: Optional[int] = None):
        random.seed(seed)
        self.maze = self.create_empty_maze(width, height)
        self.current_coords = start
        self.last_coords = start

    def create_empty_maze(self, width: int, height: int):
        maze = []
        for i in range(height):
            maze += [["N"]*width]
        return maze
    
    def check_surrounding(self, coords: tuple[int, int]) -> str:
        NESW = [0,0,0,0]

        if (coords[1] != 0):
            if (self.last_coords == (coords[0], coords[1] - 1)):
                NESW[0] = "P"
                last_bit = bin(int(self.maze[self.last_coords[1]][self.last_coords[0]], 16))[2:]
                while (len(last_bit) < 4):
                    last_bit = "0" + last_bit
                new_bit = last_bit[0]+"0"+last_bit[2]+last_bit[3]
                self.maze[self.last_coords[1]][self.last_coords[0]] = hex(int(new_bit, 2))[2:].capitalize()
            else:
                NESW[0] = self.maze[coords[1] - 1][coords[0]]
        else:
            NESW[0] = "W"

        if (coords[0] != len(self.maze[coords[1]]) - 1):
            if (self.last_coords == (coords[0] + 1, coords[1])):
                NESW[1] = "P"
                last_bit = bin(int(self.maze[self.last_coords[1]][self.last_coords[0]], 16))[2:]
                while (len(last_bit) < 4):
                    last_bit = "0" + last_bit
                new_bit = "0"+last_bit[1]+last_bit[2]+last_bit[3]
                self.maze[self.last_coords[1]][self.last_coords[0]] = hex(int(new_bit, 2))[2:].capitalize()
            else:
                NESW[1] = self.maze[coords[1]][coords[0] + 1]
        else:
            NESW[1] = "W"

        if (coords[1] != len(self.maze) - 1):
            if (self.last_coords == (coords[0], coords[1] + 1)):
                NESW[2] = "P"
                last_bit = bin(int(self.maze[self.last_coords[1]][self.last_coords[0]], 16))[2:]
                while (len(last_bit) < 4):
                    last_bit = "0" + last_bit
                new_bit = last_bit[0]+last_bit[1]+last_bit[2]+"0"
                self.maze[self.last_coords[1]][self.last_coords[0]] = hex(int(new_bit, 2))[2:].capitalize()
            else:
                NESW[2] = self.maze[coords[1] + 1][coords[0]]
        else:
            NESW[2] = "W"

        if (coords[0] != 0):
            if (self.last_coords == (coords[0] - 1, coords[1])):
                NESW[3] = "P"
                last_bit = bin(int(self.maze[self.last_coords[1]][self.last_coords[0]], 16))[2:]
                while (len(last_bit) < 4):
                    last_bit = "0" + last_bit
                new_bit = last_bit[0]+last_bit[1]+"0"+last_bit[3]
                self.maze[self.last_coords[1]][self.last_coords[0]] = hex(int(new_bit, 2))[2:].capitalize()
            else:
                NESW[3] = self.maze[coords[1]][coords[0] - 1]
        else:
            NESW[3] = "W"

        return NESW

    def hunt(self):
        found = 0
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if (self.maze[i][j] == "N"):
                    found = 1
                    self.current_coords = (j, i)
                    break
            if (found == 1):
                break
        if (found == 0):
            return (1)
        self.last_coords = (len(self.maze[0])+2, len(self.maze) + 2)
        NESW = self.check_surrounding(self.current_coords)
        last_known = []
        for i in range(4):
            if (NESW[i] != "W" and NESW[i] != "N"):
                last_known += [i]
        previous = random.choice(last_known)
        if (previous == 0):
            self.last_coords = (self.current_coords[0], self.current_coords[1] - 1)
        if (previous == 1):
            self.last_coords = ((self.current_coords[0] + 1, self.current_coords[1]))
        if (previous == 2):
            self.last_coords = (self.current_coords[0], self.current_coords[1] + 1)
        if (previous == 3):
            self.last_coords = (self.current_coords[0] - 1, self.current_coords[1])
        return (0)

    def hunt_kill_algo(self):
        coords = self.current_coords
        unknown = []
        NESW = self.check_surrounding(coords)
        bit = [0,0,0,0]
        for i in range(4):
            if (NESW[i] != "P"):
                bit[3-i] = 1
            if (NESW[i] ==  "N"):
                unknown += [i]
        new = hex(int((str(bit[0]) + str(bit[1]) + str(bit[2]) + str(bit[3])), 2))[2]
        self.maze[coords[1]][coords[0]] = new.capitalize()
        self.last_coords = coords
        if (len(unknown) == 0):
            if (self.hunt() == 0):
                print("!!!", self.last_coords, bit)
                self.hunt_kill_algo()
            else:
                print("???", self.current_coords)
                return
        else:
            next = random.choice(unknown)
            if (next == 0):
                self.current_coords = (coords[0], coords[1] - 1)
                self.hunt_kill_algo()
            if (next == 1):
                self.current_coords = ((coords[0] + 1, coords[1]))
                self.hunt_kill_algo()
            if (next == 2):
                self.current_coords = (coords[0], coords[1] + 1)
                self.hunt_kill_algo()
            if (next == 3):
                self.current_coords = (coords[0] - 1, coords[1])
                self.hunt_kill_algo()


def main():
    a = Maze(4, 6, (0,0), 150)
    a.hunt_kill_algo()
    for i in a.maze:
        print(i)


if __name__ == "__main__":
    main()

