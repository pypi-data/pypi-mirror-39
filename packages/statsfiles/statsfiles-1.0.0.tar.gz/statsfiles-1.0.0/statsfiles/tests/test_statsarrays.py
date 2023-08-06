# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: charles-david hebert
"""


import numpy as np
# import configparser
import os
import sys
import unittest
# import copy


from .. import statsarrays

# You CAN (not necessary) comment the last two lines and uncomment the next two when testing
# but the first import seems to work better when adding auto-completion features in IDE


# import stats_files
# from stats_files.stats_obs import stats_obs3 as stats_obs
# with these lines last two lines you can run "python -m unittest discover"
# or "python -m unittest tests/test_..." from the source directory

class TestStatsArray(unittest.TestCase):
    """ """
    array_files_default = ["green", "self", "hyb"]
    array_files_end_default = ["", "Up", "Down"]
    input_dir = "statsfiles/tests/testinfiles/b60"
    out_dir =   "statsfiles/tests/testoutfiles/statsarrays"

    def test_init(self):
        """ """
        statsarray = statsarrays.StatsArrays(iter_start=243, ignore_col=0,
                                             in_dir=self.input_dir)  

        # Test that the given values are ok
        self.assertEqual(statsarray.in_dir, os.path.abspath(self.input_dir))
        self.assertEqual(statsarray.ignore_col, 0)
        self.assertEqual(statsarray.array_files, self.array_files_default)
        self.assertEqual(statsarray.ext, ".dat")
        self.assertEqual(statsarray.warning_only, True)
        self.assertEqual(statsarray.iter_start, 243)


    def test_check_sanity(self):
        """Check if the constructing attributes are sain"""

        
        statsarray = statsarrays.StatsArrays(iter_start=243, ignore_col=0,
                                             in_dir=self.input_dir)
                                             
        # test that an statsarrays object with bad file names exits ok with asserts if 'warning_only'=False
        self.assertRaises(AssertionError, statsarray.check_sanity, ["dodo","lalla"], False)



    def test_read_file(self):
        """reads the files and their contents in numpy arrays (list of numpy arrays)"""

          
        statsarray = statsarrays.StatsArrays(iter_start=243, ignore_col=0,
                                             in_dir=self.input_dir)
        good_file = os.path.join(self.input_dir, "green243.dat")
        bad_file = os.path.join(self.input_dir, "green244.dat")        
        (data, file_exists) = statsarray.read_file(good_file)
        good_data = np.loadtxt(good_file)
        bad_data = np.loadtxt(bad_file)
        
        self.assertEqual(True, file_exists)
        
        try:
            np.testing.assert_array_equal(data, good_data, err_msg='', verbose=True)
        except AssertionError:
            self.fail("np.testing.assert_array_equal failed")

        self.assertRaises(AssertionError, np.testing.assert_array_equal, data, bad_data, err_msg='', verbose=True)


    def test_mean(self):
        """ """
          
        statsarray = statsarrays.StatsArrays(iter_start=243, ignore_col=0,
                                             in_dir=self.input_dir)
        
        statsarray.mean()
        calculated_means = [statsarray.means["green_moy.dat"],
                            statsarray.means["self_moy.dat"],
                            statsarray.means["hyb_moy.dat"]]
        
        good_means = [np.loadtxt(os.path.join(self.input_dir, "greenMoy.dat")),
                      np.loadtxt(os.path.join(self.input_dir, "selfMoy.dat")),
                      np.loadtxt(os.path.join(self.input_dir, "hybMoy.dat"))]
        
        for (a,b) in zip(good_means, calculated_means):
             try:
                np.testing.assert_allclose(a, b, rtol=1e-5)
             except AssertionError:
                self.fail("np.testing.assert_array_allclose failed")
                


                      
        bad_means = [np.multiply(0.1, mean) for mean in good_means]

        
        self.assertEqual(False, np.allclose(a=calculated_means, b=bad_means))

        # Another way of testing the same thing
        for i in range(len(good_means)):
            for (a, b) in zip (calculated_means[i].flatten(), good_means[i].flatten()):
                self.assertAlmostEqual(a, b, delta=1e-5)

            for (a, b) in zip (calculated_means[i].flatten(), bad_means[i].flatten()):
                self.assertNotEqual(a, b)

        
    def test_std(self):
        """Compute the std errors"""
        
        # out_dir =   "TestOutFiles"
        statsarray = statsarrays.StatsArrays(iter_start=243, ignore_col=0,
                                             in_dir=self.input_dir)
        statsarray.mean()
        statsarray.std()
        
        good_stds = [np.loadtxt(os.path.join(self.input_dir, "greenET.dat")),
                      np.loadtxt(os.path.join(self.input_dir, "selfET.dat")),
                      np.loadtxt(os.path.join(self.input_dir, "hybET.dat"))]
                      
        good_stds = [np.delete(std, statsarray.ignore_col, 1) for std in good_stds]              
        bad_stds = np.multiply(0.1, good_stds)
        
        calculated_stds = [statsarray.stds["green_et.dat"],
                           statsarray.stds["self_et.dat"],
                           statsarray.stds["hyb_et.dat"]]
                           
        for (a,b) in zip(good_stds, calculated_stds):
             try:
                np.testing.assert_allclose(a, b, rtol=5e-6)
             except AssertionError:
                self.fail("np.testing.assert_array_allclose failed")




    def test_mean_afm(self):
        """ """
        input_dir = "statsfiles/tests/testinfiles/afm"
        out_dir =   "tests/testoutfiles/statsarrays"
          
        statsarray = statsarrays.StatsArrays(iter_start=346, ignore_col=0,
                                             in_dir=input_dir)
        
        statsarray.mean()
        calculated_means = [statsarray.means["greenUp_moy.dat"],
                            statsarray.means["hybDown_moy.dat"]]
        
        good_means = [np.loadtxt(os.path.join(input_dir, "greenUpMoy.dat")),
                      np.loadtxt(os.path.join(input_dir, "hybDownMoy.dat"))]
        
        for (a,b) in zip(good_means, calculated_means):
             try:
                np.testing.assert_allclose(a, b, rtol=1e-5)
             except AssertionError:
                self.fail("np.testing.assert_array_allclose failed")
                


                      
        bad_means = [np.multiply(0.1, mean) for mean in good_means]

        
        self.assertEqual(False, np.allclose(a=calculated_means, b=bad_means))

        # Another way of testing the same thing
        for i in range(len(good_means)):
            for (a, b) in zip (calculated_means[i].flatten(), good_means[i].flatten()):
                self.assertAlmostEqual(a, b, delta=5e-6)

            for (a, b) in zip (calculated_means[i].flatten(), bad_means[i].flatten()):
                self.assertNotEqual(a, b)

    
    def test_std_afm(self):
        """Compute the std errors"""
        
        input_dir = "statsfiles/tests/testinfiles/afm"
        # out_dir =   "TestOutFiles"
        statsarray = statsarrays.StatsArrays(iter_start=346, ignore_col=0,
                                             in_dir=input_dir)
        statsarray.mean()
        statsarray.std()
        
        good_stds = [np.loadtxt(os.path.join(input_dir, "greenDownET.dat")),
                      np.loadtxt(os.path.join(input_dir, "selfUpET.dat")),
                      np.loadtxt(os.path.join(input_dir, "hybDownET.dat"))]
                      
        good_stds = [np.delete(std, statsarray.ignore_col, 1) for std in good_stds]              
        bad_stds = np.multiply(0.1, good_stds)
        
        calculated_stds = [statsarray.stds["greenDown_et.dat"],
                           statsarray.stds["selfUp_et.dat"],
                           statsarray.stds["hybDown_et.dat"]]
                           
        for (a,b) in zip(good_stds, calculated_stds):
             try:
                np.testing.assert_allclose(a, b, rtol=5e-6)
             except AssertionError:
                self.fail("np.testing.assert_array_allclose failed")
                

if __name__ == "__main__":
    unittest.main() 