from random import choice
from structures import MatrixGraph

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


class Maze(MatrixGraph):
    def __init__(self, size):
        super().__init__(True)
        self.__size = size
        for y in range(size):
            for x in range(size):
                self.add_node((x,y))

        # for y in range(size):
        #     for x in range(size):
        #         if x > 0: self.add_edge((x,y), (x-1,y))
        #         if x < size - 1: self.add_edge((x+1,y), (x,y))
        # 
        #         if y > 0: self.add_edge((x,y), (x,y-1))
        #         if y < size - 1: self.add_edge((x,y), (x,y+1))

    def get_neighbours(self, node):
        x, y = node
        
        if x > 0: yield (x-1,y)
        if x < self.__size - 1: yield (x+1,y)

        if y > 0: yield (x,y-1)
        if y < self.__size - 1: yield (x,y+1)

    def generate_maze(self, start_node):
        if start_node in self.matrix[0]:
            visited = [start_node]
            stack = [start_node]

            while len(stack) > 0:
                current = stack.pop()

                neighbours = [node for node in self.get_neighbours(current) if node not in visited]
                if len(neighbours) > 0:
                    next_neighbour = choice(neighbours)
                    self.add_edge(current, next_neighbour)
                    visited.append(next_neighbour)
                    stack.append(current)
                    stack.append(next_neighbour)

    def display(self):
        app = tk.Tk()
        app.title("Generated Maze")
        app.geometry("800x800")
        app.resizable(False,False)

        # store as bit patterns, NESW, N -> high bit
        CONNECTIONS = {
            # 0 connections
            0b0000: ImageTk.PhotoImage(Image.open("maze_tiles/space.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            # 1 connection
            0b1000: ImageTk.PhotoImage(Image.open("maze_tiles/north.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b0100: ImageTk.PhotoImage(Image.open("maze_tiles/east.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b0010: ImageTk.PhotoImage(Image.open("maze_tiles/south.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b0001: ImageTk.PhotoImage(Image.open("maze_tiles/west.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            # 2 straight connections
            0b1010: ImageTk.PhotoImage(Image.open("maze_tiles/north-south.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b0101: ImageTk.PhotoImage(Image.open("maze_tiles/east-west.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            # 2 corner connections
            0b1001: ImageTk.PhotoImage(Image.open("maze_tiles/north-west.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b0011: ImageTk.PhotoImage(Image.open("maze_tiles/south-west.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b1100: ImageTk.PhotoImage(Image.open("maze_tiles/north-east.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b0110: ImageTk.PhotoImage(Image.open("maze_tiles/east-south.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            # 3 connections
            0b1110: ImageTk.PhotoImage(Image.open("maze_tiles/north-east-south.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b1011: ImageTk.PhotoImage(Image.open("maze_tiles/north-south-west.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b1101: ImageTk.PhotoImage(Image.open("maze_tiles/north-east-west.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            0b0111: ImageTk.PhotoImage(Image.open("maze_tiles/east-south-west.png").resize((760//self.__size,760//self.__size), Image.LANCZOS)),
            # 4 connections
            0b1111: ImageTk.PhotoImage(Image.open("maze_tiles/north-east-south-west.png").resize((760//self.__size,760//self.__size), Image.LANCZOS))        }

        frame = ttk.Frame(app)
        for y in range(self.__size):
            for x in range(self.__size):
                value = 0
                if x > 0 and self.is_connected((x,y),(x-1,y)): value += 0b0001
                if x < self.__size - 1 and self.is_connected((x,y),(x+1,y)): value += 0b0100
                if y > 0 and self.is_connected((x,y),(x,y-1)): value += 0b1000
                if y < self.__size - 1 and self.is_connected((x,y),(x,y+1)): value += 0b0010
                ttk.Label(image=CONNECTIONS[value]).grid(row=y, column=x, sticky=tk.NSEW)

        app.mainloop()

if __name__ == "__main__":
    m = Maze(10)
    # m.display()
    m.generate_maze((0,0))
    m.display()

