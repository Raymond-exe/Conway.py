import tkinter

tk = tkinter.Tk()

# quick reference resources
# https://pythonbasics.org/tkinter-canvas/
# https://beltoforion.de/en/game_of_life/


#################### ZOOM SETUP ####################

zoom = 10 # zoom resolution of the grid
MIN_ZOOM = 1
MAX_ZOOM = 250

def updateZoom(event):
    global zoom
    zoom -= event.delta
    zoom = min(zoom, MAX_ZOOM)
    zoom = max(zoom, MIN_ZOOM)
    print(zoom)

tk.bind("<MouseWheel>", updateZoom) # Windows
tk.bind("<Button-4>", updateZoom)   # Linux
tk.bind("<Button-5>", updateZoom)   # Linux


#################### FRAME SETUP ####################

tk.title("Conway.py  |  A Python simulation of Conway's Game of Life")
frame = tkinter.Frame(bg="gray", width=750, height=500, bd=0)
frame.pack()


#################### CANVAS SETUP ####################

canvas = tkinter.Canvas(frame, bg="gray", width=750, height=500)
canvas.pack()


#################### GRID SETUP ####################

active_cells = [] # each active cell is stored as a tuple

# TODO make this work
def draw_grid():
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    for x in range(0, width, zoom):
        canvas.create_line(x, 0, x, height, fill="white", width=1)
    
    for y in range(0, height, zoom):
        canvas.create_line(0, y, width, y, fill="white", width=1)

    for cell in active_cells:
        canvas.create_rectangle(0, 0, 10, 10, fill="yellow")

def update_grid():
    # TODO make this work
    draw_grid()

draw_grid()

tk.mainloop()
