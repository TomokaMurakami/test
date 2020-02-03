
from scipy.spatial.transform import Rotation

def homography(X, w, h):
    assert w == h

    width = w
    rate = width / 1000
    fx = 1145.0494384765625 * rate
    fy = 1143.7811279296875 * rate
    cx = 512.54150390625 * rate
    cy = 515.4514770507812 * rate
    crop_center = 730-540
    f = 1.05963144e+03
    theta = 116.28579489613153 - 102 + np.degrees(np.arctan(crop_center / f))
    p_trans = np.float32([[[0],[0],[1]],
                    [[width],[0],[1]],
                    [[0],[width],[1]],
                    [[width],[width],[1]]])
    f = [[fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]]

    rot = Rotation.from_euler('xyz', np.array([theta, 0, 0]), degrees=True)
    R = rot.as_dcm()
    R[0][2] = -cx
    R[1][2] = -cy 
    R[2][2] = fy

    for i in range(X.shape[0]): 
        kps = np.append(X[i], np.ones((X.shape[1],1)), axis=1)

        homography = np.dot(np.linalg.inv(f), kps.T)
        s = np.dot(np.linalg.inv(R), homography)[2]
        x = np.dot(np.linalg.inv(R), homography) / s
        
        x = np.delete(x, 2, axis=0)
        X[i] = x.T
    
    return X
