from geometry import *
from graphics_tk import *

to_screen = [1, 0, 0, 0, -1, 0]
tiles = 0
level = 0

cols = {'H1':"grey", 'H':'light blue', 'T':"blue", 'P':"light grey", 'F':"White"}

vertices_to_draw = []

def drawPolygon(shape, T, fill):
    vertices_to_draw.append([[], fill])
    for i in range (0, len(shape)):
        tp = transPt(T, shape[i])
        vertices_to_draw[len(vertices_to_draw) - 1][0].append(tp)


class Child:
    def __init__(self, T, geom) -> None:
        self.T = T
        self.geom = geom

class HatTile:
    def __init__(self, label):
        self.label = label

    def draw(self, S, level):
        drawPolygon(hat_outline, S, cols[self.label])

class MetaTile:
    def __init__(self, shape, width) -> None:
        self.shape = shape
        self.width = width
        self.children = []

    def addChild(self, T, geom):
        self.children.append(Child(T, geom))

    def evalChild(self, n, i):
        return transPt(self.children[n].T, self.children[n].geom.shape[i])
    
    def draw(self, S, level):
        if level > 0:
            for child in self.children:
                child.geom.draw(mul(S, child.T), level - 1)
        else:
            drawPolygon(self.shape, S, "white")

    def recentre(self):
        cx = 0
        cy = 0

        for p in self.shape:
            cx += p.x
            cy += p.y

        cx /= len(self.shape)
        cy /= len(self.shape)
        tr = pt(-cx, -cy)

        for idx in range (0, len(self.shape)):
            self.shape[idx] = padd(self.shape[idx], tr)

        M = ttrans(-cx, -cy)

        for i in range (0, len(self.children)):
            self.children[i].T = mul(M, self.children[i].T)

H1_hat = HatTile('H1')
H_hat = HatTile('H')
T_hat = HatTile('T')
P_hat = HatTile('P')
F_hat = HatTile('F')

def H_init():
    H_outline = [pt(0, 0), pt(4, 0), pt(4.5, hr3), pt(2.5, 5 * hr3), pt(1.5, 5 * hr3), pt(-0.5, hr3)]
    
    meta = MetaTile(H_outline, 2)
    meta.addChild(matchTwo(hat_outline[5], hat_outline[7], H_outline[5], H_outline[0]), H_hat)
    meta.addChild(matchTwo(hat_outline[9], hat_outline[11], H_outline[1], H_outline[2] ), H_hat)
    meta.addChild(matchTwo(hat_outline[5], hat_outline[7], H_outline[3], H_outline[4] ), H_hat)
    meta.addChild(mul(ttrans(2.5, hr3), mul([-0.5,-hr3,0,hr3,-0.5,0], [0.5,0,0,0,-0.5,0])), H1_hat)

    return meta

def T_init():
    T_outline = [pt(0, 0), pt(3, 0), pt( 1.5, 3*hr3 )]

    meta = MetaTile(T_outline, 2)
    meta.addChild([0.5, 0, 0.5, 0, 0.5, hr3], T_hat)

    return meta

def P_init():
    P_outline = [pt(0, 0), pt(4, 0), pt(3, 2 * hr3), pt(-1, 2 * hr3)]

    meta = MetaTile(P_outline, 2)
    meta.addChild([0.5, 0, 1.5, 0, 0.5, hr3], P_hat)
    meta.addChild(mul(ttrans(0, 2 * hr3), mul([0.5, hr3, 0, -hr3, 0.5, 0], [0.5, 0.0, 0.0, 0.0, 0.5, 0.0])) ,P_hat)

    return meta

def F_init():
    F_outline = [pt(0, 0), pt(3, 0), pt(3.5, hr3), pt(3, 2 * hr3), pt(-1, 2 * hr3)]

    meta = MetaTile(F_outline, 2)
    meta.addChild([0.5, 0, 1.5, 0, 0.5, hr3], F_hat)
    meta.addChild(mul(ttrans(0, 2 * hr3), mul([0.5, hr3, 0, -hr3, 0.5, 0], [0.5, 0.0, 0.0, 0.0, 0.5, 0.0])), F_hat)

    return meta

class Shapes:
    def __init__(self, H, T, P, F):
        self.H = H
        self.T = T
        self.P = P
        self.F = F

def constructPatch(H, T, P, F):
    rules = [['H'],
            [0, 0, 'P', 2],
            [1, 0, 'H', 2],
            [2, 0, 'P', 2],
            [3, 0, 'H', 2],
            [4, 4, 'P', 2],
            [0, 4, 'F', 3],
            [2, 4, 'F', 3],
            [4, 1, 3, 2, 'F', 0],
            [8, 3, 'H', 0],
            [9, 2, 'P', 0],
            [10, 2, 'H', 0],
            [11, 4, 'P', 2],
            [12, 0, 'H', 2],
            [13, 0, 'F', 3],
            [14, 2, 'F', 1],
            [15, 3, 'H', 4],
            [8, 2, 'F', 1], 
            [17, 3, 'H', 0],
            [18, 2, 'P', 0],
            [19, 2, 'H', 2],
            [20, 4, 'F', 3],
            [20, 0, 'P', 2],
            [22, 0, 'H', 2],
            [23, 4, 'F', 3],
            [23, 0, 'F', 3],
            [16, 0, 'P', 2],
            [9, 4, 0, 2, 'T', 2],
            [4, 0, 'F', 3]]
    
    ret = MetaTile([], H.width)
    #shapes = Shapes(H, T, P, F)
    shapes = {'H':H, 'T':T, 'P':P, 'F':F }

    for r in rules:
        if len(r) == 1:
            ret.addChild(ident, shapes[r[0]])
        elif len(r) == 4:
            poly = ret.children[r[0]].geom.shape
            T = ret.children[r[0]].T
            P = transPt(T, poly[(r[1]+1)%len(poly)])
            Q = transPt(T, poly[r[1]])
            nshp = shapes[r[2]]
            npoly = nshp.shape

            ret.addChild(matchTwo(npoly[r[3]], npoly[(r[3]+1)%len(npoly)], P, Q), nshp)
        else:
            chP = ret.children[r[0]]
            chQ = ret.children[r[2]]

            P = transPt(chQ.T, chQ.geom.shape[r[3]])
            Q = transPt(chP.T, chP.geom.shape[r[1]])
            nshp = shapes[r[4]]
            npoly = nshp.shape

            ret.addChild(matchTwo( npoly[r[5]], npoly[(r[5]+1)%len(npoly)], P, Q ), nshp)

    return ret

def constructMetatiles(patch):
    bps1 = patch.evalChild(8, 2)
    bps2 = patch.evalChild(21, 2)
    rbps = transPt(rotAbout( bps1, -2.0*pi/3.0 ), bps2)

    p72 = patch.evalChild(7, 2)
    p252 = patch.evalChild(25, 2)

    llc = intersect(bps1, rbps, patch.evalChild(6, 2), p72)
    w = psub(patch.evalChild( 6, 2 ), llc)

    new_H_outline = [llc, bps1]
    w = transPt(trot(-pi/3), w)
    new_H_outline.append(padd(new_H_outline[1], w))
    new_H_outline.append(patch.evalChild(14, 2))
    w = transPt(trot(-pi/3), w)
    new_H_outline.append(psub(new_H_outline[3], w))
    new_H_outline.append(patch.evalChild(6, 2))

    new_H = MetaTile(new_H_outline, patch.width*2)
    for ch in [0, 9, 16, 27, 26, 6, 1, 8, 10, 15]:
        new_H.addChild(patch.children[ch].T, patch.children[ch].geom)

    new_P_outline = [p72, padd(p72, psub(bps1, llc)), bps1, llc]
    new_P = MetaTile(new_P_outline, patch.width * 2)
    for ch in [7,2,3,4,28]:
        new_P.addChild(patch.children[ch].T, patch.children[ch].geom)

    new_F_outline = [bps2, patch.evalChild(24, 2), patch.evalChild(25, 0), p252, padd(p252, psub( llc, bps1 ))]
    new_F = MetaTile(new_F_outline, patch.width * 2)
    for ch in [21,20,22,23,24,25]:
        new_F.addChild(patch.children[ch].T, patch.children[ch].geom)

    AAA = new_H_outline[2]
    BBB = padd(new_H_outline[1], psub( new_H_outline[4], new_H_outline[5]))
    CCC = transPt(rotAbout(BBB, -pi/3), AAA)
    new_T_outline = [BBB, CCC, AAA]
    new_T = MetaTile(new_T_outline, patch.width*2)
    new_T.addChild(patch.children[11].T, patch.children[11].geom)

    new_H.recentre()
    new_P.recentre()
    new_F.recentre()
    new_T.recentre()

    return [new_H, new_T, new_P, new_F]

def build_supertiles():
    global tiles
    global level

    patch = constructPatch(tiles[0], tiles[1], tiles[2], tiles[3])
    tiles = constructMetatiles(patch)
    level += 1

def draw():
    global level
    global tiles

    #for tile in tiles:
    tiles[0].draw(to_screen, level)

def setup():
    global tiles
    global level
    
    tiles = [H_init(), T_init(), P_init(), F_init()]
    level = 1

    while True:
        draw()
        draw_tiles(vertices_to_draw, width=1000, height=1000)
        #level += 1
        build_supertiles()

setup()