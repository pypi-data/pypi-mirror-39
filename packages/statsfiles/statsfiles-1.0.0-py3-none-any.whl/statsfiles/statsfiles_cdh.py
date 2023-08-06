# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: Charles-David Hebert
"""

import time
import os
import sys


from . import statsobs
from . import statsarrays
from . import statsparams
from . import copy_essential


def run_statsfiles(iter_start: int=0, is_afm: bool=False) -> None:

    default_obs_files = ["k.dat", "n.dat", "docc.dat", "sign.dat"]

    array_files_default = ["green", "greenDown",
                           "greenUp", "self", "hybtriangle", "hybUp", "hyb", "selfUp"]
    array_files_end_default = ["", "Up", "Down"]

    starr = statsarrays.StatsArrays(array_files=array_files_default,
                                    end_files=array_files_end_default,
                                    ext=".dat", iter_start=iter_start,
                                    ignore_col=None, in_dir=os.getcwd(),
                                    warning_only=True)

    # stobs = statsobs.StatsObs(obs_files=default_obs_files, iter_start=iter_start, ignore_col=0, in_dir=os.getcwd(),
    #                          warning_only=True)

    out_dir = time.strftime("Stats" + "-%Y-%m-%d--%Hh%M")
    os.mkdir(out_dir)

    # stobs.mean()
    # stobs.std()
    #stobs.write_results(out_dir=out_dir, file_out="statsobs.json")
    starr.mean()
    starr.std()
    starr.write_results(out_dir=out_dir, file_out="statsobs.json")
    #stparams.mean(); stparams.std(); stparams.write_results(out_dir, "statsparams.json")

    #ce = copy_essential.CopyEssential(out_dir)
    # ce.run()

    return None
