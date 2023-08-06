# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: Charles-David Hebert
"""

import numpy as np
import os
from copy import deepcopy
import re
import json

class StatsParams:


    """A class that implements the automated statistics of parameter files
       in text file format. A parameter file consists of a file with  the parameter
       names followed by spaces (or none), then a = then spaces (or none) and then
       the value, which can be a float, or a string (not implemented for now).
       
       column being the number of the iteration, the second column the value of
       the observable and the third column being the error on the observable if
       applicable. There is a parameter, 'ignore_col' that is used if a column
       is futile, such as the iteration column. If the error column does not
       exist, it is ignored. By default the program will abort if there is more
       than three columns."""

    params_files_default=["params"]
    
    # One list per element in params_files
    params_names_l_default=[["beta", "mu", "tp", "U", "n", "S", "delta", "weightR", 
                 "weightI", "EGreen", "EHyb", "EObs", "theta"]]
    
                   
    def __init__(self, params_files=params_files_default, params_names_l=params_names_l_default,
                 ext="", iter_start=1, in_dir=os.getcwd(),
                 warning_only=True):
        """Initialize the StatsParams object.

        Args:

        Keywords Args:
            arrays_files (list||str): the arrays files in a list or a single string for one file
            ext: the extensions of the arrays_files
            iter_start: the iteration from which to start the statistics
            ignore_col (None||int): the col to ignore in the computations for the std
            in_dir (str): the dir in which the arrays_files are found.
            warning_only: the boolen controlling if only warnings are issued if
                          the files are not found
        Returns:

        Raises:

         """

        # check the existence of work dir
        self.in_dir = os.path.abspath(in_dir)
        assert(os.path.exists(self.in_dir)), "Ayaya, in_dir does not exist."

        # creata a list of the params_files and of the params_names_l
        self.params_files = params_files if isinstance(params_files, list) else [params_files]
        self.params_names_l = params_names_l if isinstance(params_names_l[0], list) else [params_names_l]
        
        self.ext = ext
        self.iter_start = iter_start
        self.warning_only = warning_only # make the program continue if files don't
                                         # exist, but give warning message
        files = [file + str(self.iter_start) +  self.ext for file in self.params_files]
        
        self.check_sanity(files, params_names_l, self.warning_only)
        self.means = None # set by mean()
        self.stds = None # set by std()
        self.means_dict = None
        self.stds_dict = None

    
    @staticmethod
    def find_value(param, fin_s):
        """ """
        pattern = re.compile("""^(?:\s*)(?:""" + param + """
                \s*)    # match from zero to any number of whitespaces
                =           # match a =
                (?:\s*)?    # match from zero to any number of whitespaces
                ([-+]?(?:\d+)?(?:\.\d*)?(?:[eE][-+]?\d+)?)
                """, re.VERBOSE | re.MULTILINE)
                        
        try:
            value: float = float(re.search(pattern, fin_s).groups()[0])
        except AttributeError as ae:
            print("\n Ayayya ", param, "is not a float or not found")
            print("Attribute error: {0}".format(ae))
            raise
        
        return value


    def read_file(self, file_name, params_names, delimiter="="):
        """reads a files and their contents in a numpy array
        
        Args:
        
        Keywords Args:
                     file_name: the  to be read into a numpy array
        Returns:
               (data, file_exists):      
        
        """
        
        file_exists = os.path.isfile(file_name)
        if file_exists:
            with open (file_name) as fin:
                fin_s = fin.read()

            data: List[float] = []    
            for param in params_names:
                
                value: float = self.find_value(param, fin_s)
                data.append(value)
               
        else:
            data = None            
        
        return (np.array(data), file_exists)


    def check_sanity(self, files, params_names_l, warning_only):
        """Check if the constructing attributes are sain"""
        
        assert(len(files) == len(params_names_l)), "ayays, params_files and params_names_l do not have same length"
        
        files_tmp = []
        for (i, file) in enumerate(files):
            file_path = os.path.join(self.in_dir, file)
            file_path_exists = os.path.isfile(file_path)
            
            if file_path_exists:
                files_tmp.append(file)
                continue
            elif warning_only:
                del self.params_files[i]
                print("\n Warning, file ", file, " does not exist")
                print("")
            else:    
                assert(file_path_exists), "Ayaya, file does not exist"

        files = files_tmp
        params_names_l_tmp = []
        

        for (params_names, file) in zip(params_names_l, files):
            params_names_tmp= []
            with open(os.path.join(self.in_dir, file)) as fin:
                file_s = fin.read()
            for param in params_names:
                if re.search(param, file_s):
                    params_names_tmp.append(param)
                elif warning_only:
                    continue
                else:
                    raise IOError("parameter  " + param + " not found in file", file,". Put warning only if you dont care....")
            params_names_l_tmp.append(params_names_tmp)            
                
        self.params_names_l = params_names_l_tmp


    def mean(self):
        """Computes the means of the params_files."""
        
        #The means of the parameters
        means = [] # a list of lists (each element of the list consists of the mean of the params_names for each param_file)
        means_dict = [] # a list of dictionaries (the first dictionray is for the first params_file and its associated params_names, etc)

        for (params_names, params_file) in zip(self.params_names_l, self.params_files):
            cpt = 0
            file_name = os.path.join(self.in_dir, params_file + str(self.iter_start) + self.ext)
            # print(file_name)
            (data, file_exists) = self.read_file(file_name, params_names)
            if file_exists:
                mean = np.zeros(data.shape)
                while(file_exists):
                    mean += data
                    cpt += 1
                    # print("cpt ", cpt)
                    # print(array_file + end_file + str(self.iter_start + cpt) + self.ext)
                    file_name = os.path.join(self.in_dir, params_file + str(self.iter_start + cpt) + self.ext)
                    (data, file_exists) = self.read_file(file_name, params_names)
            
                mean /= cpt 
                mean_dict = {param_name:mean_value for (param_name, mean_value) in zip(params_names, mean)}
                # print("MEAN ", mean)
                means_dict.append(mean_dict)
                means.append(mean)
            
        self.means = means
        self.means_dict = means_dict
        #print(means)
           

    def std(self):
        """Compute the std errors of the observables and their error if applicable"""
        
        if self.means is None:
            self.mean()   
        stds = [] # a list of lists
        stds_dict = [] # a list of dictionaries
             
        for (i, param_file, params_names) in zip(range(len(self.params_files)), self.params_files, self.params_names_l):
            #for (j, params_names) in enumerate(self.params_names_l[i]):
            cpt = 0
            file_name = os.path.join(self.in_dir, param_file  + str(self.iter_start) + self.ext)
            (data, file_exists) = self.read_file(file_name, params_names)
            if file_exists:
                std = np.zeros(data.shape) 

                while(file_exists):
                    mean = self.means[i]
                    #print("mean ", mean)
                    std += np.power(data - mean, 2.0)
                    #print("data ", data)
                    #print("std " , std)
                    cpt += 1
                    file_name = os.path.join(self.in_dir, param_file  + str(self.iter_start + cpt) + self.ext)
                    #print("file_name ", file_name)
                    (data, file_exists) = self.read_file(file_name, params_names)
            
                #print("std final ", std)                
                std /= cpt
                std = np.sqrt(std)
                stds.append(std)
                #print("stds list ", stds)
                std_dict = {param_name:std_value for (param_name, std_value) in zip (params_names, std)}
                stds_dict.append(std_dict)
        #print("stds before exit ", stds)  
        #print("self.stds ", stds)
        self.stds = stds
        self.stds_dict = stds_dict  


    def write_results(self, out_dir="Results", file_out="test_json_params.json"):
        """ """
        # First concatenate the mean and the std of each parameter in the same dictionary
        cpt = 0
        #print("IN write results\n")
        #print(self.stds_dict)
        for (mean_dict, std_dict) in zip(self.means_dict, self.stds_dict):          
            out_dict = dict()
            for key in mean_dict:
                out_dict[key] = [mean_dict[key], std_dict[key]]
            
            file_result = file_out.split(".")[0] + str(cpt) + "." + file_out.split(".")[1]
            with open(os.path.join(out_dir, file_result), 'w') as fout:
                json.dump(out_dict, fout, indent=4)
            cpt += 1 


            



