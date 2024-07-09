from math import cos, sin, pi

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

y_axis_in_hex = Vector(0.5, 0.8660254037844386)
identity = [1, 0, 0, 0, 1, 0]

# Converts hex coordinates to cartesian coordinates
def hex_to_cart(x, y):
    return Vector(x + y_axis_in_hex.x*y, y_axis_in_hex.y*y)

# Inverts matrix
def invert_mat(mat):
    det = mat[0]*mat[4] - mat[1]*mat[3]
    return [mat[4]/det, -mat[1]/det, (mat[1]*mat[5]-mat[2]*mat[4])/det, 
            -mat[3]/det, mat[0]/det, (mat[2]*mat[3]-mat[0]*mat[5])/det]

# Multiplies two matrices
def mat_mul(A, B):
	return [A[0]*B[0] + A[1]*B[3], A[0]*B[1] + A[1]*B[4], A[0]*B[2] + A[1]*B[5] + A[2],
		    A[3]*B[0] + A[4]*B[3], A[3]*B[1] + A[4]*B[4], A[3]*B[2] + A[4]*B[5] + A[5]]

# Adds vectors
def vec_add(p, q):
    return Vector(p.x + q.x, p.y + q.y)

# Subtracts vectors
def vec_sub(p, q):
    return Vector(p.x - q.x, p.y - q.y)

# Returns rotation matrix
def get_rot_mat(angle):
	c = cos(angle)
	s = sin(angle)
	return [c, -s, 0, s, c, 0]

# Returns translation matrix
def get_transl_mat(tx, ty):
	return [1, 0, tx, 0, 1, ty]

# Returns a matrix that rotates around a point p
def get_rot_mat_about_point(p, angle):
	return mat_mul(get_transl_mat(p.x, p.y), mat_mul(get_rot_mat(angle), get_transl_mat(-p.x, -p.y)))

# Multiplies a matrix by a vector
def mat_vec_mul(M, P):
	return Vector(M[0]*P.x + M[1]*P.y + M[2], M[3]*P.x + M[4]*P.y + M[5])

def match_segment(p, q):
	return [q.x - p.x, p.y - q.y, p.x,  q.y - p.y, q.x - p.x, p.y]

# Generate transform matrix that places line segment (p1,q1) on to line segment (p2,q2)
def match_shapes(p1, q1, p2, q2):
	return mat_mul(match_segment(p2, q2), invert_mat(match_segment( p1, q1 )))

def get_intersect_point(p1, q1, p2, q2):
    d = (q2.y - p2.y)*(q1.x - p1.x) - (q2.x - p2.x)*(q1.y - p1.y)
    uA = ((q2.x - p2.x)*(p1.y - p2.y) - (q2.y - p2.y)*(p1.x - p2.x))/d

    return Vector(p1.x + uA*(q1.x - p1.x), p1.y + uA*(q1.y - p1.y))

# Outline goes counter-clockwise
hat_outline = [hex_to_cart(0, 0), hex_to_cart(-1,-1), hex_to_cart(0,-2), hex_to_cart(2,-2),
               hex_to_cart(2,-1), hex_to_cart(4,-2), hex_to_cart(5,-1), hex_to_cart(4, 0),
               hex_to_cart(3, 0), hex_to_cart(2, 2), hex_to_cart(0, 3), hex_to_cart(0, 2),
               hex_to_cart(-1, 2)]