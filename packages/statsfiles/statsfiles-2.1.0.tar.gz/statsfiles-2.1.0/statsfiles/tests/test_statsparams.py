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


from .. import statsparams

# You CAN (not necessary) comment the last two lines and uncomment the next two when testing
# but the first import seems to work better when adding auto-completion features in IDE


# import stats_files
# from stats_files.stats_obs import stats_obs3 as stats_obs
# with these lines last two lines you can run "python -m unittest discover"
# or "python -m unittest tests/test_..." from the source directory


class TestStatsParams(unittest.TestCase):
    """ """
   
    input_dir = "statsfiles/tests/testinfiles/b60"

    def test_init(self):
        """ """
        params_files_default = ["params", "pete"]
        params_names_l_default=[["beta", "mu", "tp", "U", "n", "S", "delta", "weightR", 
                 "weightI", "EGreen", "EHyb", "EObs", "theta"], ["lalal"]]
        # out_dir =   "TestOutFiles"
        statsp = statsparams.StatsParams(params_files=params_files_default, params_names_l=params_names_l_default,
                 ext="", iter_start=243, in_dir=self.input_dir, warning_only=True)

        # Test that the given values are ok
        self.assertEqual(statsp.in_dir, os.path.abspath(self.input_dir))
        self.assertEqual(statsp.params_files, ["params"])
        self.assertEqual(statsp.ext, "")
        self.assertEqual(statsp.params_names_l, [["beta", "mu", "tp", "U", "n", "S", "delta", "weightR", 
                 "weightI", "EGreen", "EHyb", "EObs", "theta"]])
        self.assertEqual(statsp.warning_only, True)
        self.assertEqual(statsp.iter_start, 243)
        self.assertEqual(statsp.means, None)
        self.assertEqual(statsp.stds, None)
        self.assertEqual(statsp.means_dict, None)
        self.assertEqual(statsp.stds_dict, None)




    def test_check_sanity(self):
        """Check if the constructing attributes are sain"""

        params_files_default = ["params", "pete"]
        params_names_l_default=[["beta", "mu", "tp", "U", "n", "S", "delta", "weightR", 
                 "weightI", "EGreen", "EHyb", "EObs", "theta"], ["lalal"]]
        input_dir = "tests/TestInFiles/StatsArrays/b60"
        # out_dir =   "TestOutFiles"
        statsp = statsparams.StatsParams(params_files=params_files_default, params_names_l=params_names_l_default,
                 ext="", iter_start=243, in_dir=self.input_dir, warning_only=True)
                 
        # test that an statsparamss object with bad file names exits ok with asserts
        #if warning_only=False
        self.assertRaises(AssertionError, statsp.check_sanity, ["dodo","lalla"], [["1","2"], ["3","4"]], False)


    def test_find_value(self):
        """ """
        ss_list: List[str] = ["tp=-0.9", "tp =    -0.41", "   \n tp= +.12", "tp  =10.2  ", "\n tp = 1.7E+10", "tp = -1.3e-2 \n"]
        value_list: List[float] = [-0.9, -0.41, 0.12, 10.2, 1.7e10, -1.3e-2]

        for (ss, value) in zip(ss_list, value_list):
            value_test = statsparams.StatsParams.find_value("tp", ss)
            self.assertAlmostEqual(value, value_test)
            self.assertNotAlmostEqual(value-0.0001, value_test)
        
    #@unittest.skip("")
    def test_read_file(self):
        """reads the files and their contents in numpy paramss (list of numpy paramss)"""

        params_files_default = ["params", "pete"]
        params_names_l_default=[["beta", "mu", "tp", "U", "n", "S", "delta", "weightR", 
                 "weightI", "EGreen", "EHyb", "EObs", "theta"], ["lalal"]]
        # out_dir =   "TestOutFiles"
        statsp = statsparams.StatsParams(params_files=params_files_default, params_names_l=params_names_l_default,
                 ext="", iter_start=243, in_dir=self.input_dir, warning_only=True)
                 
        good_file = os.path.join(self.input_dir, "params243")
        bad_file = os.path.join(self.input_dir, "params244")        
        (data, file_exists) = statsp.read_file(good_file, params_names_l_default[0])
        good_data = np.array([60.0, 3.3874309354805243, 0.8000000, 12.000000,
                     0.49500000, 1.000000, 2.000000, 0.30000000, 0.3000000,
                     15.000000, 15.0000000, 15.0000000, 0.9550441666912971])
        #bad_data = np.loadtxt(bad_file)
        
        self.assertEqual(True, file_exists)
        # print(data)
        try:
            np.testing.assert_allclose(data - good_data, np.zeros(good_data.shape), rtol=1e-3)
        except AssertionError:
            self.fail("np.testing.assert_params_equal failed")


        self.assertRaises(AssertionError, np.testing.assert_allclose, data, 2.1*np.array(good_data))



    #@unittest.skip("")
    def test_mean(self):
        """ """
        params_files_default = ["params", "pete"]
        params_names_l_default=[["beta", "mu", "tp", "U", "n", "S", "delta", "weightR", 
                 "weightI", "EGreen", "EHyb", "EObs", "theta"], ["lalal"]]
        input_dir = "tests/TestInFiles/StatsArrays/b60"
        out_dir =   "tests/TestOutFiles/StatsParams"        
        # out_dir =   "TestOutFiles"
        statsp = statsparams.StatsParams(params_files=params_files_default, params_names_l=params_names_l_default,
                 ext="", iter_start=243, in_dir=self.input_dir, warning_only=True)
        
        
                  
        statsp.mean()
        calculated_means = statsp.means[0]
        # print(calculated_means, type(calculated_means))
        good_means = np.array([60.0, 3.38711, 0.8, 12.0, 0.495, 1.0, 2.0, 0.3, 0.3, 15.0, 15.0, 15.0, 0.955044])
        
        try:
            np.testing.assert_allclose(calculated_means, good_means, rtol=1e-6, atol=1e-6)
        except AssertionError:
            self.fail("np.testing.assert_params_allclose failed")
                
        for (a,b) in zip(calculated_means, good_means):
            self.assertAlmostEqual(a,b, delta=1e-5)

                      
        bad_means = [np.multiply(0.1, mean) for mean in good_means]

        
        self.assertEqual(False, np.allclose(a=calculated_means, b=bad_means, rtol=1e-3))

    #@unittest.skip("")
    def test_std(self):
        """Compute the std errors"""
        params_files_default = ["params", "pete"]
        params_names_l_default=[["beta", "mu", "tp", "U", "n", "S", "delta", "weightR", 
                 "weightI", "EGreen", "EHyb", "EObs", "theta"], ["lalal"]]
        input_dir = "tests/TestInFiles/StatsArrays/b60"
        out_dir =   "tests/TestOutFiles/StatsParams"        
        # out_dir =   "TestOutFiles"
        statsp = statsparams.StatsParams(params_files=params_files_default, params_names_l=params_names_l_default,
                 ext="", iter_start=243, in_dir=self.input_dir, warning_only=True)
        
        statsp.std()
        #print("STDS: ", stats.stds_dict)
        calculated_stds = statsp.stds[0]
        # print(calculated_means, type(calculated_means))
        good_stds = np.array([0.0, 0.000265041, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        
        
        for (a,b) in zip(calculated_stds, good_stds):
            self.assertAlmostEqual(a,b, delta=1e-5)
#        try:
#            np.testing.assert_allclose(calculated_stds, good_stds, rtol=1e-3)
#        except AssertionError:
#            self.fail("np.testing.assert_allclose failed")
                


                      
        bad_stds = [np.multiply(0.1, std) for std in good_stds]

        
        self.assertEqual(False, np.allclose(a=calculated_stds, b=bad_stds, rtol=1e-3))
        

    #@unittest.skip("Debug write_result") 
    def test_write_results(self):
        """ """
        params_files_default = ["params", "pete"]
        params_names_l_default=[["beta", "mu", "tp", "U", "n", "S", "delta", "weightR", 
                 "weightI", "EGreen", "EHyb", "EObs", "theta"], ["lalal"]]
        out_dir =   "statsfiles/tests/testoutfiles/statsparams"      
        statsp = statsparams.StatsParams(params_files=params_files_default, params_names_l=params_names_l_default,
                 ext="", iter_start=243, in_dir=self.input_dir, warning_only=True)
        statsp.mean(); statsp.std() ; statsp.write_results(out_dir=out_dir)

##    def test_write_results(self, file_out="results_stats_obs.txt"):
##        """ """
##        pass
#
#
if __name__ == "__main__":
    unittest.main() 
#               