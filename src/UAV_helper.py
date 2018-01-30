# file contains helper classes for UAV_pathing.py

class circleObject():
    '''
    Creates a circle with attributes cid, xy, r, tch, ingrp, grp
    where - 
    cid: circle_id (int)
    xy: center (x, y) position tuple (x and y are floats)
    r: circle radius (float)
    tch: list of overlapping (touching) circle cids (list of ints)
    ingrp: Boolean if circle is in a group of circles (True if any touching)
    grp: list of all circles in the same group (list of ints)
    '''
    def __init__(self, cid, xy, r, tch, ingrp, grp):
        self.cid = cid 
        self.xy = xy  
        self.r = r
        self.tch = tch
        self.ingrp = ingrp
        self.grp = grp

    # for now no methods

class pathObject():
    '''
    Defines a path object that stores information about the taken path
    Attributes are xy, cid, ongrp, dir_cw
    where - 
    xy: (x, y) position tuple of path (floats)
    cid: the cid (int) of the circle that the point is on, None otherwise (start, end)
    ongrp: Boolean indicating if this point is on a group, will be True if 
           circles[cid].ingrp == True
    dir_cw: Boolean, True if this point was the cw aimpoint from the previous point
    '''
    def __init__(self, xy, cid, ongrp, dir_cw):
        self.xy = xy  
        self.cid = cid 
        self.ongrp = ongrp
        self.dir_cw = dir_cw
    # for now no methods





