from tkinter import *

from geometry import *

class EinsteinCanvas(Canvas):
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)
        self.scalar = 1

    def set_scalar(self, scalar):
        self.scalar = scalar

    def draw_polygon(self, vertices, fill="blue"):
        coordinates = []
        for vec in vertices:
            coordinates.append(vec.x*self.scalar + self.winfo_reqwidth()/2)
            coordinates.append(vec.y*self.scalar + self.winfo_reqheight()/2)

        self.create_polygon(coordinates, fill=fill, width=2, outline="black")

def draw_tiles(tiles, width=500, height=500, scalar=20):
    root = Tk()
    canvas = EinsteinCanvas(root, width=width, height=height)
    
    canvas.set_scalar(scalar)

    for tile in tiles:
        canvas.draw_polygon(tile[0], fill=tile[1][0])

    canvas.pack()
    root.mainloop()