#!/bin/bash
set -e
source /ros2_humble/install/setup.bash
if [ -f /ws/install/setup.bash ]; then
  source /ws/install/setup.bash
fi
exec "$@"


