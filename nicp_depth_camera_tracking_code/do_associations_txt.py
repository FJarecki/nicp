import glob
import cv2
import os
import time
import numpy as np
from scipy.spatial.transform import Rotation as R
import quaternion
from math import sqrt, pow, fabs


def resizing_photos(img_type): #Zmniejszanie zdjec do takich jak u autorow
    str_iter = len(img_type) + 1
    path = img_type + "_zmniejszone"
    for name in glob.glob(img_type + '/*'):
        img = cv2.imread(name)
        resized = cv2.resize(img, (120, 160), interpolation = cv2.INTER_AREA) 
        file_path = os.path.join(path , name[str_iter:])
        cv2.imwrite(file_path, resized)


def straightening_photos(): #Prostowanie zdjęć
    camera_matrix = np.array([[537.4087, 0, 320.3762], [0, 537.4836, 235.9355], [0, 0, 1]])
    dist_vec = np.array([0.0490, -0.1437, 0.0011, 0.0004])
    path = "rgb_wyprostowane"
    for name in glob.glob('rgb/*'):
        img = cv2.imread(name)
        ret = cv2.undistort(img, camera_matrix, dist_vec)
        file_path = os.path.join(path , name[4:])
        cv2.imwrite(file_path, ret)


def depth_txt_creation(): #Tworzenie depth.txt
    depth_names = []
    for name in glob.glob('depth/*'):
        depth_names.append(name)
    depth_names.sort()
    timestamp_list = []
    for line in open("groundtruth.txt"):
        timestamp_list.append(line[0:13])

    assoc_file = open("depth.txt","w")#write mode 
    for iter in range(len(depth_names)):
        assoc_file.write(timestamp_list[iter] + " " + str(depth_names[iter]) + " \n") 
    assoc_file.close()


def rgb_txt_creation(): #Tworzenie rgb.txt
    rgb_names = []
    for name in glob.glob('rgb/*'):
        rgb_names.append(name)
    rgb_names.sort()
    timestamp_list = []
    for line in open("groundtruth.txt"):
        timestamp_list.append(line[0:13])

    assoc_file = open("rgb.txt","w")#write mode 
    for iter in range(len(rgb_names)):
        assoc_file.write(timestamp_list[iter] + " " + str(rgb_names[iter]) + " \n") 
    assoc_file.close()
    
    
def associations_txt_creation(): #Tworzenie associations.txt
    rgb_names = []
    for name in glob.glob('rgb/*'):
        rgb_names.append(name)
    rgb_names.sort()
    depth_names = []
    for name in glob.glob('depth/*'):
        depth_names.append(name)
    depth_names.sort()
    timestamp_list = []
    for line in open("groundtruth.txt"):
        iter = 0
        for i in range(len(line)):
            if line[i] == ' ':
                iter = i
                break
        timestamp_list.append(line[0:iter])
    assoc_file = open("associations.txt","w")#write mode 
    for iter in range(len(rgb_names)):
        assoc_file.write(timestamp_list[iter] + " " + str(depth_names[iter]) + " " + timestamp_list[iter] + " " + str(rgb_names[iter]) + " \n") 
    assoc_file.close()


def compare_img_sizes(): #[ERROR]: image1 - image2 size mismatch in compareDepths -> rozwiazane
    for i in depth_filenames:
        img = cv2.imread(i)
        if img.shape[0] != 480 and img.shape[1] != 640 and img.shape[2] != 3:
            print(img.shape)
    for i in png_filenames:
        img = cv2.imread(i)
        if img.shape[0] != 480 and img.shape[1] != 640 and img.shape[2] != 3:
            print(img.shape)          
            
            
def compare_euclidian_distance(name):
    groundtruth_matrix = []
    first_el = True
    for line in open(name + "/groundtruth.txt"):
        el_list = []
        line_iter = 0
        for i in range(len(line)):
            if line[i] == " ":
                if first_el:
                    el_list.append(line[line_iter:i])
                else:
                    el_list.append(line[line_iter+1:i])
                    first_el = False
                line_iter = i
            if i == len(line) - 1:
                el_list.append(line[line_iter+1:i])
        groundtruth_matrix.append(el_list)
        
    euclidian_list = []
    x_list = []
    y_list = []
    z_list = []
    for i in groundtruth_matrix:
        euclidian_list.append(sqrt(pow(float(i[1]), 2) + pow(float(i[2]), 2)  + pow(float(i[3]), 2)))
        x_list.append(float(i[1]))
        y_list.append(float(i[2]))
        z_list.append(float(i[3]))
        
    odometry_matrix = []
    first_el = True
    for line in open(name + "/nicp_odometry.txt"):
        el_list = []
        line_iter = 0
        for i in range(len(line)):
            if line[i] == " ":
                if first_el:
                    el_list.append(line[line_iter:i])
                else:
                    el_list.append(line[line_iter+1:i])
                    first_el = False
                line_iter = i
            if i == len(line) - 1:
                el_list.append(line[line_iter+1:i])
        odometry_matrix.append(el_list)
        
    euclidian_list_odometry = []
    x_list_odometry = []
    y_list_odometry = []
    z_list_odometry = []
    for i in odometry_matrix:
        euclidian_list_odometry.append(sqrt(pow(float(i[1]), 2) + pow(float(i[2]), 2)  + pow(float(i[3]), 2)))
        x_list_odometry.append(float(i[1]))
        y_list_odometry.append(float(i[2]))
        z_list_odometry.append(float(i[3]))
        
    euclidian_file = open(name + ".txt","w")#write mode     
    for i in range(len(euclidian_list_odometry)):
        eucl_val = fabs(euclidian_list[i] - euclidian_list_odometry[i])
        x_val = fabs(x_list[i] - x_list_odometry[i])
        y_val = fabs(y_list[i] - y_list_odometry[i])
        z_val = fabs(z_list[i] - z_list_odometry[i])
        eucl2_val = sqrt(pow(x_val, 2) + pow(y_val, 2)  + pow(z_val, 2))  
        euclidian_file.write(str(i) +  " " + str(eucl2_val) + " " + str(x_val) + " " + str(y_val) + " " + str(z_val) + " \n") 
        
    euclidian_file.close()

    
def calculate_distance():
    groundtruth_matrix = []
    first_el = True
    for line in open("seq7/groundtruth.txt"):
        el_list = []
        line_iter = 0
        for i in range(len(line)):
            if line[i] == " ":
                if first_el:
                    el_list.append(line[line_iter:i])
                else:
                    el_list.append(line[line_iter+1:i])
                    first_el = False
                line_iter = i
            if i == len(line) - 1:
                el_list.append(line[line_iter+1:i])
        groundtruth_matrix.append(el_list)
        if len(groundtruth_matrix) == 300:
            break
        
    distance = 0.0
    prev_state = (sqrt(pow(float(groundtruth_matrix[0][1]), 2) + pow(float(groundtruth_matrix[0][2]), 2)  + pow(float(groundtruth_matrix[0][3]), 2)))
    dis = 0.0
    for i in groundtruth_matrix:
        dis = sqrt(pow(float(i[1]), 2) + pow(float(i[2]), 2)  + pow(float(i[3]), 2))
        distance += fabs(dis - prev_state)
        prev_state = dis
    print(distance)

compare_euclidian_distance("seq7")
#associations_txt_creation()

print("Done!")
