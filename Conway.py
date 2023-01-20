from math import floor
import tkinter

tk = tkinter.Tk()

color_background = "dim gray"
color_lines = "gray"
color_cells = "white"

# quick reference resources
# https://pythonbasics.org/tkinter-canvas/
# https://beltoforion.de/en/game_of_life/


#################### FRAME SETUP ####################

tk.title("Conway.py  |  A Python simulation of Conway's Game of Life")
frame = tkinter.Frame(bg=color_background, width=750, height=500, bd=0)
frame.pack()


#################### CANVAS SETUP ####################

canvas = tkinter.Canvas(frame, bg=color_background, width=750, height=500)
canvas.pack()


#################### ZOOM SETUP ####################

zoom = 10 # zoom resolution of the grid
MIN_ZOOM = 5
MAX_ZOOM = 250

def updateZoom(event):
    global zoom
    zoom += event.delta
    zoom = min(zoom, MAX_ZOOM)
    zoom = max(zoom, MIN_ZOOM)
    drawGrid()

prev_grid = (0, 0)
def userClicked(event):
    global prev_grid
    gridX = floor(event.x / zoom)
    gridY = floor(event.y / zoom)
    cell = (gridX, gridY)
    if cell in active_cells:
        active_cells.remove(cell)
    else:
        active_cells.add(cell)
    prev_grid = cell
    drawGrid()

def userDraggedLeft(event):
    global prev_grid
    gridX = floor(event.x / zoom)
    gridY = floor(event.y / zoom)
    grid_cell = (gridX, gridY)
    if (prev_grid != grid_cell):
        userClicked(event)
        prev_grid = grid_cell

def userDraggedRight(event):
    print((event.x, event.y))

#################### GRID SETUP ####################

active_cells = set() # each active cell is stored as a tuple

# TODO make this work
def drawGrid():
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # draw vertical lines
    for x in range(0, width, zoom):
        canvas.create_line(x, 0, x, height, fill=color_lines, width=1)

    # draw horizontal lines
    for y in range(0, height, zoom):
        canvas.create_line(0, y, width, y, fill=color_lines, width=1)

    for cell in active_cells:
        canvas.create_rectangle(cell[0]*zoom, cell[1]*zoom, (cell[0]+1)*zoom, (cell[1]+1)*zoom, fill=color_cells, outline=color_lines)


def getNeighbors(cell):
    neighbors = set()
    for x in range(cell[0]-1, cell[0]+2):
        for y in range(cell[1]-1, cell[1]+2):
            neighbors.add((x, y))
    return neighbors

def countLiving(cellSet):
    living = 0
    for cell in cellSet:
        if cell in active_cells:
            living += 1
    return living

def updateGrid(event):
    global active_cells
    nextGen = set()
    for cell in active_cells:
        neighbors = getNeighbors(cell)
        liveNeighbors = countLiving(neighbors)-1 # this -1 is to avoid counting this cell itself

        # life loop: decides if a cell should be brought to life
        for n in neighbors:
            if n not in active_cells and countLiving(getNeighbors(n)) == 3:
                nextGen.add(n)

        # death loop: decides if a cell should die
        if liveNeighbors == 2 or liveNeighbors == 3:
            nextGen.add(cell)

    active_cells = nextGen
    print("Active cells: ", len(active_cells))
    drawGrid()


drawGrid()

canvas.bind("<Button-1>", userClicked) # left-click
canvas.bind("<B1-Motion>", userDraggedLeft) # left-click drag
canvas.bind("<B2-Motion>", userDraggedRight) # right-click drag (move view)
tk.bind("<MouseWheel>", updateZoom) # Windows
tk.bind("<Button-4>", updateZoom)   # Linux
tk.bind("<Button-5>", updateZoom)   # Linux

tk.bind("<space>", updateGrid)

tk.mainloop()