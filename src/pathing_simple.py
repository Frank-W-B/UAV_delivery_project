'''
Code demonstrates finding obstructing circle between two points and navigating 
around it with the shortest path.  Finds the shortest path.
'''

import matplotlib.pyplot as plt
from math import sqrt, cos, sin, acos, asin, floor
import warnings
warnings.filterwarnings("ignore")
 
def make_plots(p1, p2, c, plist, xytps1, xytps2, plist2):
    ''' make plots in case there was an intersection '''
    plot_pts(plist)
    plot_line(plist, 'k', '--')
    plot_tan_pts(p1, xytps1)
    plot_tan_pts(p2, xytps2)
    plot_circle(c)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axes().set_aspect('equal')
    plt.grid()
    plt.title('Possible paths')
    plt.show()
    plot_pts(plist)
    plot_line(plist, 'k', '--')
    plot_line(plist2, 'r', '-')
    plot_circle(c)
    plt.axes().set_aspect('equal')
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Shortest path')
    plt.show()

def plot_path(plist, c1ist):
    ''' plots the path of pts in plist around the circles in clist '''
    x, y = [p[0] for p in plist], [p[1] for p in plist] # points
    circles = [plt.Circle(c[:2],c[2], color='b') for c in clist] # circles
    # plotting
    plt.plot(x, y, 'ko--')
    plt.axes().set_aspect('equal')
    plt.xlabel('x'); plt.ylabel('y')
    plt.grid()
    plt.title('Ideal path - close window for next figure.')
    plt.show() 
    plt.plot(x, y, 'ko--')
    fig = plt.gcf()
    for circle in circles:
       fig.gca().add_artist(circle)      
    plt.axes().set_aspect('equal')
    plt.xlabel('x'); plt.ylabel('y')
    plt.grid()
    plt.title('Location of circles')
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
    ''' plots a circle where xy tupl is c[:2] and radius is c[2]'''
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
    ''' angle (rad) between two vectors, A & B are tuples with (dx, dy) '''
    LA, LB = sqrt(A[0]**2 + A[1]**2), sqrt(B[0]**2 + B[1]**2)
    AdotB = dot_product(A, B)
    theta = acos(AdotB / (LA * LB))
    return theta

def check_intersection_with_circles(p1, p2, clist):
    ''' checking circle-line intersection per Wolfram Mathworld methodology, will
    indicate true if the circle lie on the line defined by p1 and p2, even if
    the circle is not between p1 and p2.  See complex code for this level of
    robustness '''
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
    for i in range(0, len(d)- 1):
        for j in range(1, len(d)):
            if i != j:
                if almost_equal(d[i],d[j],1e-6):
                    tan_pts_found = True #  2 correct tan pts give equal lengths
                    ind1, ind2 = i, j
    if tan_pts_found == True:
        return [xyints[ind1], xyints[ind2]]
    else:
        print("No tangent points found!")
        return None
    
def determine_best_tan_pt(from_p1, to_p2, xytps):
    ''' of the 2 tangent points, pick the one that give the shortest path '''
    vec_p1top2 = vector_from_two_pts(from_p1, to_p2)
    vec_p1totp = [vector_from_two_pts(from_p1, xytp) for xytp in xytps]
    angles = [angle_btw_two_vectors(vec, vec_p1top2) for vec in vec_p1totp]
    ind = angles.index(min(angles))
    return xytps[ind]

def rotate_about_z_axis(vector, theta):
    ''' rotates a 2d vector (as a tuple) about the z axis by angle theta
    rotation sign convention follows right hand rule, CCW about z + '''
    dx, dy = vector[0], vector[1]
    dxr = dx * cos(theta) - dy * sin(theta)
    dyr = dx * sin(theta) + dy * cos(theta)
    return (dxr, dyr)

def make_arc(p1, tp1, tp2, p2, c):
    ''' makes an arc between tangent point 1 and tangent point 2 every degree
    around circle c and then return the entire point list '''
    pc = (c[0], c[1]) 
    vtp1 = vector_from_two_pts(pc, tp1)
    vtp2 = vector_from_two_pts(pc, tp2)
    arc_angle = angle_btw_two_vectors(vtp1, vtp2)
    # determine angle sign to go from tp1 to tp2
    vtp1_r = rotate_about_z_axis(vtp1, arc_angle)
    if abs(angle_btw_two_vectors(vtp1_r, vtp2)) <= 0.001: # vectors coincident
        sgn = 1.0
    else:
        sgn = -1.0
    delang = sgn * 0.01745 #angle increment (radians)
    na = abs(int(floor(arc_angle / delang))) - 1 # number of angles
    arc = []
    for i in range(na):
        theta = (i + 1) * delang
        varc = rotate_about_z_axis(vtp1, theta)
        pa = (pc[0] + varc[0], pc[1] + varc[1])
        arc.append(pa)
    return [p1, tp1] + arc + [tp2, p2]

if __name__ == '__main__':
    
    # inputs
    # point locations
    p1 = (50, 0) # x,y point 1
    p2 = (200, -150) # x,y point 2
    # (x, y, radius) of circles
    c1 = (85, -50, 35) # circle 1, 85
    #c2 = (75, -100, 20) # circle 2
    
    # calculations
    plist = [p1, p2]
    clist = [c1]
    plot_path(plist, clist) # ideal path
    int_list = check_intersection_with_circles(p1, p2, clist)
    if len(int_list) == 1: # checking intersection with just one circle in this simple example
        c = clist[int_list[0]]
        xytps1 = find_line_circle_tangent_pts(p1, c)
        xytps2 = find_line_circle_tangent_pts(p2, c)
        tp1 = determine_best_tan_pt(p1, p2, xytps1)
        tp2 = determine_best_tan_pt(p2, p1, xytps2)
        if tp1 != None and tp2 != None: # best tangent points successfully determined
            plist2 = make_arc(p1, tp1, tp2, p2, c) # make full path including arc
            make_plots(p1, p2, c, plist, xytps1, xytps2, plist2)
        else:
            print("There was an error finding the tangent points.")
    else:
        print("Sorry, this code investigates intersection with exactly one circle " 
              "and that's it!")
    print("Simulation complete.")
        

