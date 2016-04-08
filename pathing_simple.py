import matplotlib.pyplot as plt
from math import sqrt, cos, sin, acos, asin


def make_plots(p1, p2, c, plist, xytps1, xytps2):
    ''' make some plots in case there was an intersection '''
    plot_pts(plist)
    plot_line(plist, 'k', '--')
    plot_tan_pts(p1, xytps1)
    plot_tan_pts(p2, xytps2)
    plot_circle(c)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axes().set_aspect('equal')
    plt.grid()
    plt.show()
    plot_pts(plist)
    plot_line([p1, tp1], 'r', '-')
    plot_line([p2, tp2], 'r', '-')
    plot_circle(c)
    plt.axes().set_aspect('equal')
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def plot_path(plist, c1ist):
    ''' plots the path of pts in plist around the circles in clist '''
   
    x, y = [p[0] for p in plist], [p[1] for p in plist] # points
    circles = [plt.Circle(c[:2],c[2], color='b') for c in clist] # circles
    
    # plotting
    plt.plot(x, y, 'ko-')
    plt.axes().set_aspect('equal')
    plt.xlabel('x'); plt.ylabel('y')
    plt.grid()
    plt.show() 
    plt.plot(x, y, 'ko-')
    fig = plt.gcf()
    for circle in circles:
       fig.gca().add_artist(circle)      
    # max_x, max_y, min_x, min_y = max(x), max(y), min(x), min(y)
    # hf_x, hf_y = (max_x + min_x)/2.,(max_y + min_y)/2. 
    # hf_span = 1.2 * max(max_x - min_x, max_y - min_y)/2.
    # plt.xlim(int(hf_x - hf_span), int(hf_x + hf_span))
    # plt.ylim(int(hf_y - hf_span), int(hf_y + hf_span))
    plt.axes().set_aspect('equal')
    plt.xlabel('x'); plt.ylabel('y')
    plt.grid()
    plt.show()

def plot_pts(plist):
    x, y = [p[0] for p in plist], [p[1] for p in plist]
    plt.plot(x, y, 'ko') 

def plot_line(plist, col, linstyle):
    x, y = [p[0] for p in plist], [p[1] for p in plist]
    line = plt.plot(x, y)
    plt.setp(line, color = col, linestyle = linstyle)

def plot_tan_pts(p, tplist):
    ''' plots the tangent points of the lines from pt p to circle c '''
    x, y = [], []
    x.append(p[0])
    y.append(p[1])
    for tp in tplist:
        x.append(tp[0])
        y.append(tp[1])
        plt.plot(x, y, 'r-')
        x.pop()
        y.pop()

def plot_circle(c):
    ''' plots a circle where xy tupl is c[:2] and radius is c[2] '''
    circle = plt.Circle(c[:2],c[2], color='b')
    fig = plt.gcf()
    fig.gca().add_artist(circle)

def distance2d(p1, p2):
    ''' euclidean distance between two points '''
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
def almost_equal(v1, v2, crit):
    ''' returns true if abs(v1 - v2) <= crit '''
    return abs(v1 - v2) <= crit

def vector_from_two_pts(from_pt1, to_pt2):
    ''' defines a 2d vector from two points, where each pt is an xy tuple  '''
    dx, dy = to_pt2[0] - from_pt1[0], to_pt2[1] - from_pt1[1]
    return (dx, dy)

def dot_product(A, B):
    ''' find dot product of vectors defined by A and B
    A and B are tuples with (dx, dy) '''
    AdotB = A[0]*B[0] + A[1]*B[1] 
    return AdotB

def angle_btw_two_vectors(A, B):
    ''' finds the angle (rad) between two vectors
    A and B are tuples with (dx, dy) '''
    LA, LB = sqrt(A[0]**2 + A[1]**2), sqrt(B[0]**2 + B[1]**2)
    AdotB = dot_product(A, B)
    theta = acos(AdotB / (LA * LB))
    return theta

def check_intersection_with_circles(p1, p2, clist):
    ''' checking circle-line intersection per Wolfram Mathworld methodology '''
    
    int_list = [] # initialize with line from p1 to p2 not intersecting any circles
    for i, c in enumerate(clist):
        xc, yc, r = c[0], c[1], c[2]
        x1, y1 = p1[0] - xc, p1[1] - yc
        x2, y2 = p2[0] - xc, p2[1] - yc
        dx, dy = x2 - x1, y2 - y1
        dr = sqrt(dx**2 + dy**2)
        D = x1 * y2 - x2 * y1
        Disc = (r**2)*(dr**2)-D**2
        if Disc > 0:
            int_list.append(i) # intersects circle with index i
    return int_list

def find_line_circle_tangent_pts(p, c):
    ''' finding pts on circle where line intersects and is tangent per
    Wolfram Mathworld's methodology for circle tangent line intersection '''

    xp, yp = p[0], p[1]
    x0, y0, a = c[0] - xp, c[1] - yp, c[2]
    ss_x2y2 = x0**2 + y0**2
    sgns = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # 4 solutions from differing signs
    ts = [] # solve for t to get x, y intersection points
    for s in sgns:
        ts.append(s[0]*acos((-a*x0 + s[1]*y0*sqrt(ss_x2y2 - a**2))/float(ss_x2y2)))
    xyints = []
    for t in ts:
        x = x0 + a * cos(t) + xp
        y = y0 + a * sin(t) + yp
        xyints.append((x, y)) # 4 points of intersection with circle
    d = []
    for xy in xyints:
       d.append(distance2d(p, xy)) # find the lengths of the 4 lines
    tan_pts_found = False
    for i in xrange(0, len(d)- 1):
        for j in xrange(1, len(d)):
            if i != j:
                if almost_equal(d[i],d[j],1e-6):
                    tan_pts_found = True #  2 correct tan pts give equal lengths
                    ind1, ind2 = i, j
    if tan_pts_found == True:
        return [xyints[ind1], xyints[ind2]]
    else:
        print "No tangent points found!"
        return None
    
def determine_best_tan_pt(from_p1, to_p2, xytps):
    ''' of the 2 tangent points, pick the one that give the shortest path '''
    vec_p1top2 = vector_from_two_pts(from_p1, to_p2)
    vec_p1totp = [vector_from_two_pts(from_p1, xytp) for xytp in xytps]
    angles = [angle_btw_two_vectors(vec, vec_p1top2) for vec in vec_p1totp]
    ind = angles.index(min(angles))
    return xytps[ind]

if __name__ == '__main__':
    p1 = (50, 0)
    p2 = (200, -150)
    c1 = (75, -30, 15)
    c2 = (125, -120, 30)
    plist = [p1, p2]
    clist = [c1, c2]
    plot_path(plist, clist)
    int_list = check_intersection_with_circles(p1, p2, clist)
    if len(int_list) == 1:
        c = clist[int_list[0]]
        xytps1 = find_line_circle_tangent_pts(p1, c)
        xytps2 = find_line_circle_tangent_pts(p2, c)
        tp1 = determine_best_tan_pt(p1, p2, xytps1)
        tp2 = determine_best_tan_pt(p2, p1, xytps2)
        make_plots(p1, p2, c, plist, xytps1, xytps2)         
        

