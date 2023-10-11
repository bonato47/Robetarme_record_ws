

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import rosbag
import rospy

import sys
import os
import glob
import pickle
import time
import math
import argparse
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from numpy import linalg as LA
from mpl_toolkits.mplot3d import Axes3D

from plot_verification import *
from transformCsv import *

from bagToCsv import *
#blob that take all the name of the folder
# Create all csv files from .bag

folder = glob.glob('../arranged_data/*')
for name in folder:
    bagshot = glob.glob( name+ "/*.bag")

    task = 1
    if not (name.find("shot") == -1):
        task = 0
    name_short= bagshot[0].replace(".bag", "")
    bagToCsv_post(name_short , task)
    print(name_short + " bag to csv is done")

    data = pd.read_csv(name_short+".csv", index_col=False)

    displacementFromTarget = [1.25,0,0.7] 


    files = os.listdir(name)
    prefix = "target"
    # Filter files that start with the specified prefix
    target_csv_name = [filename for filename in files if filename.startswith(prefix)]
    target_csv_name = name + "/" + target_csv_name[0]

    files = os.listdir(name)
    prefix = "Bias"
    # Filter files that start with the specified prefix
    bias_csv_name = [filename for filename in files if filename.startswith(prefix)]
    bias_csv_name = name + "/" + bias_csv_name[0]

    data_final= transform_data(data,name_short,displacementFromTarget,task,target_csv_name,bias_csv_name)
    print(name_short + " transform is done")
    plt.close()

    print("plotting all plots...")
    plot_quaternion(data_final,name)
    plot_angularVelocity(data_final,name)
    plot_position(data_final,name)
    plot_euler(data_final,name)
    plot_force(data_final,name)
    plot_torque(data_final,name)
    print("path is ploting ...")
    plot_path(data_final,name)
    print("All plots are saved")

    #print("path plot")
    #plot_path(data_final,name)
    print("all is plotted")

    #mainTransform(bagshot)

#boucle that go inside each folder
    #run mainTransform 

#subject1_surf_target2_tria1_bar_03_10_23   subject1_surf_target8_trial1_06_10_23