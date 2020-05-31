import open3d as o3d
import numpy as np
from scipy.spatial.transform import Rotation as Rot
import glob
import time


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      zoom=0.4459,
                                      front=[0.9288, -0.2951, -0.2242],
                                      lookat=[1.6784, 2.0612, 1.4451],
                                      up=[-0.3402, -0.9189, -0.1996])


pinhole_camera_intrinsic = o3d.io.read_pinhole_camera_intrinsic("camera_primesense.json")
data_to_txt_list = []
timestamp_iter = 0
color_images_names = []
depth_images_names = []

def read_photos():
    for name in glob.glob('/home/data_sets/Sequence_2_Kin_2/rgb/*'):
        color_images_names.append(name)
    color_images_names.sort()    
    for name in glob.glob('/home/data_sets/Sequence_2_Kin_2/depth/*'):
        depth_images_names.append(name)
    depth_images_names.sort()

def calc_trans_with_icp(timestamp_iter):
    
    source_color = o3d.io.read_image(color_images_names[timestamp_iter])
    source_depth = o3d.io.read_image(depth_images_names[timestamp_iter])
    target_color = o3d.io.read_image(color_images_names[timestamp_iter+1])
    target_depth = o3d.io.read_image(depth_images_names[timestamp_iter+1])
    
    
                
    source_rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
            source_color, source_depth)
    target_rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
            target_color, target_depth)

    source_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
            source_rgbd_image, pinhole_camera_intrinsic)
    target_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
            target_rgbd_image, pinhole_camera_intrinsic)
    

    threshold = 1
    trans_init = np.asarray([[1.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0]])

    reg_p2p = o3d.registration.registration_icp(source_pcd, target_pcd, threshold)
        
    r = Rot.from_matrix([[0, -1, 0],[1, 0, 0],[0, 0, 1]])
    

    data_to_txt_list.append(str(timestamp_iter) + " " + str(reg_p2p.transformation[0][3]) + " " +
                            str(reg_p2p.transformation[1][3]) + " " + str(reg_p2p.transformation[2][3]) + 
                            " " + str(r.as_quat()[0]) + " " + str(r.as_quat()[1]) + " " + str(r.as_quat()[2]) + 
                            " " + str(r.as_quat()[3]))
    
    

start = time.time()

read_photos()
for i in range(500):
    calc_trans_with_icp(timestamp_iter)
    timestamp_iter += 1
    print(timestamp_iter)


with open("file.txt", "w") as output:
    for i in data_to_txt_list:
        output.write(str(i) + "\n")
        
total_time = time.time() - start
print("Czas obliczen wyniosl: ", total_time, "sekund")

