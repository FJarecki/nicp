import numpy as np
import glob
import matplotlib.pyplot as plt
import os 

class cProcessData(object):
    
    def __init__(self):
        print('Initialization datasets')
        self.processed_datasets = self.__load_datasets()
        #self.processed_datasets = self.__process_datasets(datasets)
        self.minimal_error = None
        self.maximal_error = None
        self.min_max_errors = self.find_min_max_errors(self.processed_datasets)
    
    def __load_datasets(self):
        datasets = dict()
        for name in glob.glob('dataset/*'):
             name_copy = name.replace('dataset/', '')
             name_copy = name_copy.replace('.txt', '')
             print(name_copy)
             datasets[name_copy] = np.genfromtxt(name, delimiter=' ')
        return datasets
    def get_min_max_errors(self):
        return self.min_max_errors 
    
    def find_min_max_errors(self,datasets):
        min_max_errors = dict()
        min_error = None
        max_error = None
        for data_name, data in datasets.items():
            print('dn', data_name)

            for checker_iter, line in enumerate(data):
                line_iter, x_err, y_err, z_err, euc_err = line[0], line[1], line[2], line[3], line[4]
                if(min_error is None):
                    min_error = np.min([x_err, y_err, z_err])
                elif(x_err < min_error or y_err < min_error or z_err < min_error):
                    min_error = np.min([x_err, y_err, z_err])
                if(max_error is None):
                    max_error = np.max([x_err, y_err, z_err])
                elif(x_err > max_error or y_err > max_error or z_err > max_error):
                    max_error = np.max([x_err, y_err, z_err])
                #if(checker_iter != line_iter):
                #    print('Warning, there is an skipped line in dataset')
            min_max_errors[data_name] = np.array([min_error, max_error])
            min_error = None
            max_error = None
        return min_max_errors
                
    def __process_datasets(self, datasets):
        processed_datasets = []
        for data_name, data in datasets.items():
            print(data_name)
            errors_dataset = np.empty(data.shape)
            for checker_iter, line in enumerate(data):
                line_iter, x_err, y_err, z_err, euc_err = line[0], line[1], line[2], line[3], line[4]
                if(checker_iter != line_iter):
                    print('Warning, there is an skipped line in dataset')
                errors_dataset[checker_iter] = np.array([line_iter, x_err, y_err, z_err, euc_err])
            processed_datasets.append(errors_dataset)
        return processed_datasets
            
    def get_processed_datasets(self):
        return self.processed_datasets

class cPlotDataset(object):
    
    def __init__(self):
        print('Initialization charts')
        #number_of_rows = 3
        #number_of_columns = 1
        self.max_samples = 300 #set None for no limit
        
        
    def multiplot(self, rows, columns, dataset, labels, scaled_min_max= None):
        if not os.path.exists('results'):
            os.mkdir('results')
        for data_name, data in dataset.items():
            fig, axs = plt.subplots(rows, columns, sharey=False, tight_layout=True)
            min_max_val = scaled_min_max[data_name]
            fig.subplots_adjust(left=0.15, top=0.99)
            if(self.max_samples is not None):
                data = data[:self.max_samples,:]
            number_of_plots = rows * columns
            number_of_dataset_columns = data.shape[1]
            number_of_samples = data.shape[0]
            
            #if(number_of_dataset_columns == number_of_plots):
            #    for plot_number in range(number_of_plots):
            #        axs[plot_number].scatter(range(number_of_samples), data[:, plot_number])
            #    plt.show()
            #else:
            try:
                print('Skipping first column')
                for plot_number in range(number_of_plots):
                    x_label, y_label = labels[plot_number]
                    next_x_label, next_y_label = labels[(plot_number+1)%number_of_plots]
                    axs[plot_number].scatter(range(number_of_samples), data[:, (plot_number+1)%rows+1])
                    if(next_x_label != x_label or plot_number == number_of_plots-1):
                        axs[plot_number].set_xlabel(x_label)
                    else:
                        pass
                        
                    axs[plot_number].set_ylabel(y_label)
                    axs[plot_number].grid()
                    if(scaled_min_max is not None):
                        axs[plot_number].set_ylim(min_max_val) 
                #plt.show()
                print(os.path.join('results',data_name))
                fig.suptitle('Error in dataset: ' + data_name, y=1.05)
                fig.savefig(os.path.join('results',data_name), bbox_inches="tight",dpi=300)
            except:
                print('Falsed')
                    
if __name__ == "__main__":
    # execute only if run as a script
    error_data = cProcessData()
    errors_datasets = error_data.get_processed_datasets()
    min_max_errors = error_data.get_min_max_errors()
    print(min_max_errors)
    error_charts = cPlotDataset()
    labels = [['Number of sample', 'x_err [m]'],['Number of sample', 'y_err [m]'],
              ['Number of sample', 'z_err [m]'],['Number of sample', 'euc_err [m]']]
    error_charts.multiplot(4,1,errors_datasets, labels, min_max_errors)
    #datasets = error_charts.load_datasets()
