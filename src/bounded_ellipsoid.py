import numpy as np

def cos_vecs(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 0.01)

def iter_foci(pt_average, pts):
    _pts_search_animations = []
    vec_foci = pt_average * 0

    pts_len = len(pts)
    for i in range(pts_len * 2):
        idx = i % pts_len
        pt_cur = pts[idx]
        vec_cur = pt_cur - pt_average

        cos = cos_vecs(vec_foci, vec_cur)
        if cos < 0:
            vec_cur *= -1
        vec_foci += (vec_cur - vec_foci) / pts_len
        
        _pts_search_animations += [[pt_cur, np.copy(vec_foci)]]

    return vec_foci, _pts_search_animations


def find_ellipsoid(pts_cloud_orig):    
    pts = np.copy(pts_cloud_orig)
    np.random.shuffle(pts) # seems requred?
    
    pt_average =  np.sum(pts, axis = 0) / len(pts)
    
    vec_foci, _pts_search_animations = iter_foci(pt_average, pts)
    # vec_foci, _pts_search_animations = iter_foci(pt_average, np.flip(np.copy(pts)))
    # vec_foci = (vec_foci1 + vec_foci2) / 2
    
    foci_1 = pt_average + vec_foci
    foci_2 = pt_average - vec_foci

    string_pro_calc = 0
    for pt_cur in pts:
        cur_pt_radius = np.linalg.norm(pt_cur - foci_1) + np.linalg.norm(pt_cur - foci_2)
        string_pro_calc = max(string_pro_calc, cur_pt_radius)

    return foci_1, foci_2, string_pro_calc, _pts_search_animations