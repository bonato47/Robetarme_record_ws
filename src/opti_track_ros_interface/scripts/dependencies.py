import rospy
from threading import Thread
from enum import Enum
from colorama import Fore, Style, Back
import queue
import signal
import os
import sys
import time

from UDPSocket import UDPSocket

NODE_FREQUENCY = 50.0

# Socket programming
UDP_IPS = ("192.168.7.15", "192.168.7.55")
UDP_PORTS = (20016, 20013)
UDP_PACKET_BUFFER_SIZE = 1024
UDP_UPDATE_RATE = 1.0 / 50.0
UDP_LOG_ENABLED = False


SERVER_MSGS = ["ros_interface_is_not_ready",
               "ros_interface_is_ready"]

CLIENT_MSGS = ["client_is_ready"]

