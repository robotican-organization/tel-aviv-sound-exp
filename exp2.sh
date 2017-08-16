#!/bin/bash
# TO RUN: ./exp2.sh <exp_name> <num_samples> <num_locations>
ID=$1
SAMPLES=$2
LOCATIONS=$3
BASE="/home/komodo/catkin_ws/src/ronexp/data"
DIRPATH="$BASE/$ID"
angles=(-1.4 -0.3 0 0.3 1.4)

#rosservice call --wait '/diff_driver/setOdometry' "x: 0
#y:0
#theta: 0"

for (( c=1; c<=$LOCATIONS; c++ ))
do	
	echo "Drive the robot and press 'y' to record data, press any other key to quit"
	read ans
	if [[ $ans == "y" ]]; then
  		for a in "${angles[@]}"
		do
			./exp1.sh "$ID/pos_$c" $a $SAMPLES
		done
	fi
	
done

echo "${#angles[@]},$SAMPLES,$LOCATIONS" >> $DIRPATH/exp2_details.txt 
echo Files are saved in: $DIRPATH



echo Done exp2
