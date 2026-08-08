# Turtlesim Chase Demo

Two Docker containers running ROS 2 Humble built from source.

- `turtle1` follows the mouse cursor
- `turtle2` chases `turtle1`, stopping when close
- Every 10 seconds the mode flips and `turtle2` runs away instead

## Setup

Docker Desktop needs at least 8 GB memory and 60 GB disk under
Settings > Resources.

```bash
docker build -f docker/Dockerfile -t nova-turtle .
```

**macOS**

```bash
brew install --cask xquartz
```

Log out and back in. Open XQuartz, Settings > Security, enable "Allow
connections from network clients", quit and reopen. Then:

```bash
xhost + 127.0.0.1
```

**Linux**

```bash
xhost +local:docker
```

In `compose.yaml`, set turtle_a to `DISPLAY=${DISPLAY}` and add
`/tmp/.X11-unix:/tmp/.X11-unix` to its volumes.

**Windows**

Use WSL2 and follow the Linux steps from inside it.

## Run

```bash
cd docker
docker compose up -d
```

Terminal 1:
```bash
docker compose exec turtle_a bash
ros2 launch turtle_chase turtlesim_launch.py
```

Terminal 2:
```bash
docker compose exec turtle_b bash
ros2 launch turtle_chase chaser_launch.py
```

Move the mouse over the turtlesim window.

After changing code:
```bash
cd /ws && colcon build && source install/setup.bash
```

## Layout

```
docker/     Dockerfile, compose.yaml, entrypoint.sh
ws/src/
  turtle_interfaces/   ChaseMode.msg
  turtle_chase/        Three nodes, two launch files
```




[Demo recording](docs/demo.mp4)



