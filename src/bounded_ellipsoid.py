import numpy as np
from math import sqrt

def proj_length(v, v_on):
    on_norm = np.linalg.norm(v_on)
    v_len = np.linalg.norm(v)

    projection_len = 0
    rejection_len = 0
    if on_norm > 0.01:
        projection_len = np.dot(v, v_on) / on_norm

        if v_len > abs(projection_len):
            rejection_len = sqrt(v_len**2 - projection_len**2)

    return projection_len, rejection_len

def find_foci(arr_pts):
    # not nessesary for foci calc, just additional animation
    _pts_search_animations = []

    # shuffle to improve main axis search, can be optimized
    pts = np.copy(arr_pts)
    np.random.shuffle(pts)

    pts_len = len(pts)
    pt_average =  np.sum(pts, axis = 0) / pts_len
    
    vec_major = pt_average * 0
    minor_max, major_max = 0, 0
    
    # may be improved with ovelapped pass, 
    # when max calcs are started after delay when axis is less random
    for pt_cur in pts:
        vec_cur = pt_cur - pt_average
        unprojected_len = np.linalg.norm(vec_cur)
        proj_len, rej_len = proj_length(vec_cur, vec_major)

        if proj_len < 0:
            vec_cur = -vec_cur            
        vec_major += (vec_cur - vec_major) / pts_len

        major_max = max(major_max, abs(proj_len))
        minor_max = max(minor_max, rej_len)        
        _pts_search_animations += [[pt_cur, np.copy(vec_major)]]

    # if both very close, may happen
    if major_max < minor_max:
        major_max, minor_max = minor_max, major_max

    vec_major_unit = vec_major / np.linalg.norm(vec_major)
    vec_foci = vec_major_unit * sqrt( major_max**2 - minor_max**2)

    foci_1 = pt_average + vec_foci
    foci_2 = pt_average - vec_foci

    return foci_1, foci_2, _pts_search_animations

def find_ellipsoid(arr_pts):
    foci_1, foci_2, _pts_search_animations = find_foci(arr_pts)
    
    string_pro_calc = 0
    for pt_cur in arr_pts:
        cur_pt_radius = np.linalg.norm(pt_cur - foci_1) + np.linalg.norm(pt_cur - foci_2)
        string_pro_calc = max(string_pro_calc, cur_pt_radius)

    return foci_1, foci_2, string_pro_calc, _pts_search_animations