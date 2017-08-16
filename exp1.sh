#!/bin/bash
# TO RUN: ./exp1.sh <exp_name> <gimbal_angle> <num_samples>
ID=$1
ANGLE=$2
SAMPLES=$3
DATE=$(date +"%Y-%m-%d_%H%M")
BASE="/home/komodo/catkin_ws/src/ronexp/data"
DIRPATH="$BASE/$ID"
mkdir -p $DIRPATH
echo Setting gimbal angle to $ANGLE
#rosservice call --wait /DJI_RotateTo "enable: 'True'
#angle: $ANGLE"
#sleep 1.0
rosservice call --wait /ronexp "path: '$DIRPATH'
samples: $SAMPLES
angle: $ANGLE"
echo "$ANGLE,$SAMPLES" >> $DIRPATH/exp1_details.txt 
echo Files are saved in: $DIRPATH

echo Done exp1
