from math import cos, sin, pi

r3 = 1.7320508075688772
hr3 = 0.8660254037844386
ident = [1, 0, 0, 0, 1, 0]

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

def pt(x, y):
    return Vector(x, y)

# Converts hex coordinates to euler coordinates
def hexPt(x, y):
    return Vector(x + 0.5*y, hr3*y)

# Inverts matrix
def inv(mat):
    det = mat[0]*mat[4] - mat[1]*mat[3]
    return [mat[4]/det, -mat[1]/det, (mat[1]*mat[5]-mat[2]*mat[4])/det, 
            -mat[3]/det, mat[0]/det, (mat[2]*mat[3]-mat[0]*mat[5])/det]

# Multiplies two matrices
def mul(A, B):
	return [A[0]*B[0] + A[1]*B[3], A[0]*B[1] + A[1]*B[4], A[0]*B[2] + A[1]*B[5] + A[2],
		    A[3]*B[0] + A[4]*B[3], A[3]*B[1] + A[4]*B[4], A[3]*B[2] + A[4]*B[5] + A[5]]

# Adds vectors
def padd(p, q):
    return Vector(p.x + q.x, p.y + q.y)

# Subtracts vectors
def psub(p, q):
    return Vector(p.x - q.x, p.y - q.y)

# Returns rotation matrix
def trot(angle):
	c = cos(angle)
	s = sin(angle)
	return [c, -s, 0, s, c, 0]

# Returns translation matrix
def ttrans(tx, ty):
	return [1, 0, tx, 0, 1, ty]

# Returns a matrix that rotates around a point p
def rotAbout(p, angle):
	return mul(ttrans(p.x, p.y), mul(trot(angle), ttrans(-p.x, -p.y)))

# Multiplies a matrix by a vector
def transPt(M, P):
	return pt(M[0]*P.x + M[1]*P.y + M[2], M[3]*P.x + M[4]*P.y + M[5])

def matchSeg(p, q):
	return [q.x - p.x, p.y - q.y, p.x,  q.y - p.y, q.x - p.x, p.y]

def matchTwo(p1, q1, p2, q2):
	return mul(matchSeg(p2, q2), inv(matchSeg( p1, q1 )))

def intersect(p1, q1, p2, q2):
    d = (q2.y - p2.y)*(q1.x - p1.x) - (q2.x - p2.x)*(q1.y - p1.y)
    uA = ((q2.x - p2.x)*(p1.y - p2.y) - (q2.y - p2.y)*(p1.x - p2.x))/d

    return pt(p1.x + uA*(q1.x - p1.x), p1.y + uA*(q1.y - p1.y))

hat_outline = [hexPt(0, 0), hexPt(-1,-1), hexPt(0,-2), hexPt(2,-2),
               hexPt(2,-1), hexPt(4,-2), hexPt(5,-1), hexPt(4, 0),
               hexPt(3, 0), hexPt(2, 2), hexPt(0, 3), hexPt(0, 2),
               hexPt(-1, 2) ]