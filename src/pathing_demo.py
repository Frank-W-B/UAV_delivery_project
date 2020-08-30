from UAV_helper import circleObject, pathObject
import matplotlib.pyplot as plt
from math import sqrt, cos, sin, tan, acos, asin, atan2, degrees, pi
from random import random, seed
import os
import warnings
warnings.filterwarnings("ignore")

def plot_pointlist(plist, desig):
    ''' plots point list (each pt is an x, y tuple) with designated format '''
    x, y = [p[0] for p in plist], [p[1] for p in plist]
    plt.plot(x, y, desig)

def plot_path(plist, desig):
    ''' plots point list (each pt is an x, y tuple) with designated format '''
    x, y = [p[0] for p in plist], [p[1] for p in plist]
    plt.plot(x, y, desig, linewidth = 2)


def plot_circles():
    ''' plots circles, fc is the x, y location of the field center, fsl is
    the field length (equal in x and y)'''
    circs = []
    xmin, xmax, ymin, ymax, rmax = 1e6, -1e6, 1e6, -1e6, 0  # for graph scaling
    nc = len(circles) # number of circles
    for i in range(nc):
        xy, r = circles[i].xy, circles[i].r
        x, y = xy[0], xy[1]
        circs.append(plt.Circle(xy, r, color='r'))
        if x > xmax: xmax = x
        if x < xmin: xmin = x
        if y > ymax: ymax = y
        if y < ymin: ymin = y
        if r > rmax: rmax = r
    fsl = max(xmax - xmin, ymax - ymin) # field side length
    fc = ((xmax + xmin) / 2.,(ymax + ymin) / 2.) # field center
    fig = plt.gcf()
    for circ in circs:
       fig.gca().add_artist(circ)
    #for i in xrange(nc):
    #    x, y = circles[i].xy[0], circles[i].xy[1]
    #    plt.text(x, y, str(circles[i].cid))
    hsl = fsl / 2. # half the field length
    sf = 1.1 # scale factor to set plot limits
    xmin, xmax = int(sf * (fc[0] - hsl - rmax)), int(sf * (fc[0] + hsl + rmax))
    ymin, ymax = int(sf * (fc[1] - hsl - rmax)), int(sf * (fc[1] + hsl + rmax))
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.axes().set_aspect('equal')
    plt.xlabel('x'); plt.ylabel('y')
    fig = plt.gcf()
    plt.rcParams["figure.figsize"] = [10.0, 10.0]
    # plt.grid()
    plt.show()

def distance(p1, p2):
    ''' euclidean distance between two points, each is (x, y) tuple '''
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def vector_from_two_pts(from_pt1, to_pt2):
    ''' defines a 2d vector from two points, where each pt is an xy tuple  '''
    dx, dy = to_pt2[0] - from_pt1[0], to_pt2[1] - from_pt1[1]
    return (dx, dy)

def length_vector(vector):
    ''' determines length of a vector, where vector is a tuple of (dx, dy) '''
    return sqrt(vector[0]**2 + vector[1]**2)

def unit_vector(vector):
    ''' turns a vector into a unit vector (length 1) '''
    mag = float(length_vector(vector))
    dx, dy = vector[0]/mag, vector[1]/mag
    return (dx, dy)

def rotate_about_z_axis(vector, theta):
    ''' rotates a 2d vector (as a tuple) about the z axis by angle theta
    rotation sign convention follows right hand rule, CCW about z + '''
    dx, dy = vector[0], vector[1]
    dxr = dx * cos(theta) - dy * sin(theta)
    dyr = dx * sin(theta) + dy * cos(theta)
    return (dxr, dyr)

def dot_product(A, B):
    ''' find dot product of vectors defined by A and B
    A and B are tuples with (dx, dy) '''
    AdotB = A[0]*B[0] + A[1]*B[1]
    return AdotB

def angle_btw_two_vectors(A, B):
    ''' Finds the angle (rad) between two vectors (A and B), measured from A to
    B. Angle convention follows RHR (+ is cw, - is ccw).
    A and B are tuples with (dx, dy) '''
    LA, LB = length_vector(A), length_vector(B)
    AdotB = dot_product(A, B)
    theta = abs(acos(AdotB / (LA * LB)))
    A_uv, B_uv  = unit_vector(A), unit_vector(B)
    A_uv_r = rotate_about_z_axis(A_uv, theta)
    if dot_product(A_uv_r, B_uv) > 0.9999:
        return theta # collinear, theta positive
    else:
        return -theta

def angle_vector_cw_from_x_axis(vector):
    ''' finds the angle between a vector and the x axis measured cw from x axis
        return 0 to 2pi '''
    dx, dy = vector[0], vector[1]
    angle = atan2(dy, dx)
    if angle < 0:
        angle = 2 * pi + angle
    return angle

def check_circle_on_infinite_line(p1, p2, circle):
    ''' checks whether a circle is on the infinite line defined by p1 and p2
        Uses Wolfram Mathworld methodology '''
    xc, yc, r = circle.xy[0], circle.xy[1], circle.r
    x1, y1 = p1[0] - xc, p1[1] - yc
    x2, y2 = p2[0] - xc, p2[1] - yc
    dx, dy = x2 - x1, y2 - y1
    dr = sqrt(dx**2 + dy**2)
    D = x1 * y2 - x2 * y1
    Disc = (r**2)*(dr**2)-D**2
    return Disc > 0 # will return true if line intersects obstacle (circle)

def check_circle_in_front_of_p1(p1, p2, circle):
    ''' checks that obstacle is in front of p1 on way to p2 '''
    pc = circle.xy # circle center location
    v_to_c = unit_vector(vector_from_two_pts(p1, pc))
    v_to_p2 = unit_vector(vector_from_two_pts(p1, p2))
    return dot_product(v_to_c, v_to_p2) > 0 # obstacle in front if dp > 0

def check_circle_not_behind_p2(p1, p2, circle):
    ''' checks that obstacle is not past p2 '''
    pc = circle.xy # circle center location
    v_to_c = unit_vector(vector_from_two_pts(p2, pc))
    v_to_p2 = unit_vector(vector_from_two_pts(p1, p2))
    return dot_product(v_to_c, v_to_p2) < 0 # obstacle not behind if dp < 0

def find_nearest_circle(p1, blocking_cids):
    ''' finds the nearest circle to p1 in the blocking list '''
    d = []
    for cid in blocking_cids:
        pc = circles[cid].xy # circle center location
        dist = distance(p1, pc)
        d.append(dist)
    minindex = d.index(min(d))
    return blocking_cids[minindex]

def check_if_blocked(p1, p2, cid_p2):
    ''' Checking circle-line intersection per Wolfram Mathworld methodology
    with some other checks needed for a finite line.  p1, p2 are (x, y) tuples
    that define the start, end points, respectively, and cid_list is the
    subset of obstacles that may intersect the line from p1 to p2
    Ignores cid_p2 in analysis '''
    blocked = False # intialize as not blocked
    blocking_cids = [] # initialize intersection list
    ignore_list = [cid_p2, path[-1].cid]
    for circle in circles:
        if circle.cid not in ignore_list:
            circle_on_line = check_circle_on_infinite_line(p1, p2, circle)
            if circle_on_line:
                # print("Circle {} is on the line".format(circle.cid))
                circle_in_front_p1 = check_circle_in_front_of_p1(p1, p2, circle)
                if circle_in_front_p1:
                    # print("Circle {} is in front of p1".format(circle.cid))
                    circle_not_behind_p2 = check_circle_not_behind_p2(p1, p2, circle)
                    if circle_not_behind_p2:
                        # print("Circle {} is not behind p2".format(circle.cid))
                        blocking_cids.append(circle.cid)
                        blocked = True
    if blocked:
        # print("It's blocked, and the blocking cids are {}".format(blocking_cids))
        cid_nearest = find_nearest_circle(p1, blocking_cids)
        # print("Circle {} is the nearest".format(circles[cid_nearest].cid))
    else:
        cid_nearest = None
    return blocked, cid_nearest

def aimpoint_on_circle_cw(p1, p2, cid_blk, offset):
    ''' defines the best cw aimpoint to get around the blocking circle
        and returns the aimpoint (pa), and that dir_cw = True
        offset is used to slightly offset aimpoint from circle edge
    '''
    v_p1p2 = vector_from_two_pts(p1, p2) # vector from p1 to p2
    circle = circles[cid_blk] # blocking circle
    pc, r = circle.xy, circle.r
    v_p1pc = vector_from_two_pts(p1, pc) # vector from p1 to pc
    ang_from_x = angle_vector_cw_from_x_axis(v_p1pc)
    v_pc_on_x = rotate_about_z_axis(v_p1pc, -ang_from_x)
    # adjust by discrepancy in p1p2 and p1pc angles
    ang_from_x_p1p2 = angle_vector_cw_from_x_axis(v_p1p2)
    del_ang = ang_from_x_p1p2 - ang_from_x
    adj = (0, + r + offset)
    adj = rotate_about_z_axis(adj, del_ang)
    # apply adjustment
    v_pa_on_x = (v_pc_on_x[0] + adj[0], v_pc_on_x[1] + adj[1])
    v_p1pa = rotate_about_z_axis(v_pa_on_x, ang_from_x)
    pa = (p1[0] + v_p1pa[0], p1[1] + v_p1pa[1])
    dir_cw = True
    return pa, dir_cw

def aimpoint_on_circle_ccw(p1, p2, cid_blk, offset):
    ''' defines the best ccw aimpoint to get around the blocking circle
        and returns the aimpoint (pa), and that dir_cw = False
        offset is used to slightly offset aimpoint from circle edge
    '''
    v_p1p2 = vector_from_two_pts(p1, p2) # vector from p1 to p2
    circle = circles[cid_blk] # blocking circle
    pc, r = circle.xy, circle.r
    v_p1pc = vector_from_two_pts(p1, pc) # vector from p1 to pc
    ang_from_x = angle_vector_cw_from_x_axis(v_p1pc)
    v_pc_on_x = rotate_about_z_axis(v_p1pc, -ang_from_x)
    # adjust by discrepancy in p1p2 and p1pc angles
    ang_from_x_p1p2 = angle_vector_cw_from_x_axis(v_p1p2)
    del_ang = ang_from_x_p1p2 - ang_from_x
    adj = (0, - r - offset)
    adj = rotate_about_z_axis(adj, del_ang)
    # apply adjustment
    v_pa_on_x = (v_pc_on_x[0] + adj[0], v_pc_on_x[1] + adj[1])
    v_p1pa = rotate_about_z_axis(v_pa_on_x, ang_from_x)
    pa = (p1[0] + v_p1pa[0], p1[1] + v_p1pa[1])
    dir_cw = False
    return pa, dir_cw

def aimpoint_on_circle_cw_or_ccw(p1, p2, cid_blk, offset):
    ''' defines the best aimpoint (cw or ccw) to get around the blocking circle
        and returns the aimpoint (pa), and whether the cw or ccw aimpoint was
        chosen (dir_cw = True if cw)
        offset is used to slightly offset aimpoint from circle edge
    '''
    pa_cw, dir_cw_cw = aimpoint_on_circle_cw(p1, p2, cid_blk, offset)
    pa_ccw, dir_cw_ccw = aimpoint_on_circle_ccw(p1, p2, cid_blk, offset)
    v_p1p2 = vector_from_two_pts(p1, p2) # vector from p1 to p2
    v_p1pa_cw = vector_from_two_pts(p1, pa_cw) # vector from p1 to pa_cw
    v_p1pa_ccw = vector_from_two_pts(p1, pa_ccw) # vector from p1 to pa_ccw
    ang_cw = abs(angle_btw_two_vectors(v_p1p2, v_p1pa_cw))
    ang_ccw = abs(angle_btw_two_vectors(v_p1p2, v_p1pa_ccw))
    if ang_cw <= ang_ccw:
        pa, dir_cw = pa_cw, dir_cw_cw
    else:
        pa, dir_cw = pa_ccw, dir_cw_ccw
    return pa, dir_cw

def aimpoint_on_group_cw(p1, p2, cid_blk, offset):
    ''' defines the best cw aimpoint around a group of circles and returns the
    aimpoint (pa), the maximum cw aimpoint dir_cw = True, and the cid of the
    circle that the aimpoint rests on '''
    blocking_cids = circles[cid_blk].grp
    pa_list, dir_cw_list = [], []
    for cid_blk in blocking_cids:
        pa, dir_cw = aimpoint_on_circle_cw(p1, p2, cid_blk, offset)
        pa_list.append(pa)
        dir_cw_list.append(dir_cw)
    v_p1p2 = vector_from_two_pts(p1, p2) # vector from p1 to p2
    v_p1pa_list = []
    for pa in pa_list:
        v_p1pa = vector_from_two_pts(p1, pa) # vector from p1 to pa
        v_p1pa_list.append(v_p1pa)
    ang_list = []
    for v_p1pa in v_p1pa_list:
        ang = angle_btw_two_vectors(v_p1p2, v_p1pa)
        ang_list.append(ang)
    ind_cw_max = ang_list.index(max(ang_list))
    pa = pa_list[ind_cw_max]
    dir_cw = dir_cw_list[ind_cw_max]
    cid_blk = blocking_cids[ind_cw_max]
    return pa, dir_cw, cid_blk

def aimpoint_on_group_ccw(p1, p2, cid_blk, offset):
    ''' defines the best ccw aimpoint around a group of circles and returns the
    aimpoint (pa), the maximum cw aimpoint dir_cw = True, and the cid of the
    circle that the aimpoint rests on '''
    blocking_cids = circles[cid_blk].grp
    pa_list, dir_cw_list = [], []
    for cid_blk in blocking_cids:
        pa, dir_cw = aimpoint_on_circle_ccw(p1, p2, cid_blk, offset)
        pa_list.append(pa)
        dir_cw_list.append(dir_cw)
    v_p1p2 = vector_from_two_pts(p1, p2) # vector from p1 to p2
    v_p1pa_list = []
    for pa in pa_list:
        v_p1pa = vector_from_two_pts(p1, pa) # vector from p1 to pa
        v_p1pa_list.append(v_p1pa)
    ang_list = []
    for v_p1pa in v_p1pa_list:
        ang = angle_btw_two_vectors(v_p1p2, v_p1pa)
        ang_list.append(ang)
    ind_ccw_min = ang_list.index(min(ang_list))
    pa = pa_list[ind_ccw_min]
    dir_cw = dir_cw_list[ind_ccw_min]
    cid_blk = blocking_cids[ind_ccw_min]
    return pa, dir_cw, cid_blk

def aimpoint_on_group_cw_or_ccw(p1, p2, cid_blk, offset):
    ''' defines the best aimpoint (cw or ccw) to get around the blocking group
        and returns the aimpoint (pa), and whether the cw or ccw aimpoint was
        chosen (dir_cw = True if cw), and the cid of the aimpoint
        offset is used to slightly offset aimpoints from circle edges
    '''
    pa_cw, dir_cw_cw, cid_blk_cw = aimpoint_on_group_cw(p1, p2, cid_blk, offset)
    pa_ccw, dir_cw_ccw, cid_blk_ccw = aimpoint_on_group_ccw(p1, p2, cid_blk, offset)
    v_p1p2 = vector_from_two_pts(p1, p2) # vector from p1 to p2
    v_p1pa_cw = vector_from_two_pts(p1, pa_cw) # vector from p1 to pa_cw
    v_p1pa_ccw = vector_from_two_pts(p1, pa_ccw) # vector from p1 to pa_ccw
    ang_cw = abs(angle_btw_two_vectors(v_p1p2, v_p1pa_cw))
    ang_ccw = abs(angle_btw_two_vectors(v_p1p2, v_p1pa_ccw))
    if ang_cw <= ang_ccw:
        pa, dir_cw, cid_blk = pa_cw, dir_cw_cw, cid_blk_cw
    else:
        pa, dir_cw, cid_blk = pa_ccw, dir_cw_ccw, cid_blk_ccw
    return pa, dir_cw, cid_blk

def get_route(p1, p2, cid_p2, dir_cw_p2, offset):
    ''' Determines the route from point 1 to point 2 given the cid on which
        point 2 resides and whether p2 was the cw or ccw aimpoint.
        Offset is used to slightly offset aimpoints from circle edges if
        necessary. '''
    p1x,p1y,p2x,p2y = round(p1[0],2), round(p1[1],2), round(p2[0],2), round(p2[1],2)
    print("Check if blocked btw {}, {} and {}, {}".format(p1x, p1y, p2x, p2y))
    blocked, cid_blk = check_if_blocked(p1, p2, cid_p2)
    if not blocked:
        print("Not blocked!")
        print("Now on circle {}".format(cid_p2))
        add_path_point(xy = p2, cid = cid_p2, dir_cw = dir_cw_p2)
        distance_from_end = distance(p2, pe)
        if distance_from_end < 0.01:
            print("Made it to end!\n")
        else:
            print("Not at end, continuing path")
            get_route(p2, pe, None, None, offset)
    else:
        if circles[cid_blk].ingrp:
            print("Blocked by group {}".format(circles[cid_blk].grp))
        else:
            print("Blocked by circle {}".format(cid_blk))
        if path[-1].ongrp != True: # not coming from a group
            if circles[cid_blk].ingrp == True: # a group blocks the path
                # can go around the group on either side
                pa, dir_cw, cid_blk = aimpoint_on_group_cw_or_ccw(p1, p2, \
                                      cid_blk, offset)
                pax, pay = round(pa[0], 2), round(pa[1],2)
                print("New aimpoint: {}, {} on circle {}".format(pax, pay, cid_blk))
                get_route(p1, pa, cid_blk, dir_cw, offset)
            else:
                # can go around the circle on either side
                pa, dir_cw = aimpoint_on_circle_cw_or_ccw(p1, p2, cid_blk, offset)
                pax, pay = round(pa[0], 2), round(pa[1],2)
                print("New aimpoint: {}, {} on circle {}".format(pax, pay, cid_blk))
                get_route(p1, pa, cid_blk, dir_cw, offset)
        else: # was coming from a group
            if circles[cid_blk].ingrp: # if the blocking circle is part of a group
                group_blocking = circles[cid_blk].grp
                group_current = circles[path[-1].cid].grp
                if group_blocking != group_current: # changing groups
                    pa, dir_cw, cid_blk = aimpoint_on_group_cw_or_ccw(p1, p2, \
                                          cid_blk, offset) # both directions ok
                    pax, pay = round(pa[0], 2), round(pa[1],2)
                    print("New aimpoint: {}, {} on circle {}".format(pax, pay, cid_blk))
                    get_route(p1, pa, cid_blk, dir_cw, offset)
                else: # continue navigating around same group, direction limited
                    if path[-1].dir_cw == True:
                        direc = "CCW"
                    else:
                        direc = "CW"
                    print("Navigating {} around group {}".format(direc, group_current))
                    if path[-1].dir_cw == True:
                        pa, dir_cw, cid_blk = aimpoint_on_group_cw(p1, p2, \
                                              cid_blk, offset)
                    else:
                        pa, dir_cw, cid_blk = aimpoint_on_group_ccw(p1, p2, \
                                              cid_blk, offset)
                    pax, pay = round(pa[0], 2), round(pa[1],2)
                    print("New aimpoint: {}, {} on circle {}".format(pax, pay, cid_blk))
                    get_route(p1, pa, cid_blk, dir_cw, offset)
            else:
                # blocking circle is not part of a group
                pa, dir_cw = aimpoint_on_circle_cw_or_ccw(p1, p2, cid_blk, offset)
                pax, pay = round(pa[0], 2), round(pa[1],2)
                print("New aimpoint: {}, {} on circle {}".format(pax, pay, cid_blk))
                get_route(p1, pa, cid_blk, dir_cw, offset)

def find_route_length(point_list):
    ''' finds length of the route '''
    num_pts = len(point_list)
    route_length = 0
    for i in range(num_pts-1):
        route_length += distance(point_list[i], point_list[i+1])
    return route_length

def add_path_point(xy, cid, dir_cw):
    ''' adds a point to the path object, xy is location tuple and cid is the
    circle the point is on '''
    if cid != None:
        ongrp = circles[cid].ingrp
    else:
        ongrp = False
    if len(path) == 0:
        dir_cw = None
    else:
        dir_cw = dir_cw
    pt = pathObject(xy = xy, cid = cid, ongrp = ongrp, dir_cw = dir_cw)
    path.append(pt)

def get_path_points(list_path_objects):
    ''' pulls the xy tuples out of path for plotting '''
    plist = []
    for p in list_path_objects:
        plist.append(p.xy)
    return plist

def determine_touching_circles(circles):
    ''' determines which circles are touching and populates their object'''
    nc = len(circles) # number of circles
    for i in range(nc):
        xy_i, r_i  = circles[i].xy, circles[i].r
        for j in range(nc):
            if j != i:
                xy_j, r_j  = circles[j].xy, circles[j].r
                if distance(xy_i, xy_j) <= (r_i + r_j):
                    circles[i].tch.append(j)
    return circles

def append_tchlist(cid, group, circles):
    ''' appends touch list of circle cid and calls itself recursively'''
    tchlist = circles[cid].tch
    for tch in tchlist:
        if tch not in group:
            group.append(tch)
            append_tchlist(tch, group, circles) # call recursively

def make_circle_groups(circles):
    ''' makes groups of those circles that touch other circles '''
    circles_in_groups = []
    groups = []
    nc = len(circles)
    for i in range(nc):
        group = []
        if circles[i].tch and i not in circles_in_groups:
            group.append(i)
            append_tchlist(i, group, circles)
            circles_in_groups += group
            groups.append(group)
    return groups

def add_groups_to_circles(groups, circles):
    ''' if a circle is a member of a group, add the group list to its object '''
    for circle in circles:
        for group in groups:
            if circle.cid in group:
                circle.ingrp = True
                circle.grp = group
    return circles

def route_start_and_end_random(fc, fl, fract_fl, circ_max_rad):
    ''' randomly defines the route start and end points using fc (field center),
        fsl (field side length), fract_fsl (the fraction of the fsl that will
        set the radius of the pt from the fc), and obs_mad_rad (obstacle maximum
        radius that will be used to see if the generated point is too close to
        an obstacle '''
    pts_assigned = False
    while not pts_assigned:
        r = (1 + (random() - 0.5) / 5.) * fract_fl * fl / 2. # radius
        angle_start = random() * 2 * pi # angle
        angle_end = angle_start + pi + (random() - 0.5) * pi / 2.
        pt_s = (r * cos(angle_start) + fc[0], r * sin(angle_start) + fc[1])
        pt_e = (r * cos(angle_end) + fc[0], r * sin(angle_end) + fc[1])
        one_too_close = False
        for i in range(len(circles)):
            xy_i = circles[i].xy
            if distance(pt_s, xy_i) <= circ_max_rad:
                one_too_close = True
            if distance(pt_e, xy_i) <= circ_max_rad:
                one_too_close = True
        if not one_too_close:
            pts_assigned = True
    return pt_s, pt_e

def make_field_of_circles_random(num_circ, rad_mnmx, fc, fl, set_seed, r_seed):
    ''' makes a field of circles and randomly assigns locations
        num_circ is the number of circles, rad_mnmx is a tuple with the min and
        maximum radius ranges, fl is the field length, set_seed is a Boolean
        True if the seed will be set, and r_seed is an int'''
    circles = []
    if set_seed:
        seed(r_seed)
    rad_min, rad_rng = rad_mnmx[0], rad_mnmx[1] - rad_mnmx[0]
    for i in range(num_circ):
        x = round((random() - 0.5) * fl, 2) + fc[0]
        y = round((random() - 0.5) * fl, 2) + fc[1]
        r = round(rad_min + random() * rad_rng, 2)
        circles.append(circleObject(cid = i, xy = (x, y), r = r, tch = [], \
                                    ingrp = False, grp = []))
    circles = determine_touching_circles(circles)
    groups = make_circle_groups(circles)
    circles = add_groups_to_circles(groups, circles)
    return circles

def make_field_of_circles_manually():
    ''' makes a field of circles, at time manually, later will add randomly '''
    circles = []
    circles.append(circleObject(cid = 0, xy = (  90, -100), r = 300, tch = [], \
                  ingrp = False, grp = []))
    circles.append(circleObject(cid = 1, xy = ( 300,  400), r = 200, tch = [], \
                  ingrp = False, grp = []))
    circles.append(circleObject(cid = 2, xy = ( 250,  400), r = 100, tch = [], \
                  ingrp = False, grp = []))
    circles.append(circleObject(cid = 3, xy = ( 100,  400), r =  50, tch = [], \
                  ingrp = False, grp = []))
    circles.append(circleObject(cid = 4, xy = (-200,    0), r =  25, tch = [], \
                  ingrp = False, grp = []))
    circles.append(circleObject(cid = 5, xy = (-575, -400), r = 100, tch = [], \
                  ingrp = False, grp = []))
    circles.append(circleObject(cid = 6, xy = ( 800,  800), r =  25, tch = [], \
                  ingrp = False, grp = []))
    circles.append(circleObject(cid = 7, xy = (-800, -800), r =  25, tch = [], \
                  ingrp = False, grp = []))
    circles.append(circleObject(cid = 8, xy = ( 500,  250), r = 100, tch = [], \
                  ingrp = False, grp = []))
    circles = determine_touching_circles(circles)
    groups = make_circle_groups(circles)
    circles = add_groups_to_circles(groups, circles)
    return circles


if __name__ == '__main__':
    global circles, path, pe # used in many places by recursive functions

    # inputs
    # assign mannually
    # circles = make_field_of_circles_manually() # define in method above for now
    # ps, pe = ( 750, 750), (-750, -750)  # start point and end point
    # random assignment
    os.system('clear') 
    inp = input('Go? (y or n): ')
    while inp == 'y':
        nc = 50 # number of circles
        rad_mnmx = (15, 150) #radius minimum, maximum
        fc = (0, 0) # field center
        fl = 2000 # field length
        fract_fl = 1 # sets radius of start, stop points
        set_seed, r_seed = False, 1
        circles = make_field_of_circles_random(nc, rad_mnmx, fc, fl, set_seed, r_seed)
        ps, pe = route_start_and_end_random(fc, fl, fract_fl, rad_mnmx[1])

        # used whether manual or random
        offset = 1 # slightly offset aimpoint locations from edge of circles

        # calculations
        path = [] # initialize
        add_path_point(xy = ps, cid = None, dir_cw = None) # add start
        # forward
        print("Starting path forward")
        get_route(p1 = ps, p2 = pe, cid_p2 = None, dir_cw_p2 = None, offset = offset)
        path_forward = path # ran from start to end
        path_forward_points_list = get_path_points(path_forward) # points
        dist_for = find_route_length(path_forward_points_list)
        # backward
        print("Starting path backward")
        ps, pe = pe, ps # reversed
        path = []
        add_path_point(xy = ps, cid = None, dir_cw = None) # start with end
        get_route(p1 = ps, p2 = pe, cid_p2 = None, dir_cw_p2 = None, offset = offset)
        path_backward = path # ran from start to end
        path_backward_points_list = get_path_points(path_backward) # points
        dist_back = find_route_length(path_backward_points_list)
        print("Comparison of distances:")
        print("Forward: {}, backward {}".format(round(dist_for, 2), round(dist_back,2)))
        if dist_for <= dist_back:
            print("Forward the shortest")
            path_points = path_forward_points_list
            ps, pe = pe, ps
        else:
            print("Backward the shortest")
            path_points = path_backward_points_list

        # plotting
        plot_pointlist([ps],'ko') # start point
        plot_pointlist([pe],'ko') # end point
        plot_pointlist([ps, pe], 'g--') # perfect route
        plot_path(path_points, 'b+-') # actual route
        plot_circles()
        print("\n")
        os.system('clear') 
        inp = input('Go? (y or n): ')
