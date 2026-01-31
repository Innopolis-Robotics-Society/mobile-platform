# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04
# Use ROS 2 Humble from Docker Hub as the base image
# Set non-interactive frontend fodebconf
ENV DEBIAN_FRONTEND=noninteractive

# Set arguments for user creation
ARG USERNAME=mobile
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Update and install necessary packages
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y sudo curl gnupg2 lsb-release net-tools python3-pip \
    && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - \
    && echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list

# Install slcan-utils from source if not available
RUN apt-get install -y git build-essential \
    && git clone https://github.com/linux-can/can-utils.git \
    && cd can-utils \
    && make \
    && make install


# Set arguments for user creation
ARG USERNAME=mobile
ARG USER_UID=1000
ARG USER_GID=$USER_UID


# Install additional ROS 2 packages including development tools
RUN apt-get update && apt-get install -y \
    python3-pip \
    ros-humble-slam-toolbox \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-rosbridge-suite \
    ros-humble-ros2-control \
    ros-humble-ign-ros2-control \
    ros-humble-ros2-controllers \
    ros-humble-rqt-robot-steering \
    ros-humble-nav2-msgs \
    ros-humble-pcl-conversions \
    ros-humble-nav2-map-server \
    ros-humble-controller-manager \
    ros-humble-rviz2 \
    ros-humble-rqt-tf-tree \
    ros-humble-xacro \
    ros-humble-ament-cmake \       
    ros-humble-ament-cmake-auto \
    ros-humble-ament-lint-auto \
    ros-humble-launch-testing-ros \
    ros-humble-ros-gz-sim \
    ros-humble-ros-gz-bridge \
    liburdfdom-tools \
    ros-humble-joint-state-publisher-gui \
    ros-humble-robot-state-publisher \
    ros-humble-ros2-controllers-test-nodes \
    ros-humble-ros2launch \
    ros-humble-gazebo-ros \
    ros-humble-rclc \
    ros-humble-turtlebot3-gazebo \
    ros-humble-robot-localization \
    ros-dev-tools \
    x11-apps \
    xauth \
    --fix-missing

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install colcon and necessary extensions using pip
# RUN pip3 install -U colcon-common-extensions

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set up workspace  
# WORKDIR /home/ws/src
# COPY . /home/ws/src

# Copy startup script and set permissions
# COPY startup.bash /home/ws/startup.bash
# RUN chmod +x /home/ws/startup.bash

# Set the default user
USER $USERNAME

# Set the entry point
CMD ["bash"]
