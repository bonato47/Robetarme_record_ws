#!/bin/bash

rosservice call /imu/calibrate_gyroscope
rosservice call /imu/reset_heading
