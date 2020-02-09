
def normalize_homography(w, h):

    rot = Rotation.from_euler('xyz', np.array([theta, 0, 0]), degrees=True)
    R = rot.as_dcm()
    R[0][2] = -cx
    R[1][2] = -cy 
    R[2][2] = fy

    w_def = np.float32([[0],[w],[1]])

    homography = np.dot(np.linalg.inv(f), w_def)
    s = np.dot(np.linalg.inv(R), homography)[2]
    x = np.dot(np.linalg.inv(R), homography) / s

    return 2*(-x[0]) + w, x[1]


def normalize_screen_coordinates(X, w, h): 
    assert X.shape[-1] == 2
    
    x = X
    w_x, w_y = normalize_homography(w, h)
    x[0] = (w_x - w) / 2 + X[0]  

    # Normalize so that [0, w] is mapped to [-1, 1], while preserving the aspect ratio
    if h > w:
        return X/w*2 - [1, h/w]
    else:
        return X/h*2 - [w/h, 1]

    if w_x > w_y:
        return x/w_x*2 - [1, w_y/w_x]
    else:
        return x/w_y*2 - [w_x/w_y, 1]
