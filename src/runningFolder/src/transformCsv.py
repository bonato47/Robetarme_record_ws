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

#from plot_verification import *


from bagToCsv import *

from plot_verification import *


def median_filter_1d(signal, window_size):
    filtered_signal = []
    half_window = window_size // 2

    for i in range(len(signal)):
        window = signal[max(0, i - half_window):min(len(signal), i + half_window + 1)]
        sorted_window = sorted(window)
        median_value = sorted_window[len(window) // 2]
        filtered_signal.append(median_value)

    return filtered_signal

def calc_angular_velocities(quat, quat_d):
    w = np.zeros((quat.shape[0], 3))
    for i in range(quat.shape[0]):
        q = quat[i, :]
        q_d = quat_d[i, :]
        a = np.array([[-q[1], -q[2], -q[3]],
                      [q[0], -q[3], q[2]],
                      [q[3], q[0], -q[1]],
                      [-q[2], q[1], q[0]]])
        b = 2*q_d
        w_i = np.linalg.lstsq(a, b, rcond=None)[0]
        w[i, 0], w[i, 1], w[i, 2] = w_i[0], w_i[1], w_i[2]
    return w

def extract_angular_velocities(dataInter):

    time_stamp = dataInter['Time']
    time_stamp = np.array(time_stamp.values.tolist(), dtype=np.float64)
    time_stamp = time_stamp  # converting ms to S

    quat_org = dataInter[['quatw_filter', 'quatx_filter', 'quaty_filter', 'quatz_filter']]
    # quat_org = dataInter[['_vrpnQuat_w', '_vrpnQuat_x', '_vrpnQuat_y', '_vrpnQuat_z']]

    quat_org = np.array(quat_org.values.tolist(), dtype=np.float64)

    quat = quat_org / np.linalg.norm(quat_org, axis=1).reshape(-1, 1)

    quat_d = np.zeros(quat.shape)
    for i in range(quat.shape[1]):
        quat_d[:, i] = np.gradient(quat[:, i], time_stamp, edge_order=2)

    w = calc_angular_velocities(quat, quat_d)
    return w

def transformToolGround(Vquat,Vpos):
        #tool in fct ground
        r = R.from_quat(Vquat)
        p = np.array(Vpos)
        Rot = r.as_matrix()
        T_tool_ground = np.insert(Rot, 3, p, axis=1)

        T_tool_ground = np.insert(T_tool_ground, 3,[0,0,0,1] , axis=0)
        T_tool_ground= np.matrix(T_tool_ground)
        return T_tool_ground

def transformGroundBase(Vpos):

    t = math.pi/2
    Rx = [[1, 0, 0],[0 ,math.cos(t), -math.sin(t)] ,[0 ,math.sin(t), math.cos(t)] ]
    Rx= np.matrix(Rx)

    t = math.pi/2
    Ry = [[math.cos(t),0, math.sin(t)],[0 ,1,0] ,[-math.sin(t),0, math.cos(t)] ]
    Ry= np.matrix(Ry)

    Rtot = Rx

    T_ground_Base = np.insert(Rtot, 3, Vpos, axis=1)
    T_ground_Base = np.insert(T_ground_Base, 3,[0,0,0,1] , axis=0)

    return T_ground_Base

def transformBaseEef(stringTransform , t):

    Rx = [[1, 0, 0],[0 ,math.cos(t), -math.sin(t)] ,[0 ,math.sin(t), math.cos(t)] ]
    Ry = [[math.cos(t),0, math.sin(t)],[0 ,1,0] ,[-math.sin(t),0, math.cos(t)] ]
    Rz = [[math.cos(t), -math.sin(t), 0],[math.sin(t), math.cos(t),0] ,[0 ,0,1] ]

    Ry= np.matrix(Ry)
    Rz= np.matrix(Rz)
    Rx= np.matrix(Rx)
    
    if stringTransform == "x":
        Rtot = Rx
    if stringTransform == "y":
        Rtot = Ry
    if stringTransform == "z":
        Rtot = Rz

    T_tool_eef = np.insert(Rtot, 3,[0,0,0], axis=1)
    T_tool_eef = np.insert(T_tool_eef, 3,[0,0,0,1] , axis=0)
    return T_tool_eef

def take_target(file_name):
    for i in range(10):
        target= "target" + str(i+1)
        if not ((file_name.find(target)==-1)):
            break

    return target

def extractQuatPos (T):
    condition = [[0, 0, 0,1],[0, 0, 0,1],[0, 0, 0,1],[0,0,0,0] ]
    pos_opt_world =  np.extract(condition, T)

    condition = [[1, 1, 1,0],[1, 1, 1,0],[1, 1, 1,0],[0,0,0,0] ]
    R_opt_world =  np.matrix(np.extract(condition, T).reshape((3, 3)))
    R_opt_world = R.from_matrix(R_opt_world)
    quat_opt_world  = R_opt_world.as_quat()
    euler_opt_world = R_opt_world.as_euler("XYZ")

    return quat_opt_world, pos_opt_world, euler_opt_world

def transformTarget(quatTarget, posTarget,dataInter):

        #tool in fct ground
        T_tool_ground = transformToolGround(quatTarget,posTarget)

        # ground in function of base
        p =[0,0,0]
        T_ground_Base =  transformGroundBase(p)
        T_tilt = T_ground_Base* T_tool_ground  
        quat_opt_world , pos_opt_world, e = extractQuatPos(T_tilt)

        return  quat_opt_world , pos_opt_world

def clean_force_and_add_to_dataframe(datainter,datafinal):
    wSize=30
    datafinal["forcex"] = datainter["_ftforce_x"]
    datafinal["forcey"] = datainter["_ftforce_y"]
    datafinal["forcez"] = datainter["_ftforce_z"]
    datafinal["forcex_filter"] = median_filter_1d(datainter["_ftforce_x"], wSize)
    datafinal["forcey_filter"] = median_filter_1d(datainter["_ftforce_y"], wSize)
    datafinal["forcez_filter"] = median_filter_1d(datainter["_ftforce_z"], wSize)

    datafinal["torquex"] = datainter["_fttorque_x"]
    datafinal["torquey"] = datainter["_fttorque_y"]
    datafinal["torquez"] = datainter["_fttorque_z"]

    datafinal["torquex_filter"] = median_filter_1d(datainter["_fttorque_x"], wSize)
    datafinal["torquey_filter"] = median_filter_1d(datainter["_fttorque_y"], wSize)
    datafinal["torquez_filter"] = median_filter_1d(datainter["_fttorque_z"], wSize)

    return datafinal
    
def take_pos_target(t):  
        dfTarget = pd.read_csv("../data/targets/" + t + ".csv", index_col=False)
        qTar = [dfTarget["Orientation_X"][0],dfTarget["Orientation_Y"][0],dfTarget["Orientation_Z"][0],dfTarget["Orientation_W"][0]]
        pTar = [dfTarget["Position_X"][0],dfTarget["Position_Y"][0],dfTarget["Position_Z"][0]]
        return qTar, pTar

def add_target_dataframe(Name, data, Disp):
    #compute target pos
    t = take_target(Name)
    if t != "target9" and t != "target10": 

        QuatTarget, a = take_pos_target(t)
        PosTarget = [0,0,0]
        QuatTarget, PosTarget = transformTarget(QuatTarget, PosTarget, data)
        PosTarget = PosTarget + Disp
        data["quatwTarget"] = '-'
        data["quatxTarget"] = '-'
        data["quatyTarget"] = '-'
        data["quatzTarget"] = '-' 

        data["posxTarget"] = '-'
        data["posyTarget"] = '-'
        data["poszTarget"] = '-' 

        data["quatwTarget"][0] = QuatTarget[3] 
        data["quatxTarget"][0] = QuatTarget[0]
        data["quatyTarget"][0] = QuatTarget[1]
        data["quatzTarget"][0] = QuatTarget[2] 


        data["posxTarget"][0] = PosTarget[0]
        data["posyTarget"][0] = PosTarget[1]
        data["poszTarget"][0] = PosTarget[2]
        return data 

def transform_data(dataInitial,Name,Disp,task):
    wSize = 30

    dataInter = dataInitial
    posx= []
    posy= []
    posz= []

    quat_x =[]
    quat_y =[]
    quat_z =[]
    quat_w =[]

    eulerx = []
    eulery = []
    eulerz = []

    qx= []
    qy= []
    qz= []
    qw= []
    i = 0
    while i < len(dataInter):

        #Center to the center of the target
        t = take_target(Name)

        qTar, pTar = take_pos_target(t) 
        #tool in fct ground
        quatTarget = [dataInter["_vrpnQuat_x"][i],dataInter["_vrpnQuat_y"][i],dataInter["_vrpnQuat_z"][i],dataInter["_vrpnQuat_w"][i]]
        posTarget  = [dataInter["_vrpnPos_x"][i]- pTar[0],dataInter["_vrpnPos_y"][i]-pTar[1],dataInter["_vrpnPos_z"][i]-pTar[2]]
        T_tool_ground = transformToolGround(quatTarget,posTarget)


        # ground in function of base
        p = [0,0,0]
        #p = [-np.mean(dataInter["_vrpnPos_z"]),-np.mean(dataInter["_vrpnPos_x"])+0.6,1]
        T_ground_Base =  transformGroundBase(p)

        #quat of the tools in function of the iiwa tools
    
        if task == 0:
            T_tool_eef = transformBaseEef("x", -math.pi/2)
        else:
            T_tool_eef = transformBaseEef("y", math.pi)


        T_tilt = T_ground_Base* T_tool_ground* T_tool_eef

        #extractt quat,pos and euler from Transformation matrix
        quat_opt_world , pos_opt_world, euler_opt_world = extractQuatPos(T_tilt)

        posx.append(pos_opt_world[0]+ Disp[0])
        posy.append(pos_opt_world[1]+ Disp[1])
        posz.append(pos_opt_world[2]+ Disp[2])
        eulerx.append(euler_opt_world[0])
        eulery.append(euler_opt_world[1])
        eulerz.append(euler_opt_world[2])
        qx.append(quat_opt_world[0])
        qy.append(quat_opt_world[1])
        qz.append(quat_opt_world[2])
        qw.append(quat_opt_world[3])

        i= 1+i
        
 

    #replace the position of the target on the robot frame
    #Prepare csvfile
    data_df_T = pd.DataFrame()
    
    data_df_T["Time"]  = dataInter['Time']
    data_df_T["dt"]    = dataInter['dt']
    data_df_T["quatx"] = qx
    data_df_T["quaty"] = qy
    data_df_T["quatz"] = qz
    data_df_T["quatw"] = qw
    data_df_T["quatx_filter"] = median_filter_1d(qx, wSize)
    data_df_T["quaty_filter"] = median_filter_1d(qy, wSize)
    data_df_T["quatz_filter"] = median_filter_1d(qz, wSize)
    data_df_T["quatw_filter"] = median_filter_1d(qw, wSize)


    data_df_T["posx"] = posx 
    data_df_T["posy"] = posy 
    data_df_T["posz"] = posz 
    data_df_T["eulerx"] = eulerx
    data_df_T["eulery"] = eulery
    data_df_T["eulerz"] = eulerz
    data_df_T["eulerx_filter"] = median_filter_1d(eulerx, wSize) 
    data_df_T["eulery_filter"] = median_filter_1d(eulery, wSize) 
    data_df_T["eulerz_filter"] = median_filter_1d(eulerz, wSize) 

    # compute angular velocity
    w = extract_angular_velocities(data_df_T)
    #w_euler= calc_angular_velocities_euler(data_df_T)

    data_df_T["wx"] = w[:, 0]
    data_df_T["wy"] = w[:, 1]
    data_df_T["wz"] = w[:, 2]

    data_df_T["wx_filter"] = median_filter_1d( w[:, 0], wSize)
    data_df_T["wy_filter"] = median_filter_1d( w[:, 1], wSize)
    data_df_T["wz_filter"] = median_filter_1d( w[:, 2], wSize)

    if task == 1:
        data_df_T =clean_force_and_add_to_dataframe(dataInter,data_df_T)

    #compute target pos
    data_df_T = add_target_dataframe(Name, data_df_T, Disp)

    nameFinal = "../data/csv_transform/" + Name + "_transform"
    data_df_T.to_csv(nameFinal, index= None )
    return data_df_T    
    
def mainTransform(name):
    task = 1
    if not (name.find("shot") == -1):
        task = 0
    print(name)
    bagToCsv(name , task)
    print('bag to csv done')
    file_name = "../data/csv/" + name + ".csv"
    data = pd.read_csv(file_name, index_col=False)
    file_name_short= file_name.replace("../data/csv/", "")


    displacementFromTarget = [1.25,0,0.7] 

    data_final= transform_data(data,file_name_short,displacementFromTarget,task)
    print('transform done, wait for plot')
    plot_quaternion(data_final,name)
    plot_angularVelocity(data_final,name)
    plot_position(data_final,name)
    plot_euler(data_final,name)
    plot_force(data_final,name)
    plot_torque(data_final,name)
    print('plot saved')
    print(data_final)

if __name__ == '__main__':
    parameter_value = sys.argv[1]
    mainTransform(parameter_value)
