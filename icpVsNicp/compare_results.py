from math import sqrt, fabs


def compare_euclidian_distance(name):
    groundtruth_matrix = []
    first_el = True
    for line in open("nicp_groundtruth_transition/groundtruth_transition.txt"):
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
    for line in open("nicp_depth_image_registration_code/nicp_transitions_calc.txt"):
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
    
    
    
compare_euclidian_distance("wynik_nicp")
