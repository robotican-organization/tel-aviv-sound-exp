#!/bin/bash

TIME_TO_SLEEP=3

echo "Start Driving..."
rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[1.0, 0.0, 0.0]' '[0.0, 0.0, 0.0]' &
PID=$!
./exp1.sh &
sleep(TIME_TO_SLEEP)
echo "Stop Driving..."
kill $PID
