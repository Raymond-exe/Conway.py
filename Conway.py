from math import floor, sqrt
from threading import Timer
import tkinter

settings = {
    'Visual': {
        'Minimum zoom': 1,
        'Maximum zoom': 250,
        # TODO add zoom linearization option

        'Background Color': 'dim gray',
        'Cell Color': 'white',
        'Line Color': 'gray',
        'Selection Color': 'dark gray', # TODO make this work

        'Cell Ghosting': True, # TODO turn into an int-based setting
        'Ghost Color #1': 'light gray',
        'Ghost Color #2': 'dark gray',

        'Only render visible cells': False, # TODO test with + without setting enabled
    },
    'Controls': {
        'Center zoom on cursor': True,
        # TODO add more keybind options
    }
}

# quick reference resources
# https://pythonbasics.org/tkinter-canvas/
# https://beltoforion.de/en/game_of_life/

tk = tkinter.Tk()


#################### FRAME SETUP ####################
tk.title("Conway.py  |  A Python simulation of Conway's Game of Life")
frame = tkinter.Frame(bg=settings['Visual']['Background Color'], width=750, height=500, bd=0)
frame.pack()


#################### CANVAS SETUP ####################
canvas = tkinter.Canvas(frame, bg=settings['Visual']['Background Color'], width=750, height=500, highlightthickness=3, highlightbackground=settings['Visual']['Line Color'])
canvas.pack()


#################### ZOOM SETUP ####################
zoom = 25 # (the size of grid cells in pixels)
viewport_location = (0, 0)

def scalePointFrom(pt, origin, scale):
    x = scale * (pt[0] - origin[0]) + origin[0]
    y = scale * (pt[1] - origin[1]) + origin[1]
    return (round(x), round(y))

def updateZoom(event):
    global canvas, viewport_location, settings, zoom

    # update + cap zoom
    old = zoom
    zoom += event.delta
    zoom = min(zoom, settings['Visual']['Maximum zoom'])
    zoom = max(zoom, settings['Visual']['Minimum zoom'])
    ratio = zoom / old

    # move viewport location to keep camera in the same place
    viewport_location = scalePointFrom(viewport_location, (0, 0), ratio)

    # scale viewport location relative mouse pointer (if enabled)
    if settings['Controls']['Center zoom on cursor']:
        center = (
            (viewport_location[0] + event.x), # X
            (viewport_location[1] + event.y)  # Y
        )
    else:
        center = (
            (viewport_location[0] + canvas.winfo_width() / 2),
            (viewport_location[1] + canvas.winfo_height() / 2)
        )
    viewport_location = scalePointFrom(viewport_location, center, ratio)

    drawGrid()


#################### CELL TOGGLING SETUP ####################
prev_cell = (0, 0)
def userLeftClicked(event):
    global prev_cell
    event.x -= viewport_location[0]
    event.y -= viewport_location[1]
    cell = (floor(event.x / zoom), floor(event.y / zoom))

    # Sometimes I love python
    active_cells.remove(cell) if cell in active_cells else active_cells.add(cell)

    prev_cell = cell
    drawGrid()

def fillCellsBetween(a, b):
    def distanceBetween(a, b):
        x = b[0] - a[0]
        y = b[1] - a[1]
        return sqrt(x*x + y*y)
    def normalize(vect, dimension = ''):
        len = distanceBetween((0,0), vect)
        norm = (vect[0] / len, vect[1] / len)
        if dimension:
            x = 1 if dimension == 'x' else norm[0] / norm[1]
            y = 1 if dimension == 'y' else norm[1] / norm[0]
            return (x, y)
        else:
            return norm

    if distanceBetween(a, b) < 2: return
    slope2d = (
        b[0] - a[0], # X
        b[1] - a[1]  # Y
    )
    wider = (abs(slope2d[0]) > abs(slope2d[1]))
    normal = normalize(slope2d, 'x' if wider else 'y')
    counter = 0
    if wider:
        for index in range(0, slope2d[0], 1 if slope2d[0] > 0 else -1):
            active_cells.add((
                round(index * normal[0]) + a[0],
                round(index * normal[1]) + a[1]
            ))
            counter += 1
    else:
        for index in range(0, slope2d[1], 1 if slope2d[1] > 0 else -1):
            active_cells.add((
                round(index * normal[0]) + a[0],
                round(index * normal[1]) + a[1]
            ))
            counter += 1

def userDraggedLeft(event):
    global prev_cell
    x = event.x - viewport_location[0]
    y = event.y - viewport_location[1]
    gridX = floor(x / zoom)
    gridY = floor(y / zoom)
    if (prev_cell != (gridX, gridY)):
        fillCellsBetween(prev_cell, (gridX, gridY))
        userLeftClicked(event)


#################### RIGHT-CLICK DRAG MOVEMENT SETUP ####################
right_click = False # True if right click was already being held down
prev_right_click_location = (0, 0)
def userDraggedRight(event):
    global right_click, prev_right_click_location, viewport_location

    if (not right_click):
        right_click = True
    else:
        delta = (event.x - prev_right_click_location[0], event.y - prev_right_click_location[1])
        viewport_location = (viewport_location[0] + delta[0], viewport_location[1] + delta[1])

    prev_right_click_location = (event.x, event.y)
    drawGrid()

def userReleasedRightClick(event):
    global right_click
    right_click = False
    drawGrid()


#################### GRID SETUP ####################
# cells are stored as tuples in the below sets
active_cells = set()
ghost_cells_1 = set()
ghost_cells_2 = set()

def viewportBounds():
    global canvas, viewport_location, zoom
    screenCellWidth = canvas.winfo_width() / zoom
    screenCellHeight = canvas.winfo_height() / zoom

    x = -viewport_location[0] / zoom
    y = -viewport_location[1] / zoom

    return {
        'min': (x, y),
        'max': (
            x + screenCellWidth,  # X
            y + screenCellHeight, # Y
        )
    }

def drawGrid():
    global canvas, viewport_location, active_cells, ghost_cells_1, ghost_cells_2, settings, zoom
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    if zoom > 4:
        # vertical grid lines
        for x in range(viewport_location[0]%zoom - zoom, viewport_location[0]%zoom + width, zoom):
            canvas.create_line(x, 0, x, height, fill=settings['Visual']['Line Color'], width=1)

        # horizontal grid lines
        for y in range(viewport_location[1]%zoom - zoom, viewport_location[1]%zoom + height, zoom):
            canvas.create_line(0, y, width, y, fill=settings['Visual']['Line Color'], width=1)

    # X & Y axis
    canvas.create_line(0, viewport_location[1], width, viewport_location[1], fill="red", width=1) # x-axis
    canvas.create_line(viewport_location[0], 0, viewport_location[0], height, fill="lime green", width=1) # y-axis

    bounds = viewportBounds()

    # draw cells from active_cells set
    for cell in active_cells:
        if (settings['Visual']['Only render visible cells'] and not pointWithin(cell, bounds)): continue
        canvas.create_rectangle(
            viewport_location[0] + cell[0]*zoom,     # left edge
            viewport_location[1] + cell[1]*zoom,     # top edge
            viewport_location[0] + (cell[0]+1)*zoom, # right edge
            viewport_location[1] + (cell[1]+1)*zoom, # bottom edge
            fill=settings['Visual']['Cell Color'], outline=settings['Visual']['Line Color'] if zoom > 1 else settings['Visual']['Cell Color'])

    # TODO Show selected cell (currently under the mouse cursor)

    # Cell ghosting
    if not settings['Visual']['Cell Ghosting']: return
    for cell in ghost_cells_1:
        if cell in active_cells or not pointWithin(cell, bounds):
            continue

        canvas.create_rectangle(
            viewport_location[0] + cell[0]*zoom,     # left edge
            viewport_location[1] + cell[1]*zoom,     # top edge
            viewport_location[0] + (cell[0]+1)*zoom, # right edge
            viewport_location[1] + (cell[1]+1)*zoom, # bottom edge
            fill=settings['Visual']['Ghost Color #1'], outline=settings['Visual']['Line Color'] if zoom > 1 else settings['Visual']['Cell Color'])

    for cell in ghost_cells_2:
        if cell in active_cells or cell in ghost_cells_1 or not pointWithin(cell, bounds):
            continue

        canvas.create_rectangle(
            viewport_location[0] + cell[0]*zoom,     # left edge
            viewport_location[1] + cell[1]*zoom,     # top edge
            viewport_location[0] + (cell[0]+1)*zoom, # right edge
            viewport_location[1] + (cell[1]+1)*zoom, # bottom edge
            fill=settings['Visual']['Ghost Color #2'], outline=settings['Visual']['Line Color'])

def pointWithin(point, bounds = viewportBounds()):
    xBounded = point[0] >= bounds.get('min')[0]-1 and point[0] < bounds.get('max')[0]
    yBounded = point[1] >= bounds.get('min')[1]-1 and point[1] < bounds.get('max')[1]
    return xBounded and yBounded

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

# TODO optimize
def updateGrid(event):
    global active_cells, ghost_cells_1, ghost_cells_2
    nextGen = set()
    checked = set()
    for cell in active_cells:

        # life loop: decides if a cell should be brought to life
        neighbors = getNeighbors(cell)
        for n in neighbors:
            if n in checked or n in active_cells: continue
            if countLiving(getNeighbors(n)) == 3:
                nextGen.add(n)
            checked.add(n)

        # death loop: decides if a cell should die
        liveNeighbors = countLiving(neighbors)-1 # this -1 is to avoid counting this cell itself
        if liveNeighbors == 2 or liveNeighbors == 3:
            nextGen.add(cell)

    if (settings['Visual']['Cell Ghosting']):
        ghost_cells_2 = ghost_cells_1
        ghost_cells_1 = active_cells
    active_cells = nextGen
    drawGrid()

def reset(event = None):
    global active_cells, viewport_location, ghost_cells_1, ghost_cells_2, canvas, zoom
    ghost_cells_1 = set()
    ghost_cells_2 = set()
    active_cells = set()
    zoom = 25
    viewport_location = (round(canvas.winfo_width()/2), round(canvas.winfo_height()/2))
    drawGrid()


#################### EVENT BINDINGS ####################
canvas.bind("<Button-1>", userLeftClicked) # left-click
canvas.bind("<B1-Motion>", userDraggedLeft) # left-click drag
canvas.bind("<B2-Motion>", userDraggedRight) # right-click drag (move view)
canvas.bind("<ButtonRelease-2>", userReleasedRightClick) # right-click mouseup
tk.bind("<MouseWheel>", updateZoom) # Windows
tk.bind("<Button-4>", updateZoom)   # Linux
tk.bind("<Button-5>", updateZoom)   # Linux

tk.bind("<space>", updateGrid)
tk.bind("r", reset)

Timer(0.1, reset, ()).start()
tk.mainloop()
