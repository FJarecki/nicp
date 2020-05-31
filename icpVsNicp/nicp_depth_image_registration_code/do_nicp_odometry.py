from scipy.spatial.transform import Rotation as R

data = []

def read_from_file():
    coord_system = []
    with open('nicp_transitions.txt') as f:
        for line in f:
            iter = -1
            for i in range(len(line)):
                if line[i] == ' ':
                    coord_system.append(float(line[iter+1:i]))
                    iter = i
            coord_system.append(float(line[iter+1:i]))
            data.append(coord_system)
            coord_system = []
        

def save_to_file():
    data_to_txt_list = []
    for iter in range(len(data)):
        print(data[iter][0:3])
        r = R.from_matrix([data[iter][0:3], data[iter][3:6], data[iter][6:9]])
        print(r.as_quat())
        print(r.as_quat()[3])
        print(data[iter])
        data_to_txt_list.append(str(iter) + " " + str(data[iter][9]) + " " +
                            str(data[iter][10]) + " " + str(data[iter][11]) + 
                            " " + str(r.as_quat()[0]) + " " + str(r.as_quat()[1]) + " " + str(r.as_quat()[2]) + " " + str(r.as_quat()[3]))
        
                
    with open("nicp_transitions_calc.txt", "w") as output:
        for i in data_to_txt_list:
            output.write(str(i) + "\n")
        


read_from_file()
save_to_file()
