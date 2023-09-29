# Handle ros distro

ARG ROS_DISTRO=noetic
ARG BASE_TAG=noetic
FROM ros:${BASE_TAG} as environment-variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR 1
ENV USER ros
ENV HOME /home/${USER}
ENV ROS_WORKSPACE /home/${USER}/ros_ws
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

FROM environment-variables as base-dependencies


# User provided arguments
ARG HOST_GID=1000
ARG GIT_NAME=""
ARG GIT_EMAIL=""
ARG USE_SIMD=OFF

# Tell docker we want to use bash instead of sh in general
SHELL ["/bin/bash", "-c"]

### Add the user to the current GID of the host to avoid permisson issues in volumes
# AICA uses the same name for user and user group
ENV USER_GROUP=${USER}
USER root
# create and configure a new user
ARG UID=1000
ARG GID=1000
RUN addgroup --gid ${GID} ${USER}
RUN adduser --gecos "ROS User" --uid ${UID} --gid ${GID} ${USER} && yes | passwd ${USER}
RUN usermod -a -G dialout ${USER}
RUN usermod -a -G tty ${USER}
RUN echo "${USER} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/99_aptget
RUN chmod 0440 /etc/sudoers.d/99_aptget && chown root:root /etc/sudoers.d/99_aptget

USER ${USER}
RUN sudo apt update
RUN sudo apt install git -y
# Setup git identity
RUN git config --global user.name "${GIT_NAME}"
RUN git config --global user.email "${GIT_EMAIL}"

# Setup python version for noetic
RUN sudo apt update
RUN if [ "${ROS_DISTRO}" == "noetic" ] ; \
    then sudo apt install python-is-python3 ; fi
RUN sudo apt install pip -y
RUN pip install scipy  
RUN pip install matplotlib 
RUN pip install pandas 

### Add a few tools
RUN sudo apt-get update && sudo apt-get install -y \
    bash-completion \
    silversearcher-ag \
    apt-transport-https \
    less \
    nano \
    alsa-utils \
    netbase \
    ros-noetic-vrpn-client-ros \
    ros-noetic-ros-control \
    ros-noetic-ros-controllers \
    ros-noetic-diagnostic-updater \
    ros-noetic-mavros* \
    dbus-x11 \
    libcanberra-gtk-module libcanberra-gtk3-module \
    gnome-terminal \
    build-essential \
    mesa-common-dev \
    libqt5opengl5 \
    freeglut3-dev \
    libbluetooth-dev \
    qtbase5-dev \
    qtconnectivity5-dev \
    && sudo apt-get upgrade -y && sudo apt-get clean


#    ros-noetic-openzen-sensor \
#    libspdlog-dev \

# Handle SIMD option
RUN if [ "${USE_SIMD}" = "ON" ] ; \ 
    then export CMAKE_CXX_FLAGS="-march=native -faligned-new" ; fi

# Remove temporari files
RUN sudo ldconfig
RUN rm -rf /tmp/*

# Install workspace
WORKDIR /home/${USER}/ros_ws
RUN git clone -b raspberry https://github.com/bonato47/robetarme_record_ws.git
RUN cp -r robetarme_record_ws/* .
RUN rm -rf robetarme_record_ws

### Add environement variables to bashrc
WORKDIR /home/${USER}


# Give bashrc back to user
RUN sudo chown -R ${USER}:${HOST_GID} .bashrc

# Add cmake option to bash rc if needed
RUN if [ "${USE_SIMD}" = "ON" ] ; \
    then echo "export ENABLE_SIMD=ON" >> /home/${USER}/.bashrc ; fi
RUN sudo apt install bluez
#RUN sudo service dbus start
RUN sudo service bluetooth start


### Build ros workspace
USER ${USER}
WORKDIR /home/${USER}/ros_ws
RUN rosdep update
RUN source /opt/ros/noetic/setup.bash && rosdep install --from-paths src --ignore-src -r -y


RUN source /opt/ros/noetic/setup.bash && catkin_make

RUN echo "source devel/setup.bash" >> ~/.bashrc
### Final apt clean
RUN sudo apt update && sudo apt upgrade && sudo apt clean
