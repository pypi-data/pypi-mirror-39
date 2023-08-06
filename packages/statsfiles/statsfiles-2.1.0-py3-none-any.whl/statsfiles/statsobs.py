# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: Charles-David Hebert
"""

import numpy as np
# import configparser
import os
from copy import deepcopy
import json

class StatsObs:


    """A class that implements the automated statistics of observables written
       in text file format. An observable consists of a file with  the first
       column being the number of the iteration, the second column the value of
       the observable and the third column being the error on the observable if
       applicable. There is a parameter, 'ignore_col' that is used if a column
       is futile, such as the iteration column. If the error column does not
       exist, it is ignored. By default the program will abort if there is more
       than three columns."""


    def __init__(self, obs_files="params.txt", iter_start=0, ignore_col=None, in_dir=os.getcwd(),
                 warning_only=True):
        """Initialize the StatsObs object.

        Args:

        Keywords Args:
            obs_files (list||str): the observables files in a list or a single string for one file
            ignore_col (None||int): the col to ignore in the computations
            in_dir (str): the dir in which the obs_files are found.
        Returns:

        Raises:

         """

        # check the existence of work dir
        self.in_dir = os.path.abspath(in_dir)
        assert(os.path.exists(self.in_dir)), "ayaya, in_dir does not exist"

        # creata a list of the obs_files
        self.obs_files = obs_files if isinstance(obs_files, list) else [obs_files]
        self.iter_start = iter_start
        if ignore_col is None:
            self.ignore_col = ignore_col
        else:
            assert(isinstance(ignore_col, int)), "Ayayaya, ignore_col must be None or int"
            self.ignore_col = ignore_col
            
        self.warning_only = warning_only # make the program continue if files don't
                                         # exist, but give warning message
        self.check_sanity(self.obs_files)
        self.datas = None # set by read_files
        self.means = None # set by mean()
        self.means_dict = None
        self.stds = None # set by std()
        self.stds_dict = None
        self.iter_max = None
        self.read_files()



    def read_files(self):
        """reads the files and their contents in numpy arrays (list of numpy arrays)"""

        datas = []
        for file in self.obs_files:
            file_path = os.path.join(self.in_dir, file)
            data = np.loadtxt(file_path)
            if self.ignore_col is not None:
                data = np.delete(data, self.ignore_col, 1)

            datas.append(data)
        
        #delete the unwanted rows from 0 to iter_start
        if self.iter_start:
            datas_cut = []
            size_row = datas[0].shape[0]
            for data in datas:
                for i in range(self.iter_start ): # put -1 if you want to start exactly 
                    data = np.delete(data, 0, 0)  # at iter_start and not at iter_start + 1
                datas_cut.append(data)
            datas = datas_cut        
                
        self.datas = deepcopy(datas)
        # print(self.datas)
        self.iter_max = self.datas[0].shape[0] + self.iter_start #-1 if the above comment is applied


    def check_sanity(self, files):
        """Check if the constructing attributes are sain"""

        files_tmp = []
        
        for file in files:
            file_path = os.path.join(self.in_dir, file)
            file_path_exists = os.path.isfile(file_path)
            
            if file_path_exists:
                files_tmp.append(file)
            elif self.warning_only:
                print("\n Warning, file ", file, " does not exist")
            else:    
                assert(os.path.isfile(file_path)), "Ayaya, file does not exist"
            
            # print(file_path)
            # print(os.path.isfile(file_path)), "ayaya file does not exist"
        self.obs_files = files_tmp
        if isinstance(self.ignore_col, int):
            assert(self.ignore_col >= 0 and self.ignore_col <= 2), \
                "Ayayya, wrong colum ignored in obs files"


    def mean(self):
        """Computes the means of the observables and their errors if applicable """

        means = []

        for data in self.datas:
            mean = np.average(data, 0)
            means.append(mean)
            #print(mean)
            #print(self.obs_files)
        self.means = np.vstack(means)
        self.means_dict = {obs_file:mean for (obs_file, mean) in zip (self.obs_files, means)}

    def std(self):
        """Compute the std errors of the observables and their error if applicable"""

        stds = []

        for data in self.datas:
            std = np.std(data, 0)
            stds.append(std)

        self.stds = np.vstack(stds)
        self.stds_dict = {obs_file:std for (obs_file, std) in zip (self.obs_files, stds)}


    def write_results(self, out_dir="Results", file_out="results_stats_obs.json"):
        """ """

        # Add checking if the directory exists, create it if not, also, back_up old
        # stats_files. by backing up the ancient result directory in a new
        # directory with name Result-date or something like this

        file_out = os.path.join(out_dir, file_out)
        out_dict = dict()
        out_dict["iter_start"] = self.iter_start
        out_dict["iter_max"] = self.iter_max

        # By convention, I will write only the first mean and std to disk
        for i in range(len(self.obs_files)):
            out_dict[self.obs_files[i]] = [self.means[i][0], self.stds[i][0]]

        with open(file_out, mode="a") as fout:
            json.dump(out_dict, fout, indent=4)
