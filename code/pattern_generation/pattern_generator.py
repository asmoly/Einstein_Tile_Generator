from geometry import *
from graphics_tk import *

to_screen_mat = [1, 0, 0, 0, -1, 0]
tiles = 0
level = 0

colors = {'H1':["grey", (90, 90, 90)], 'H':['light blue', (254, 100, 100)], 'T':["blue", (254, 0, 0)], 'P':["light grey", (150, 150, 150)], 'F':["White", (200, 200, 200)]}

vertices_to_draw = []

def draw_polygon(shape, T, fill):
    vertices_to_draw.append([[], fill])
    for i in range (0, len(shape)):
        tp = mat_vec_mul(T, shape[i])
        vertices_to_draw[len(vertices_to_draw) - 1][0].append(tp)


class Child:
    def __init__(self, T, geom) -> None:
        self.T = T
        self.geom = geom

class HatTile:
    def __init__(self, label):
        self.label = label

    def draw(self, S, level):
        draw_polygon(hat_outline, S, colors[self.label])

class MetaTile:
    def __init__(self, shape, width) -> None:
        self.shape = shape
        self.width = width
        self.children = []

    def add_child(self, T, geom):
        self.children.append(Child(T, geom))

    def eval_child(self, n, i):
        return mat_vec_mul(self.children[n].T, self.children[n].geom.shape[i])
    
    def draw(self, S, level):
        if level > 0:
            for child in self.children:
                child.geom.draw(mat_mul(S, child.T), level - 1)
        else:
            draw_polygon(self.shape, S, "white")

    def recentre(self):
        cx = 0
        cy = 0

        for p in self.shape:
            cx += p.x
            cy += p.y

        cx /= len(self.shape)
        cy /= len(self.shape)
        tr = Vector(-cx, -cy)

        for idx in range (0, len(self.shape)):
            self.shape[idx] = vec_add(self.shape[idx], tr)

        M = get_transl_mat(-cx, -cy)

        for i in range (0, len(self.children)):
            self.children[i].T = mat_mul(M, self.children[i].T)

H1_hat = HatTile('H1')
H_hat = HatTile('H')
T_hat = HatTile('T')
P_hat = HatTile('P')
F_hat = HatTile('F')

# Outlines go counter-clockwise
def H_init():
    H_outline = [Vector(0, 0), Vector(4, 0), Vector(4.5, y_axis_in_hex.y), Vector(2.5, 5 * y_axis_in_hex.y), Vector(1.5, 5 * y_axis_in_hex.y), Vector(-y_axis_in_hex.x, y_axis_in_hex.y)]
    
    meta = MetaTile(H_outline, 2)
    meta.add_child(match_shapes(hat_outline[5], hat_outline[7], H_outline[5], H_outline[0]), H_hat)
    meta.add_child(match_shapes(hat_outline[9], hat_outline[11], H_outline[1], H_outline[2] ), H_hat)
    meta.add_child(match_shapes(hat_outline[5], hat_outline[7], H_outline[3], H_outline[4] ), H_hat)
    meta.add_child(mat_mul(get_transl_mat(2.5, y_axis_in_hex.y), mat_mul([-y_axis_in_hex.x,-y_axis_in_hex.y,0,y_axis_in_hex.y,-y_axis_in_hex.x,0], [y_axis_in_hex.x,0,0,0,-y_axis_in_hex.x,0])), H1_hat)

    return meta

def T_init():
    T_outline = [Vector(0, 0), Vector(3, 0), Vector( 1.5, 3*y_axis_in_hex.y )]

    meta = MetaTile(T_outline, 2)
    meta.add_child([y_axis_in_hex.x, 0, y_axis_in_hex.x, 0, y_axis_in_hex.x, y_axis_in_hex.y], T_hat)

    return meta

def P_init():
    P_outline = [Vector(0, 0), Vector(4, 0), Vector(3, 2 * y_axis_in_hex.y), Vector(-1, 2 * y_axis_in_hex.y)]

    meta = MetaTile(P_outline, 2)
    meta.add_child([y_axis_in_hex.x, 0, 1.5, 0, y_axis_in_hex.x, y_axis_in_hex.y], P_hat)
    meta.add_child(mat_mul(get_transl_mat(0, 2 * y_axis_in_hex.y), mat_mul([y_axis_in_hex.x, y_axis_in_hex.y, 0, -y_axis_in_hex.y, y_axis_in_hex.x, 0], [y_axis_in_hex.x, 0.0, 0.0, 0.0, y_axis_in_hex.x, 0.0])) ,P_hat)

    return meta

def F_init():
    F_outline = [Vector(0, 0), Vector(3, 0), Vector(3.5, y_axis_in_hex.y), Vector(3, 2 * y_axis_in_hex.y), Vector(-1, 2 * y_axis_in_hex.y)]

    meta = MetaTile(F_outline, 2)
    meta.add_child([y_axis_in_hex.x, 0, 1.5, 0, y_axis_in_hex.x, y_axis_in_hex.y], F_hat)
    meta.add_child(mat_mul(get_transl_mat(0, 2 * y_axis_in_hex.y), mat_mul([y_axis_in_hex.x, y_axis_in_hex.y, 0, -y_axis_in_hex.y, y_axis_in_hex.x, 0], [y_axis_in_hex.x, 0.0, 0.0, 0.0, y_axis_in_hex.x, 0.0])), F_hat)

    return meta

class Shapes:
    def __init__(self, H, T, P, F):
        self.H = H
        self.T = T
        self.P = P
        self.F = F

def construct_patch(H, T, P, F):
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
    shapes = {'H':H, 'T':T, 'P':P, 'F':F }

    for r in rules:
        if len(r) == 1:
            ret.add_child(identity, shapes[r[0]])
        elif len(r) == 4:
            poly = ret.children[r[0]].geom.shape
            T = ret.children[r[0]].T
            P = mat_vec_mul(T, poly[(r[1]+1)%len(poly)])
            Q = mat_vec_mul(T, poly[r[1]])
            nshp = shapes[r[2]]
            npoly = nshp.shape

            ret.add_child(match_shapes(npoly[r[3]], npoly[(r[3]+1)%len(npoly)], P, Q), nshp)
        else:
            chP = ret.children[r[0]]
            chQ = ret.children[r[2]]

            P = mat_vec_mul(chQ.T, chQ.geom.shape[r[3]])
            Q = mat_vec_mul(chP.T, chP.geom.shape[r[1]])
            nshp = shapes[r[4]]
            npoly = nshp.shape

            ret.add_child(match_shapes( npoly[r[5]], npoly[(r[5]+1)%len(npoly)], P, Q ), nshp)

    return ret

def construct_metatiles(patch):
    bps1 = patch.eval_child(8, 2)
    bps2 = patch.eval_child(21, 2)
    rbps = mat_vec_mul(get_rot_mat_about_point( bps1, -2.0*pi/3.0 ), bps2)

    p72 = patch.eval_child(7, 2)
    p252 = patch.eval_child(25, 2)

    llc = get_intersect_point(bps1, rbps, patch.eval_child(6, 2), p72)
    w = vec_sub(patch.eval_child( 6, 2 ), llc)

    new_H_outline = [llc, bps1]
    w = mat_vec_mul(get_rot_mat(-pi/3), w)
    new_H_outline.append(vec_add(new_H_outline[1], w))
    new_H_outline.append(patch.eval_child(14, 2))
    w = mat_vec_mul(get_rot_mat(-pi/3), w)
    new_H_outline.append(vec_sub(new_H_outline[3], w))
    new_H_outline.append(patch.eval_child(6, 2))

    new_H = MetaTile(new_H_outline, patch.width*2)
    for ch in [0, 9, 16, 27, 26, 6, 1, 8, 10, 15]:
        new_H.add_child(patch.children[ch].T, patch.children[ch].geom)

    new_P_outline = [p72, vec_add(p72, vec_sub(bps1, llc)), bps1, llc]
    new_P = MetaTile(new_P_outline, patch.width * 2)
    for ch in [7,2,3,4,28]:
        new_P.add_child(patch.children[ch].T, patch.children[ch].geom)

    new_F_outline = [bps2, patch.eval_child(24, 2), patch.eval_child(25, 0), p252, vec_add(p252, vec_sub( llc, bps1 ))]
    new_F = MetaTile(new_F_outline, patch.width * 2)
    for ch in [21,20,22,23,24,25]:
        new_F.add_child(patch.children[ch].T, patch.children[ch].geom)

    AAA = new_H_outline[2]
    BBB = vec_add(new_H_outline[1], vec_sub( new_H_outline[4], new_H_outline[5]))
    CCC = mat_vec_mul(get_rot_mat_about_point(BBB, -pi/3), AAA)
    new_T_outline = [BBB, CCC, AAA]
    new_T = MetaTile(new_T_outline, patch.width*2)
    new_T.add_child(patch.children[11].T, patch.children[11].geom)

    new_H.recentre()
    new_P.recentre()
    new_F.recentre()
    new_T.recentre()

    return [new_H, new_T, new_P, new_F]

def build_supertiles():
    global tiles
    global level

    patch = construct_patch(tiles[0], tiles[1], tiles[2], tiles[3])
    tiles = construct_metatiles(patch)
    level += 1

def draw():
    global level
    global tiles

    #for tile in tiles:
    tiles[0].draw(to_screen_mat, level)
    
tiles = [H_init(), T_init(), P_init(), F_init()]
level = 1

def next_generation():
    draw()
    build_supertiles()