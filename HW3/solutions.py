import numpy as np
from scipy.spatial.transform import Rotation as Rot

class Pose3D:
    def __init__(self, position, rotation):
        # translation from the inertial frame to this frame
        self.translation = np \
            .asarray(position, dtype=float) \
            .reshape(3)
        
        # rotation from the inertial frame to this frame
        self.rotation = np \
            .asarray(rotation, dtype=float) \
            .reshape(3, 3)

    def to_matrix(self):
        transform = np.eye(4)
        transform[:3, :3] = self.rotation
        transform[:3, 3] = self.translation
        return transform
    
def frame_to_frame(pose1, pose2):
    T1 = pose1.to_matrix()
    T2 = pose2.to_matrix()
    
    # https://numpy.org/doc/stable/reference/generated/numpy.matmul.html
    # huh, neat
    return np.linalg.inv(T2) @ T1
    
def test_case_1():
    # translation only
    f1 = Pose3D([1, 0, 0], np.eye(3))
    f2 = Pose3D([3, 0, 0], np.eye(3))
    T = frame_to_frame(f1, f2)

    p_in_f1 = np.array([0, 0, 0, 1])
    p_in_f2 = T @ p_in_f1
    print([int(x) for x in p_in_f2]) # [-2, 0, 0, 1]

    assert np.allclose(p_in_f2, [-2, 0, 0, 1])
    
def test_case_2():
    # translation and rotation
    f1 = Pose3D([1, 0, 0], np.eye(3))
    f2 = Pose3D([3, 0, 0], Rot.from_euler('z', 90, degrees=True).as_matrix())
    T = frame_to_frame(f1, f2)
    
    p_in_f1 = np.array([0, 0, 0, 1])
    p_in_f2 = T @ p_in_f1
    print([int(x) for x in p_in_f2]) # [0, 2, 0, 1]
    
    assert np.allclose(p_in_f2, [0, 2, 0, 1])

def main():
    test_case_1()
    test_case_2()

if __name__ == "__main__":
    main()
