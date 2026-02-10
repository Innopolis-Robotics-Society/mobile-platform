<h1 align="center">
   Overlord100 Simulation
</h1>

<p align="center">
  ROS 2 packages for simulation Autonomus Mobile Platform Overlord100.<br>
</p>

This repository allows the software development team to test the developed algorithms without the risk of damaging the real equipment, as well as to conduct tests in parallel and without the need for personal presence in the laboratory.

# Built with

[![Gazebo][Gazebo-badge]][Gazebo-url] [![ROS2][ROS2-badge]][ROS2-url]  [![Python][Python-badge]][Python-url] [![C++][C++-badge]][C++-url] [![CMake][CMake-badge]][CMake-url] [![Docker][Docker-badge]][Docker-url] [![Devcontainer][Devcontainer-badge]][Devcontainer-url] [![Docker Hub][Docker Hub-badge]][Docker Hub-url] [![Harbor][Harbor-badge]][Harbor-url] [![Git][Git-badge]][Git-url]

# Demo

<p align="center">
   <img src="media/demo.png" width="800" alt="text">
   <img src="media/demo_gitlab.gif">
</p>


[Docker-url]: https://www.docker.com/
[Docker-badge]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=FFFFFF

[ROS2-url]: https://docs.ros.org/
[ROS2-badge]: https://img.shields.io/badge/ROS2-22314E?style=for-the-badge&logo=ROS

[Gazebo-url]: https://gazebosim.org/home/
[Gazebo-badge]: https://img.shields.io/badge/Gazebo-orange?style=for-the-badge&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8%2BCjxzdmcKICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICB4bWxuczpjYz0iaHR0cDovL2NyZWF0aXZlY29tbW9ucy5vcmcvbnMjIgogICB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIKICAgdmVyc2lvbj0iMS4xIgogICBpZD0ic3ZnNjQwOCIKICAgaGVpZ2h0PSIzMDAiCiAgIHdpZHRoPSIzMDAiPgogIDxkZWZzCiAgICAgaWQ9ImRlZnM2NDEwIiAvPgogIDxtZXRhZGF0YQogICAgIGlkPSJtZXRhZGF0YTY0MTMiPgogICAgPHJkZjpSREY%2BCiAgICAgIDxjYzpXb3JrCiAgICAgICAgIHJkZjphYm91dD0iIj4KICAgICAgICA8ZGM6Zm9ybWF0PmltYWdlL3N2Zyt4bWw8L2RjOmZvcm1hdD4KICAgICAgICA8ZGM6dHlwZQogICAgICAgICAgIHJkZjpyZXNvdXJjZT0iaHR0cDovL3B1cmwub3JnL2RjL2RjbWl0eXBlL1N0aWxsSW1hZ2UiIC8%2BCiAgICAgICAgPGRjOnRpdGxlPjwvZGM6dGl0bGU%2BCiAgICAgIDwvY2M6V29yaz4KICAgIDwvcmRmOlJERj4KICA8L21ldGFkYXRhPgogIDxnCiAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMCwtNzUyLjM2MjE4KSIKICAgICBpZD0ibGF5ZXIxIj4KICAgIDxwYXRoCiAgICAgICBpZD0icGF0aDMyMjYiCiAgICAgICBkPSJtIDE0OS45ODQzNyw3NTcuMzE1NjcgYyAtMS41MDAwOSw5LjRlLTQgLTIuOTg4NSwwLjM5NzUgLTQuMzEyNSwxLjIxODc1IEwgMzEuNDUzMTI1LDgyOS40NDA2NyBjIC0yLjQxMDE1LDEuNDkzNzUgLTMuODc1LDQuMTYyNSAtMy44NzUsNyBsIDAsMTMxLjg0Mzc1IGMgMCwyLjg0MjUgMS40NjQ4NSw1LjUgMy44NzUsNyBsIDExNC4yMTg3NDUsNzAuOTA2MjggYyAwLjA1NDYsMC4wMjkgMC4xMDAxMywwLjA2IDAuMTU2MjUsMC4wOTQgMC4wNjEsMC4wMzUgMC4xMjU1LDAuMDg2IDAuMTg3NSwwLjEyNSAwLjEzMTg3LDAuMDY5IDAuMjczNSwwLjA5NCAwLjQwNjI1LDAuMTU2MiAwLjEzNTI1LDAuMDY5IDAuMjcsMC4xNjUgMC40MDYyNSwwLjIxODggMC4yMTI4OCwwLjA5MiAwLjQzOCwwLjE1MDkgMC42NTYyNSwwLjIxODcgMC4xMjc4NywwLjA0MyAwLjI0NTYyLDAuMDkgMC4zNzUsMC4xMjUgMC4yNDU2MiwwLjA2NyAwLjQ5OTUsMC4xMTI0IDAuNzUsMC4xNTYzIDAuMTA2ODcsMC4wMTUgMC4yMDUxMiwwLjA0NyAwLjMxMjUsMC4wNjIgMC4zNTczOCwwLjA0OSAwLjcwMjYzLDAuMDYyIDEuMDYyNSwwLjA2MiAwLjc0NjQ5LDAgMS40OTM3NSwtMC4xMDI1IDIuMjE4NzUsLTAuMzEyNSBsIDAuMDMxMiwwIGMgMC4yODA4NywtMC4wNzggMC41NCwtMC4xNjg0IDAuODEyNSwtMC4yODEzIDAuMDgxMywtMC4wMyAwLjE2NjI1LC0wLjA2IDAuMjUsLTAuMDk0IDAuMjIzNzUsLTAuMDk5IDAuNDM2MjUsLTAuMjIxNyAwLjY1NjI1LC0wLjM0MzcgMC4xMiwtMC4wNjggMC4yNTc1LC0wLjExODYgMC4zNzUsLTAuMTg3NSBsIDAuMjE4NzUsLTAuMTU2MyAxMTQsLTcwLjc0OTk4IGMgMi40MTc1LC0xLjUwNSAzLjg4NSwtNC4xNDg3NSAzLjg3NSwtNyBsIC0wLjIxODc1LC02Ni4wOTM3NSBjIC0wLjAxLC0yLjk3NjI1IC0xLjYxMzc1LC01LjcxNSAtNC4yMTg3NSwtNy4xNTYyNSAtMi42MDI1LC0xLjQ0NSAtNS43ODI1LC0xLjM1Mzc1IC04LjMxMjUsMC4yMTg3NSBsIC00OC42MjUsMzAuMjgxMjUgLTM3LjQ2ODc1LC0yMy4yMTg3NSA5NC45Njg3NSwtNTkuMTI1IGMgMi40MSwtMS40OTg3NSAzLjg3NzUsLTQuMTMgMy44NzUsLTYuOTY4NzUgLTAuMDA1LC0yLjgzNzUgLTEuNDkzNzUsLTUuNDc1IC0zLjkwNjI1LC02Ljk2ODc1IEwgMTU0LjMyODEyLDc1OC41MzQ0MiBjIC0xLjMyNTg3LC0wLjgyIC0yLjg0MzY2LC0xLjIxOTY5IC00LjM0Mzc1LC0xLjIxODc1IHogbSAtMTA2LjI4MTI0NSw5My42ODc1IDgyLjcxODc0NSw1MS4zNzUgLTgyLjcxODc0NSw1MS4zNDM3NSAwLC0xMDIuNzE4NzUgeiBtIDExNC4zMTI0OTUsNjEgMzcuNSwyMy4yMTg3NSAtNTAuMDYyNSwzMS4xNTYyNSBjIC0yLjQxNDUsMS41IC0zLjg1MzAxLDQuMTI3NSAtMy44NDM3NSw2Ljk2ODc1IGwgMC4xMjUsNTEuMDkzNzggLTkwLjM3NDk5NSwtNTYuMTU2MjggOTAuNjI0OTk1LC01Ni4yNSAzLjY4NzUsMi4yODEyNSBjIDEuMzI2NjIsMC44MjEyNSAyLjgxMSwxLjIxODc1IDQuMzEyNSwxLjIxODc1IDEuNTA0ODgsMCAzLjAxNSwtMC4zODg3NSA0LjM0Mzc1LC0xLjIxODc1IGwgMy42ODc1LC0yLjMxMjUgeiBtIDk3Ljg0Mzc1LDQuOTY4NzUgMC4xMjUsNDYuNzgxMjUgLTk3LjgxMjUsNjAuNzUwMDMgLTAuMTU2MjUsLTQ2LjYyNTAzIDk3Ljg0Mzc1LC02MC45MDYyNSB6IgogICAgICAgc3R5bGU9ImZpbGw6I2ZmZmZmZjtmaWxsLW9wYWNpdHk6MTtmaWxsLXJ1bGU6bm9uemVybztzdHJva2U6bm9uZSIgLz4KICA8L2c%2BCjwvc3ZnPgo%3D

[Python-url]: https://www.python.org/
[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=FFFFFF

[CMake-url]: https://cmake.org/
[CMake-badge]: https://img.shields.io/badge/CMake-064F8C?style=for-the-badge&logo=CMake

[C++-badge]: https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus
[C++-url]: https://isocpp.org/

[Devcontainer-badge]: https://img.shields.io/badge/Devcontainer-add1ea?style=for-the-badge&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBMaWNlbnNlOiBNSVQuIE1hZGUgYnkgdnNjb2RlLWljb25zOiBodHRwczovL2dpdGh1Yi5jb20vdnNjb2RlLWljb25zL3ZzY29kZS1pY29ucyAtLT4KPHN2ZyB3aWR0aD0iODAwcHgiIGhlaWdodD0iODAwcHgiIHZpZXdCb3g9IjAgMCAzMiAzMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48dGl0bGU%2BZmlsZV90eXBlX2RldmNvbnRhaW5lcjwvdGl0bGU%2BPGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTQiIHN0eWxlPSJmaWxsOiMxOTNlNjMiLz48cG9seWdvbiBwb2ludHM9IjEwLjc3NyAyMi43NDIgOS4zNDMgMjEuMzQ4IDEyLjcyOSAxNy44NjUgOS4zNDYgMTQuNDE3IDEwLjc3NCAxMy4wMTcgMTUuNTI1IDE3Ljg1OSAxMC43NzcgMjIuNzQyIiBzdHlsZT0iZmlsbDojYWRkMWVhIi8%2BPHBvbHlnb24gcG9pbnRzPSIyMS40MiAxOS4xMDEgMjIuODU0IDE3LjcwNiAxOS40NjggMTQuMjI0IDIyLjg1MSAxMC43NzYgMjEuNDIzIDkuMzc2IDE2LjY3MiAxNC4yMTggMjEuNDIgMTkuMTAxIiBzdHlsZT0iZmlsbDojYWRkMWVhIi8%2BPC9zdmc%2B
[Devcontainer-url]: https://containers.dev/

[Harbor-badge]: https://img.shields.io/badge/Harbor-60B932?style=for-the-badge&logo=harbor&logoColor=FFFFFF
[Harbor-url]: https://goharbor.io/

[Docker Hub-badge]: https://img.shields.io/badge/Docker_Hub-2496ED?style=for-the-badge&logo=Docker&logoColor=FFFFFF
[Docker Hub-url]: https://hub.docker.com/

[Git-badge]: https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=FFFFFF
[Git-url]: https://git-scm.com/
# Installation

## Prerequisites

 - [Ubuntu 22.04 (Jammy Jellyfish)](https://releases.ubuntu.com/jammy/) or [Ubuntu 20.04 (Focal Fossa)](https://releases.ubuntu.com/20.04/) or [Windows 11](https://www.microsoft.com/en-gb/software-download/windows11) or [Windows 10](https://www.microsoft.com/en-gb/software-download/windows10ISO) or [MacOS ](https://support.apple.com/en-us/102662)
 - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
 - [Visual Studio Code](https://code.visualstudio.com/)
 - [Dev Containers extension for VS Code](https://code.visualstudio.com/docs/devcontainers/containers#_installation)
 - [Git](https://git-scm.com/downloads)
 - [X Server or VcXsrv](https://sourceforge.net/projects/vcxsrv/) (Only for Windows)

> *note:* The Apple Sillicon architecture is criticaly unstable and the preferred OS is Ubuntu

## Build and Launch container through terminal (For Linux and Windows)

   Firstly, you need to choose, would you download container or build it on your own machine.

   ### Download Container from Harbor Registry or Docker Hub
   
   ```
   docker pull harbor.pg.innopolis.university/sim_overlord100/simoverlord:latest
   ``` 

   Or

   ```
   docker pull simoverlord100/simoverlord:latest
   ```
   ### Build on your own machine

   1. Clone the repository to your workspace folder
      ```   
      git clone https://gitlab.pg.innopolis.university/e.shlomov/simoverlord100.git
      ```
   2. Build container
      ```
      docker build -t <name_of_image> .
      ```
   ### Run container

   - For Linux and MacOS
      ```
      docker run -it \
         -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
         -v /dev/dri:/dev/dri:rw \
         <name_of_image> bash
      ```
   - For Windows (10 or 11)
      ```
      docker run -it /
         -v /usr/lib/dri:/usr/lib/dri:rw /
         -e DISPLAY=host.docker.internal:0.0 /
         <name_of_image> bash
      ```

   > *note:* If you remove `bash` property, then docker container will simultaneously launch simulation from terminal without setup, but will not provide access to change files.

   ### Setup workspace to start 
   ```
   source /opt/ros/humble/setup.bash
   cd /home/ws/src
   colcon build
   source install/local_setup.bash
   ```

Now you can move on to [Starting simultion](#starting-simulation)

## Launch container through Visual Studio Code

   - For MacOS and Linux

      1. Open Visual Studio Code
      2. Press `Ctrl + Shift + G` and choose option `Clone Repository`
      3. Paste repository link
         ```
         https://gitlab.pg.innopolis.university/e.shlomov/simoverlord100.git
         ```   
      4. Select the repository download path
      5. Press `Ctrl+Shift+P` and choose option `DevContainers: Reopen in Container`.
      6. Choose the platform you are working on (`arm64` if you are using Apple Sillicon, otherwise `x86`)
      7. Source and build ROS 2 workspace
         ```
         source /opt/ros/humble/setup.bash
         cd /home/ws/src
         colcon build
         source install/local_setup.bash
         ```

Now you can move on to [Starting simultion](#starting-simulation)

# How to use

## Starting simulation

To start simulation, open terminal and run `ros2 launch` command:
```
ros2 launch overlord100_simulation simulation.launch.py
```

By default, the simulation expects to connect a third-party controller for the robot, but you can connect the built-in controller by specifying `False` for the launch argument `enable_custom_controller`:
```
ros2 launch overlord100_simulation simulation.launch.py enable_custom_controller:=False
```
> *note:* More about the arguments can be found in the [launch arguments section](#launch-arguments)


After that, you will have several windows open. 

In the `RViz` window, the readings of sensors and other systems are visualized.

In the `rqt_robot_steering` window (only for built-in controller), you can control the robot by setting the speed and direction of movement. 

To display the simulation window, you need to close the `Gazebo` window, after which a new one will open, with a scene.

## Launch arguments

Launch files have several arguments that can be controlled via the main file `simulation.launch.py`.

The description of the startup arguments can be seen by specifying the `-s` option in any startup file (`ros2 launch overlord100_simulation <launch_file> -s`) or in the following table:

| Name | Default value | Description | Acceptable values | 
|---|---|---|---|
|world|`simple_office.sdf`|Defines the world that will be used in the simulation|`simple_office.sdf`, `large_office.sdf`, `clear_world.sdf` or any world file specified in `worlds` folder |
|enable_custom_controller|`True`|Defines the type of robot control. Use third-party controller if true or built-in otherwise |`True`/`false`|
|custom_controller_pkg|`overlord100_controller`|Defines which ros 2 package will control the robot|Any suitable package|
|use_sim_time|`True`|Use simulation (Gazebo) clock if true|`True`/`false`|

Pass arguments as `<name>:=<value>`

# Features
1. Different processors architectures are supported (yet, `x86` works much better).
2. Code linting for `Python`.
3. Support to custom controllers of robot.

# Development: Continuous Integration
This repository has the following pipelines:
1. Python `black` linting.
2. C++ `clang-tidy` linting.
2. ROS2 package build test.
3. Container deployment on Docker Hub and Harbor Registry.
4. Unit testing.

# Development
 
## Code Style

1. `CPP`
   1. `Google` style: [link](https://google.github.io/styleguide/cppguide.html)
   2. `C++ Core Guidelines` style: [link](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
2. `Python`
   1. `PEP8` style: [link](https://peps.python.org/pep-0008/)
3. `Git Flow`
   1. `Conventional Commits`: [link](https://www.conventionalcommits.org/en/v1.0.0/)

## Unit testing

To launch unit testing, open terminal and run `launch_test` command:
```
launch_test urdf_dummy/test/test_converter_is_available.py
```

These unit tests checks connection to each sensor that installed on robot.

# License

Distributed under MIT License. See [LICENSE](LICENSE) for more information.
