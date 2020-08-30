# Code is Python 2

from UAV_helper import circleObject, pathObject
import matplotlib.pyplot as plt
from math import sqrt, cos, sin, tan, acos, asin, atan2, degrees, pi
from random import random, seed, sample
import numpy as np
import pandas as pd
import sys
import csv


def plot_pointlist(plist, desig):
    ''' plots point list (each pt is an x, y tuple) with designated format '''
    x, y = [p[0] for p in plist], [p[1] for p in plist]
    plt.plot(x, y, desig)

def plot_pointlist_narrow_line(plist, desig):
    ''' plots point list (each pt is an x, y tuple) with designated format '''
    x, y = [p[0] for p in plist], [p[1] for p in plist]
    plt.plot(x, y, desig, linewidth = 0.2)


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
    for i in xrange(nc):
        xy, r = circles[i].xy, circles[i].r
        x, y = xy[0], xy[1]
        circs.append(plt.Circle(xy, r, color='b'))
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
    #plt.xlim(xmin, xmax)
    #plt.ylim(ymin, ymax)
    # plt.axes().set_aspect('equal')
    plt.xlabel('x'); plt.ylabel('y')
    fig = plt.gcf()
    plt.rcParams["figure.figsize"] = [10.0, 10.0]
    # plt.grid()
    plt.show()

def plot_circles_2():
    nc = len(circles)
    na = 101
    angs = np.linspace(0, 2 * pi, na)
    for i in xrange(nc):
        xy_clist = []
        cent_xy, r = circles[i].xy, circles[i].r
        cx, cy = cent_xy[0], cent_xy[1]
        for ang in angs:
            xy = (r * cos(ang) + cx, r * sin(ang) + cy)
            xy_clist.append(xy)
        plot_pointlist(xy_clist, 'r-')
    #for i in xrange(nc):
    #    x, y = circles[i].xy[0], circles[i].xy[1]
    #    plt.text(x, y, str(circles[i].cid))
    #plt.xlabel('longitude (deg)')
    #plt.ylabel('latitude (deg)')
    #plt.axes().set_aspect('equal')

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
    denom = (LA * LB)
    if denom == 0:
        denom = 1e-6
    val = AdotB / denom
    if abs(val) > 1:
        sgn = val/abs(val)
        val = sgn * 1
    theta = abs(acos(val))
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
                # print "Circle {} is on the line".format(circle.cid)
                circle_in_front_p1 = check_circle_in_front_of_p1(p1, p2, circle)
                if circle_in_front_p1:
                    # print "Circle {} is in front of p1".format(circle.cid)
                    circle_not_behind_p2 = check_circle_not_behind_p2(p1, p2, circle)
                    if circle_not_behind_p2:
                        # print "Circle {} is not behind p2".format(circle.cid)
                        blocking_cids.append(circle.cid)
                        blocked = True
    if blocked:
        # print "It's blocked, and the blocking cids are {}".format(blocking_cids)
        cid_nearest = find_nearest_circle(p1, blocking_cids)
        # print "Circle {} is the nearest".format(circles[cid_nearest].cid)
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
    global rc
    rc += 1
    if rc < 100: # limit the number of calls to this function
        p1x,p1y,p2x,p2y = round(p1[0],2), round(p1[1],2), round(p2[0],2), round(p2[1],2)
        blocked, cid_blk = check_if_blocked(p1, p2, cid_p2)
        if not blocked:
            add_path_point(xy = p2, cid = cid_p2, dir_cw = dir_cw_p2)
            distance_from_end = distance(p2, pe)
            if distance_from_end < 1e-6:
                #print "Made it to end!\n"
                dummy = 0
            else:
                get_route(p2, pe, None, None, offset)
        else:
            if path[-1].ongrp != True: # not coming from a group
                if circles[cid_blk].ingrp == True: # a group blocks the path
                    # can go around the group on either side
                    pa, dir_cw, cid_blk = aimpoint_on_group_cw_or_ccw(p1, p2, \
                                          cid_blk, offset)
                    pax, pay = round(pa[0], 2), round(pa[1],2)
                    get_route(p1, pa, cid_blk, dir_cw, offset)
                else:
                    # can go around the circle on either side
                    pa, dir_cw = aimpoint_on_circle_cw_or_ccw(p1, p2, cid_blk, offset)
                    pax, pay = round(pa[0], 2), round(pa[1],2)
                    get_route(p1, pa, cid_blk, dir_cw, offset)
            else: # was coming from a group
                if circles[cid_blk].ingrp: # if the blocking circle is part of a group
                    group_blocking = circles[cid_blk].grp
                    group_current = circles[path[-1].cid].grp
                    if group_blocking != group_current: # changing groups
                        pa, dir_cw, cid_blk = aimpoint_on_group_cw_or_ccw(p1, p2, \
                                              cid_blk, offset) # both directions ok
                        pax, pay = round(pa[0], 2), round(pa[1],2)
                        get_route(p1, pa, cid_blk, dir_cw, offset)
                    else: # continue navigating around same group, direction limited
                        if path[-1].dir_cw == True:
                            direc = "CCW"
                        else:
                            direc = "CW"
                        if path[-1].dir_cw == True:
                            pa, dir_cw, cid_blk = aimpoint_on_group_cw(p1, p2, \
                                                  cid_blk, offset)
                        else:
                            pa, dir_cw, cid_blk = aimpoint_on_group_ccw(p1, p2, \
                                                  cid_blk, offset)
                        pax, pay = round(pa[0], 2), round(pa[1],2)
                        get_route(p1, pa, cid_blk, dir_cw, offset)
                else:
                    # blocking circle is not part of a group
                    pa, dir_cw = aimpoint_on_circle_cw_or_ccw(p1, p2, cid_blk, offset)
                    pax, pay = round(pa[0], 2), round(pa[1],2)
                    get_route(p1, pa, cid_blk, dir_cw, offset)

def find_route_length(point_list):
    ''' finds length of the route '''
    num_pts = len(point_list)
    route_length = 0
    for i in xrange(num_pts-1):
        p1, p2 = point_list[i], point_list[i+1]
        del_lng = (p2[0] - p1[0]) * 280163 # ft
        del_lat = (p2[1] - p1[1]) * 364286 # ft
        dist = sqrt(del_lng**2 + del_lat**2)
        route_length += dist
    return route_length / 5280.0 # route length in miles

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
    for i in xrange(nc):
        xy_i, r_i  = circles[i].xy, circles[i].r
        for j in xrange(nc):
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
    for i in xrange(nc):
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

def merge_all_df(df_skyscrapers, df_govbuildings, df_heliports, df_publicspaces, \
                 df_schools):
    ''' merges all no fly zones into one dataframe '''
    frames = [df_skyscrapers, df_govbuildings, df_heliports, df_publicspaces, \
              df_schools]
    return pd.concat(frames)

def create_circleslist(df):
    ''' create a list of circleObjects that represent no-fly zones from data
        frame '''
    circles = []
    for i in xrange(len(df)):
        xy = (df['longitude'].iloc[i], df['latitude'].iloc[i])
        r = df['radius_ll'].iloc[i]
        circles.append(circleObject(cid = i, xy = xy, r = r, tch = [], \
                       ingrp = False, grp = []))
    circles = determine_touching_circles(circles)
    groups = make_circle_groups(circles)
    circles = add_groups_to_circles(groups, circles)
    return circles

def export_path_points(path_points):
    ''' will export path points out to make a video '''
    out = csv.writer(open("path_points.csv","w"), delimiter=',', \
                     quoting=csv.QUOTE_MINIMAL)
    for ppt in path_points:
        out.writerow(ppt)

def adjust_one_pt_with_other_const(xy_const, cent_adj, xy_adj):
    ''' rotates one point holding other constant in an attempt to get it tangent
        to the circle '''
    # first find direction of rotation needed
    v_con_centadj = vector_from_two_pts(xy_const, cent_adj)
    v_con_xyadj = vector_from_two_pts(xy_const, xy_adj)
    sgn = round(angle_btw_two_vectors(v_con_centadj, v_con_xyadj) / \
          (abs(angle_btw_two_vectors(v_con_centadj, v_con_xyadj) + 1e-6)),1)
    # now find the angle that, when tangent, will be pi / 2
    vc = vector_from_two_pts(xy_adj, cent_adj)
    vp = vector_from_two_pts(xy_adj, xy_const)
    ang = abs(angle_btw_two_vectors(vc, vp))
    ang_r = pi / 2. - ang 
    v_cxy = vector_from_two_pts(cent_adj, xy_adj)
    v_cxy_r = rotate_about_z_axis(v_cxy, sgn*ang_r)
    xy_adj_new = (cent_adj[0] + v_cxy_r[0], cent_adj[1] + v_cxy_r[1])
    return xy_adj_new

def correct_tan_pts(p_p1, p_p2, crit, correct_path):
    ''' finds the correct tan pts from approximate tan pts, crit is
        how much it can be off from the desired pi / 2 in radians '''
    c1_xy0, c2_xy0 = p_p1.xy, p_p2.xy
    c1_cid, c2_cid = p_p1.cid, p_p2.cid
    if c1_cid != None:
        c1_cent = circles[c1_cid].xy
        c1_r = circles[c1_cid].r
    if c2_cid != None:
        c2_cent = circles[c2_cid].xy
        c2_r = circles[c2_cid].r
    if c1_cid == None: # only adjust p2
        correct_path.append([c1_xy0, c1_cid])
        c2_xy = adjust_one_pt_with_other_const(c1_xy0, c2_cent, c2_xy0) 
        correct_path.append([c2_xy, c2_cid])
    if c2_cid == None: # only adjust p1
        c1_xy = adjust_one_pt_with_other_const(c2_xy0, c1_cent, c1_xy0)
        correct_path.append([c1_xy, c1_cid])
        correct_path.append([c2_xy0, c2_cid])
    # both points need to be adjusted
    if (c1_cid != None and c2_cid != None):
        c1_xy, c2_xy = c1_xy0, c2_xy0
        p1_not_tangent = True
        while p1_not_tangent:
            # adjust point 1
            c1_xy = adjust_one_pt_with_other_const(c2_xy, c1_cent, c1_xy)
            # adjust point 2
            c2_xy = adjust_one_pt_with_other_const(c1_xy, c2_cent, c2_xy)
            # check point 1's new angle
            vc = vector_from_two_pts(c1_xy, c1_cent)
            vp = vector_from_two_pts(c1_xy, c2_xy)
            ang = abs(angle_btw_two_vectors(vc, vp))
            ang_r = abs(pi / 2. - ang)
            if ang_r < crit:
                p1_not_tangent = False
        correct_path.append([c1_xy, c1_cid])
        correct_path.append([c2_xy, c2_cid])

def path_with_correct_tanpts(crit):
    ''' returns entire path with correct tangent points, crit is allowable
        angular error in tangent pt'''
    path_correct_tan = []
    for i in xrange(len(path)-1):
        path1 = path[i]
        path2 = path[i+1]
        correct_tan_pts(path1, path2, crit, path_correct_tan) 
    return path_correct_tan

def make_arc_p1_to_p2(p1, p2, pc, delang):
    ''' makes an arc from p1 to p2 at every delang '''
    arcpath = []
    v_c1 = vector_from_two_pts(pc, p1) 
    v_c2 = vector_from_two_pts(pc, p2)
    ang_p1top2 = angle_btw_two_vectors(v_c1, v_c2)
    sgn = ang_p1top2 / abs(ang_p1top2)
    if abs(ang_p1top2) > delang:
        na = int(abs(ang_p1top2)/delang) - 1 # number of angles
        for i in xrange(na):
            ang_r = (i + 1) * sgn * delang
            v_c1_r = rotate_about_z_axis(v_c1, ang_r)
            p_arc = (pc[0] + v_c1_r[0], pc[1] + v_c1_r[1])
            arcpath.append(p_arc)
    return arcpath    

def smoothe_path(path_corrected, delang):
    ''' returns path with arcs filled between tangent points at angular 
        discretization, delang '''
    path_smoothed = []    
    for i in xrange(len(path_corrected)-1):
        p1, cid1 = path_corrected[i][0], path_corrected[i][1]
        p2, cid2 = path_corrected[i+1][0], path_corrected[i+1][1]
        path_smoothed.append(p1)
        if cid2 != cid1:
            path_smoothed.append(p2)
        else: # on the same arc
            pc = circles[cid1].xy
            arcpath = make_arc_p1_to_p2(p1, p2, pc, delang)
            for pt in arcpath:
                path_smoothed.append(pt)
    return path_smoothed

if __name__ == '__main__':
    global circles, path, pe, rc # used in many places by recursive functions
    
    # read in circles (no-fly zones) 
    df_skyscrapers = pd.read_csv('../simulation_data/db_skyscrapers_250.csv')
    df_govbuildings = pd.read_csv('../simulation_data/db_government_buildings.csv')
    df_heliports = pd.read_csv('../simulation_data/db_heliports.csv')
    df_publicspaces = pd.read_csv('../simulation_data/db_publicspaces.csv')
    df_schools = pd.read_csv('../simulation_data/db_schools.csv')
    # make into one dataframe
    df_circles = merge_all_df(df_skyscrapers, df_govbuildings, df_heliports, \
                             df_publicspaces, df_schools)
    # create list of circleObjects
    circles = create_circleslist(df_circles)
    # read in addresses 
    df_addresses = pd.read_csv('../simulation_data/db_addresses.csv')
    num_addresses = df_addresses.shape[0]
    address_list = []
    for i in xrange(num_addresses):
        lng = df_addresses['longitude'].iloc[i]
        lat = df_addresses['latitude'].iloc[i]
        address_list.append((lng, lat))
    del df_addresses 
    print "Done making address list."
    address_nifz = []
    for i in xrange(num_addresses):
        axy = address_list[i]
        in_nflz = False
        for circle in circles:
            cxy = circle.xy
            cr = circle.r
            if distance(axy, cxy) <= cr:
                in_nflz = True
        if not in_nflz:
            address_nifz.append(axy)
    print "Done screening addresses"
    num_deliveries_per_day = 3500 #14000 # based on UPS data for deliveries & USPS addresses
    lst_rt_dist = []
    lst_dist_st = []
    lst_rt_dist_inc = []
    lst_rt_dist_inc_pc = []
    lst_routes = []
    
    deladdrs = sample(address_nifz, num_deliveries_per_day)
    sa = 0
    for addr in deladdrs:
        ps = (-104.925723, 39.797400)
        sa += 1
        if sa % 50 == 0: print "Simulation {}".format(sa)
        pe = addr
        # route
        offset = 0.00004 # slightly offset (~10 ft) from edge of circles
        #print "Starting path forward"
        path = [] # initialize
        add_path_point(xy = ps, cid = None, dir_cw = None) # add start
        found_path_forward = False
        rc = 0 # initialize recursive counter
        get_route(p1 = ps, p2 = pe, cid_p2 = None, dir_cw_p2 = None, offset = offset)
        # print "There were {} calls going forward".format(rc) 
        if rc < 100:
            found_path_forward = True
            path_forward = path # ran from start to end
            path_forward_points_list = get_path_points(path_forward) # points
            dist_for = find_route_length(path_forward_points_list)
        # backward
        #print "Starting path backward"
        ps, pe = pe, ps # reversed
        path = []
        add_path_point(xy = ps, cid = None, dir_cw = None) # start with end
        found_path_backward = False
        rc = 0
        get_route(p1 = ps, p2 = pe, cid_p2 = None, dir_cw_p2 = None, offset = offset)
        #print "There were {} calls going backward".format(rc)
        if rc < 100:
            found_path_backward = True
            path_backward = path # ran from start to end
            path_backward_points_list = get_path_points(path_backward) # points
            dist_back = find_route_length(path_backward_points_list)
        if found_path_forward and found_path_backward:
            #print "Comparison of distances:"
            #print "Forward: {}, backward {}".format(round(dist_for, 2), round(dist_back,2))
            if dist_for <= dist_back:
                #print "Forward the shortest"
                ps, pe = pe, ps
                path_points = path_forward_points_list
                path = path_forward
                rt_dist = find_route_length(path_forward_points_list)
            else:
                #print "Backward the shortest"
                path_points = path_backward_points_list
                path = path_backward
                rt_dist = find_route_length(path_backward_points_list)
        elif found_path_forward:
            #print "Only found forward"
            path_points = path_forward_points_list
            ps, pe = pe, ps
            path = path_forward
            rt_dist = find_route_length(path_forward_points_list)
        elif found_path_backward:
            #print "Only found backward"
            path_points = path_backward_points_list
            path = path_backward
            rt_dist = find_route_length(path_backward_points_list)
        else:
            print "No solutions, please pick another address"
        
        if found_path_forward or found_path_backward:
            rt_dist_st = find_route_length([ps, pe])
            rt_dist_inc = rt_dist - rt_dist_st
            rt_dist_inc_pc = (rt_dist - rt_dist_st) / rt_dist_st * 100
            lst_rt_dist.append(rt_dist)
            lst_dist_st.append(rt_dist_st)
            lst_rt_dist_inc.append(rt_dist_inc)
            lst_rt_dist_inc_pc.append(rt_dist_inc_pc) 
            #path_corrected = path_with_correct_tanpts(0.017)
            #path_smoothed = smoothe_path(path_corrected, 0.08725)
            lst_routes.append(path_points)

            
            
            #print "The straight distance was {} miles.".format(round(rt_dist_st, 2))
            #print "The actual route was {} miles.".format(round(rt_dist, 2))
            #print "No fly zones caused an increased flight length of {} miles.".format( round(rt_dist_inc, 2))
            #print "This is an increase of {} percent.".format(round(rt_dist_inc_pc,2))
            
            # final smoothed path - not doing smoothed path for system simulation
            # find the correct tan pts
            #path_corrected = path_with_correct_tanpts(0.017)
            # smooth the path 
            #path_smoothed = smoothe_path(path_corrected, 0.08725)
            # export path for video
            # export_path_points(path_smoothed) 
    # values
    np_rt_dist = np.array(lst_rt_dist)
    np_dist_st = np.array(lst_dist_st)
    np_rt_dist_inc = np.array(lst_rt_dist_inc)
    np_rt_dist_inc_pc = np.array(lst_rt_dist_inc_pc)
    rt_dist_ave, rt_dist_std = np_rt_dist.mean(), np_rt_dist.std() 
    dist_st_ave, dist_st_std = np_dist_st.mean(), np_dist_st.std()
    rt_dist_inc_ave, rt_dist_inc_std = np_rt_dist_inc.mean(), np_rt_dist_inc.std() 
    rt_dist_inc_pc_ave, rt_dist_inc_pc_std = np_rt_dist_inc_pc.mean(), \
                                            np_rt_dist_inc_pc.std() 
    print "Straight route length: {} mean,  {} std mile.".format(round(dist_st_ave,2), \
                                              round(dist_st_std,2))
    print "  Actual route length: {} mean,  {} std mile.".format(round(rt_dist_ave,2), \
                                              round(rt_dist_std,2))
    print "   Increase in length: {} mean,  {} std mile.".format(round(rt_dist_inc_ave,2), \
                                              round(rt_dist_inc_std,2))
    print " Increase in % length: {} mean,  {} std.".format(round(rt_dist_inc_pc_ave,2), \
                                              round(rt_dist_inc_pc_std,2))



   
   # plotting
    plt.rcParams.update({'font.size': 16})
    plot_circles_2()
    for route in lst_routes:
        p1, p2 = route[0], route[-1]
        plot_pointlist([p1, p2],'k.') # start and end points
        plot_pointlist_narrow_line(route, 'b-')
        #plot_pointlist(route,'b-')
    plt.xlim(-105.06, -104.90)
    plt.ylim(39.71, 39.80)
    plt.xlabel('longitude (deg)')
    plt.ylabel('latitude (deg)')
    plt.show()
        
        # plot_pointlist(path_points, 'kx-') # rough route
        # plot_circles_2()
