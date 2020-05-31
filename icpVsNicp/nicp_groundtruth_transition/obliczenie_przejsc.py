import numpy as np
import quaternion
from numpy.linalg import inv
from scipy.spatial.transform import Rotation as R

coordinate_systems = []
transformations = []
data_to_txt_list = []

def read_transformations():
     for line in open("groundtruth.txt"):
        iter = 0
        spaces_iter = 0
        coordinate_system = []
        for i in range(len(line)):
            if line[i] == ' ':
                if spaces_iter > 0:
                    coordinate_system.append(float(line[iter:i]))
                iter = i
                spaces_iter += 1
        coordinate_system.append(float(line[iter+1:-1]))
        coordinate_systems.append(coordinate_system)
        

def parse_to_trans_matrix(position_vector, orientation_quaternion):
    rot_matrix = quaternion.as_rotation_matrix(orientation_quaternion)
    transformation_matrix=np.eye(4)
    transformation_matrix[0:3,0:3]=rot_matrix
    transformation_matrix[0:3,3]=position_vector
    return transformation_matrix


def coordinate_systems_to_trans_matrix():
    for iter in range(len(coordinate_systems)):
        coordinate_systems[iter] = parse_to_trans_matrix(np.asarray(coordinate_systems[iter][0:3]),
                                                         np.quaternion(coordinate_systems[iter][6], coordinate_systems[iter][3], coordinate_systems[iter][4], coordinate_systems[iter][5]))


def calculate_transformations():
    for iter in range(len(coordinate_systems)-1):
        transformations.append(np.dot(inv(coordinate_systems[iter]), coordinate_systems[iter+1]))
        
        
def save_to_file():
    for iter in range(len(transformations)):
        r = R.from_matrix(transformations[iter][0:3, 0:3])
        data_to_txt_list.append(str(iter) + " " + str(transformations[iter][0][3]) + " " +
                            str(transformations[iter][1][3]) + " " + str(transformations[iter][2][3]) + 
                            " " + str(r.as_quat()[0]) + " " + str(r.as_quat()[1]) + " " + str(r.as_quat()[2]) + 
                            " " + str(r.as_quat()[3]))
        
    with open("groundtruth_transition.txt", "w") as output:
        for i in data_to_txt_list:
            output.write(str(i) + "\n")
        
        
read_transformations()
coordinate_systems_to_trans_matrix()
calculate_transformations()
save_to_file()
