#!/bin/bash

TIME_TO_DRIVE=5

echo "Start Driving..."
rostopic pub -r 1 /cmd_vel geometry_msgs/Twist -- '[1.0, 0.0, 0.0]' '[0.0, 0.0, 0.0]' &
PID=$!
./exp1.sh &
sleep $TIME_TO_DRIVE
echo "Stop Driving..."
kill $PID
