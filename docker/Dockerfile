FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV ROS_DISTRO=humble

RUN apt-get update && apt-get install -y locales \
 && locale-gen en_US en_US.UTF-8 \
 && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

RUN apt-get update && apt-get install -y software-properties-common curl \
 && add-apt-repository universe \
 && ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}') \
 && curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.jammy_all.deb" \
 && dpkg -i /tmp/ros2-apt-source.deb \
 && rm /tmp/ros2-apt-source.deb

RUN apt-get update && apt-get install -y \
    python3-flake8-docstrings \
    python3-pip \
    python3-pytest-cov \
    ros-dev-tools \
    python3-flake8-blind-except \
    python3-flake8-builtins \
    python3-flake8-class-newline \
    python3-flake8-comprehensions \
    python3-flake8-deprecated \
    python3-flake8-import-order \
    python3-flake8-quotes \
    python3-pytest-repeat \
    python3-pytest-rerunfailures \
    python3-xlib \
    x11-apps \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_humble

RUN mkdir -p src \
 && vcs import --input https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos src

RUN apt-get update \
 && rosdep init \
 && rosdep update --rosdistro humble \
 && rosdep install --from-paths src --ignore-src -y --rosdistro humble \
      --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers" \
 && rm -rf /var/lib/apt/lists/*

RUN colcon mixin add default https://github.com/colcon/colcon-mixin-repository/raw/master/index.yaml \
 && colcon mixin update default

RUN colcon build --symlink-install --mixin release --parallel-workers 2 \
      --packages-up-to \
        turtlesim \
        demo_nodes_cpp \
        demo_nodes_py \
        ros2cli_common_extensions \
        ros2launch \
        rclpy \
        geometry_msgs \
        rosidl_default_generators \
        ament_cmake_python

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
